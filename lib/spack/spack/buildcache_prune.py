# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import re
import tempfile
import uuid
from concurrent.futures import Future, as_completed
from fnmatch import fnmatch
from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Set, Tuple, cast

import spack.binary_distribution
import spack.error
import spack.llnl.util.tty as tty
import spack.stage
import spack.util.parallel
import spack.util.url as url_util
import spack.util.web as web_util

from .mirrors.mirror import Mirror
from .url_buildcache import BuildcacheComponent, URLBuildcacheEntry, get_entries_from_cache


def _fetch_manifests(
    mirror: Mirror, tmpspecsdir: str
) -> Tuple[Dict[str, float], Callable[[str], URLBuildcacheEntry], List[str]]:
    """
    Fetch all manifests from the buildcache for a given mirror.

    This function retrieves all the manifest files from the buildcache of the specified
    mirror and returns a list of tuples containing the file names and a callable to read
    each manifest.

    :param mirror: The mirror from which to fetch the manifests.
    :return: A tuple with three elements - a list of manifest files in the mirror, a
             callable to read each manifest, and a list of blobs in the mirror.
    """
    manifest_file_to_mtime_mapping, read_fn = get_entries_from_cache(
        mirror.fetch_url, tmpspecsdir, BuildcacheComponent.MANIFEST
    )
    url_to_list = url_util.join(
        mirror.fetch_url, spack.binary_distribution.buildcache_relative_blobs_path()
    )
    tty.debug(f"Listing blobs in {url_to_list}")
    blobs = web_util.list_url(url_to_list, recursive=True) or []
    if not blobs:
        tty.warn(f"Unable to list blobs in {url_to_list}")
    blobs = [
        url_util.join(
            mirror.fetch_url, spack.binary_distribution.buildcache_relative_blobs_path(), blob_name
        )
        for blob_name in blobs
    ]
    tty.debug(f"Found {len(blobs)} blobs")
    return manifest_file_to_mtime_mapping, read_fn, blobs


def _delete_entries_from_cache(
    manifests_to_delete: Set[str], blobs_to_delete: Set[str], dry_run: bool
) -> int:
    urls_to_delete = blobs_to_delete.union(manifests_to_delete)
    pruned_objects = 0
    futures: List[Future] = []

    with spack.util.parallel.make_concurrent_executor() as executor:
        for url in urls_to_delete:
            futures.append(executor.submit(_delete_object, url, dry_run))

        for manifest_or_blob_future in as_completed(futures):
            pruned_objects += manifest_or_blob_future.result()

    return pruned_objects


def _delete_object(url: str, dry_run: bool) -> int:
    try:
        if dry_run:
            tty.info(f"Would have removed object {url}")
        else:
            web_util.remove_url(url=url)
            tty.info(f"Removed object {url}")
        return 1
    except Exception as e:
        tty.warn(f"Unable to remove object {url} due to: {e}")
        return 0


def _object_has_prunable_mtime(url: str, pruning_started_at: float) -> Tuple[str, bool]:
    """Check if an object's modification time makes it eligible for pruning.

    Objects modified after pruning started should not be pruned to avoid
    race conditions with concurrent uploads.
    """
    stat_result = web_util.stat_url(url)
    assert stat_result is not None
    if stat_result[1] > pruning_started_at:
        tty.info(f"Skipping deletion of {url} because it was modified after pruning started")
        return url, False
    return url, True


def _filter_new_specs(urls: Iterable[str], pruning_started_at: float) -> Iterator[str]:
    """Filter out URLs that were modified after pruning started.

    Runs parallel modification time checks on all URLs and yields only
    those that are old enough to be safely pruned.
    """
    with spack.util.parallel.make_concurrent_executor() as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(_object_has_prunable_mtime, url, pruning_started_at))

        for manifest_or_blob_future in as_completed(futures):
            url, has_prunable_mtime = manifest_or_blob_future.result()
            if has_prunable_mtime:
                yield url


def _prune_orphans(
    mirror: Mirror,
    manifests: List[str],
    read_fn: Callable[[str], URLBuildcacheEntry],
    blobs: List[str],
    pruning_started_at: float,
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

    # Filter out any new specs that have been uploaded since the pruning started
    orphaned_blobs = set(_filter_new_specs(orphaned_blobs, pruning_started_at))
    orphaned_manifests = set(_filter_new_specs(orphaned_manifests, pruning_started_at))

    if orphaned_blobs:
        tty.info(f"Found {len(orphaned_blobs)} blob(s) with no manifest")
    if orphaned_manifests:
        tty.info(f"Found {len(orphaned_manifests)} manifest(s) that are missing blobs")

    pruned_object_count = _delete_entries_from_cache(
        manifests_to_delete=orphaned_manifests, blobs_to_delete=orphaned_blobs, dry_run=dry_run
    )

    for manifest in orphaned_manifests:
        manifests.remove(manifest)
    for blob in orphaned_blobs:
        blobs.remove(blob)

    return pruned_object_count


def prune_direct(
    mirror: Mirror,
    keeplist_file: pathlib.Path,
    manifest_to_mtime_mapping: Dict[str, float],
    read_fn: Callable[[str], URLBuildcacheEntry],
    blob_list: List[str],
    tmpspecsdir: str,
    pruning_started_at: float,
    dry_run: bool,
) -> None:
    """
    Execute direct pruning for a given mirror using a keeplist file.

    This function reads a file containing spec hashes to keep, then deletes
    all other spec manifests from the buildcache.
    Note that this function does *not* prune the blobs associated with the manifests;
    to do that, `prune_orphan` must be invoked to clean up the now-orphaned blobs.

    Args:
        mirror: Mirror to prune
        keeplist_file: Path to file containing newline-delimited hashes to keep
        pruning_started_at: Timestamp of when the pruning started
        dry_run: Whether to perform a dry run without actually deleting
    """
    tty.info("Running Direct Pruning")
    tty.debug(f"Direct pruning mirror: {mirror.fetch_url}" + (" (dry run)" if dry_run else ""))

    keep_hashes: Set[str] = set()
    for line in keeplist_file.read_text().splitlines():
        keep_hash = line.strip().lstrip("/")
        if len(keep_hash) != 32:
            raise MalformedKeepListException(f"Found malformed hash in keeplist: {line}")
        keep_hashes.add(keep_hash)

    if not keep_hashes:
        raise BuildcachePruningException(f"No hashes found in keeplist file: {keeplist_file}")

    tty.info(f"Loaded {len(keep_hashes)} hashes to keep from {keeplist_file}")
    total_pruned: Optional[int] = None
    manifests_url = url_util.join(
        mirror.fetch_url,
        *URLBuildcacheEntry.get_relative_path_components(BuildcacheComponent.MANIFEST),
    )

    # Determine which manifests correspond to specs we want to prune
    manifests_to_prune: List[str] = []
    specs_to_prune: List[str] = []

    tty.info(f"Found {len(manifest_to_mtime_mapping)} total manifests in mirror")

    for manifest in manifest_to_mtime_mapping.keys():
        # Convert back from local to remote path.
        manifest = manifest.replace(tmpspecsdir, manifests_url)
        if not fnmatch(
            manifest,
            URLBuildcacheEntry.get_buildcache_component_include_pattern(BuildcacheComponent.SPEC),
        ):
            tty.debug(f"Found a non-spec manifest at {manifest}, skipping...")
            continue

        # Attempt to regex match the manifest name in order to extract the name, version,
        # and hash for the spec.
        manifest_name = manifest.split("/")[-1]  # strip off parent directories
        # Schema is <package>-<version>-<spec hash>
        regex_match = re.match(r"([^ ]+)-([^- ]+)[-_]([^-_\. ]+)", manifest_name)

        if regex_match is None:
            # This should never happen, unless the buildcache is somehow corrupted
            # and/or there is a bug.
            raise BuildcachePruningException(
                "Unable to extract spec name, version, and hash from "
                f'the manifest named "{manifest_name}"'
            )

        spec_name, spec_version, spec_hash = regex_match.groups()

        if spec_hash not in keep_hashes:
            manifests_to_prune.append(manifest)
            specs_to_prune.append(f"{spec_name}/{spec_hash[:7]}")

    if not manifests_to_prune:
        tty.info("No specs to prune - all specs are in the keeplist")
        return

    manifests_to_delete = set(_filter_new_specs(manifests_to_prune, pruning_started_at))

    tty.info(f"Found {len(manifests_to_delete)} spec(s) to prune")

    total_pruned = _delete_entries_from_cache(
        manifests_to_delete=manifests_to_delete, blobs_to_delete=set(), dry_run=dry_run
    )

    # Remove pruned specs from manifest_to_mtime_mapping.
    for manifest in manifests_to_delete:
        manifest_to_mtime_mapping.pop(manifest, None)

    if dry_run:
        tty.info(f"Would have pruned {total_pruned} objects from mirror: {mirror.fetch_url}")
    else:
        tty.info(f"Pruned {total_pruned} objects from mirror: {mirror.fetch_url}")
        if total_pruned > 0:
            tty.info(
                "As a consequence of pruning, the buildcache index is now likely out of date."
            )
            tty.info("Run `spack buildcache update-index` to update the index for this mirror.")


def prune_orphan(
    mirror: Mirror,
    manifest_to_mtime_mapping: Dict[str, float],
    read_fn: Callable[[str], URLBuildcacheEntry],
    blob_list: List[str],
    tmpspecsdir: str,
    pruning_started_at: float,
    dry_run: bool,
) -> None:
    """
    Execute the pruning process for a given mirror.

    Currently, this function only performs the pruning of orphaned manifests and blobs.
    """
    tty.info("=== Orphan Pruning Phase ===")
    tty.debug(f"Pruning mirror: {mirror.fetch_url}" + (" (dry run)" if dry_run else ""))

    total_pruned = 0
    manifests = list(manifest_to_mtime_mapping.keys())

    while True:
        # Continue pruning until no more orphaned objects are found
        pruned = _prune_orphans(
            mirror=mirror,
            manifests=manifests,
            read_fn=read_fn,
            blobs=blob_list,
            pruning_started_at=pruning_started_at,
            tmpspecsdir=tmpspecsdir,
            dry_run=dry_run,
        )
        if pruned == 0:
            break
        total_pruned += pruned

    if dry_run:
        tty.info(
            f"Would have pruned {total_pruned} orphaned objects from mirror: " + mirror.fetch_url
        )
    else:
        tty.info(f"Pruned {total_pruned} orphaned objects from mirror: {mirror.fetch_url}")
        if total_pruned > 0:
            # If we pruned any objects, the buildcache index is likely out of date.
            # Inform the user about this.
            tty.info(
                "As a consequence of pruning, the buildcache index is now likely out of date."
            )
            tty.info("Run `spack buildcache update-index` to update the index for this mirror.")


def get_buildcache_normalized_time(mirror: Mirror) -> float:
    """
    Get the current time as reported by the buildcache.

    This is necessary because different buildcache implementations may use different
    time formats/time zones. This function creates a temporary file, calls `stat_url`
    on it, and then deletes it. This guarantees that the time used for the beginning
    of the pruning is consistent across all buildcache implementations.
    """
    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as f:
        tmpdir = Path(f)
        touch_file = tmpdir / f".spack-prune-marker-{uuid.uuid4()}"
        touch_file.touch()
        remote_path = url_util.join(mirror.push_url, touch_file.name)

        web_util.push_to_url(
            local_file_path=str(touch_file), remote_path=remote_path, keep_original=True
        )

        stat_info = web_util.stat_url(remote_path)
        assert stat_info is not None
        start_time = stat_info[1]

        web_util.remove_url(remote_path)

        return start_time


def prune_buildcache(mirror: Mirror, keeplist: Optional[str] = None, dry_run: bool = False):
    """
    Runs buildcache pruning for a given mirror.

    Args:
        mirror: Mirror to prune
        keeplist_file: Path to file containing newline-delimited hashes to keep
        dry_run: Whether to perform a dry run without actually deleting
    """
    # Determine the time to use as the "started at" time for pruning.
    # If a cache index exists, use that time. Otherwise, use the current time (normalized
    # to the buildcache's time zone).
    cache_index_url = URLBuildcacheEntry.get_index_url(mirror_url=mirror.fetch_url)
    stat_result = web_util.stat_url(cache_index_url)
    if stat_result is not None:
        started_at = stat_result[1]
    else:
        started_at = get_buildcache_normalized_time(mirror)

    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpspecsdir:
        try:
            manifest_to_mtime_mapping, read_fn, blob_list = _fetch_manifests(mirror, tmpspecsdir)
        except Exception as e:
            raise BuildcachePruningException("Error getting entries from buildcache") from e

        if keeplist:
            prune_direct(
                mirror,
                pathlib.Path(keeplist),
                manifest_to_mtime_mapping,
                read_fn,
                blob_list,
                tmpspecsdir,
                started_at,
                dry_run,
            )

        prune_orphan(
            mirror, manifest_to_mtime_mapping, read_fn, blob_list, tmpspecsdir, started_at, dry_run
        )


class BuildcachePruningException(spack.error.SpackError):
    """
    Raised when pruning fails irrevocably
    """

    pass


class MalformedKeepListException(BuildcachePruningException):
    """
    Raised when the keeplist passed to the direct pruner
    is invalid or malformed in some way
    """

    pass
