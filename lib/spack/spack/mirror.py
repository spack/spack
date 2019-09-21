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
from spack.util.compression import allowed_archive


def mirror_archive_filename(spec, fetcher, resource_name=None):
    """Get the name of the spec's archive in the mirror."""
    if not spec.version.concrete:
        raise ValueError("mirror.path requires spec with concrete version.")

    if resource_name:
        if fetcher.source_id():
            resource_id = str(fetcher.source_id())
        else:
            resource_id = str(spec.version)
        filename = "%s-%s" % (resource_name, resource_id)
    else:
        filename = "%s-%s" % (spec.package.name, spec.version)

    ext = _determine_extension(fetcher, spec)
    if ext:
        return filename + ".%s" % ext
    else:
        return filename


def _determine_extension(fetcher, spec):
    if isinstance(fetcher, fs.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = url.determine_url_file_extension(fetcher.url)

            # If the filename does not end with a normal suffix,
            # see if the package explicitly declares the extension
            if not ext:
                ext = spec.package.versions[spec.package.version].get(
                    'extension', None)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip('.')

            if not ext:
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


def mirror_archive_paths(spec, fetcher, resource_name=None):
    """Get the relative path to the spec's archive within a mirror."""
    per_package_ref = os.path.join(
        spec.name, mirror_archive_filename(spec, fetcher, resource_name))

    global_ref = fetcher.mirror_id()
    if not global_ref:
        return [per_package_ref]

    ext = _determine_extension(fetcher, spec)
    if ext:
        global_ref += ".%s" % ext

    return [global_ref, per_package_ref]


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
            version_spec.versions = VersionList([v])
            version_specs.append(version_spec)


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

    # Things to keep track of while parsing specs.
    categories = {
        'present': [],
        'mirrored': [],
        'error': []
    }

    mirror_cache = spack.caches.MirrorCache(mirror_root)
    try:
        spack.caches.mirror_cache = mirror_cache
        # Iterate through packages and download all safe tarballs for each
        for spec in specs:
            add_single_spec(spec, mirror_root, categories)
    finally:
        spack.caches.mirror_cache = None

    categories['mirrored'] = list(mirror_cache.new_resources)
    categories['present'] = list(mirror_cache.existing_resources)

    return categories['present'], categories['mirrored'], categories['error']


def add_single_spec(spec, mirror_root, categories):
    tty.msg("Adding package {pkg} to mirror".format(
        pkg=spec.format("{name}{@version}")
    ))
    num_retries = 3
    while num_retries > 0:
        try:
            spec.package.do_fetch()
            exception = None
            break
        except Exception as e:
            exception = sys.exc_info()
        finally:
            num_retries -= 1
            spec.package.do_clean()

    if exception:
        if spack.config.get('config:debug'):
            traceback.print_exception(file=sys.stderr, *exception)
        else:
            tty.warn(
                "Error while fetching %s" % spec.cformat('{name}{@version}'),
                e.message)
        categories['error'].append(spec)


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
