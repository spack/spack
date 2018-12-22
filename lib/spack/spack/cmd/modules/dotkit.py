# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools

import spack.cmd.modules


def add_command(parser, command_dict):
    dotkit_parser = parser.add_parser(
        'dotkit', help='manipulate dotkit module files'
    )
    spack.cmd.modules.setup_parser(dotkit_parser)

    command_dict['dotkit'] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type='dotkit'
    )
