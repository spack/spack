##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
This file contains code for creating spack mirror directories.  A
mirror is an organized hierarchy containing specially named archive
files.  This enabled spack to know where to find files in a mirror if
the main server for a particualr package is down.  Or, if the computer
where spack is run is not connected to the internet, it allows spack
to download packages directly from a mirror (e.g., on an intranet).
"""
import sys
import os
import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack
import spack.error
import spack.url as url
import spack.fetch_strategy as fs
from spack.spec import Spec
from spack.stage import Stage
from spack.version import *
from spack.util.compression import extension


def mirror_archive_filename(spec):
    """Get the path that this spec will live at within a mirror."""
    if not spec.version.concrete:
        raise ValueError("mirror.path requires spec with concrete version.")

    fetcher = spec.package.fetcher
    if isinstance(fetcher, fs.URLFetchStrategy):
        # If we fetch this version with a URLFetchStrategy, use URL's archive type
        ext = url.downloaded_file_extension(fetcher.url)
    else:
        # Otherwise we'll make a .tar.gz ourselves
        ext = 'tar.gz'

    return "%s-%s.%s" % (spec.package.name, spec.version, ext)


def get_matching_versions(specs, **kwargs):
    """Get a spec for EACH known version matching any spec in the list."""
    matching = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s." % pkg.name)
            continue

        num_versions = kwargs.get('num_versions', 0)
        for i, v in enumerate(reversed(sorted(pkg.versions))):
            # Generate no more than num_versions versions for each spec.
            if num_versions and i >= num_versions:
                break

            # Generate only versions that satisfy the spec.
            if v.satisfies(spec.versions):
                s = Spec(pkg.name)
                s.versions = VersionList([v])
                matching.append(s)

    return matching


def create(path, specs, **kwargs):
    """Create a directory to be used as a spack mirror, and fill it with
       package archives.

       Arguments:
         path    Path to create a mirror directory hierarchy in.
         specs   Any package versions matching these specs will be added
                 to the mirror.

       Keyword args:
         no_checksum:  If True, do not checkpoint when fetching (default False)
         num_versions: Max number of versions to fetch per spec,
                       if spec is ambiguous (default is 0 for all of them)

       Return Value:
         Returns a tuple of lists: (present, mirrored, error)
         * present:  Package specs that were already prsent.
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
        mkdirp(mirror_root)

    # Things to keep track of while parsing specs.
    present  = []
    mirrored = []
    error    = []

    # Iterate through packages and download all the safe tarballs for each of them
    for spec in version_specs:
        pkg = spec.package

        stage = None
        try:
            # create a subdirectory for the current package@version
            subdir = join_path(mirror_root, pkg.name)
            mkdirp(subdir)

            archive_file = mirror_archive_filename(spec)
            archive_path = join_path(subdir, archive_file)

            if os.path.exists(archive_path):
                tty.msg("Already added %s" % spec.format("$_$@"))
                present.append(spec)
                continue

            # Set up a stage and a fetcher for the download
            unique_fetch_name = spec.format("$_$@")
            fetcher = fs.for_package_version(pkg, pkg.version)
            stage = Stage(fetcher, name=unique_fetch_name)
            fetcher.set_stage(stage)

            # Do the fetch and checksum if necessary
            fetcher.fetch()
            if not kwargs.get('no_checksum', False):
                fetcher.check()
                tty.msg("Checksum passed for %s@%s" % (pkg.name, pkg.version))

            # Fetchers have to know how to archive their files.  Use
            # that to move/copy/create an archive in the mirror.
            fetcher.archive(archive_path)
            tty.msg("Added %s." % spec.format("$_$@"))
            mirrored.append(spec)

        except Exception, e:
            if spack.debug:
                sys.excepthook(*sys.exc_info())
            else:
                tty.warn("Error while fetching %s." % spec.format('$_$@'), e.message)
            error.append(spec)

        finally:
            if stage:
                stage.destroy()

    return (present, mirrored, error)


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""
    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
