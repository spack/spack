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

description = "run a program inside of the spack repo"
section = "system"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "subcommand", nargs=argparse.REMAINDER, help="program and args to run within spack repo"
    )


def git(parser, args):
    # this is a placeholder shell for spack help
    # spack run is located in the bash start up script
    # we should never reach this point of execution
    pass
