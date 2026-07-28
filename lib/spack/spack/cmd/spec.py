# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import re
import sys
from typing import List, Optional

import spack
import spack.binary_distribution
import spack.cmd
import spack.config
import spack.environment as ev
import spack.hash_types as ht
import spack.package_base
import spack.spec
from spack.active_environment import active_environment
from spack.cmd.common import arguments
from spack.solver import asp
from spack.util import tty

description = "show what would be installed, given a spec"
section = "build"
level = "short"

#: output options
show_options = ("asp", "opt", "solutions")


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.epilog = """\
when an environment is active and no specs are provided, the environment root \
specs are used instead

for further documentation regarding the spec syntax, see:
    spack help --spec
"""
    arguments.add_common_arguments(subparser, ["long", "very_long", "namespaces"])

    install_status_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(install_status_group, ["install_status", "no_install_status"])
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        "-y",
        "--yaml",
        action="store_const",
        dest="format",
        default=None,
        const="yaml",
        help="print concrete spec as YAML",
    )
    format_group.add_argument(
        "-j",
        "--json",
        action="store_const",
        dest="format",
        default=None,
        const="json",
        help="print concrete spec as JSON",
    )
    format_group.add_argument(
        "--format",
        action="store",
        default=None,
        help="print concrete spec with the specified format string",
    )
    arguments.add_common_arguments(format_group, ["show_non_defaults"])

    subparser.add_argument(
        "-c",
        "--cover",
        action="store",
        default="nodes",
        choices=["nodes", "edges", "paths"],
        help="how extensively to traverse the DAG (default: nodes)",
    )
    subparser.add_argument(
        "-t", "--types", action="store_true", default=False, help="show dependency types"
    )
    arguments.add_common_arguments(subparser, ["specs"])
    arguments.add_concretizer_args(subparser)

    # debugging arguments
    subparser.add_argument(
        "--show",
        action="store",
        default="solutions",
        help="select outputs\n\ncomma-separated list of:\n"
        "  asp          asp program text\n"
        "  opt          optimization criteria for best model\n"
        "  output       raw clingo output\n"
        "  solutions    models found by asp program\n"
        "  all          all of the above",
    )
    subparser.add_argument(
        "--timers",
        action="store_true",
        default=False,
        help="print out timers for different solve phases",
    )
    subparser.add_argument(
        "--stats", action="store_true", default=False, help="print out statistics from clingo"
    )


def _display_specs(specs: List[spack.spec.Spec], required_format: Optional[str], kwargs) -> None:
    """Print concrete specs in the requested format (tree by default)."""
    if required_format:
        for spec in specs:
            # With -y, just print YAML to output.
            if required_format == "yaml":
                # use write because to_yaml already has a newline.
                sys.stdout.write(spec.to_yaml(hash=ht.dag_hash))
            elif required_format == "json":
                sys.stdout.write(spec.to_json(hash=ht.dag_hash))
            else:
                print(spec.format(required_format))
    else:
        tree_str = spack.spec.tree(specs, color=sys.stdout.isatty(), **kwargs)
        sys.stdout.write(tree_str)
    print()


def _process_result(result, show, required_format, kwargs):
    if ("opt" in show) and (not required_format):
        result.show_criteria()

    # dump the solutions as concretized specs
    if "solutions" in show:
        _display_specs(result.specs, required_format, kwargs)

    if result.unsolved_specs and "solutions" in show:
        tty.msg(asp.Result.format_unsolved(result.unsolved_specs))


def _env_spec(env: ev.Environment, args, show, required_format, kwargs) -> None:
    """Show the environment roots, concretizing only the ones that aren't yet concrete.

    The environment is not modified, in memory or on disk. Solver diagnostics (asp
    program, optimization criteria, timers, statistics) cover only the new solves.
    """
    diagnostics = asp.OutputConfiguration(
        timers=args.timers,
        stats=args.stats,
        out=sys.stdout if "asp" in show else None,
        setup_only=set(show) == {"asp"},
        criteria="opt" in show and not required_format,
    )
    wants_diagnostics = any(diagnostics)

    # With setup_only nothing concretizes, so we can't use the result to detect a
    # fully concrete environment; check the roots upfront instead.
    force = spack.config.CONFIG.get("concretizer:force")
    already_concrete = {x.root for x in env.concretized_roots}
    fully_concrete = not force and all(s in already_concrete for s in env.user_specs)

    if wants_diagnostics and fully_concrete:
        tty.msg(
            "The environment is already concrete, so there is nothing to solve and no"
            " solver diagnostics to show. Re-run with --force to see diagnostics for a"
            " full re-concretization."
        )

    with env.transient_concretization():
        env.concretize(output=diagnostics if wants_diagnostics else None)
        concrete_specs = [concrete for _, concrete in env.concretized_specs()]

    if "solutions" in show and not diagnostics.setup_only:
        _display_specs(concrete_specs, required_format, kwargs)


def spec(parser, args):
    # these are the same options as `spack spec`
    fmt = spack.spec.DISPLAY_FORMAT
    if args.namespaces:
        fmt = "{namespace}." + fmt

    show_status = args.install_status
    if show_status:
        spack.binary_distribution.load_buildcache_index()
        status_fn = spack.cmd.buildcache_status_fn(spack.binary_distribution.BINARY_INDEX)
    else:
        status_fn = None

    kwargs = {
        "cover": args.cover,
        "format": fmt,
        "hashlen": None if args.very_long else 7,
        "show_types": args.types,
        "status_fn": status_fn,
        "hashes": args.long or args.very_long,
        "version_style_fn": (
            spack.package_base.non_preferred_version if args.non_defaults else None
        ),
        "variant_style_fn": (
            spack.package_base.non_default_variant if args.non_defaults else None
        ),
    }

    # process output options
    show = re.split(r"\s*,\s*", args.show)
    if "all" in show:
        show = show_options
    for d in show:
        if d not in show_options:
            raise ValueError(
                "Invalid option for '--show': '%s'\nchoose from: (%s)"
                % (d, ", ".join(show_options + ("all",)))
            )

    # Format required for the output (JSON, YAML or None)
    required_format = args.format

    # If we have an active environment, pick the specs from there
    env = active_environment()
    if args.specs:
        specs = spack.cmd.parse_specs(args.specs)
    elif env:
        # Concretize through the environment, so specs that are already concrete
        # are kept as-is and only new user specs are solved for.
        _env_spec(env, args, show, required_format, kwargs)
        return
    else:
        args.subparser.error("requires at least one spec or an active environment")

    solver = asp.Solver()
    output = sys.stdout if "asp" in show else None
    setup_only = set(show) == {"asp"}
    unify = spack.config.CONFIG.get("concretizer:unify")
    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    if unify == "when_possible":
        for idx, result in enumerate(
            solver.solve_in_rounds(
                specs,
                out=output,
                timers=args.timers,
                stats=args.stats,
                allow_deprecated=allow_deprecated,
            )
        ):
            if "solutions" in show:
                tty.msg("ROUND {0}".format(idx))
                tty.msg("")
            else:
                print("% END ROUND {0}\n".format(idx))
            if not setup_only:
                _process_result(result, show, required_format, kwargs)
    elif unify:
        # set up solver parameters
        # Note: reuse and other concretizer prefs are passed as configuration
        result = solver.solve(
            specs,
            out=output,
            timers=args.timers,
            stats=args.stats,
            setup_only=setup_only,
            allow_deprecated=allow_deprecated,
        )
        if not setup_only:
            _process_result(result, show, required_format, kwargs)
    else:
        for spec in specs:
            result = solver.solve(
                [spec],
                out=output,
                timers=args.timers,
                stats=args.stats,
                setup_only=setup_only,
                allow_deprecated=allow_deprecated,
            )
            if not setup_only:
                _process_result(result, show, required_format, kwargs)
