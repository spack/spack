# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Single util module where Spack should get a git executable."""

import os
import sys
from typing import List, Optional, overload

from _vendoring.typing_extensions import Literal

import llnl.util.lang

import spack.util.executable as exe


@llnl.util.lang.memoized
def _find_git() -> Optional[str]:
    """Find the git executable in the system path."""
    return exe.which_string("git", required=False)


@overload
def git(required: Literal[True]) -> exe.Executable: ...


@overload
def git(required: bool = ...) -> Optional[exe.Executable]: ...


def git(required: bool = False) -> Optional[exe.Executable]:
    """Get a git executable. Raises CommandNotFoundError if `required` and git is not found."""
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

    git_exe("fetch", "--all")
    git_exe("checkout", commit)


def pull_checkout_tag(
    tag: str, remote: str = "origin", depth: int = 20, git_exe: Optional[exe.Executable] = None
):
    """Fetch tags with specified depth and checkout the given tag."""
    git_exe = git_exe or git(required=True)

    git_exe("fetch", f"--depth={depth}", "--force", "--tags", remote)
    git_exe("checkout", tag)


def pull_checkout_branch(
    branch: str, remote: str = "origin", depth: int = 20, git_exe: Optional[exe.Executable] = None
):
    """Fetch and checkout branch, then rebase with remote tracking branch."""
    git_exe = git_exe or git(required=True)

    git_exe("fetch", f"--depth={depth}", remote, branch)
    git_exe("checkout", "--quiet", branch)

    try:
        git_exe("rebase", "--quiet", f"{remote}/{branch}")
    except exe.ProcessError:
        git_exe("rebase", "--abort", fail_on_error=False, error=str, output=str)
        raise


def get_modified_files(
    from_ref: str = "HEAD~1", to_ref: str = "HEAD", git_exe: Optional[exe.Executable] = None
) -> List[str]:
    """Get a list of files modified between `from_ref` and `to_ref`
    Args:
       from_ref (str): oldest git ref, defaults to `HEAD~1`
       to_ref (str): newer git ref, defaults to `HEAD`
    Returns: list of file paths
    """
    git_exe = git_exe or git(required=True)

    stdout = git_exe("diff", "--name-only", from_ref, to_ref, output=str)

    return stdout.split()


def get_commit_sha(path: str, ref: str) -> Optional[str]:
    """Get a commit sha for an arbitrary ref using ls-remote"""

    # search for matching branch, then tag
    ref_list = [f"refs/heads/{ref}", f"refs/tags/{ref}"]

    if os.path.isdir(path):
        # for the filesystem an unpacked mirror could be in a detached state from a depth 1 clone
        # only reference there will be HEAD
        ref_list.append("HEAD")

    for try_ref in ref_list:
        # this command enabled in git@1.7 so no version checking supplied (1.7 released in 2009)
        query = git(required=True)("ls-remote", path, try_ref, output=str, error=str)

        if query:
            return query.strip().split()[0]

    return None
