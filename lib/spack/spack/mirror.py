##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.config
import spack.error
import spack.url as url
import spack.fetch_strategy as fs
from spack.spec import Spec
from spack.version import VersionList
from spack.util.compression import allowed_archive


def mirror_archive_filename(spec, fetcher, resourceId=None):
    """Get the name of the spec's archive in the mirror."""
    if not spec.version.concrete:
        raise ValueError("mirror.path requires spec with concrete version.")

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

    if resourceId:
        filename = "%s-%s" % (resourceId, spec.version) + ".%s" % ext
    else:
        filename = "%s-%s" % (spec.package.name, spec.version) + ".%s" % ext

    return filename


def mirror_archive_path(spec, fetcher, resourceId=None):
    """Get the relative path to the spec's archive within a mirror."""
    return os.path.join(
        spec.name, mirror_archive_filename(spec, fetcher, resourceId))


def get_matching_versions(specs, **kwargs):
    """Get a spec for EACH known version matching any spec in the list."""
    matching = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        num_versions = kwargs.get('num_versions', 0)
        matching_spec = []
        for i, v in enumerate(reversed(sorted(pkg.versions))):
            # Generate no more than num_versions versions for each spec.
            if num_versions and i >= num_versions:
                break

            # Generate only versions that satisfy the spec.
            if v.satisfies(spec.versions):
                s = Spec(pkg.name)
                s.versions = VersionList([v])
                s.variants = spec.variants.copy()
                # This is needed to avoid hanging references during the
                # concretization phase
                s.variants.spec = s
                matching_spec.append(s)

        if not matching_spec:
            tty.warn("No known version matches spec: %s" % spec)
        matching.extend(matching_spec)

    return matching


def suggest_archive_basename(resource):
    """Return a tentative basename for an archive.

    Raises:
        RuntimeError: if the name is not an allowed archive type.
    """
    basename = os.path.basename(resource.fetcher.url)
    if not allowed_archive(basename):
        raise RuntimeError("%s is not an allowed archive tye" % basename)
    return basename


def create(path, specs, **kwargs):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.

    Arguments:
        path: Path to create a mirror directory hierarchy in.
        specs: Any package versions matching these specs will be added \
            to the mirror.

    Keyword args:
        no_checksum: If True, do not checkpoint when fetching (default False)
        num_versions: Max number of versions to fetch per spec, \
            if spec is ambiguous (default is 0 for all of them)

    Return Value:
        Returns a tuple of lists: (present, mirrored, error)

        * present:  Package specs that were already present.
        * mirrored: Package specs that were successfully mirrored.
        * error:    Package specs that failed to mirror due to some error.

    This routine iterates through all known package versions, and
    it creates specs for those versions.  If the version satisfies any spec
    in the specs list, it is downloaded and added to the mirror.
    """
    # Make sure nothing is in the way.
    if os.path.isfile(path):
        raise MirrorError("%s already exists and is a file." % path)

    # automatically spec-ify anything in the specs array.
    specs = [s if isinstance(s, Spec) else Spec(s) for s in specs]

    # Get concrete specs for each matching version of these specs.
    version_specs = get_matching_versions(
        specs, num_versions=kwargs.get('num_versions', 0))
    for s in version_specs:
        s.concretize()

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

    recursive = True
    # Iterate through packages and download all safe tarballs for each
    visited = set()
    for spec in version_specs:
        if recursive:
            to_add = set(spec.traverse()) - visited
        else:
            to_add = set([spec]) if spec not in visited else set()

        for child_spec in to_add:
            add_single_spec(child_spec, mirror_root, categories, **kwargs)

    return categories['present'], categories['mirrored'], categories['error']


def _fetch_and_archive(name, fetcher, archive_path, do_checksum):
    # This function returns whether the archive path already exists (and the
    # fetcher did not need to retrieve the source)
    if os.path.exists(archive_path):
        tty.msg("{name} : already added".format(name=name))
        return True

    subdir = os.path.dirname(archive_path)
    mkdirp(subdir)

    spec_exists_in_mirror = False
    fetcher.fetch()
    if do_checksum:
        fetcher.check()
        tty.msg("{name} : checksum passed".format(name=name))

    # Fetchers have to know how to archive their files.  Use
    # that to move/copy/create an archive in the mirror.
    fetcher.archive(archive_path)
    tty.msg("{name} : added".format(name=name))
    return False


def add_single_spec(spec, mirror_root, categories, **kwargs):
    tty.msg("Adding package {pkg} to mirror".format(pkg=spec.format("$_$@")))
    spec_exists_in_mirror = True
    do_checksum = not kwargs.get('no_checksum', False)
    try:
        with spec.package.stage:
            for ii, stage in enumerate(spec.package.stage):
                fetcher = stage.fetcher
                archive_path = os.path.abspath(os.path.join(
                        mirror_root, stage.mirror_path))
                if ii == 0:
                    name = spec.cformat("$_$@")
                else:
                    resource = stage.resource
                    name = "{resource} ({pkg}).".format(
                        resource=resource.name, pkg=spec.cformat("$_$@"))

                spec_exists_in_mirror &= _fetch_and_archive(
                    name, fetcher, archive_path, do_checksum)

            for patch in spec.patches:
                try:
                    fetcher = patch.fetcher()
                except AttributeError:
                    continue
                archive_path = os.path.abspath(os.path.join(
                    mirror_root,
                    patch.mirror_archive_path(spec.package.stage)))
                name = "{patch} ({pkg})".format(
                    patch=os.path.basename(patch.path_or_url),
                    pkg=spec.cformat("$_$@"))

                patch_stage = spack.stage.Stage(
                    fetcher, mirror_path=archive_path)
                patch_stage.create()
                _fetch_and_archive(name, fetcher, archive_path, do_checksum)

        if spec_exists_in_mirror:
            categories['present'].append(spec)
        else:
            categories['mirrored'].append(spec)

    except Exception as e:
        if spack.config.get('config:debug'):
            sys.excepthook(*sys.exc_info())
        else:
            tty.warn(
                "Error while fetching %s" % spec.cformat('$_$@'), e.message)
        categories['error'].append(spec)


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
