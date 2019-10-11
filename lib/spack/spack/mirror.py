# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains code for creating spack mirror directories.  A
mirror is an organized hierarchy containing specially named archive
files.  This enabled spack to know where to find files in a mirror if
the main server for a particular package is down.  Or, if the computer
where spack is run is not connected to the internet, it allows spack
to download packages directly from a mirror (e.g., on an intranet).
"""
import sys
import os
import traceback

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.config
import spack.error
import spack.url as url
import spack.fetch_strategy as fs
from spack.spec import Spec
from spack.version import VersionList


def _determine_extension(fetcher):
    if isinstance(fetcher, fs.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = url.determine_url_file_extension(fetcher.url)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip('.')
            else:
                msg = """\
Unable to parse extension from {0}.

If this URL is for a tarball but does not include the file extension
in the name, you can explicitly declare it with the following syntax:

    version('1.2.3', 'hash', extension='tar.gz')

If this URL is for a download like a .jar or .whl that does not need
to be expanded, or an uncompressed installation script, you can tell
Spack not to expand it with the following syntax:

    version('1.2.3', 'hash', expand=False)
"""
                raise MirrorError(msg.format(fetcher.url))
        else:
            # If the archive shouldn't be expanded, don't check extension.
            ext = None
    else:
        # Otherwise we'll make a .tar.gz ourselves
        ext = 'tar.gz'

    return ext


class MirrorReference(object):
    def __init__(self, cosmetic_path, global_path=None):
        self.global_path = global_path
        self.cosmetic_path = cosmetic_path

    @property
    def storage_path(self):
        if self.global_path:
            return self.global_path
        else:
            return self.cosmetic_path

    def __iter__(self):
        if self.global_path:
            yield self.global_path
        yield self.cosmetic_path


def mirror_archive_paths(fetcher, per_package_ref, spec=None):
    """Get the relative path to the source archive within a mirror."""
    ext = None
    if spec:
        ext = spec.package.versions[spec.package.version].get(
            'extension', None)
    # If the spec does not explicitly specify an extension (the default case),
    # then try to determine it automatically. An extension can only be
    # specified for the primary source of the package (e.g. the source code
    # identified in the 'version' declaration). Resources/patches don't have
    # an option to specify an extension, so it must be inferred for those.
    ext = ext or _determine_extension(fetcher)

    if ext:
        per_package_ref += ".%s" % ext

    global_ref = fetcher.mirror_id()
    if global_ref and ext:
        global_ref += ".%s" % ext

    return MirrorReference(per_package_ref, global_ref)


def get_all_versions(base_specs):
    version_specs = []

    for spec in base_specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        for version in pkg.versions:
            version_spec = Spec(pkg.name)
            version_spec.versions = VersionList([version])
            version_specs.append(version_spec)

    return version_specs


def get_matching_versions(specs, num_versions=1):
    """Get a spec for EACH known version matching any spec in the list.
    For concrete specs, this retrieves the concrete version and, if more
    than one version per spec is requested, retrieves the latest versions
    of the package.
    """
    matching = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        pkg_versions = num_versions

        version_order = list(reversed(sorted(pkg.versions)))
        matching_spec = []
        if spec.concrete:
            matching_spec.append(spec)
            pkg_versions -= 1
            if spec.version in version_order:
                version_order.remove(spec.version)

        for v in version_order:
            # Generate no more than num_versions versions for each spec.
            if pkg_versions < 1:
                break

            # Generate only versions that satisfy the spec.
            if spec.concrete or v.satisfies(spec.versions):
                s = Spec(pkg.name)
                s.versions = VersionList([v])
                s.variants = spec.variants.copy()
                # This is needed to avoid hanging references during the
                # concretization phase
                s.variants.spec = s
                matching_spec.append(s)
                pkg_versions -= 1

        if not matching_spec:
            tty.warn("No known version matches spec: %s" % spec)
        matching.extend(matching_spec)

    return matching


def create(path, specs):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.

    Arguments:
        path: Path to create a mirror directory hierarchy in.
        specs: Any package versions matching these specs will be added \
            to the mirror.

    Return Value:
        Returns a tuple of lists: (present, mirrored, error)

        * present:  Package specs that were already present.
        * mirrored: Package specs that were successfully mirrored.
        * error:    Package specs that failed to mirror due to some error.

    This routine iterates through all known package versions, and
    it creates specs for those versions.  If the version satisfies any spec
    in the specs list, it is downloaded and added to the mirror.
    """
    # automatically spec-ify anything in the specs array.
    specs = [s if isinstance(s, Spec) else Spec(s) for s in specs]

    # Get the absolute path of the root before we start jumping around.
    mirror_root = os.path.abspath(path)
    if not os.path.isdir(mirror_root):
        try:
            mkdirp(mirror_root)
        except OSError as e:
            raise MirrorError(
                "Cannot create directory '%s':" % mirror_root, str(e))

    mirror_cache = spack.caches.MirrorCache(mirror_root)
    mirror_stats = MirrorStats()
    try:
        spack.caches.mirror_cache = mirror_cache
        # Iterate through packages and download all safe tarballs for each
        for spec in specs:
            mirror_stats.next_spec(spec)
            add_single_spec(spec, mirror_root, mirror_stats)
    finally:
        spack.caches.mirror_cache = None

    return mirror_stats.stats()


class MirrorStats(object):
    def __init__(self):
        self.present = {}
        self.new = {}
        self.errors = set()

        self.current_spec = None
        self.added_resources = set()
        self.existing_resources = set()

    def next_spec(self, spec):
        self._tally_current_spec()
        self.current_spec = spec

    def _tally_current_spec(self):
        if self.current_spec:
            if self.added_resources:
                self.new[self.current_spec] = len(self.added_resources)
            if self.existing_resources:
                self.present[self.current_spec] = len(self.existing_resources)
            self.added_resources = set()
            self.existing_resources = set()
        self.current_spec = None

    def stats(self):
        self._tally_current_spec()
        return list(self.present), list(self.new), list(self.errors)

    def already_existed(self, resource):
        # If an error occurred after caching a subset of a spec's
        # resources, a secondary attempt may consider them already added
        if resource not in self.added_resources:
            self.existing_resources.add(resource)

    def added(self, resource):
        self.added_resources.add(resource)

    def error(self):
        self.errors.add(self.current_spec)


def add_single_spec(spec, mirror_root, mirror_stats):
    tty.msg("Adding package {pkg} to mirror".format(
        pkg=spec.format("{name}{@version}")
    ))
    num_retries = 3
    while num_retries > 0:
        try:
            with spec.package.stage as pkg_stage:
                pkg_stage.cache_mirror(mirror_stats)
                for patch in spec.package.all_patches():
                    patch.fetch(pkg_stage)
                    if patch.cache():
                        patch.cache().cache_mirror(mirror_stats)
                    patch.clean()
            exception = None
            break
        except Exception as e:
            exc_tuple = sys.exc_info()
            exception = e
        num_retries -= 1

    if exception:
        if spack.config.get('config:debug'):
            traceback.print_exception(file=sys.stderr, *exc_tuple)
        else:
            tty.warn(
                "Error while fetching %s" % spec.cformat('{name}{@version}'),
                exception.message)
        mirror_stats.error()


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
