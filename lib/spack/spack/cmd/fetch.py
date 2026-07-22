# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import spack.cmd
import spack.config
import spack.repo
import spack.store
import spack.traverse
from spack.active_environment import active_environment
from spack.cmd.common import arguments

description = "fetch archives for packages"
section = "build"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    arguments.add_common_arguments(subparser, ["no_checksum", "specs"])
    subparser.add_argument(
        "-m",
        "--missing",
        action="store_true",
        help="fetch only missing (not yet installed) dependencies",
    )
    subparser.add_argument(
        "-D", "--dependencies", action="store_true", help="also fetch all dependencies"
    )
    arguments.add_concretizer_args(subparser)
    subparser.epilog = (
        "With an active environment, the specs "
        "parameter can be omitted. In this case all (uninstalled"
        ", in case of --missing) specs from the environment are fetched"
    )


def fetch(parser, args):
    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    if args.specs:
        specs = spack.cmd.parse_specs(args.specs, concretize=True)
    else:
        # No specs were given explicitly, check if we are in an
        # environment. If yes, check the missing argument, if yes
        # fetch all uninstalled specs from it otherwise fetch all.
        # If we are also not in an environment, complain to the
        # user that we don't know what to do.
        env = active_environment()
        if env:
            if args.missing:
                specs = env.uninstalled_specs()
            else:
                specs = env.all_specs()
            if specs == []:
                args.subparser.error(
                    "no uninstalled specs in environment. Did you run `spack concretize` yet?"
                )
        else:
            args.subparser.error("requires at least one spec argument")

    if args.dependencies or args.missing:
        to_be_fetched = spack.traverse.traverse_nodes(specs, key=spack.traverse.by_dag_hash)
    else:
        to_be_fetched = specs

    for spec in to_be_fetched:
        if args.missing and spack.store.STORE.db.installed(spec):
            continue

        pkg = spack.repo.PATH.get(spec)

        pkg.stage.keep = True
        with pkg.stage:
            pkg.do_fetch()
