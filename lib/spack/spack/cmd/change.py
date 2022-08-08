# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments

description = "change an existing spec in an environment"
section = "environments"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["specs"])


def change(parser, args):
    env = spack.cmd.require_active_env(cmd_name="change")

    with env.write_transaction():
        for spec in spack.cmd.parse_specs(args.specs):
            env.change_existing_spec(spec)
        env.write()
