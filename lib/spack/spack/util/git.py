# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Single util module where Spack should get a git executable."""

import sys
from typing import Dict, List, Optional, Union

import llnl.util.lang

import spack.util.executable as exe
from spack.version import GitVersion, StandardVersion


@llnl.util.lang.memoized
def git(required: bool = False):
    """Get a git executable.

    Arguments:
        required: if ``True``, fail if ``git`` is not found. By default return ``None``.
    """
    git: Optional[exe.Executable] = exe.which("git", required=required)

    # If we're running under pytest, add this to ignore the fix for CVE-2022-39253 in
    # git 2.38.1+. Do this in one place; we need git to do this in all parts of Spack.
    if git and "pytest" in sys.modules:
        git.add_default_arg("-c", "protocol.file.allow=always")

    return git


def get_modified_files(from_ref: str = "HEAD~1", to_ref: str = "HEAD") -> List[str]:
    """Get a list of files modified between `from_ref` and `to_ref`

    Args:
       from_ref (str): oldest git ref, defaults to `HEAD~1`
       to_ref (str): newer git ref, defaults to `HEAD`

    Returns:
      files (list): list of file paths
    """
    git_exe = git(required=True)

    stdout = git_exe("diff", "--name-only", from_ref, to_ref, output=str)

    return stdout.split()


def get_added_versions(
    checksums_version_dict: Dict[str, Union[StandardVersion, GitVersion]],
    path: str,
    from_ref: str = "HEAD~1",
    to_ref: str = "HEAD",
) -> List[Union[StandardVersion, GitVersion]]:
    """Get a list of the versions added between `from_ref` and `to_ref`.

    Args:
       checksums_version_dict (Dict): all package versions keyed by known checksums.
       path (str): path to the package.py
       from_ref (str): oldest git ref, defaults to `HEAD~1`
       to_ref (str): newer git ref, defaults to `HEAD`

    Returns:
       versions_list (List): list of versions added between refs
    """
    git_exe = git(required=True)

    # Gather git diff
    diff_lines = git_exe("diff", from_ref, to_ref, "--", path, output=str).split("\n")

    # Store added and removed versions
    added_checksums = set()
    removed_checksums = set()

    # Scrape diff for modified versions
    for checksum in checksums_version_dict.keys():
        for line in diff_lines:
            if checksum in line:
                if line.startswith("+"):
                    added_checksums.add(checksum)
                if line.startswith("-"):
                    removed_checksums.add(checksum)

    return [checksums_version_dict[c] for c in added_checksums - removed_checksums]
