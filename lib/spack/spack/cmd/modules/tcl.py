# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools

import spack.cmd.modules


def add_command(parser, command_dict):
    tcl_parser = parser.add_parser(
        'tcl', help='manipulate non-hierarchical module files'
    )
    spack.cmd.modules.setup_parser(tcl_parser)

    command_dict['tcl'] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type='tcl'
    )
