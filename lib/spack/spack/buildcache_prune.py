# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile
from concurrent.futures import as_completed
from typing import Dict, Optional, Set, cast

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.stage
import spack.util.parallel
import spack.util.url as url_util
import spack.util.web as web_util

from .mirrors.mirror import Mirror
from .url_buildcache import URLBuildcacheEntry, get_entries_from_cache


def _prune_orphans(mirror: Mirror) -> int:
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

    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpspecsdir:
        file_list, read_fn = get_entries_from_cache(url=mirror.fetch_url, tmpspecsdir=tmpspecsdir)

        def process_manifest(blob_name: str) -> Dict[str, str]:
            cache_entry: Optional[URLBuildcacheEntry] = None
            try:
                cache_entry = cast(URLBuildcacheEntry, read_fn(blob_name))
                assert cache_entry.manifest is not None  # to satisfy type checker
                return {
                    cache_entry.get_blob_url(mirror_url=mirror.fetch_url, record=data): blob_name
                    for data in cache_entry.manifest.data
                }
            except Exception as e:
                tty.warn(f"Unable to fetch spec for manifest {blob_name} due to: {e}")
                return {}
            finally:
                if cache_entry:
                    cache_entry.destroy()

        with spack.util.parallel.make_concurrent_executor() as executor:
            futures = {executor.submit(process_manifest, blob): blob for blob in file_list}
            for future in as_completed(futures):
                result = future.result()
                blob_to_manifest_mapping.update(result)

    url_to_list = url_util.join(mirror.fetch_url, bindist.buildcache_relative_blobs_path())
    tty.debug(f"Listing blobs in {url_to_list}")
    blobs = web_util.list_url(url_to_list, recursive=True)
    if not blobs:
        tty.warn(f"Unable to list blobs in {url_to_list}")

    # Blobs that are referenced in a manifest file (but not necessarily present in the cache)
    blob_hashes_referenced_by_manifest = set(blob_to_manifest_mapping.keys())

    # Blobs that are actually present in the cache (but not necessarily referenced in any manifest)
    blob_hashes_present_in_cache: Set[str] = {
        url_util.join(mirror.fetch_url, bindist.buildcache_relative_blobs_path(), blob_name)
        for blob_name in blobs
    }

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
        tty.info("No orphaned manifest(s) or blob(s) found")
        return 0

    if orphaned_blobs:
        tty.info(f"Found {len(orphaned_blobs)} blob(s) with no manifest")
    if orphaned_manifests:
        tty.info(f"Found {len(orphaned_manifests)} manifest(s) that are missing blobs")

    pruned_objects = 0

    def remove_manifest(url: str) -> int:
        try:
            web_util.remove_url(url=url)
            tty.info(f"Removed manifest {url}")
            return 1
        except Exception as e:
            tty.warn(f"Unable to prune manifest {url} due to: {e}")
            return 0

    def remove_blob(url: str) -> int:
        try:
            web_util.remove_url(url=url)
            tty.debug(f"Removed {url}")
            return 1
        except Exception as e:
            tty.warn(f"Unable to prune blob {url} due to: {e}")
            return 0

    with spack.util.parallel.make_concurrent_executor() as executor:
        manifest_futures = [executor.submit(remove_manifest, url) for url in orphaned_manifests]
        blob_futures = [executor.submit(remove_blob, url) for url in orphaned_blobs]

        for manifest_or_blob_future in as_completed(manifest_futures + blob_futures):
            pruned_objects += manifest_or_blob_future.result()

    return pruned_objects


def prune(mirror: Mirror) -> None:
    """
    Execute the pruning process for a given mirror.

    Currently, this function only performs the pruning of orphaned manifests and blobs.
    """
    tty.debug(f"Pruning mirror: {mirror.fetch_url}")

    total_pruned = 0
    while True:
        # Continue pruning until no more orphaned objects are found
        pruned = _prune_orphans(mirror)
        if pruned == 0:
            break
        total_pruned += pruned

    tty.debug(f"Pruned {total_pruned} orphaned objects from mirror: {mirror.fetch_url}")
