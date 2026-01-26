# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import warnings

import spack.cmd
import spack.environment
import spack.spec
from spack.cmd.common import arguments

description = "change an existing spec in an environment"
section = "environments"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-l",
        "--list-name",
        dest="list_name",
        default="specs",
        help="name of the list to remove abstract specs from",
    )
    subparser.add_argument(
        "--match-spec",
        dest="match_spec",
        help="change all specs matching match-spec (default is match by spec name)",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="change all matching abstract specs (allow changing more than one abstract spec)",
    )
    subparser.add_argument(
        "-c",
        "--concrete",
        action="store_true",
        default=False,
        help="change concrete specs in the environment",
    )
    subparser.add_argument(
        "-C",
        "--concrete-only",
        action="store_true",
        default=False,
        help="change only concrete specs in the environment",
    )
    arguments.add_common_arguments(subparser, ["specs"])


def change(parser, args):
    if args.all and args.concrete_only:
        warnings.warn("'spack change --all' argument is ignored with '--concrete-only'")
    if args.list_name != "specs" and args.concrete_only:
        warnings.warn("'spack change --list-name' argument is ignored with '--concrete-only'")

    env = spack.cmd.require_active_env(cmd_name="change")

    match_spec = None
    if args.match_spec:
        match_spec = spack.spec.Spec(args.match_spec)
    specs = spack.cmd.parse_specs(args.specs)

    with env.write_transaction():
        if not args.concrete_only:
            try:
                for spec in specs:
                    env.change_existing_spec(
                        spec,
                        list_name=args.list_name,
                        match_spec=match_spec,
                        allow_changing_multiple_specs=args.all,
                    )
            except (ValueError, spack.environment.SpackEnvironmentError) as e:
                msg = "Cannot change abstract specs."
                msg += " Try again with '--concrete-only' to change concrete specs only."
                raise ValueError(msg) from e

        if args.concrete or args.concrete_only:
            for spec in specs:
                env.mutate(selector=match_spec or spack.spec.Spec(spec.name), mutator=spec)

        env.write()
