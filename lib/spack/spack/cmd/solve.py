# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import pprint
import re
import sys
from typing import Any, Dict, Iterator, List, Optional, Sequence

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
from spack.concretize_ui import ConcretizerUI, SolveKind
from spack.solver import asp
from spack.solver.error import format_unsolved
from spack.solver.result import OptimizationKind, Result
from spack.spec import Spec
from spack.util import tty
from spack.util.timer import BaseTimer
from spack.util.tty import color

description = "concretize a specs using an ASP solver"
section = "developer"
level = "long"


class SolveUI(ConcretizerUI):
    """Frontend for the debug output of a solve, which only ``spack solve`` asks for. A request
    may take more than one solve, so the output of each of them is delimited: solving one spec at
    a time announces the spec, solving in rounds closes each round.
    """

    def __init__(
        self,
        *,
        kind: SolveKind,
        show_asp: bool,
        show_opt: bool,
        show_solutions: bool,
        timers: bool,
        stats: bool,
    ) -> None:
        self.kind = kind
        self.show_asp = show_asp
        self.show_opt = show_opt
        self.show_solutions = show_solutions
        self.timers = timers
        self.stats = stats
        self.rounds = 0

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        if self.kind is SolveKind.SEPARATELY:
            tty.msg("SOLVING SPEC:", *(str(x) for x in specs))

    def on_asp_program_generated(self, program: List[str]) -> None:
        if self.show_asp:
            sys.stdout.write("\n".join(program))

    def on_solve_finished(
        self, result: Result, *, timer: BaseTimer, statistics: Optional[Dict], cached: bool
    ) -> None:
        if self.kind is SolveKind.WHEN_POSSIBLE:
            self._delimit_round()

        if self.timers:
            timer.write_tty()
            print()

        if self.stats:
            print("Statistics:")
            pprint.pprint(statistics)

        if self.show_opt:
            self._print_criteria(result)

    def _delimit_round(self) -> None:
        """Mark the boundary of a round: a header for the output that follows, or a comment
        terminating the ASP program that precedes it.
        """
        if self.show_solutions:
            tty.msg(f"ROUND {self.rounds}")
            tty.msg("")
        else:
            print(f"% END ROUND {self.rounds}\n")
        self.rounds += 1

    def _print_criteria(self, result: Result) -> None:
        """Print the optimization criteria of the best model, and their value."""
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
            elif criterion.kind == OptimizationKind.CONCRETE:
                lc = "@b"
            elif criterion.kind == OptimizationKind.BUILD:
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


def _print_solutions(
    result: Result, *, required_format: Optional[str], kwargs: Dict[str, Any]
) -> None:
    """Dump the solutions of a solve as concretized specs."""
    if required_format:
        for spec in result.specs:
            # With -y, just print YAML to output.
            if required_format == "yaml":
                # use write because to_yaml already has a newline.
                sys.stdout.write(spec.to_yaml(hash=ht.dag_hash))
            elif required_format == "json":
                print(spec.to_json(hash=ht.dag_hash))
            else:
                print(spec.format(required_format))
    else:
        tree_str = spack.spec.tree(result.specs, color=color.get_color_when(sys.stdout), **kwargs)
        sys.stdout.write(tree_str)
    print()

    if result.unsolved_specs:
        tty.msg(format_unsolved(result.unsolved_specs))


def _solve(
    solver: asp.Solver,
    specs: Sequence[Spec],
    *,
    kind: SolveKind,
    setup_only: bool,
    allow_deprecated: bool,
) -> Iterator[Result]:
    """Yield the result of each of the solves that concretize ``specs``."""
    if kind is SolveKind.WHEN_POSSIBLE:
        # solve_in_rounds has no setup_only, since it cannot know upfront how many rounds it takes
        yield from solver.solve_in_rounds(specs, allow_deprecated=allow_deprecated)
        return

    inputs = [[s] for s in specs] if kind is SolveKind.SEPARATELY else [list(specs)]
    for current in inputs:
        yield solver.solve(current, setup_only=setup_only, allow_deprecated=allow_deprecated)


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

    # If we have an active environment, pick the specs from there
    env = active_environment()
    if args.specs:
        specs = spack.cmd.parse_specs(args.specs)
    elif env:
        specs = list(env.user_specs)
    else:
        args.subparser.error("requires at least one spec or an active environment")

    # Early exit in case of empty environment
    if not specs:
        return

    # Note: reuse and other concretizer prefs are passed as configuration
    kind = spack.concretize.solve_kind(spack.config.CONFIG.get("concretizer:unify"))
    ui = SolveUI(
        kind=kind,
        show_asp="asp" in show,
        show_opt="opt" in show and not required_format,
        show_solutions="solutions" in show,
        timers=args.timers,
        stats=args.stats,
    )

    setup_only = set(show) == {"asp"}
    results = _solve(
        asp.Solver(ui=ui),
        specs,
        kind=kind,
        setup_only=setup_only,
        allow_deprecated=spack.config.CONFIG.get("config:deprecated", False),
    )
    for result in results:
        if not setup_only and "solutions" in show:
            _print_solutions(result, required_format=required_format, kwargs=kwargs)
