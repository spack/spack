# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import spack.cmd
import spack.llnl.util.tty as tty
from spack.cmd.common import arguments

description = "add a spec to an environment"
section = "environments"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-l",
        "--list-name",
        dest="list_name",
        default="specs",
        help="name of the list to add specs to",
    )
    arguments.add_common_arguments(subparser, ["specs"])


def add(parser, args):
    env = spack.cmd.require_active_env(args.subparser)

    with env.write_transaction():
        for spec in spack.cmd.parse_specs(args.specs):
            if not env.add(spec, args.list_name):
                tty.msg(f"Package {spec.name} was already added to {env.name}")
            else:
                tty.msg(f"Adding {spec} to environment {env.name}")
        env.write()
