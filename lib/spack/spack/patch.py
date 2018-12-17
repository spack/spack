# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import hashlib

import llnl.util.filesystem

import spack.error
import spack.fetch_strategy as fs
import spack.stage
from spack.util.crypto import checksum, Checker

from spack.util.executable import which
from spack.util.compression import allowed_archive


def create(pkg, path_or_url, level=1, working_dir=".", **kwargs):
    """Make either a FilePatch or a UrlPatch, depending on arguments.

      Args:
          pkg: package that needs to be patched
          path_or_url: path or url where the patch is found
          level: patch level (default 1)
          working_dir (str): relative path within the package stage;
              change to this before before applying (default '.')

      Returns:
          (Patch): a patch object on which ``apply(stage)`` can be called
    """
    # Check if we are dealing with a URL (which will be fetched)
    if '://' in path_or_url:
        return UrlPatch(path_or_url, level, working_dir, **kwargs)

    # If not, it's a file patch, which is stored within the repo directory.
    patch_path = os.path.join(pkg.package_dir, path_or_url)
    return FilePatch(patch_path, level, working_dir)


def apply_patch(stage, patch_path, level=1, working_dir='.'):
    """Apply the patch at patch_path to code in the stage.

    Args:
        stage (spack.stage.Stage): stage with code that will be patched
        patch_path (str): filesystem location for the patch to apply
        level (int, optional): patch level (default 1)
        working_dir (str): relative path *within* the stage to change to
            (default '.')
    """
    patch = which("patch", required=True)
    with llnl.util.filesystem.working_dir(stage.source_path):
        patch('-s',
              '-p', str(level),
              '-i', patch_path,
              '-d', working_dir)


class Patch(object):
    """Base class for patches.

    Defines the interface (basically just ``apply()``, at the moment) and
    common variables.
    """
    def __init__(self, path_or_url, level, working_dir):
        # validate level (must be an integer >= 0)
        if not isinstance(level, int) or not level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")

        # Attributes shared by all patch subclasses
        self.path_or_url = path_or_url  # needed for debug output
        self.level = level
        self.working_dir = working_dir

        # path needs to be set by subclasses before calling self.apply()
        self.path = None

    def apply(self, stage):
        """Apply this patch to code in a stage."""
        assert self.path, "self.path must be set before Patch.apply()"
        apply_patch(stage, self.path, self.level, self.working_dir)


class FilePatch(Patch):
    """Describes a patch that is retrieved from a file in the repository"""
    def __init__(self, path, level, working_dir):
        super(FilePatch, self).__init__(path, level, working_dir)

        if not os.path.isfile(path):
            raise NoSuchPatchError("No such patch: %s" % path)
        self.path = path
        self._sha256 = None

    @property
    def sha256(self):
        if self._sha256 is None:
            self._sha256 = checksum(hashlib.sha256, self.path)
        return self._sha256


class UrlPatch(Patch):
    """Describes a patch that is retrieved from a URL"""
    def __init__(self, url, level, working_dir, **kwargs):
        super(UrlPatch, self).__init__(url, level, working_dir)

        self.url = url

        self.archive_sha256 = kwargs.get('archive_sha256')
        if allowed_archive(self.url) and not self.archive_sha256:
            raise PatchDirectiveError(
                "Compressed patches require 'archive_sha256' "
                "and patch 'sha256' attributes: %s" % self.url)

        self.sha256 = kwargs.get('sha256')
        if not self.sha256:
            raise PatchDirectiveError("URL patches require a sha256 checksum")

    def apply(self, stage):
        """Retrieve the patch in a temporary stage, computes
        self.path and calls `super().apply(stage)`

        Args:
            stage: stage for the package that needs to be patched
        """
        # use archive digest for compressed archives
        fetch_digest = self.sha256
        if self.archive_sha256:
            fetch_digest = self.archive_sha256

        fetcher = fs.URLFetchStrategy(self.url, fetch_digest)
        mirror = os.path.join(
            os.path.dirname(stage.mirror_path),
            os.path.basename(self.url))

        with spack.stage.Stage(fetcher, mirror_path=mirror) as patch_stage:
            patch_stage.fetch()
            patch_stage.check()
            patch_stage.cache_local()

            root = patch_stage.path
            if self.archive_sha256:
                patch_stage.expand_archive()
                root = patch_stage.source_path

            files = os.listdir(root)
            if not files:
                if self.archive_sha256:
                    raise NoSuchPatchError(
                        "Archive was empty: %s" % self.url)
                else:
                    raise NoSuchPatchError(
                        "Patch failed to download: %s" % self.url)

            self.path = os.path.join(root, files.pop())

            if not os.path.isfile(self.path):
                raise NoSuchPatchError(
                    "Archive %s contains no patch file!" % self.url)

            # for a compressed archive, Need to check the patch sha256 again
            # and the patch is in a directory, not in the same place
            if self.archive_sha256 and spack.config.get('config:checksum'):
                checker = Checker(self.sha256)
                if not checker.check(self.path):
                    raise fs.ChecksumError(
                        "sha256 checksum failed for %s" % self.path,
                        "Expected %s but got %s" % (self.sha256, checker.sum))

            super(UrlPatch, self).apply(stage)


class NoSuchPatchError(spack.error.SpackError):
    """Raised when a patch file doesn't exist."""


class PatchDirectiveError(spack.error.SpackError):
    """Raised when the wrong arguments are suppled to the patch directive."""
