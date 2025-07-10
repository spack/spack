# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import tempfile
from concurrent.futures import Future, as_completed
from typing import Callable, Dict, List, Optional, Set, Tuple, cast

import spack.binary_distribution as bindist
import spack.llnl.util.tty as tty
import spack.stage
import spack.util.parallel
import spack.util.url as url_util
import spack.util.web as web_util
from spack.util.executable import which

from .mirrors.mirror import Mirror
from .url_buildcache import (
    CURRENT_BUILD_CACHE_LAYOUT_VERSION,
    URLBuildcacheEntry,
    get_entries_from_cache,
    get_url_buildcache_class,
)


def _fetch_manifests(
    mirror: Mirror, tmpspecsdir: str
) -> Tuple[List[str], Callable[[str], URLBuildcacheEntry], List[str]]:
    """
    Fetch all manifests from the buildcache for a given mirror.

    This function retrieves all the manifest files from the buildcache of the specified
    mirror and returns a list of tuples containing the file names and a callable to read
    each manifest.

    :param mirror: The mirror from which to fetch the manifests.
    :return: A tuple with three elements - a list of manifest files in the mirror, a
             callable to read each manifest, and a list of blobs in the mirror.
    """
    manifests, read_fn = get_entries_from_cache(url=mirror.fetch_url, tmpspecsdir=tmpspecsdir)
    url_to_list = url_util.join(mirror.fetch_url, bindist.buildcache_relative_blobs_path())
    tty.debug(f"Listing blobs in {url_to_list}")
    blobs = web_util.list_url(url_to_list, recursive=True) or []
    if not blobs:
        tty.warn(f"Unable to list blobs in {url_to_list}")
    blobs = [
        url_util.join(mirror.fetch_url, bindist.buildcache_relative_blobs_path(), blob_name)
        for blob_name in blobs
    ]
    return manifests, read_fn, blobs


def _delete_manifests_from_cache_aws(
    url: str, tmpspecsdir: str, urls_to_delete: Set[str]
) -> Optional[int]:
    aws = which("aws")

    if not aws:
        tty.warn("AWS CLI not found, skipping deletion of cache entries.")
        return None

    cache_class = get_url_buildcache_class(layout_version=CURRENT_BUILD_CACHE_LAYOUT_VERSION)

    include_pattern = cache_class.get_buildcache_component_include_pattern()

    file_count_before_deletion = len(list(pathlib.Path(tmpspecsdir).rglob(include_pattern)))

    # Add file:// prefix to URLs so that they are deleted properly by web_util.remove_url
    urls_to_delete = {url_util.path_to_file_url(url) for url in urls_to_delete}

    tty.debug(f"Deleting {len(urls_to_delete)} entries from cache at {url}")
    deleted = _delete_entries_from_cache_manual(tmpspecsdir, urls_to_delete)
    tty.debug(f"Deleted {deleted} entries from cache at {url}")

    sync_command_args = [
        "s3",
        "sync",
        "--delete",
        "--exclude",
        "*",
        "--include",
        include_pattern,
        tmpspecsdir,
        url,
    ]

    try:
        aws(*sync_command_args, output=os.devnull, error=os.devnull)
        # `aws s3 sync` doesn't return the number of deleted files,
        # but we can calculate it based on the local file count from
        # before and after the deletion.
        return file_count_before_deletion - len(
            list(pathlib.Path(tmpspecsdir).rglob(include_pattern))
        )
    except Exception:
        tty.warn(
            "Failed to use aws s3 sync to delete manifests, falling back to parallel deletion."
        )

    return None


def _delete_entries_from_cache_manual(url: str, urls_to_delete: Set[str]) -> int:
    pruned_objects = 0
    futures: List[Future] = []

    with spack.util.parallel.make_concurrent_executor() as executor:
        for url in urls_to_delete:
            futures.append(executor.submit(_delete_object, url))

        for manifest_or_blob_future in as_completed(futures):
            pruned_objects += manifest_or_blob_future.result()

    return pruned_objects


def _delete_object(url: str) -> int:
    try:
        web_util.remove_url(url=url)
        tty.info(f"Removed object {url}")
        return 1
    except Exception as e:
        tty.warn(f"Unable to remove object {url} due to: {e}")
        return 0


def _prune_orphans(
    mirror: Mirror,
    manifests: List[str],
    read_fn: Callable[[str], URLBuildcacheEntry],
    blobs: List[str],
    tmpspecsdir: str,
    dry_run: bool,
) -> int:
    """
    Prune orphaned manifests and blobs from the buildcache.

    This function crawls the buildcache for a given mirror and identifies orphaned
    manifests and blobs. An "orphaned manifest" is one that references blobs that
    are not present in the cache, while an "orphaned blob" is one that is present in
    the cache but not referenced in any manifest.

    It uses the following steps to identify and prune orphaned objects:

    1. Fetch all the manifests in the cache and build up a list of all the blobs that they
       reference.
    2. List all the blobs in the buildcache, resulting in a list of all the blobs that
       *actually* exist in the cache.
    3. Compare the two lists and use the difference to determine which objects are orphaned.
        - If a blob is listed in the cache but not in any manifest, that blob is orphaned.
        - If a blob is listed in a manifest but not in the cache, that manifest is orphaned.
    """

    # As part of the pruning process, we need to keep track of the mapping between
    # blob URLs and their corresponding manifest URLs. Once we start computing
    # which blobs are referenced by a manifest but not present in the cache,
    # we will need to know which manifest to prune.
    blob_to_manifest_mapping: Dict[str, str] = {}

    for manifest in manifests:
        cache_entry: Optional[URLBuildcacheEntry] = None
        try:
            cache_entry = cast(URLBuildcacheEntry, read_fn(manifest))
            assert cache_entry.manifest is not None  # to satisfy type checker
            blob_to_manifest_mapping.update(
                {
                    cache_entry.get_blob_url(mirror_url=mirror.fetch_url, record=data): manifest
                    for data in cache_entry.manifest.data
                }
            )
        except Exception as e:
            tty.warn(f"Unable to fetch manifest {manifest} due to: {e}")
            continue
        finally:
            if cache_entry:
                cache_entry.destroy()

    # Blobs that are referenced in a manifest file (but not necessarily present in the cache)
    blob_urls_referenced_by_manifest = set(blob_to_manifest_mapping.keys())

    # Blobs that are actually present in the cache (but not necessarily referenced in any manifest)
    blob_urls_present_in_cache: Set[str] = set(blobs)

    # Compute set of blobs that are present in the cache but not referenced in any manifest
    orphaned_blobs = blob_urls_present_in_cache - blob_urls_referenced_by_manifest

    # Compute set of blobs that are referenced in a manifest but not present in the cache
    nonexisting_referenced_blobs = blob_urls_referenced_by_manifest - blob_urls_present_in_cache

    # Compute set of manifests that are orphaned (i.e., they reference blobs that are not
    # present in the cache)
    orphaned_manifests = {
        blob_to_manifest_mapping[blob_url] for blob_url in nonexisting_referenced_blobs
    }

    if not orphaned_blobs and not orphaned_manifests:
        return 0

    if orphaned_blobs:
        tty.info(f"Found {len(orphaned_blobs)} blob(s) with no manifest")
    if orphaned_manifests:
        tty.info(f"Found {len(orphaned_manifests)} manifest(s) that are missing blobs")

    if dry_run:
        pruned_object_count = len(orphaned_blobs) + len(orphaned_manifests)
        for manifest in orphaned_manifests:
            manifests.remove(manifest)
            tty.info(f"  Would prune manifest: {manifest}")
        for blob in orphaned_blobs:
            blobs.remove(blob)
            tty.info(f"  Would prune blob: {blob}")
        return pruned_object_count

    # Try to delete the orphaned manifests using the AWS CLI,
    # if possible.
    pruned_manifests: Optional[int] = None
    if mirror.fetch_url.startswith("s3://"):
        pruned_manifests = _delete_manifests_from_cache_aws(
            url=mirror.fetch_url, tmpspecsdir=tmpspecsdir, urls_to_delete=orphaned_manifests
        )

    if pruned_manifests is None:
        # If the AWS CLI deletion failed, we fall back to deleting both manifests
        # and blobs with the fallback method.
        orphans_to_delete = orphaned_blobs.union(orphaned_manifests)
        pruned_object_count = 0
    else:
        # If the AWS CLI deletion succeeded, we only need to worry about
        # deleting the blobs, since the manifests have already been deleted.
        orphans_to_delete = orphaned_blobs
        pruned_object_count = pruned_manifests

    pruned_object_count += _delete_entries_from_cache_manual(
        url=mirror.fetch_url, urls_to_delete=orphans_to_delete
    )

    for manifest in orphaned_manifests:
        manifests.remove(manifest)
    for blob in orphaned_blobs:
        blobs.remove(blob)

    return pruned_object_count


def prune(mirror: Mirror, dry_run: bool) -> None:
    """
    Execute the pruning process for a given mirror.

    Currently, this function only performs the pruning of orphaned manifests and blobs.
    """
    tty.debug(f"Pruning mirror: {mirror.fetch_url}" + (" (dry run)" if dry_run else ""))

    total_pruned = 0
    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpspecsdir:
        manifest_list, read_fn, blob_list = _fetch_manifests(mirror, tmpspecsdir)
        while True:
            # Continue pruning until no more orphaned objects are found
            pruned = _prune_orphans(
                mirror=mirror,
                manifests=manifest_list,
                read_fn=read_fn,
                blobs=blob_list,
                tmpspecsdir=tmpspecsdir,
                dry_run=dry_run,
            )
            if pruned == 0:
                break
            total_pruned += pruned

        if dry_run:
            tty.info(
                f"Would have pruned {total_pruned} orphaned objects from mirror: "
                + mirror.fetch_url
            )
        else:
            tty.info(f"Pruned {total_pruned} orphaned objects from mirror: {mirror.fetch_url}")
            if total_pruned > 0:
                # If we pruned any objects, the buildcache index is likely out of date.
                # Inform the user about this.
                tty.info(
                    "As a consequence of pruning, the buildcache index is now likely out of date."
                )
                tty.info(
                    "Run `spack buildcache update-index` to update the index for this mirror."
                )
