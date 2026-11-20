# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""The result of an ASP solve, and the types needed to read and serialize it.

This module is importable without pulling in the solver itself, so that frontends can be
typed against a result without depending on how it is produced.
"""

import enum
from typing import Any, Dict, List, NamedTuple, Optional, Set, Tuple

import spack.repo
import spack.spec
from spack.util import tty

from .core import NodeFlag, NodeId, min_dupe_node

# type aliases for the data structures we get back from the solver
SpecDict = Dict[NodeId, spack.spec.Spec]


class OptimizationKind:
    """Enum for the optimization KIND of a criteria.

    It's not using enum.Enum since it must be serializable.
    """

    BUILD = 0
    CONCRETE = 1
    OTHER = 2


class OptimizationBand(enum.Enum):
    """Grouping for optimization criteria by their priority range."""

    LOW = "Lowest priority"
    REUSED = "Reused nodes"
    FIXED = "Fixed (reuse vs build)"
    BUILD = "Built nodes"
    HIGHEST = "Highest priority"


class OptimizationCriteria(NamedTuple):
    """A named tuple describing an optimization criteria."""

    priority: int
    value: int
    name: str
    band: str
    kind: OptimizationKind


def build_criteria_names(costs, arg_tuples):
    """Construct an ordered mapping from criteria names to costs."""
    # pull optimization criteria names out of the solution
    priorities_names = []

    # translate ASP band names into display names
    band_names = {
        "low": OptimizationBand.LOW,
        "concr": OptimizationBand.REUSED,
        "hinge": OptimizationBand.FIXED,
        "built": OptimizationBand.BUILD,
        "high": OptimizationBand.HIGHEST,
    }

    for args in arg_tuples:
        priority, band, name = args[0], band_names[args[2]].value, args[4]
        priority = int(priority)

        if band == OptimizationBand.REUSED.value:
            # Reused/concrete criterion
            priorities_names.append((priority, name, band, OptimizationKind.CONCRETE))
        elif band == OptimizationBand.BUILD.value:
            # Build criterion
            priorities_names.append((priority, name, band, OptimizationKind.BUILD))
        else:
            priorities_names.append((priority, name, band, OptimizationKind.OTHER))

    # sort the criteria by priority
    priorities_names = sorted(priorities_names, reverse=True)

    # We only have opt-criterion values for non-error types
    # error type criteria are excluded (they come first)
    error_criteria = len(costs) - len(priorities_names)
    costs = costs[error_criteria:]

    return [
        OptimizationCriteria(priority, value, name, band, status)
        for (priority, name, band, status), value in zip(priorities_names, costs)
    ]


def _encode(value: Any) -> Any:
    """Turns a value from ``extract_args`` into JSON data."""
    # NodeId and NodeFlag are tuples, so they are checked first
    if isinstance(value, NodeId):
        return {"node": [_encode(x) for x in value]}
    if isinstance(value, NodeFlag):
        return {"node_flag": [_encode(x) for x in value]}
    if isinstance(value, tuple):
        return [_encode(x) for x in value]
    return value


def _decode(value: Any) -> Any:
    """Inverse of ``_encode``. Raises ``ValueError`` on data ``_encode`` cannot produce."""
    if isinstance(value, list):
        return tuple(_decode(x) for x in value)
    if isinstance(value, dict):
        if "node" in value:
            return NodeId(*_decode(value["node"]))
        if "node_flag" in value:
            return NodeFlag(*_decode(value["node_flag"]))
        raise ValueError(f"Invalid answer data: {value}")
    return value


class Answer(NamedTuple):
    """The best model of a satisfiable solve, in the form ``SpecBuilder`` takes it."""

    #: cost of the model, one entry per optimization priority
    cost: List[int]
    #: ``(name, args)`` for each ``attr`` atom
    attrs: List[Tuple[str, Tuple]]
    #: arguments of each ``opt_priority`` atom
    opt_priority: List[Tuple]
    #: number of models clingo found
    nmodels: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cost": list(self.cost),
            "attrs": [_encode(attr) for attr in self.attrs],
            "opt_priority": [_encode(args) for args in self.opt_priority],
            "nmodels": self.nmodels,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Answer":
        """Reads the output of ``to_dict``. Raises ``KeyError``, ``TypeError`` or ``ValueError``
        on malformed data."""
        return Answer(
            cost=[int(x) for x in data["cost"]],
            attrs=[_decode(attr) for attr in data["attrs"]],
            opt_priority=[_decode(args) for args in data["opt_priority"]],
            nmodels=int(data["nmodels"]),
        )


class Result:
    """Result of an ASP solve."""

    def __init__(self, specs, *, repo: spack.repo.RepoPath):
        self.repo = repo
        self.satisfiable: Optional[bool] = None
        self.optimal = None
        self.warnings = None
        self.nmodels = 0

        # specs ordered by optimization level
        self.answers: List[Tuple[List[int], int, SpecDict]] = []

        # names of optimization criteria
        self.criteria: List[OptimizationCriteria] = []

        # Abstract user requests
        self.abstract_specs = specs

        # possible dependencies
        self.possible_dependencies: Optional[Set[str]] = None

        # Concrete specs
        self._concrete_specs_by_input = None
        self._concrete_specs = None
        self._unsolved_specs = None

    @property
    def specs(self):
        """List of concretized specs satisfying the initial
        abstract request.
        """
        if self._concrete_specs is None:
            self._compute_specs_from_answer_set()
        return self._concrete_specs

    @property
    def unsolved_specs(self):
        """List of tuples pairing abstract input specs that were not
        solved with their associated candidate spec from the solver
        (if the solve completed).
        """
        if self._unsolved_specs is None:
            self._compute_specs_from_answer_set()
        return self._unsolved_specs

    @property
    def specs_by_input(self) -> Dict[spack.spec.Spec, spack.spec.Spec]:
        if self._concrete_specs_by_input is None:
            self._compute_specs_from_answer_set()
        return self._concrete_specs_by_input  # type: ignore

    def _compute_specs_from_answer_set(self):
        if not self.satisfiable:
            self._concrete_specs = []
            self._unsolved_specs = [(x, None) for x in self.abstract_specs]
            self._concrete_specs_by_input = {}
            return

        self._concrete_specs, self._unsolved_specs = [], []
        self._concrete_specs_by_input = {}
        best = min(self.answers)
        opt, _, answer = best
        for input_spec in self.abstract_specs:
            # The specs must be unified to get here, so it is safe to associate any satisfying spec
            # with the input. Multiple inputs may be matched to the same concrete spec
            node = min_dupe_node(pkg=input_spec.name)
            if self.repo.is_virtual(input_spec.name):
                providers = [
                    spec.name
                    for spec in answer.values()
                    if self.repo.get(spec).provides(input_spec.name)
                ]
                node = min_dupe_node(pkg=providers[0])
            candidate = answer.get(node)

            if candidate and candidate.satisfies(input_spec):
                self._concrete_specs.append(answer[node])
                self._concrete_specs_by_input[input_spec] = answer[node]
            elif candidate and candidate.build_spec.satisfies(input_spec):
                tty.warn(
                    "explicit splice configuration has caused the concretized spec"
                    f" {candidate} not to satisfy the input spec {input_spec}"
                )
                self._concrete_specs.append(answer[node])
                self._concrete_specs_by_input[input_spec] = answer[node]
            else:
                self._unsolved_specs.append((input_spec, candidate))

    def __eq__(self, other):
        eq = (
            self.satisfiable == other.satisfiable,
            self.optimal == other.optimal,
            self.warnings == other.warnings,
            self.nmodels == other.nmodels,
            self.criteria == other.criteria,
            self.answers == other.answers,
            self.abstract_specs == other.abstract_specs,
            # Not considered for equality
            # self._concrete_specs_by_input   # These three are computed
            # self._concrete_specs
            # self._unsolved_specs
            # self.control                    # Currently we just don't serialize these
            # self.possible_dependencies
        )
        return all(eq)
