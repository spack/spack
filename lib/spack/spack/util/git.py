# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Single util module where Spack should get a git executable."""

import sys

import llnl.util.lang

import spack.util.executable


@llnl.util.lang.memoized
def get_git(required=False):
    """Get a git executable.

    Arguments:
        required: if ``True``, fail if ``git`` is not found. By default return ``None``.
    """
    git = spack.util.executable.which("git", required=required)

    # If we're running under pytest, add this to ignore the fix for CVE-2022-39253 in
    # git 2.38.1+. Do this in one place; we need git to do this in all parts of Spack.
    if "pytest" in sys.modules:
        git.add_default_arg("-c")
        git.add_default_arg("protocol.file.allow=always")

    return git
