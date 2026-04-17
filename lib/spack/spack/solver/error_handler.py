# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Error handling and message formatting for Spack's ASP-based concretizer."""

import pathlib
import typing
from typing import Dict, List, Sequence, Set, Tuple

import spack.error
import spack.spec
from spack.llnl.util.lang import elide_list

from .core import UnsatisfiableSpecError, clingo, extract_args, symbol_to_string

if typing.TYPE_CHECKING:
    clingo()
    import clingo as _clingo

_CONSTRAINT_CHARS = "@^+~%="


def _is_node_symbol(clingo_symbol: "_clingo.Symbol") -> bool:
    """Returns true if the given clingo symbol is a node(ID, Pkg) term."""
    try:
        return clingo_symbol.name == "node" and len(clingo_symbol.arguments) == 2
    except RuntimeError:
        return False


def _package_from_node_symbol(node_sym: "_clingo.Symbol") -> str:
    """Extract the package name string from a raw clingo node(ID, Pkg) symbol."""
    if not _is_node_symbol(node_sym):
        raise FormattingError(f"Expected node(ID, Pkg) term, got {node_sym}")
    return symbol_to_string(node_sym.arguments[1])


def _clingo_arg_to_str(clingo_symbol: "_clingo.Symbol") -> str:
    """Convert a raw clingo symbol argument to a display string.

    For node(ID, Pkg) terms, returns the package name. For string literals,
    returns the string. For all others, falls back to str().
    """
    if _is_node_symbol(clingo_symbol):
        return _package_from_node_symbol(clingo_symbol)
    return symbol_to_string(clingo_symbol)


class ErrorFormatter:
    """Formats concretization error messages from error/3 ASP facts.

    Dispatches on the ErrorType functor name. Each method receives
    ``pkg`` (the package name from the NodeTerm) followed by the
    string-converted arguments of the ErrorType compound term.
    """

    def format(self, error_type: "_clingo.Symbol", node: "_clingo.Symbol") -> str:
        """Format an error message from raw clingo symbols."""
        error_callback_fn = error_type.name
        method = getattr(self, error_callback_fn, self._unknown)
        pkg = _package_from_node_symbol(node)
        try:
            args = [_clingo_arg_to_str(a) for a in error_type.arguments]
        except RuntimeError:
            args = []
        return method(pkg, *args)

    def namespace_missing(self, pkg: str) -> str:
        return f"{pkg} does not have a namespace"

    def namespace_conflict(self, pkg: str, ns1: str, ns2: str) -> str:
        return f"{pkg} cannot come from both {ns1} and {ns2} namespaces"

    def unification_set_conflict(self, pkg: str, set_id: str) -> str:
        return f"Cannot have multiple nodes for {pkg} in the same unification set {set_id}"

    def literal_not_in_dag(self, pkg: str) -> str:
        return (
            f"{pkg} is not a direct 'build' or 'test' dependency, "
            f"or transitive 'link' or 'run' dependency of any root"
        )

    def no_value(self, pkg: str, attribute: str) -> str:
        return f'No value found for "{attribute}" in package "{pkg}"'

    def multiple_values(self, pkg: str, attribute: str) -> str:
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

    def deprecated_version(self, pkg: str, version: str) -> str:
        return (
            f"Package '{pkg}' needs the deprecated version '{version}', "
            f"and this is not allowed"
        )

    def version_constraint_unsatisfied(self, pkg: str, constraint: str) -> str:
        return f"Cannot satisfy '{pkg}@{constraint}'"

    def commit_variant_incompatible(self, pkg: str, version: str) -> str:
        return f"Cannot use commit variant with '{pkg}@={version}'"

    def commit_mismatch(self, pkg: str, vsha: str, psha: str, version: str) -> str:
        return f"Commit '{vsha}' must match package.py value '{psha}' for '{pkg}@={version}'"

    def concrete_build_dep_mismatch(
        self, pkg: str, build_dep: str, attribute: str, *args: str
    ) -> str:
        start_str = f"Cannot satisfy the request on {build_dep}"
        if attribute == "variant":
            variant, value = args
            return f"{start_str} to have {variant}={value}"
        elif attribute == "target":
            target = args[0]
            return f"{start_str} to have the target set to {target}"
        elif attribute == "os":
            node_os = args[0]
            return f"{start_str} to have the OS set to {node_os}"
        elif attribute == "platform":
            platform = args[0]
            return f"{start_str} to have the platform set to {platform}"
        elif attribute == "hash":
            build_hash = args[0]
            return f"{start_str} to have the following hash {build_hash}"
        return f"Cannot satisfy a request on {build_dep}"

    def virtual_on_edge_missing(self, pkg: str, virtual: str) -> str:
        return f"{pkg} cannot have a dependency on {virtual}"

    def node_not_needed(self, pkg: str) -> str:
        return f"'{pkg}' is not a valid dependency for any package in the DAG"

    def extensions_must_share(self, pkg: str, extension_child: str, extendee_pkg: str) -> str:
        return f"{pkg} and {extension_child} must depend on the same {extendee_pkg}"

    def conflict(self, pkg: str, msg: str) -> str:
        return msg

    def provided_together_incomplete(self, pkg: str, virtual: str) -> str:
        return f"Package '{pkg}' must also provide '{virtual}', and it does not"

    def provider_condition_unsatisfied(self, pkg: str, virtual: str) -> str:
        return f"'{pkg}' cannot be a provider for the '{virtual}' virtual"

    def no_valid_provider(self, pkg: str) -> str:
        return f"Cannot find valid provider for virtual {pkg}"

    def multiple_providers(self, pkg: str) -> str:
        return f"Cannot select a single provider for virtual '{pkg}'"

    def buildable_false(self, pkg: str) -> str:
        return (
            f"Cannot build {pkg}, since it is configured `buildable:false` "
            f"and no externals satisfy the request"
        )

    def required_provider_unavailable(self, pkg: str, provider: str) -> str:
        return f"Cannot use {provider} for the {pkg} virtual, but that is required"

    def requirement_unsatisfied(self, pkg: str, message: str) -> str:
        if message:
            return message
        return f"cannot satisfy a requirement for package '{pkg}'."

    def variant_undefined(self, pkg: str, variant: str) -> str:
        return (
            f"Cannot set variant '{variant}' for package '{pkg}' "
            f"because the variant condition cannot be satisfied for the given spec"
        )

    def variant_value_conflict(self, pkg: str, variant: str, value1: str, value2: str) -> str:
        spec1_str = f"{variant}={value1}"
        spec2_str = f"{variant}={value2}"
        try:
            spec1 = str(spack.spec.Spec(spec1_str))
            spec2 = str(spack.spec.Spec(spec2_str))
        except Exception:
            spec1, spec2 = spec1_str, spec2_str
        return f"'{pkg}' requires conflicting variant values '{spec1}' and '{spec2}'"

    def variant_no_value(self, pkg: str, variant: str) -> str:
        return f"No valid value for variant '{variant}' of package '{pkg}'"

    def variant_concrete_extra_value(self, pkg: str, variant: str, value: str) -> str:
        return (
            f"The variant {variant} in package {pkg} "
            f"specified as := has the extra value {value}"
        )

    def variant_invalid_value(self, pkg: str, variant: str, value: str) -> str:
        spec_str = f"{variant}={value}"
        try:
            spec_str = str(spack.spec.Spec(spec_str))
        except Exception:
            pass
        return f"'{spec_str}' is not a valid value for '{pkg}' variant '{variant}'"

    def variant_disjoint_sets(self, pkg: str, variant: str, value1: str, value2: str) -> str:
        return (
            f"{pkg} variant '{variant}' cannot have values "
            f"'{value1}' and '{value2}' as they come from disjoint value sets"
        )

    def variant_none_conflict(self, pkg: str, variant: str, value: str) -> str:
        return f"{pkg} variant '{variant}' cannot have values '{value}' and 'none'"

    def propagation_conflict_to_dep(
        self, pkg: str, other_pkg: str, variant: str, dep_pkg: str
    ) -> str:
        return (
            f"{pkg} and {other_pkg} cannot both propagate "
            f"variant '{variant}' to the shared dependency: {dep_pkg}"
        )

    def propagation_conflict(self, pkg: str, other_pkg: str, variant: str) -> str:
        return f"{pkg} and {other_pkg} cannot both propagate variant '{variant}'"

    def propagation_excluded(self, pkg: str, variant: str, source: str) -> str:
        return (
            f"Cannot propagate the variant '{variant}' from the package: "
            f"{source} because package: {pkg} is set to exclude it"
        )

    def flag_propagation_conflict(
        self, pkg: str, source1: str, source2: str, flag_type: str
    ) -> str:
        return (
            f"{source1} and {source2} cannot both propagate compiler flags '{flag_type}' to {pkg}"
        )

    def compiler_mixing_disabled(self, pkg: str, language: str) -> str:
        return f"Compiler mixing is disabled for the {language} language"

    def os_not_buildable(self, pkg: str, os_name: str) -> str:
        return (
            f"Cannot select '{pkg} os={os_name}' "
            f"(operating system '{os_name}' is not buildable)"
        )

    def target_constraint_unsatisfied(self, pkg: str, target: str, constraint: str) -> str:
        return f"'{pkg} target={target}' cannot satisfy constraint 'target={constraint}'"

    def target_incompatible(self, pkg: str, dependency: str) -> str:
        return f"Cannot find compatible targets for {pkg} and {dependency}"

    def compiler_must_be_external(self, pkg: str, language: str) -> str:
        return f"Only external, or concrete, compilers are allowed for the {language} language"

    def compiler_target_incompatible(
        self, pkg: str, target: str, compiler: str, version: str
    ) -> str:
        return f"{pkg} compiler '{compiler}@{version}' incompatible with 'target={target}'"

    def target_not_on_machine(self, pkg: str, target: str) -> str:
        return f"'{pkg} target={target}' is not compatible with this machine"

    def multiple_cli_flags(self, pkg: str, flag_type: str) -> str:
        return f"Cannot set multiple {flag_type} values for {pkg} from cli"

    def libc_incompatible(self, pkg: str) -> str:
        return f"Cannot reuse {pkg} since we cannot determine libc compatibility"

    def _unknown(self, pkg: str, *args: str) -> str:
        return f"unknown error for {pkg}: {args}"


ErrorTypeTuple = Tuple[str, str]
CauseType = Tuple[str, str]


class ErrorHandler:
    def __init__(self, model: Sequence["_clingo.Symbol"], input_specs: List[spack.spec.Spec]):
        self.model = model
        self.input_specs = input_specs
        self.full_model: List["_clingo.Symbol"] = []

    def _get_cause_tree(
        self,
        cause: CauseType,
        conditions: Dict[str, str],
        condition_causes: Dict[CauseType, List[CauseType]],
        seen: Set[CauseType],
        indent: str = "        ",
    ) -> List[str]:
        """
        Implementation of recursion for self.get_cause_tree. Much of this operates on tuples
        (condition_id, set_id) in which the latter idea means that the condition represented by
        the former held in the condition set represented by the latter.
        """
        seen.add(cause)
        parents = [c for c in condition_causes.get(cause, []) if c not in seen]
        local = f"required because {conditions[cause[0]]} "

        return [indent + local] + [
            c
            for parent in parents
            for c in self._get_cause_tree(
                parent, conditions, condition_causes, seen, indent=indent + "  "
            )
        ]

    def raise_if_errors(self) -> None:
        initial_errors = [sym for sym in self.model if sym.name == "error"]
        if not initial_errors:
            return

        error_causation = clingo().Control()

        parent_dir = pathlib.Path(__file__).parent
        errors_lp = parent_dir / "error_messages.lp"

        def on_model(model):
            self.full_model = model.symbols(shown=True, terms=True)

        with error_causation.backend() as backend:
            for atom in self.model:
                atom_id = backend.add_atom(atom)
                backend.add_rule([atom_id], [], choice=False)

            error_causation.load(str(errors_lp))
            error_causation.ground([("base", []), ("error_messages", [])])
            _ = error_causation.solve(on_model=on_model)

        # Extract error/3 and error_cause/4 as raw clingo symbols
        error_symbols = [
            sym for sym in self.full_model if sym.name == "error" and len(sym.arguments) == 3
        ]
        cause_symbols = [
            sym for sym in self.full_model if sym.name == "error_cause" and len(sym.arguments) == 4
        ]

        # Build causes lookup: (ErrorType, Node) -> [(cond_id, cause_id), ...]
        # Use symbol_to_string rather than str() to correctly handle string atoms
        # (e.g. conflict("msg")) across both native clingo and the CFFI binding.
        causes_by_error: Dict[ErrorTypeTuple, List[CauseType]] = {}
        for sym in cause_symbols:
            error_key = (symbol_to_string(sym.arguments[0]), symbol_to_string(sym.arguments[1]))
            cond_id = symbol_to_string(sym.arguments[2])
            cause_id = symbol_to_string(sym.arguments[3])
            causes_by_error.setdefault(error_key, []).append((cond_id, cause_id))

        # Sort errors by weight descending
        errors = sorted(
            [
                # ( Weight, ErrorType, Node )
                (int(symbol_to_string(sym.arguments[1])), sym.arguments[0], sym.arguments[2])
                for sym in error_symbols
            ],
            reverse=True,
        )

        conditions: Dict[str, str] = dict(extract_args(self.full_model, "condition_reason"))
        condition_causes: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
        for Effect, EID, Cause, CID in extract_args(self.full_model, "condition_cause"):
            condition_causes.setdefault((Effect, EID), []).append((Cause, CID))

        formatter = ErrorFormatter()
        try:
            messages = []
            for _weight, error_type_sym, node_sym in errors:
                try:
                    msg = formatter.format(error_type_sym, node_sym)
                except Exception as e:
                    msg = f"unknown error [{e}]"
                error_key = (symbol_to_string(error_type_sym), symbol_to_string(node_sym))
                seen_causes: Set[Tuple[str, str]] = set()
                for cond_id, cause_id in causes_by_error.get(error_key, []):
                    cause = (cond_id, cause_id)
                    if cause not in seen_causes:
                        seen_causes.add(cause)
                        lines = self._get_cause_tree(cause, conditions, condition_causes, set())
                        informative = [
                            line
                            for line in lines
                            if not (
                                "requested explicitly" in line
                                and not any(c in line for c in _CONSTRAINT_CHARS)
                            )
                        ]
                        for line in informative if informative else lines:
                            msg += f"\n{line}"
                messages.append(msg)

            input_specs = ", ".join(elide_list([f"`{s}`" for s in self.input_specs], 5))
            header = f"failed to concretize {input_specs} for the following reasons:"
            full_msg = "\n".join(
                [header] + [f"    {i + 1:2}. {m}" for i, m in enumerate(messages)]
            )
        except Exception as e:
            full_msg = (
                f"unexpected error during concretization [{str(e)}]. "
                f"Please report a bug at https://github.com/spack/spack/issues"
            )
            raise spack.error.SpackError(full_msg) from e
        raise UnsatisfiableSpecError(full_msg)


class FormattingError(spack.error.SpackError):
    """Raised when formatting an error message fails"""
