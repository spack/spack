# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile
from concurrent.futures import Future, as_completed
from contextlib import contextmanager
from typing import Callable, Dict, Generator, List, Optional, Set, Tuple, cast

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.stage
import spack.util.parallel
import spack.util.url as url_util
import spack.util.web as web_util

from .mirrors.mirror import Mirror
from .url_buildcache import URLBuildcacheEntry, get_entries_from_cache


@contextmanager
def _fetch_manifests(
    mirror: Mirror,
) -> Generator[Tuple[List[str], Callable[[str], URLBuildcacheEntry], List[str]], None, None]:
    """
    Fetch all manifests from the buildcache for a given mirror.

    This function retrieves all the manifest files from the buildcache of the specified
    mirror and returns a list of tuples containing the file names and a callable to read
    each manifest.

    :param mirror: The mirror from which to fetch the manifests.
    :return: A list of tuples, each containing a list of file names and a callable to read
             the manifest entries.
    """
    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpspecsdir:
        file_list, read_fn = get_entries_from_cache(url=mirror.fetch_url, tmpspecsdir=tmpspecsdir)
        url_to_list = url_util.join(mirror.fetch_url, bindist.buildcache_relative_blobs_path())
        tty.debug(f"Listing blobs in {url_to_list}")
        blobs = web_util.list_url(url_to_list, recursive=True) or []
        if not blobs:
            tty.warn(f"Unable to list blobs in {url_to_list}")
        blobs = [
            url_util.join(mirror.fetch_url, bindist.buildcache_relative_blobs_path(), blob_name)
            for blob_name in blobs
        ]
        yield file_list, read_fn, blobs


def _delete_object(url: str, dry_run: bool) -> int:
    if dry_run:
        tty.info(f"Dry run: would remove object {url}")
        return 1
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
            tty.warn(f"Unable to fetch spec for manifest {manifest} due to: {e}")
            continue
        finally:
            if cache_entry:
                cache_entry.destroy()

    # Blobs that are referenced in a manifest file (but not necessarily present in the cache)
    blob_hashes_referenced_by_manifest = set(blob_to_manifest_mapping.keys())

    # Blobs that are actually present in the cache (but not necessarily referenced in any manifest)
    blob_hashes_present_in_cache: Set[str] = set(blobs)

    # Compute set of blobs that are present in the cache but not referenced in any manifest
    orphaned_blobs = blob_hashes_present_in_cache - blob_hashes_referenced_by_manifest

    # Compute set of blobs that are referenced in a manifest but not present in the cache
    nonexisting_referenced_blobs = (
        blob_hashes_referenced_by_manifest - blob_hashes_present_in_cache
    )

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

    pruned_objects = 0
    futures: List[Future] = []

    with spack.util.parallel.make_concurrent_executor() as executor:
        for manifest in orphaned_manifests:
            futures.append(executor.submit(_delete_object, manifest, dry_run))
            try:
                manifests.remove(manifest)
            except ValueError:
                # If the manifest was already removed during the pruning of another orphaned blob,
                # it will not be in the list, so we can safely ignore this error.
                pass

        for blob in orphaned_blobs:
            futures.append(executor.submit(_delete_object, blob, dry_run))
            try:
                blobs.remove(blob)
                del blob_to_manifest_mapping[blob]
            except (KeyError, ValueError):
                # If the blob was already removed during the pruning of another orphaned manifest,
                # it will not be in the list, so we can safely ignore this error.
                pass

        for manifest_or_blob_future in as_completed(futures):
            pruned_objects += manifest_or_blob_future.result()

    return pruned_objects


def prune(mirror: Mirror, dry_run: bool) -> None:
    """
    Execute the pruning process for a given mirror.

    Currently, this function only performs the pruning of orphaned manifests and blobs.
    """
    tty.debug(f"Pruning mirror: {mirror.fetch_url}" + (" (dry run)" if dry_run else ""))

    total_pruned = 0
    with _fetch_manifests(mirror) as (manifest_list, read_fn, blob_list):
        while True:
            # Continue pruning until no more orphaned objects are found
            pruned = _prune_orphans(
                mirror=mirror,
                manifests=manifest_list,
                read_fn=read_fn,
                blobs=blob_list,
                dry_run=dry_run,
            )
            if pruned == 0:
                break
            total_pruned += pruned

    tty.info(
        ("Would have pruned" if dry_run else "Pruned")
        + f" {total_pruned} orphaned objects from mirror: {mirror.fetch_url}"
    )
