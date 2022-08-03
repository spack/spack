# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools

import spack.cmd.modules


def add_command(parser, command_dict):
    ups_table_parser = parser.add_parser("ups_table", help="manipulate ups files")
    spack.cmd.modules.setup_parser(ups_table_parser)

    command_dict["ups_table"] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type="ups_table"
    )
