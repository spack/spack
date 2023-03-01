# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

description = "run git inside of the spack repo"
section = "system"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "subcommand", nargs=argparse.REMAINDER, help="git command to run within spack repo"
    )


def git(parser, args):
    # this is a placeholder shell for spack help
    # spack git is located in the bash start up script
    # we should never reach this point of execution
    pass
