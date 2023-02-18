# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack.cmd
import spack.util.git
from spack.cmd import spack_is_git_repo

description = "run git inside of the spack repo"
section = "system"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "command", nargs=argparse.REMAINDER, help="git command to run within spack repo"
    )


def git(parser, args):
    # make sure this is a git repo
    if not spack_is_git_repo():
        tty.die("This spack is not a git clone. Can't use 'spack git'")
    git = spack.util.git.git(required=True)

    # execute git within the local spack repository
    with working_dir(spack.paths.prefix):
        print(git(*args.command, output=str, fail_on_error=False), end="")
        exit(git.returncode)
