# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import re
import sys

import spack
import spack.binary_distribution
import spack.cmd
import spack.config
import spack.hash_types as ht
import spack.package_base
import spack.spec
from spack.active_environment import active_environment
from spack.cmd.common import arguments
from spack.solver import asp
from spack.util import tty
from spack.util.tty import color

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


def _process_result(result, show, required_format, kwargs):
    opt, _, _ = min(result.answers)
    if ("opt" in show) and (not required_format):
        tty.msg("Best of %d considered solutions." % result.nmodels)

        print()
        maxlen = max(len(s.name) for s in result.criteria)

        # Build a 2D array: (name, band) => list of values by level
        criteria_by_priority = sorted(result.criteria, key=lambda x: x.priority, reverse=True)
        row_order = []
        row_kinds = {}  # Store the kind for each (name, band)
        seen = set()
        for criterion in criteria_by_priority:
            key = (criterion.name, criterion.band)
            if key not in seen:
                row_order.append(key)
                row_kinds[key] = criterion.kind
                seen.add(key)

        max_level = max(criterion.level for criterion in result.criteria) if result.criteria else 0
        num_levels = max_level + 1
        rows = {key: [None] * num_levels for key in row_order}

        for criterion in result.criteria:
            key = (criterion.name, criterion.band)
            rows[key][max_level - criterion.level] = criterion.value

        # Remove prefix sum effect from criteria values
        for key in rows:
            row = rows[key]
            prev_cumulative = 0
            for i in range(len(row)):
                if row[i] is not None:
                    cumulative_value = row[i]
                    row[i] = cumulative_value - prev_cumulative
                    prev_cumulative = cumulative_value

        # Print header with level labels (L0 for highest level, L1, L2... for lower)
        level_headers = "  ".join(f"L{i}".rjust(5) for i in range(num_levels))
        color.cprint(f"@*{{  {level_headers}  Criterion}}")

        # Width of a data row:
        # (5-wide value + 2 gap) * num_levels + maxlen-wide criterion name
        divider_width = (5 + 2) * num_levels + maxlen
        prev_band = None

        # Print criteria using the 2D table
        for name, band in row_order:
            # Print band header when it changes
            if band != prev_band:
                label = f"-- {band}"
                dashes = "-" * max(0, divider_width - len(label) - 1)
                color.cprint(f"  @*{{{label}}} @K{{{dashes}}}")
                prev_band = band

            # Build the values string for all levels (highest level first, on the left)
            row_data = rows[(name, band)]
            values_parts = []
            has_nonzero = False
            # Iterate through the row
            for value in row_data:
                if value is not None:
                    if value > 0:
                        has_nonzero = True
                        values_parts.append(f"@*{{{value:>5}}}")
                    else:
                        values_parts.append(f"@K{{{value:>5}}}")
                else:
                    values_parts.append(f"@K{{{'    -'}}}")

            values_str = "  ".join(values_parts)

            # Determine color: only color if there's a non-zero value
            kind = row_kinds[(name, band)]
            if has_nonzero:
                if kind == asp.OptimizationKind.CONCRETE:
                    lc = "@b"
                elif kind == asp.OptimizationKind.BUILD:
                    lc = "@g"
                else:
                    lc = "@y"
            else:
                lc = "@K"

            color.cprint(f"  {values_str}  {lc}{{{name:<{maxlen}}}}")
        print()
        print()
        color.cprint("  @*{Legend:}")
        color.cprint("    @g{Specs to be built}")
        color.cprint("    @b{Reused specs}")
        color.cprint("    @y{Other criteria}")
        print()

    # dump the solutions as concretized specs
    if "solutions" in show:
        if required_format:
            for spec in result.specs:
                # With -y, just print YAML to output.
                if required_format == "yaml":
                    # use write because to_yaml already has a newline.
                    sys.stdout.write(spec.to_yaml(hash=ht.dag_hash))
                elif required_format == "json":
                    sys.stdout.write(spec.to_json(hash=ht.dag_hash))
                else:
                    print(spec.format(required_format))
        else:
            tree_str = spack.spec.tree(
                result.specs, color=color.get_color_when(sys.stdout), **kwargs
            )
            sys.stdout.write(tree_str)
        print()

    if result.unsolved_specs and "solutions" in show:
        tty.msg(asp.Result.format_unsolved(result.unsolved_specs))


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
        specs = list(env.user_specs)
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
