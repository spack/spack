# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from typing import List, Optional

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.cmd.common.confirmation as confirmation
import spack.environment as ev
import spack.spec
import spack.traverse as traverse

description = "remove specs from the concretized lockfile of an environment"
section = "environments"
level = "short"

error_message = """You can either:
    a) use a more specific spec, or
    b) specify the spec by its hash (e.g. `spack deconcretize /hash`), or
    c) use `spack deconcretize --all` to deconcretize ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {"long": True, "show_flags": False, "variants": False, "indent": 4}


def setup_parser(subparser):
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="remove regardless of whether other packages or environments " "depend on this one",
    )
    arguments.add_common_arguments(subparser, ["recurse_dependents", "yes_to_all", "specs"])
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="deconcretize ALL specs that match each supplied spec",
    )


def find_matching_specs(
    env: ev.Environment, specs: List[spack.spec.Spec], allow_multiple_matches: bool = False
):
    """Returns a list of concrete specs in the environment matching the abstract specs from CLI

    Args:
        env: active environment
        specs: list of specs to be matched against concrete environment
        allow_multiple_matches: if True mulitple matches are permitted

    Return:
        list: list of specs
    """
    matching_specs = []
    has_errors = False
    for spec in specs:
        if spec is any:
            matching = [s for _, s in env.concretized_specs()]
        else:
            matching = [s for _, s in env.concretized_specs() if s.satisfies(spec)]

        if not allow_multiple_matches and len(matching) > 1:
            tty.error(f"{spec} matches multiple concrete specs:")
            sys.stderr.write("\n")
            spack.cmd.display_specs(matching, output=sys.stderr, **display_args)
            sys.stderr.write("\n")
            sys.stderr.flush()
            has_errors = True

        if len(matching) == 0 and spec is not any:
            tty.die(f"{spec} does not match any concrete spec.")

        matching_specs.extend(matching)

    if has_errors:
        tty.die(error_message)

    return matching_specs


def concrete_dependents(
    specs: List[spack.spec.Spec], env: ev.Environment
) -> List[spack.spec.Spec]:
    # Note this traversal will not return any spec in the original list
    return [
        spec
        for spec in traverse.traverse_nodes(
            specs,
            root=False,
            order="breadth",
            cover="nodes",
            direction="parents",
            key=lambda s: s.dag_hash(),
        )
        if spec.dag_hash() in env.concretized_order
    ]


def get_deconcretize_list(args, specs, env):
    matching_specs = find_matching_specs(env, specs, args.all)
    dependent_specs = concrete_dependents(matching_specs, env)
    to_deconcretize = matching_specs + dependent_specs if args.dependents else matching_specs

    dangling_dependents = dependent_specs and not args.dependents
    has_error = not args.force and dangling_dependents

    if has_error:
        tty.info("Refusing to deconcretize the following specs")
        spack.cmd.display_specs(matching_specs, **display_args)
        print()
        tty.info("The following dependents are still concrete in the environment:")
        spack.cmd.display_specs(dependent_specs, **display_args)
        tty.die(
            "There are still dependents.",
            "use `spack deconcretize --dependents` to deconcretize dependents too",
            "use `spack deconcretize --force` to override",
        )

    return to_deconcretize


def deconcretize_specs(args, specs):
    env = spack.cmd.require_active_env(cmd_name="deconcretize")

    deconcretize_list = get_deconcretize_list(args, specs, env)

    if not deconcretize_list:
        tty.warn("There are no concrete specs to deconcretize.")
        return

    if not args.yes_to_all:
        confirmation.confirm_action(deconcretize_list, "deconcretized", "deconcretization")

    with env.write_transaction():
        for spec in deconcretize_list:
            env.deconcretize(spec)
        env.write()


def deconcretize(parser, args):
    if not args.specs and not args.all:
        tty.die(
            "deconcretize requires at least one spec argument.",
            " Use `spack deconcretize --all` to deconcretize ALL specs.",
        )

    specs = spack.cmd.parse_specs(args.specs) if args.specs else [any]
    deconcretize_specs(args, specs)
