##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os

import spack
import spack.error
import spack.stage
import spack.fetch_strategy as fs

from llnl.util.filesystem import join_path
from spack.util.executable import which


class Patch(object):
    """Base class to describe a patch that needs to be applied to some
    expanded source code.
    """

    @staticmethod
    def create(pkg, path_or_url, level, **kwargs):
        """
        Factory method that creates an instance of some class derived from
        Patch

        Args:
            pkg: package that needs to be patched
            path_or_url: path or url where the patch is found
            level: patch level

        Returns:
            instance of some Patch class
        """
        # Check if we are dealing with a URL
        if '://' in path_or_url:
            return UrlPatch(pkg, path_or_url, level, **kwargs)
        # Assume patches are stored in the repository
        return FilePatch(pkg, path_or_url, level)

    def __init__(self, pkg, path_or_url, level):
        # Check on level (must be an integer > 0)
        if not isinstance(level, int) or not level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")
        # Attributes shared by all patch subclasses
        self.path_or_url = path_or_url
        self.level = level
        # self.path needs to be computed by derived classes
        # before a call to apply
        self.path = None

        if not isinstance(self.level, int) or not self.level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")

    def apply(self, stage):
        """Apply the patch at self.path to the source code in the
        supplied stage

        Args:
            stage: stage for the package that needs to be patched
        """
        stage.chdir_to_source()
        # Use -N to allow the same patches to be applied multiple times.
        _patch = which("patch", required=True)
        _patch('-s', '-p', str(self.level), '-i', self.path)


class FilePatch(Patch):
    """Describes a patch that is retrieved from a file in the repository"""
    def __init__(self, pkg, path_or_url, level):
        super(FilePatch, self).__init__(pkg, path_or_url, level)

        pkg_dir = spack.repo.dirname_for_package_name(pkg.name)
        self.path = join_path(pkg_dir, path_or_url)
        if not os.path.isfile(self.path):
            raise NoSuchPatchFileError(pkg.name, self.path)


class UrlPatch(Patch):
    """Describes a patch that is retrieved from a URL"""
    def __init__(self, pkg, path_or_url, level, **kwargs):
        super(UrlPatch, self).__init__(pkg, path_or_url, level)
        self.url = path_or_url
        self.md5 = kwargs.get('md5')

    def apply(self, stage):
        """Retrieve the patch in a temporary stage, computes
        self.path and calls `super().apply(stage)`

        Args:
            stage: stage for the package that needs to be patched
        """
        fetcher = fs.URLFetchStrategy(self.url, digest=self.md5)
        mirror = join_path(
            os.path.dirname(stage.mirror_path),
            os.path.basename(self.url)
        )
        with spack.stage.Stage(fetcher, mirror_path=mirror) as patch_stage:
            patch_stage.fetch()
            patch_stage.check()
            patch_stage.cache_local()
            patch_stage.expand_archive()
            self.path = os.path.abspath(
                os.listdir(patch_stage.path).pop()
            )
            super(UrlPatch, self).apply(stage)


class NoSuchPatchFileError(spack.error.SpackError):
    """Raised when user specifies a patch file that doesn't exist."""

    def __init__(self, package, path):
        super(NoSuchPatchFileError, self).__init__(
            "No such patch file for package %s: %s" % (package, path))
        self.package = package
        self.path = path
