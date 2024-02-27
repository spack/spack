# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import inspect
import os
import os.path
import pathlib
import sys

import llnl.util.filesystem
import llnl.util.lang
from llnl.url import allowed_archive

import spack
import spack.error
import spack.fetch_strategy as fs
import spack.mirror
import spack.repo
import spack.stage
import spack.util.spack_json as sjson
from spack.util.crypto import Checker, checksum
from spack.util.executable import which, which_string


def apply_patch(stage, patch_path, level=1, working_dir="."):
    """Apply the patch at patch_path to code in the stage.

    Args:
        stage (spack.stage.Stage): stage with code that will be patched
        patch_path (str): filesystem location for the patch to apply
        level (int or None): patch level (default 1)
        working_dir (str): relative path *within* the stage to change to
            (default '.')
    """
    git_utils_path = os.environ.get("PATH", "")
    if sys.platform == "win32":
        git = which_string("git")
        if git:
            git = pathlib.Path(git)
            git_root = git.parent.parent
            git_root = git_root / "usr" / "bin"
            git_utils_path = os.pathsep.join([str(git_root), git_utils_path])

    # TODO: Decouple Spack's patch support on Windows from Git
    # for Windows, and instead have Spack directly fetch, install, and
    # utilize that patch.
    # Note for future developers: The GNU port of patch to windows
    # has issues handling CRLF line endings unless the --binary
    # flag is passed.
    patch = which("patch", required=True, path=git_utils_path)
    with llnl.util.filesystem.working_dir(stage.source_path):
        patch("-s", "-p", str(level), "-i", patch_path, "-d", working_dir)


class Patch:
    """Base class for patches.

    Arguments:
        pkg (str): the package that owns the patch

    The owning package is not necessarily the package to apply the patch
    to -- in the case where a dependent package patches its dependency,
    it is the dependent's fullname.

    """

    def __init__(self, pkg, path_or_url, level, working_dir):
        # validate level (must be an integer >= 0)
        if not isinstance(level, int) or not level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")

        # Attributes shared by all patch subclasses
        self.owner = pkg.fullname
        self.path_or_url = path_or_url  # needed for debug output
        self.path = None  # must be set before apply()
        self.level = level
        self.working_dir = working_dir

    def apply(self, stage: "spack.stage.Stage"):
        """Apply a patch to source in a stage.

        Arguments:
            stage (spack.stage.Stage): stage where source code lives
        """
        if not self.path or not os.path.isfile(self.path):
            raise NoSuchPatchError(f"No such patch: {self.path}")

        apply_patch(stage, self.path, self.level, self.working_dir)

    @property
    def stage(self):
        return None

    def to_dict(self):
        """Partial dictionary -- subclases should add to this."""
        return {
            "owner": self.owner,
            "sha256": self.sha256,
            "level": self.level,
            "working_dir": self.working_dir,
        }

    def __eq__(self, other):
        return self.sha256 == other.sha256

    def __hash__(self):
        return hash(self.sha256)


class FilePatch(Patch):
    """Describes a patch that is retrieved from a file in the repository.

    Arguments:
        pkg (str): the class object for the package that owns the patch
        relative_path (str): path to patch, relative to the repository
            directory for a package.
        level (int): level to pass to patch command
        working_dir (str): path within the source directory where patch
            should be applied
    """

    def __init__(self, pkg, relative_path, level, working_dir, ordering_key=None):
        self.relative_path = relative_path

        # patches may be defined by relative paths to parent classes
        # search mro to look for the file
        abs_path = None
        # At different times we call FilePatch on instances and classes
        pkg_cls = pkg if inspect.isclass(pkg) else pkg.__class__
        for cls in inspect.getmro(pkg_cls):
            if not hasattr(cls, "module"):
                # We've gone too far up the MRO
                break

            # Cannot use pkg.package_dir because it's a property and we have
            # classes, not instances.
            pkg_dir = os.path.abspath(os.path.dirname(cls.module.__file__))
            path = os.path.join(pkg_dir, self.relative_path)
            if os.path.exists(path):
                abs_path = path
                break

        if abs_path is None:
            msg = "FilePatch: Patch file %s for " % relative_path
            msg += "package %s.%s does not exist." % (pkg.namespace, pkg.name)
            raise ValueError(msg)

        super().__init__(pkg, abs_path, level, working_dir)
        self.path = abs_path
        self._sha256 = None
        self.ordering_key = ordering_key

    @property
    def sha256(self):
        if self._sha256 is None:
            self._sha256 = checksum(hashlib.sha256, self.path)
        return self._sha256

    def to_dict(self):
        return llnl.util.lang.union_dicts(super().to_dict(), {"relative_path": self.relative_path})


class UrlPatch(Patch):
    """Describes a patch that is retrieved from a URL.

    Arguments:
        pkg (str): the package that owns the patch
        url (str): URL where the patch can be fetched
        level (int): level to pass to patch command
        working_dir (str): path within the source directory where patch
            should be applied
    """

    def __init__(self, pkg, url, level=1, working_dir=".", ordering_key=None, **kwargs):
        super().__init__(pkg, url, level, working_dir)

        self.url = url
        self._stage = None

        self.ordering_key = ordering_key

        self.archive_sha256 = kwargs.get("archive_sha256")
        if allowed_archive(self.url) and not self.archive_sha256:
            raise PatchDirectiveError(
                "Compressed patches require 'archive_sha256' "
                "and patch 'sha256' attributes: %s" % self.url
            )

        self.sha256 = kwargs.get("sha256")
        if not self.sha256:
            raise PatchDirectiveError("URL patches require a sha256 checksum")

    def apply(self, stage: "spack.stage.Stage"):
        assert self.stage.expanded, "Stage must be expanded before applying patches"

        # Get the patch file.
        files = os.listdir(self.stage.source_path)
        assert len(files) == 1, "Expected one file in stage source path, found %s" % files
        self.path = os.path.join(self.stage.source_path, files[0])

        return super().apply(stage)

    @property
    def stage(self):
        if self._stage:
            return self._stage

        fetch_digest = self.archive_sha256 or self.sha256

        # Two checksums, one for compressed file, one for its contents
        if self.archive_sha256:
            fetcher = fs.FetchAndVerifyExpandedFile(
                self.url, archive_sha256=self.archive_sha256, expanded_sha256=self.sha256
            )
        else:
            fetcher = fs.URLFetchStrategy(self.url, sha256=self.sha256, expand=False)

        # The same package can have multiple patches with the same name but
        # with different contents, therefore apply a subset of the hash.
        name = "{0}-{1}".format(os.path.basename(self.url), fetch_digest[:7])

        per_package_ref = os.path.join(self.owner.split(".")[-1], name)
        mirror_ref = spack.mirror.mirror_archive_paths(fetcher, per_package_ref)
        self._stage = spack.stage.Stage(
            fetcher,
            name=f"{spack.stage.stage_prefix}patch-{fetch_digest}",
            mirror_paths=mirror_ref,
        )
        return self._stage

    def to_dict(self):
        data = super().to_dict()
        data["url"] = self.url
        if self.archive_sha256:
            data["archive_sha256"] = self.archive_sha256
        return data


def from_dict(dictionary, repository=None):
    """Create a patch from json dictionary."""
    repository = repository or spack.repo.PATH
    owner = dictionary.get("owner")
    if "owner" not in dictionary:
        raise ValueError("Invalid patch dictionary: %s" % dictionary)
    pkg_cls = repository.get_pkg_class(owner)

    if "url" in dictionary:
        return UrlPatch(
            pkg_cls,
            dictionary["url"],
            dictionary["level"],
            dictionary["working_dir"],
            sha256=dictionary["sha256"],
            archive_sha256=dictionary.get("archive_sha256"),
        )

    elif "relative_path" in dictionary:
        patch = FilePatch(
            pkg_cls, dictionary["relative_path"], dictionary["level"], dictionary["working_dir"]
        )

        # If the patch in the repo changes, we cannot get it back, so we
        # just check it and fail here.
        # TODO: handle this more gracefully.
        sha256 = dictionary["sha256"]
        checker = Checker(sha256)
        if not checker.check(patch.path):
            raise fs.ChecksumError(
                "sha256 checksum failed for %s" % patch.path,
                "Expected %s but got %s " % (sha256, checker.sum)
                + "Patch may have changed since concretization.",
            )
        return patch
    else:
        raise ValueError("Invalid patch dictionary: %s" % dictionary)


class PatchCache:
    """Index of patches used in a repository, by sha256 hash.

    This allows us to look up patches without loading all packages.  It's
    also needed to properly implement dependency patching, as need a way
    to look up patches that come from packages not in the Spec sub-DAG.

    The patch index is structured like this in a file (this is YAML, but
    we write JSON)::

        patches:
            sha256:
                namespace1.package1:
                    <patch json>
                namespace2.package2:
                    <patch json>
                ... etc. ...

    """

    def __init__(self, repository, data=None):
        if data is None:
            self.index = {}
        else:
            if "patches" not in data:
                raise IndexError("invalid patch index; try `spack clean -m`")
            self.index = data["patches"]

        self.repository = repository

    @classmethod
    def from_json(cls, stream, repository):
        return PatchCache(repository=repository, data=sjson.load(stream))

    def to_json(self, stream):
        sjson.dump({"patches": self.index}, stream)

    def patch_for_package(self, sha256: str, pkg):
        """Look up a patch in the index and build a patch object for it.

        Arguments:
            sha256: sha256 hash to look up
            pkg (spack.package_base.PackageBase): Package object to get patch for.

        We build patch objects lazily because building them requires that
        we have information about the package's location in its repo."""
        sha_index = self.index.get(sha256)
        if not sha_index:
            raise PatchLookupError(
                f"Couldn't find patch for package {pkg.fullname} with sha256: {sha256}"
            )

        # Find patches for this class or any class it inherits from
        for fullname in pkg.fullnames:
            patch_dict = sha_index.get(fullname)
            if patch_dict:
                break
        else:
            raise PatchLookupError(
                f"Couldn't find patch for package {pkg.fullname} with sha256: {sha256}"
            )

        # add the sha256 back (we take it out on write to save space,
        # because it's the index key)
        patch_dict = dict(patch_dict)
        patch_dict["sha256"] = sha256
        return from_dict(patch_dict, repository=self.repository)

    def update_package(self, pkg_fullname):
        # remove this package from any patch entries that reference it.
        empty = []
        for sha256, package_to_patch in self.index.items():
            remove = []
            for fullname, patch_dict in package_to_patch.items():
                if patch_dict["owner"] == pkg_fullname:
                    remove.append(fullname)

            for fullname in remove:
                package_to_patch.pop(fullname)

            if not package_to_patch:
                empty.append(sha256)

        # remove any entries that are now empty
        for sha256 in empty:
            del self.index[sha256]

        # update the index with per-package patch indexes
        pkg_cls = self.repository.get_pkg_class(pkg_fullname)
        partial_index = self._index_patches(pkg_cls)
        for sha256, package_to_patch in partial_index.items():
            p2p = self.index.setdefault(sha256, {})
            p2p.update(package_to_patch)

    def update(self, other):
        """Update this cache with the contents of another."""
        for sha256, package_to_patch in other.index.items():
            p2p = self.index.setdefault(sha256, {})
            p2p.update(package_to_patch)

    @staticmethod
    def _index_patches(pkg_class):
        index = {}

        # Add patches from the class
        for cond, patch_list in pkg_class.patches.items():
            for patch in patch_list:
                patch_dict = patch.to_dict()
                patch_dict.pop("sha256")  # save some space
                index[patch.sha256] = {pkg_class.fullname: patch_dict}

        for deps_by_name in pkg_class.dependencies.values():
            for dependency in deps_by_name.values():
                for patch_list in dependency.patches.values():
                    for patch in patch_list:
                        dspec_cls = spack.repo.PATH.get_pkg_class(dependency.spec.fullname)
                        patch_dict = patch.to_dict()
                        patch_dict.pop("sha256")  # save some space
                        index[patch.sha256] = {dspec_cls.fullname: patch_dict}

        return index


class NoSuchPatchError(spack.error.SpackError):
    """Raised when a patch file doesn't exist."""


class PatchLookupError(NoSuchPatchError):
    """Raised when a patch file cannot be located from sha256."""


class PatchDirectiveError(spack.error.SpackError):
    """Raised when the wrong arguments are suppled to the patch directive."""
