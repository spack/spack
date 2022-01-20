# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
from spack.cmd.compiler import compiler_list

description = "list available compilers"
section = "system"
level = "short"


def setup_parser(subparser):
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        help="configuration scope to read/modify")


def compilers(parser, args):
    compiler_list(args)
