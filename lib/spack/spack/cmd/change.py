# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import warnings

import spack.cmd
import spack.environment
import spack.spec
import spack.variant
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
    subparser.add_argument(
        "--remove-variant",
        dest="remove_variants",
        action="append",
        default=[],
        metavar="VARIANT",
        help="remove a variant from matching concrete specs"
        " (requires '--concrete' or '--concrete-only', may be used multiple times)",
    )
    arguments.add_common_arguments(subparser, ["specs"])


def change(parser, args):
    if args.all and args.concrete_only:
        warnings.warn("'spack change --all' argument is ignored with '--concrete-only'")
    if args.list_name != "specs" and args.concrete_only:
        warnings.warn("'spack change --list-name' argument is ignored with '--concrete-only'")
    if args.remove_variants and not (args.concrete or args.concrete_only):
        raise ValueError(
            "'spack change --remove-variant' requires '--concrete' or '--concrete-only'"
        )

    env = spack.cmd.require_active_env(args.subparser)

    match_spec = None
    if args.match_spec:
        match_spec = spack.cmd.parse_specs([args.match_spec])[0]
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
            if args.remove_variants and not specs:
                if not match_spec:
                    raise ValueError(
                        "'spack change --remove-variant' without a spec requires '--match-spec'"
                    )
                specs = [spack.spec.Spec()]

            selectors = []
            mutators = []
            for spec in specs:
                for variant_name in args.remove_variants:
                    if variant_name in spec.variants:
                        raise ValueError(
                            f"Cannot remove variant '{variant_name}' that is also set"
                            f" by the change spec '{spec}'"
                        )
                    spec.variants[variant_name] = spack.variant.VariantValueRemoval(variant_name)
                selectors.append(match_spec or spack.spec.Spec(spec.name))
                mutators.append(spec)

            env.mutate(selectors=selectors, mutators=mutators)

        env.write()
