# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Single util module where Spack should get a git executable."""

import os
import re
import sys
from typing import List, Optional, overload

from spack.vendor.typing_extensions import Literal

import spack.llnl.util.lang
import spack.util.executable as exe

# regex for a commit version
COMMIT_VERSION = re.compile(r"^[a-f0-9]{40}$")


def is_git_commit_sha(string: str) -> bool:
    return len(string) == 40 and bool(COMMIT_VERSION.match(string))


@spack.llnl.util.lang.memoized
def _find_git() -> Optional[str]:
    """Find the git executable in the system path."""
    return exe.which_string("git", required=False)


@overload
def git(required: Literal[True]) -> exe.Executable: ...


@overload
def git(required: bool = ...) -> Optional[exe.Executable]: ...


def git(required: bool = False) -> Optional[exe.Executable]:
    """Get a git executable. Raises CommandNotFoundError if ``required`` and git is not found."""
    git_path = _find_git()

    if not git_path:
        if required:
            raise exe.CommandNotFoundError("spack requires 'git'. Make sure it is in your path.")
        return None

    git = exe.Executable(git_path)

    # If we're running under pytest, add this to ignore the fix for CVE-2022-39253 in
    # git 2.38.1+. Do this in one place; we need git to do this in all parts of Spack.
    if git and "pytest" in sys.modules:
        git.add_default_arg("-c", "protocol.file.allow=always")

    return git


def init_git_repo(
    repository: str, remote: str = "origin", git_exe: Optional[exe.Executable] = None
):
    """Initialize a new Git repository and configure it with a remote."""
    git_exe = git_exe or git(required=True)

    git_exe("init", "--quiet", output=str)
    git_exe("remote", "add", remote, repository)
    # versions of git prior to v2.24 may not have the manyFiles feature
    # so we should ignore errors here on older versions of git
    git_exe("config", "feature.manyFiles", "true", ignore_errors=True)


def pull_checkout_commit(commit: str, git_exe: Optional[exe.Executable] = None):
    """Fetch all remotes and checkout the specified commit."""
    git_exe = git_exe or git(required=True)

    git_exe("fetch", "--quiet", "--progress", "--all")
    git_exe("checkout", commit)


def pull_checkout_tag(
    tag: str,
    remote: str = "origin",
    depth: Optional[int] = None,
    git_exe: Optional[exe.Executable] = None,
):
    """Fetch tags with specified depth and checkout the given tag."""
    git_exe = git_exe or git(required=True)

    fetch_args = ["--quiet", "--progress", "--tags"]
    if depth is not None:
        if depth <= 0:
            raise ValueError("depth must be a positive integer")
        fetch_args.append(f"--depth={depth}")

    git_exe("fetch", *fetch_args, remote)
    git_exe("checkout", tag)


def pull_checkout_branch(
    branch: str,
    remote: str = "origin",
    depth: Optional[int] = None,
    git_exe: Optional[exe.Executable] = None,
):
    """Fetch and checkout branch, then rebase with remote tracking branch."""
    git_exe = git_exe or git(required=True)

    fetch_args = ["--quiet", "--progress"]
    if depth:
        if depth <= 0:
            raise ValueError("depth must be a positive integer")
        fetch_args.append(f"--depth={depth}")

    git_exe("fetch", *fetch_args, remote, branch)
    git_exe("checkout", "--quiet", branch)

    try:
        git_exe("rebase", "--quiet", f"{remote}/{branch}")
    except exe.ProcessError:
        git_exe("rebase", "--abort", fail_on_error=False, error=str, output=str)
        raise


def get_modified_files(
    from_ref: str = "HEAD~1", to_ref: str = "HEAD", git_exe: Optional[exe.Executable] = None
) -> List[str]:
    """Get a list of files modified between ``from_ref`` and ``to_ref``
    Args:
       from_ref (str): oldest git ref, defaults to ``HEAD~1``
       to_ref (str): newer git ref, defaults to ``HEAD``
    Returns: list of file paths
    """
    git_exe = git_exe or git(required=True)

    stdout = git_exe("diff", "--name-only", from_ref, to_ref, output=str)

    return stdout.split()


def get_commit_sha(path: str, ref: str) -> Optional[str]:
    """Get a commit sha for an arbitrary ref using ls-remote"""

    # search for matching branch, annotated tag's commit, then lightweight tag
    ref_list = [f"refs/heads/{ref}", f"refs/tags/{ref}^{{}}", f"refs/tags/{ref}"]

    if os.path.isdir(path):
        # for the filesystem an unpacked mirror could be in a detached state from a depth 1 clone
        # only reference there will be HEAD
        ref_list.append("HEAD")

    for try_ref in ref_list:
        # this command enabled in git@1.7 so no version checking supplied (1.7 released in 2009)
        try:
            query = git(required=True)(
                "ls-remote",
                path,
                try_ref,
                output=str,
                error=os.devnull,
                extra_env={"GIT_TERMINAL_PROMPT": "0"},
            )

            if query:
                return query.strip().split()[0]
        except spack.util.executable.ProcessError:
            continue

    return None


class GitCommandArgumentAssembler:
    def __init__(self, cmd_name, git_exe=None, min_version=(1, 0, 0)):
        self.git_exe = git_exe or git(required=True)
        self.version = self.extract_git_version(self.git_exe)
        self.cmd_min_version = min_version
        self.name = cmd_name
        self.args = []
        # make command unusable for invalid git versions
        if self.cmd_min_version <= self.version:
            self.args.append(self.name)

    @staticmethod
    def extract_git_version(git_exe):
        v_string = git_exe("--version").strip()
        return tuple(int(i) for i in v_string.split("."))

    def add_arguments(self, *args, min_version=(1, 0, 0)):
        if min_version < self.cmd_min_version:
            return
        if self.version >= min_version:
            self.args.extend(args)

    def __call__(self, *args, **exe_args):
        if self.args:
            cmd = self.args + list(args)
            return self.git_exe(*cmd, **exe_args)


def git_fetch_by_ref(git_exe, url, ref, depth=1, sparse_paths=[], debug=False, clone_dir="."):
    if is_git_commit_sha(ref) and GitCommandArgumentAssembler.extract_git_version(git_exe) < (
        2,
        5,
        0,
    ):
        raise spack.util.executable.ProcessError(
            "Git version older than 2.5 and fetch by ref for commit can't be used"
        )
    init = GitCommandArgumentAssembler("init", git_exe)
    fetch = GitCommandArgumentAssembler("fetch", git_exe)
    checkout = GitCommandArgumentAssembler("checkout", git_exe)

    init.add_arguments(clone_dir)
    checkout.add_arguments("FETCH_HEAD")
    if debug:
        fetch.add_arguments("--quiet")
        checkout.add_arguments("--quiet")

    if depth:
        fetch.add_arguments("--depth", str(depth), min_version=(1, 9, 0))
    fetch.add_arguments("--filter=blob:none", min_version=(2, 19, 0))
    fetch.add_arguments(url, ref)

    init()
    fetch()

    if sparse_paths:
        # technically sparse-checkout was added in 2.25, but we go forward since the model we implemented assumes `--cone` is a valid arument
        sparse_checkout = GitCommandArgumentAssembler(
            "sparse-checkout", git_exe, min_version=(2, 34, 0)
        )
        sparse_checkout.add_arguments(*sparse_paths)
        sparse_checkout.add_arguments("--cone")
        sparse_checkout()

    if debug:
        checkout(error=str)
    else:
        checkout()
