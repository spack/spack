# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""The result of an ASP solve, and the types needed to read and serialize it.

This module is importable without pulling in the solver itself, so that frontends can be
typed against a result without depending on how it is produced.
"""

import enum
import warnings
from typing import Dict, List, NamedTuple

import spack.hash_types as ht
import spack.repo
import spack.spec
import spack.traverse

from .core import NodeId, min_dupe_node
from .error import SolverError, SpliceSerializationError

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


# We have to take some care with how we serialize a `SpecDict` fresh from a solve,
# because it contains specs that are in between concrete and abstract. The hash is not
# yet final, because there are spec changes yet to be made in post-processing that will
# change the hashes. We still need an identifier for the nodes in the spec DAG, though.
# So, we use hashes as ids during serialization, but we must clear them afterwards so
# that they are not cached, and they can be set again when the final changes are made.


def spec_dict_to_json(spec_dict: SpecDict) -> Dict:
    """Serialize a SpecDict to JSON, taking care to preserve node structure in serialized specs.

    Note: this does not yet handle spliced specs and will raise an error if they're passed in.

    Raises:
        SpliceSerializationError: if any node in ``spec_dict`` has a ``build_spec``.
    """
    # Specs are keyed in spec_dict by their solver-assigned NodeId, but reused concrete
    # specs may have transitive dependencies that do not have a NodeId.
    # Make a dictionary preserving the NodeIds from input.
    node_id_for: Dict[int, NodeId] = {id(spec): nid for nid, spec in spec_dict.items()}

    specs = list(spec_dict.values())

    try:
        # A SpecDict has one entry for each spec in a solution, but some are abstract and some
        # are concrete. We need DAG hashes for the abstract specs to serialize them, so
        # force-cache them, taking care to do so bottom-up, to avoid exponential recomputation.
        # TODO: spec serialization was really designed for concrete and small abstract specs.
        # This should really be handled by Spec, but it will take some work to adjust the format.
        for spec in spack.traverse.traverse_nodes(specs, key=id, order="post"):
            if spec.build_spec is not spec:
                raise SpliceSerializationError(
                    f"cannot serialize spliced spec {spec.name}; SpecDicts with spliced "
                    "specs are not serializable."
                )
            if not spec.concrete:
                spec._cached_hash(ht.dag_hash, force=True)

        # Traverse every spec reachable from spec_dict's values, deduped by hash, and add them
        # to the serialized entries either a) with their original NodeId, or b) with None if they
        # don't have a NodeId. This ensures that all nodes are added and NodeIds are preserved.
        entries = []
        for dep in spack.traverse.traverse_nodes(specs, key=lambda s: s.dag_hash()):
            node = dep.to_node_dict()
            node["hash"] = dep.dag_hash()
            entries.append((node_id_for.get(id(dep)), node))

    finally:
        # Clear hashes cached above, which must be recomputed in post-concretization
        # They're only used here as keys for reading and writing spec DAGs.
        for spec in spack.traverse.traverse_nodes(specs, key=id):
            if not spec.concrete:
                spec.clear_caches()

    return {"_meta": {"spec_version": spack.spec.SpecfileLatest.SPEC_VERSION}, "specs": entries}


def spec_dict_from_json(data: Dict) -> SpecDict:
    """Deserialize a SpecDict from JSON, taking care not to duplicate nodes."""
    try:
        spec_version = int(data["_meta"]["spec_version"])
        entries = data["specs"]
    except (KeyError, ValueError):
        raise ValueError(f"Invalid spec dict data: {data}")

    reader = spack.spec.specfile_reader_for_version(spec_version)
    nodes = [node for _, node in entries]
    specs_by_hash = spack.spec.wire_spec_nodes(nodes, "hash", reader)

    # clear the hashes we cached on any abstract specs, so that they can be recomputed later
    for spec in spack.traverse.traverse_nodes(list(specs_by_hash.values()), key=id):
        if not spec.concrete:
            spec.clear_caches()

    # Anonymous nodes (nid=None) are reachable transitively through named roots' edges, and
    # are handled by wire_spec_nodes() above. Skip them here to preserve SpecDict on round-trip.
    return {NodeId(*nid): specs_by_hash[node["hash"]] for nid, node in entries if nid is not None}


class Result:
    """Result of an ASP solve."""

    def __init__(self, specs):
        self.satisfiable = None
        self.optimal = None
        # Diagnostics about the answer set. Stored, rather than warned about while building
        # specs, so that a result served from the concretization cache reports them too.
        self.warnings: List[str] = []
        self.nmodels = 0

        # specs ordered by optimization level
        self.answers = []

        # names of optimization criteria
        self.criteria = []

        # Abstract user requests
        self.abstract_specs = specs

        # possible dependencies
        self.possible_dependencies = None

        # Concrete specs
        self._concrete_specs_by_input = None
        self._concrete_specs = None
        self._unsolved_specs = None

    def raise_if_unsat(self):
        """Raise a generic internal error if the result is unsatisfiable."""
        if self.satisfiable:
            return

        constraints = self.abstract_specs
        if len(constraints) == 1:
            constraints = constraints[0]

        raise SolverError(constraints)

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
            if spack.repo.PATH.is_virtual(input_spec.name):
                providers = [
                    spec.name for spec in answer.values() if spec.package.provides(input_spec.name)
                ]
                node = min_dupe_node(pkg=providers[0])
            candidate = answer.get(node)

            if candidate and candidate.satisfies(input_spec):
                self._concrete_specs.append(answer[node])
                self._concrete_specs_by_input[input_spec] = answer[node]
            elif candidate and candidate.build_spec.satisfies(input_spec):
                warnings.warn(
                    "explicit splice configuration has caused the concretized spec"
                    f" {candidate} not to satisfy the input spec {input_spec}"
                )
                self._concrete_specs.append(answer[node])
                self._concrete_specs_by_input[input_spec] = answer[node]
            else:
                self._unsolved_specs.append((input_spec, candidate))

    def to_dict(self) -> dict:
        """Produces dict representation of Result object

        Does not include anything related to unsatisfiability as we
        are only interested in storing satisfiable results
        """

        # NOTE: _unsolved_specs, _concrete_specs_by_input, and _concrete_specs are all
        # computed dynamically from self.answers, so they're not serialized.
        return {
            "criteria": self.criteria,
            "optimal": self.optimal,
            "warnings": self.warnings,
            "nmodels": self.nmodels,
            # abstract specs are not used for deserialization, but dropping them is
            # forward-incompatible with Spack 1.2 and earlier.
            "abstract_specs": [s.to_dict() for s in self.abstract_specs],
            "satisfiable": self.satisfiable,
            "answers": [
                (opt, i, spec_dict_to_json(spec_dict)) for opt, i, spec_dict in self.answers
            ],
        }

    @staticmethod
    def from_dict(obj: dict, specs: List[spack.spec.Spec]):
        """Returns Result object from compatible dictionary, for the given input specs.

        The stored abstract specs are troubleshooting metadata and are deliberately not
        deserialized: the caller's input specs are authoritative. This also keeps cache
        entries with unreadable abstract spec data usable.
        """
        result = Result(specs)
        result.criteria = [OptimizationCriteria(*t) for t in obj["criteria"]]
        result.optimal = obj["optimal"]
        # Entries written before warnings were recorded store None here
        result.warnings = obj["warnings"] or []
        result.nmodels = obj["nmodels"]
        result.satisfiable = obj["satisfiable"]
        result.answers = [
            (opt, i, spec_dict_from_json(spec_dict)) for opt, i, spec_dict in obj["answers"]
        ]
        # NOTE: _unsolved_specs, _concrete_specs_by_input, and _concrete_specs are all
        # computed dynamically from self.answers, so they're not serialized.

        return result

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
