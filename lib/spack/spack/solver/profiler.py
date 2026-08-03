# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Profiling propagator for clingo solves.

Registers a custom propagator with ``clingo.Control`` that counts propagate/undo
operations per solver literal, then aggregates by predicate name (with the first
arg preserved for ``attr(...)`` atoms) for a rough view of where the solver is
spending its time during search.

**Caveat on equivalence collapse.** Clingo's preprocessor may collapse multiple
distinct symbolic atoms to the same solver literal. This propagator sees
propagations/undos at the *literal* level and attaches each count to whichever
symbolic atom the ``init`` scan visited last for that literal. So per-literal
counts are precise, but the symbolic-atom label is somewhat arbitrary when
equivalence collapse has occurred. Treat the aggregated output as a
**categorical** signal ("this predicate family drives lots of propagation
relative to that one") rather than a precise per-atom attribution.
"""

import re
from typing import Any, Dict, List

import spack.util.tty.color as color


class Data:
    """Counters for propagations and undos of an atom."""

    __slots__ = ["atom", "literal", "prop", "undo"]

    # currently we use Any for clingo types because clingo has a bunch of import
    # wrappers around it that make typing difficult (see spack.solver.core for details)
    def __init__(self, atom: Any, literal: int, prop: int, undo: int):
        self.atom = atom
        self.literal = literal
        self.prop = prop
        self.undo = undo


class AggregatedData:
    """Aggregated data for a profile, constructed from ``Data``.

    We coarsen from atom granularity to string keys when aggregating.
    """

    __slots__ = ["name", "prop", "undo"]

    def __init__(self, name: str, prop: int, undo: int):
        self.name = name
        self.prop = prop
        self.undo = undo


class ProfilePropagator:
    """Profiling propagator for ``spack spec --profile``.

    Register this with the ``clingo.Control`` object to profile a solve.
    """

    _literal_to_atom: Dict
    _profile: Dict[int, Data]

    def init(self, init) -> None:
        self._literal_to_atom = {}
        self._profile = {}
        for atom in init.symbolic_atoms:
            solver_literal = init.solver_literal(atom.literal)
            self._profile[solver_literal] = Data(atom, solver_literal, 0, 0)
            init.add_watch(solver_literal)

    def propagate(self, ctl, changes: List[int]) -> bool:
        """Record a propagation in the solve."""
        for literal in changes:
            data = self._profile.get(literal)
            if data is not None:
                data.prop += 1
        return True

    def undo(self, solver_id: int, assign, undo: List[int]) -> None:
        """Record an undo in the solve."""
        for literal in undo:
            data = self._profile.get(literal)
            if data is not None:
                data.undo += 1

    def color_sym(self, string: str) -> str:
        """Colorize a symbol for profile output"""
        string = re.sub(r"^(\w+)", r"@C{\1}", string)
        string = re.sub(r'("[^"]*")', r"@G{\1}", string)
        string = re.sub(r"([\(\)])", r"@b{\1}", string)
        return color.colorize(string)

    def key(self, atom) -> str:
        """Convert an atom into an aggregate key for our profile.

        Currently this compresses most things to their function name, and expands
        ``attr("name", ...)`` to ``attr("name")`` so we can see which attributes affect
        the solve most.

        """
        sym = atom.symbol
        return f"attr({sym.arguments[0]})" if sym.name == "attr" else sym.name

    def print_profile(self, n_atoms: int) -> None:
        """Aggregate and print nicely formatted profile data."""
        aggregated: Dict[str, AggregatedData] = {}
        for data in self._profile.values():
            name = self.key(data.atom)
            if name not in aggregated:
                aggregated[name] = AggregatedData(name, data.prop, data.undo)
            else:
                agg = aggregated[name]
                agg.prop += data.prop
                agg.undo += data.undo

        values = sorted(
            (x for x in aggregated.values() if x.prop), key=lambda x: x.prop, reverse=True
        )

        # format the output nicely
        w = 12  # width for number fields
        print(color.colorize(f"  @*{{{'Prop':<{w}}{'Undo':<{w}}{'Symbol'}}}"))
        for a in values[:n_atoms]:
            print(f"  {a.prop:<{w},}{a.undo:<{w},}{self.color_sym(a.name)}")
        if len(values) > n_atoms:
            print(f"  ... ({len(values) - n_atoms} more categories omitted)")
