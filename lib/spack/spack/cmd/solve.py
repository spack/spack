# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import re
import sys

import spack
import spack.binary_distribution
import spack.cmd
import spack.cmd.spec
import spack.concretize
import spack.config
import spack.hash_types as ht
import spack.package_base
import spack.spec
from spack.active_environment import active_environment
from spack.solver import asp
from spack.util import tty
from spack.util.tty import color

description = "concretize a specs using an ASP solver"
section = "developer"
level = "long"


#: output options
show_options = ("asp", "opt", "output", "solutions")


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    # Solver arguments
    subparser.add_argument(
        "--show",
        action="store",
        default="opt,solutions",
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

    spack.cmd.spec.setup_parser(subparser)


def _print_criteria(result):
    tty.msg("Best of %d considered solutions." % result.nmodels)

    print()
    maxlen = max(len(s.name) for s in result.criteria)
    color.cprint("@*{  Priority  Value  Criterion}")

    # Width of a data row past its 2-space indent, matching the row format below:
    # 8-wide priority + 2 gap + 5-wide value + 2 gap + maxlen-wide criterion name.
    divider_width = 8 + 2 + 5 + 2 + maxlen
    prev_band = None

    for i, criterion in enumerate(result.criteria, 1):
        # Criteria are grouped into priority bands; print a header when the band changes.
        band = criterion.band
        if band != prev_band:
            label = f"-- {band}"
            dashes = "-" * max(0, divider_width - len(label) - 1)
            color.cprint(f"  @*{{{label}}} @K{{{dashes}}}")
            prev_band = band

        value = f"@K{{{criterion.value:>5}}}"
        grey_out = True
        if criterion.value > 0:
            value = f"@*{{{criterion.value:>5}}}"
            grey_out = False

        if grey_out:
            lc = "@K"
        elif criterion.kind == asp.OptimizationKind.CONCRETE:
            lc = "@b"
        elif criterion.kind == asp.OptimizationKind.BUILD:
            lc = "@g"
        else:
            lc = "@y"

        color.cprint(f"  @K{{{i:8}}}  {value}  {lc}{{{criterion.name:<{maxlen}}}}")
    print()
    print()
    color.cprint("  @*{Legend:}")
    color.cprint("    @g{Specs to be built}")
    color.cprint("    @b{Reused specs}")
    color.cprint("    @y{Other criteria}")
    print()


def _report_result(result, show, required_format, *, label_inputs=False):
    """Prints what a single solve has to show, before any spec is reported.

    An environment is solved in more than one round, so *label_inputs* says which specs the
    criteria that follow belong to.
    """
    if label_inputs and not required_format:
        tty.msg("SOLVING SPEC:", *result.abstract_specs)

    if ("opt" in show) and (not required_format):
        _print_criteria(result)

    if result.unsolved_specs and "solutions" in show:
        tty.msg(asp.Result.format_unsolved(result.unsolved_specs))


def _print_specs(specs, show, required_format, kwargs):
    """Dumps the concretized specs, in the format that was asked for."""
    if "solutions" not in show or not specs:
        return

    if required_format:
        for spec in specs:
            # With -y, just print YAML to output.
            if required_format == "yaml":
                # use write because to_yaml already has a newline.
                sys.stdout.write(spec.to_yaml(hash=ht.dag_hash))
            elif required_format == "json":
                # print, so that each spec stays a JSON document of its own
                print(spec.to_json(hash=ht.dag_hash))
            else:
                print(spec.format(required_format))
    else:
        tree_str = spack.spec.tree(specs, color=color.get_color_when(sys.stdout), **kwargs)
        sys.stdout.write(tree_str)
    print()


def solve(parser, args):
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

    env = active_environment()
    specs = spack.cmd.parse_specs(args.specs)
    if not specs and env is None:
        args.subparser.error("requires at least one spec or an active environment")

    if not specs and set(show) == {"asp"}:
        args.subparser.error(
            "'--show asp' needs specs to solve for, since an environment is solved one "
            "group of specs at a time"
        )

    if specs:
        _solve_specs(specs, args=args, show=show, required_format=required_format, kwargs=kwargs)
    else:
        _solve_environment(
            env, args=args, show=show, required_format=required_format, kwargs=kwargs
        )


def _output_configuration(args, show, *, setup_only):
    return asp.OutputConfiguration(
        timers=args.timers,
        stats=args.stats,
        out=sys.stdout if "asp" in show else None,
        setup_only=setup_only,
    )


def _solve_specs(specs, *, args, show, required_format, kwargs):
    """Solves the specs given on the command line, honoring concretizer:unify."""
    solver = asp.Solver()
    setup_only = set(show) == {"asp"}
    output = _output_configuration(args, show, setup_only=setup_only)
    unify = spack.config.CONFIG.get("concretizer:unify")
    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)

    def _report(result):
        if setup_only:  # nothing was solved, so there is no result to look at
            return
        _report_result(result, show, required_format)
        _print_specs(result.specs, show, required_format, kwargs)

    if unify == "when_possible":
        for idx, result in enumerate(
            solver.solve_in_rounds(specs, allow_deprecated=allow_deprecated, output=output)
        ):
            if "solutions" in show:
                tty.msg("ROUND {0}".format(idx))
                tty.msg("")
            else:
                print("% END ROUND {0}\n".format(idx))
            _report(result)
    elif unify:
        # set up solver parameters
        # Note: reuse and other concretizer prefs are passed as configuration
        _report(solver.solve(specs, allow_deprecated=allow_deprecated, output=output))
    else:
        for spec in specs:
            tty.msg("SOLVING SPEC:", spec)
            _report(solver.solve([spec], allow_deprecated=allow_deprecated, output=output))


def _solve_environment(env, *, args, show, required_format, kwargs):
    """Solves the active environment, one group of specs at a time."""
    # An output configuration also states that the solving has to happen in this process, so
    # ask for one only when something the reporter prints actually needs it
    needs_in_process = args.timers or args.stats or "asp" in show or "opt" in show
    reporter = spack.concretize.SolveReporter(
        output=_output_configuration(args, show, setup_only=False) if needs_in_process else None,
        on_result=lambda result: _report_result(result, show, required_format, label_inputs=True),
    )

    # Solving is forced, so that this command always shows a solve and never the lockfile.
    # Nothing is written back, so the environment is left as it was for other commands.
    env.concretize(force=True, reporter=reporter)

    roots = list(env.concrete_roots())
    if not roots and not required_format:
        tty.msg("The environment has no input specs")

    _print_specs(roots, show, required_format, kwargs)
