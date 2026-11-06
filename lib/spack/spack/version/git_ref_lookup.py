# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Optional, Tuple

import spack.config
import spack.fetch_strategy
import spack.paths
import spack.repo
import spack.util.executable
import spack.util.file_cache
import spack.util.hash
import spack.util.spack_json as sjson
from spack.util.filesystem import mkdirp, working_dir

from .common import VersionLookupError
from .version_types import GitVersion, StandardVersion, VersionList, VersionType

if TYPE_CHECKING:
    import spack.spec

# regular expression for semantic versioning
_VERSION_CORE = r"\d+\.\d+\.\d+"
_IDENT = r"[0-9A-Za-z-]+"
_SEPARATED_IDENT = rf"{_IDENT}(?:\.{_IDENT})*"
_PRERELEASE = rf"\-{_SEPARATED_IDENT}"
_BUILD = rf"\+{_SEPARATED_IDENT}"
_SEMVER = rf"{_VERSION_CORE}(?:{_PRERELEASE})?(?:{_BUILD})?"

# clamp on the end, so versions like v1.2.3-rc1 will match
# without the leading 'v'.
SEMVER_REGEX = re.compile(rf"{_SEMVER}$")


class GitRefLookup:
    """An object for cached lookups of git refs. GitRefLookup objects delegate to the misc cache
    for locking."""

    def __init__(
        self,
        pkg_name: str,
        *,
        repo: spack.repo.RepoPath,
        misc_cache: spack.util.file_cache.FileCache,
        config: spack.config.Configuration,
    ) -> None:
        self.pkg_name = pkg_name
        self.repo = repo
        self.misc_cache = misc_cache
        self.config = config

        self.data: Dict[str, Tuple[Optional[str], int]] = {}

        self._pkg = None
        self._fetcher = None
        self._cache_key = None

    @property
    def cache_key(self):
        if not self._cache_key:
            key_base = "git_metadata"
            self._cache_key = (Path(key_base) / self.repository_uri).as_posix()

        return self._cache_key

    @property
    def pkg(self):
        if not self._pkg:
            try:
                pkg = self.repo.get_pkg_class(self.pkg_name)
                pkg.git
            except (spack.repo.RepoError, AttributeError) as e:
                raise VersionLookupError(f"Couldn't get the git repo for {self.pkg_name}") from e
            self._pkg = pkg
        return self._pkg

    @property
    def fetcher(self):
        if not self._fetcher:
            # We require the full git repository history
            fetcher = spack.fetch_strategy.GitFetchStrategy(git=self.pkg.git, config=self.config)
            fetcher.get_full_repo = True
            self._fetcher = fetcher
        return self._fetcher

    @property
    def repository_uri(self):
        """Identifier for git repos used within the repo and metadata caches."""
        return Path(spack.util.hash.b32_hash(self.pkg.git)[-7:])

    def save(self):
        """Save the data to file"""
        with self.misc_cache.write_transaction(self.cache_key) as (old, new):
            sjson.dump(self.data, new)

    def load_data(self):
        """Load data if the path already exists."""
        with self.misc_cache.read_transaction(self.cache_key) as cache_file:
            if cache_file is not None:
                self.data = sjson.load(cache_file)

    def get(self, ref) -> Tuple[Optional[str], int]:
        if not self.data:
            self.load_data()

        if ref not in self.data:
            self.data[ref] = self.lookup_ref(ref)
            self.save()

        return self.data[ref]

    def lookup_ref(self, ref) -> Tuple[Optional[str], int]:
        """Lookup the previous version and distance for a given commit.

        We use git to compare the known versions from package to the git tags,
        as well as any git tags that are SEMVER versions, and find the latest
        known version prior to the commit, as well as the distance from that version
        to the commit in the git repo. Those values are used to compare Version objects.
        """
        pathlib_dest = Path(spack.paths.user_repos_cache_path) / self.repository_uri
        dest = str(pathlib_dest)

        # prepare a cache for the repository
        dest_parent = os.path.dirname(dest)
        if not os.path.exists(dest_parent):
            mkdirp(dest_parent)

        # Only clone if we don't have it!
        if not os.path.exists(dest):
            self.fetcher.bare_clone(dest)

        # Lookup commit info
        with working_dir(dest):
            # TODO: we need to update the local tags if they changed on the
            # remote instance, simply adding '-f' may not be sufficient
            # (if commits are deleted on the remote, this command alone
            # won't properly update the local rev-list)
            self.fetcher.git("fetch", "--tags", output=os.devnull, error=os.devnull)

            # Ensure ref is a commit object known to git
            # Note the brackets are literals, the ref replaces the format string
            try:
                self.fetcher.git(
                    "cat-file", "-e", "%s^{commit}" % ref, output=os.devnull, error=os.devnull
                )
            except spack.util.executable.ProcessError:
                raise VersionLookupError("%s is not a valid git ref for %s" % (ref, self.pkg_name))

            # List tags (refs) by date, so last reference of a tag is newest
            tag_info = self.fetcher.git(
                "for-each-ref",
                "--sort=creatordate",
                "--format",
                "%(objectname) %(refname)",
                "refs/tags",
                output=str,
            ).split("\n")

            # Lookup of commits to spack versions
            commit_to_version = {}

            for entry in tag_info:
                if not entry:
                    continue
                tag_commit, tag = entry.split()
                tag = tag.replace("refs/tags/", "", 1)

                # For each tag, try to match to a version
                for v in [v.string for v in self.pkg.versions]:
                    if v == tag or "v" + v == tag:
                        commit_to_version[tag_commit] = v
                        break
                else:
                    # try to parse tag to compare versions spack does not know
                    match = SEMVER_REGEX.search(tag)
                    if match:
                        commit_to_version[tag_commit] = match.group()

            ancestor_commits = []
            for tag_commit in commit_to_version:
                self.fetcher.git("merge-base", "--is-ancestor", tag_commit, ref, ignore_errors=[1])
                if self.fetcher.git.returncode == 0:
                    distance = self.fetcher.git(
                        "rev-list", "%s..%s" % (tag_commit, ref), "--count", output=str, error=str
                    ).strip()
                    ancestor_commits.append((tag_commit, int(distance)))

            if ancestor_commits:
                # Get nearest ancestor that is a known version
                prev_version_commit, distance = min(ancestor_commits, key=lambda x: x[1])
                prev_version = commit_to_version[prev_version_commit]
            else:
                # Get list of all commits, this is in reverse order
                # We use this to get the first commit below
                ref_info = self.fetcher.git("log", "--all", "--pretty=format:%H", output=str)
                commits = [c for c in ref_info.split("\n") if c]

                # No previous version and distance from first commit
                prev_version = None
                distance = int(
                    self.fetcher.git(
                        "rev-list", "%s..%s" % (commits[-1], ref), "--count", output=str, error=str
                    ).strip()
                )

        return prev_version, distance


def assign_git_version(
    pkg_name: str,
    version: VersionType,
    *,
    repo: spack.repo.RepoPath,
    misc_cache: spack.util.file_cache.FileCache,
    config: spack.config.Configuration,
) -> VersionType:
    """Return ``version`` with a Spack version assigned, by looking its ref up in the git
    repository of package ``pkg_name``. This may trigger a git clone.

    Assignment queries the git repo for the most recent version previous to this git ref, as
    well as the distance between them expressed as a number of commits. If the previous
    version is ``X.Y.Z`` and the distance is ``D``, the git commit version is represented by
    the tuple ``(X, Y, Z, '', D)``. The component ``''`` cannot be parsed as part of any valid
    version, but is a valid component. This allows a git ref version to be less than (older
    than) every Version newer than its previous version, but still newer than its previous
    version.

    To find the previous version from a git ref version, Spack queries the git repo for its
    tags. Any tag that matches a version known to Spack is associated with that version, as
    is any tag that is a known version prepended with the character ``v`` (i.e., a tag
    ``v1.0`` is associated with the known version ``1.0``). Additionally, any tag that
    represents a semver version (X.Y.Z with X, Y, Z all integers) is associated with the
    version it represents, even if that version is not known to Spack. Each tag is then
    queried in git to see whether it is an ancestor of the git ref in question, and if so
    the distance between the two. The previous version is the version that is an ancestor
    with the least distance from the git ref in question.

    Raises a ``VersionLookupError`` when the package has no ``git`` attribute, the ref is
    unknown, or the version found is outside the range the ref is constrained to.
    """
    if not isinstance(version, GitVersion) or version.std_version is not None:
        return version
    version_string, distance = GitRefLookup(
        pkg_name, repo=repo, misc_cache=misc_cache, config=config
    ).get(version.ref)
    version_string = version_string or "0"
    # Add a -git.<distance> suffix when we're not exactly on a tag
    if distance > 0:
        version_string += f"-git.{distance}"
    return version.assigned(StandardVersion.from_string(version_string))


def _needs_assignment(node: "spack.spec.Spec") -> bool:
    return bool(node.name) and any(
        isinstance(v, GitVersion) and v.std_version is None for v in node.versions
    )


def assign_git_versions(
    spec: "spack.spec.Spec",
    *,
    repo: spack.repo.RepoPath,
    misc_cache: spack.util.file_cache.FileCache,
    config: spack.config.Configuration,
) -> "spack.spec.Spec":
    """Return a copy of ``spec`` in which every git ref version is assigned a Spack version, or
    ``spec`` itself when there are no git ref versions to assign."""
    if not any(_needs_assignment(node) for node in spec.traverse()):
        return spec
    result = spec.copy()
    for node in result.traverse():
        if _needs_assignment(node):
            node.versions = VersionList(
                [
                    assign_git_version(
                        node.fullname, v, repo=repo, misc_cache=misc_cache, config=config
                    )
                    for v in node.versions
                ]
            )
    return result
