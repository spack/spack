# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Error handling and message formatting for Spack's ASP-based concretizer."""
import pathlib
from typing import Dict, List, Optional, Set, Tuple

import spack.error
import spack.spec
from spack.llnl.util.lang import elide_list

from .core import UnsatisfiableSpecError, clingo, extract_args


def _node_pkg_from_sym(node_sym) -> str:
    """Extract the package name string from a raw clingo node(ID, Pkg) symbol."""
    try:
        if node_sym.name == "node" and len(node_sym.arguments) == 2:
            pkg_sym = node_sym.arguments[1]
            try:
                return pkg_sym.string
            except RuntimeError:
                return str(pkg_sym)
    except RuntimeError:
        pass
    return str(node_sym)


def _clingo_arg_to_str(sym) -> str:
    """Convert a raw clingo symbol argument to a display string.

    For node(ID, Pkg) terms, returns the package name. For string literals,
    returns the string. For all others, falls back to str().
    """
    try:
        if sym.name == "node" and len(sym.arguments) == 2:
            return _node_pkg_from_sym(sym)
    except RuntimeError:
        pass
    try:
        val = sym.string
        if val:
            return val
    except RuntimeError:
        pass
    return str(sym)


class ErrorFormatter:
    """Formats concretization error messages from error/3 ASP facts.

    Dispatches on the ErrorType functor name. Each method receives
    ``pkg`` (the package name from the NodeTerm) followed by the
    string-converted arguments of the ErrorType compound term.
    """

    def format(self, error_type_sym, node_sym) -> str:
        """Format an error message from raw clingo symbols."""
        try:
            name = error_type_sym.name
        except RuntimeError:
            name = str(error_type_sym)
        pkg = _node_pkg_from_sym(node_sym)
        try:
            args = [_clingo_arg_to_str(a) for a in error_type_sym.arguments]
        except RuntimeError:
            args = []
        method = getattr(self, name, self._unknown)
        return method(pkg, *args)

    def namespace_missing(self, pkg):
        return f"{pkg} does not have a namespace"

    def namespace_conflict(self, pkg, ns1, ns2):
        return f"{pkg} cannot come from both {ns1} and {ns2} namespaces"

    def unification_set_conflict(self, pkg, set_id):
        return f"Cannot have multiple nodes for {pkg} in the same unification set {set_id}"

    def literal_not_in_dag(self, pkg):
        return (
            f"'{pkg}' is not a direct 'build' or 'test' dependency, "
            f"or transitive 'link' or 'run' dependency of any root"
        )

    def no_value(self, pkg, attribute):
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

    def multiple_values(self, pkg, attribute):
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

    def deprecated_version(self, pkg, version):
        return (
            f"Package '{pkg}' needs the deprecated version '{version}', "
            f"and this is not allowed"
        )

    def version_constraint_unsatisfied(self, pkg, constraint):
        return f"Cannot satisfy '{pkg}@{constraint}'"

    def commit_variant_incompatible(self, pkg, version):
        return f"Cannot use commit variant with '{pkg}@={version}'"

    def commit_mismatch(self, pkg, vsha, psha, version):
        return f"Commit '{vsha}' must match package.py value '{psha}' for '{pkg}@={version}'"

    def concrete_build_dep_variant(self, pkg, build_dep, variant, value):
        return f"Cannot satisfy the request on {build_dep} to have {variant}={value}"

    def concrete_build_dep_target(self, pkg, build_dep, target):
        return f"Cannot satisfy the request on {build_dep} to have the target set to {target}"

    def concrete_build_dep_os(self, pkg, build_dep, node_os):
        return f"Cannot satisfy the request on {build_dep} to have the os set to {node_os}"

    def concrete_build_dep_platform(self, pkg, build_dep, platform):
        return f"Cannot satisfy the request on {build_dep} to have the platform set to {platform}"

    def concrete_build_dep_hash(self, pkg, build_dep, build_hash):
        return (
            f"Cannot satisfy the request on {build_dep} "
            f"to have the following hash {build_hash}"
        )

    def provider_edge_missing(self, pkg, build_dep, virtual):
        return f"{pkg} cannot have a dependency on {virtual}"

    def virtual_edge_missing(self, pkg, virtual):
        return f"{pkg} cannot have a dependency on {virtual}"

    def node_not_needed(self, pkg):
        return f"'{pkg}' is not a valid dependency for any package in the DAG"

    def extensions_must_share(self, pkg, extension_child, extendee_pkg):
        return f"{pkg} and {extension_child} must depend on the same {extendee_pkg}"

    def conflict(self, pkg, msg):
        return str(msg)

    def provided_together_incomplete(self, pkg, virtual1, virtual2):
        return (
            f"Package '{pkg}' needs to provide both '{virtual1}' and '{virtual2}' "
            f"together, but provides only '{virtual1}'"
        )

    def provider_condition_unsatisfied(self, pkg, virtual):
        return f"'{pkg}' cannot be a provider for the '{virtual}' virtual"

    def no_valid_provider(self, pkg):
        return f"Cannot find valid provider for virtual {pkg}"

    def multiple_providers(self, pkg):
        return f"Cannot select a single provider for virtual '{pkg}'"

    def buildable_false(self, pkg):
        return (
            f"Cannot build {pkg}, since it is configured `buildable:false` "
            f"and no externals satisfy the request"
        )

    def required_provider_unavailable(self, pkg, provider):
        return f"Cannot use {provider} for the {pkg} virtual, but that is required"

    def requirement_unsatisfied(self, pkg):
        return f"cannot satisfy a requirement for package '{pkg}'."

    def requirement_unsatisfied_msg(self, pkg, message):
        return str(message)

    def variant_condition_unsatisfied(self, pkg, variant):
        return (
            f"Cannot set variant '{variant}' for package '{pkg}' "
            f"because the variant condition cannot be satisfied for the given spec"
        )

    def variant_value_condition_unsatisfied(self, pkg, variant):
        return (
            f"Cannot set variant '{variant}' for package '{pkg}' "
            f"because the variant condition cannot be satisfied for the given spec"
        )

    def variant_value_conflict(self, pkg, variant, value1, value2):
        spec1_str = f"{variant}={value1}"
        spec2_str = f"{variant}={value2}"
        try:
            spec1 = str(spack.spec.Spec(spec1_str))
            spec2 = str(spack.spec.Spec(spec2_str))
        except Exception:
            spec1, spec2 = spec1_str, spec2_str
        return f"'{pkg}' requires conflicting variant values '{spec1}' and '{spec2}'"

    def variant_no_value(self, pkg, variant):
        return f"No valid value for variant '{variant}' of package '{pkg}'"

    def variant_concrete_extra_value(self, pkg, variant, value):
        return (
            f"The variant {variant} in package {pkg} "
            f"specified as := has the extra value {value}"
        )

    def variant_invalid_value(self, pkg, variant, value):
        spec_str = f"{variant}={value}"
        try:
            spec_str = str(spack.spec.Spec(spec_str))
        except Exception:
            pass
        return f"'{spec_str}' is not a valid value for '{pkg}' variant '{variant}'"

    def variant_disjoint_sets(self, pkg, variant, value1, value2):
        return (
            f"{pkg} variant '{variant}' cannot have values "
            f"'{value1}' and '{value2}' as they come from disjoint value sets"
        )

    def variant_none_conflict(self, pkg, variant, value):
        return f"{pkg} variant '{variant}' cannot have values '{value}' and 'none'"

    def propagation_conflict_to_dep(self, pkg, other_pkg, variant, dep_pkg):
        return (
            f"{pkg} and {other_pkg} cannot both propagate "
            f"variant '{variant}' to the shared dependency: {dep_pkg}"
        )

    def propagation_conflict(self, pkg, other_pkg, variant):
        return f"{pkg} and {other_pkg} cannot both propagate variant '{variant}'"

    def propagation_excluded(self, pkg, variant, source):
        return (
            f"Cannot propagate the variant '{variant}' from the package: "
            f"{source} because package: {pkg} is set to exclude it"
        )

    def flag_propagation_conflict(self, pkg, source2, flag_type):
        return (
            f"{pkg}: cannot propagate compiler flags '{flag_type}' "
            f"from multiple sources including {source2}"
        )

    def compiler_mixing_disabled(self, pkg, language):
        return f"Compiler mixing is disabled for the {language} language"

    def os_not_buildable(self, pkg, os_name):
        return (
            f"Cannot select '{pkg} os={os_name}' "
            f"(operating system '{os_name}' is not buildable)"
        )

    def target_constraint_unsatisfied(self, pkg, target, constraint):
        return f"'{pkg} target={target}' cannot satisfy constraint 'target={constraint}'"

    def target_incompatible(self, pkg, dependency):
        return f"Cannot find compatible targets for {pkg} and {dependency}"

    def compiler_must_be_external(self, pkg, language):
        return f"Only external, or concrete, compilers are allowed for the {language} language"

    def compiler_target_incompatible(self, pkg, target, compiler, version):
        return f"{pkg} compiler '{compiler}@{version}' incompatible with 'target={target}'"

    def target_not_on_machine(self, pkg, target):
        return f"'{pkg} target={target}' is not compatible with this machine"

    def multiple_cli_flags(self, pkg, flag_type):
        return f"Cannot set multiple {flag_type} values for {pkg} from cli"

    def libc_incompatible(self, pkg):
        return f"Cannot reuse {pkg} since we cannot determine libc compatibility"

    def _unknown(self, pkg, *args):
        return f"unknown error for {pkg}: {args}"


class ErrorHandler:
    def __init__(self, model, input_specs: List[spack.spec.Spec]):
        self.model = model
        self.input_specs = input_specs
        self.full_model: Optional[List] = None

    def _get_cause_tree(
        self,
        cause: Tuple[str, str],
        conditions: Dict[str, str],
        condition_causes: List[Tuple[Tuple[str, str], Tuple[str, str]]],
        seen: Set,
        indent: str = "        ",
    ) -> List[str]:
        """
        Implementation of recursion for self.get_cause_tree. Much of this operates on tuples
        (condition_id, set_id) in which the latter idea means that the condition represented by
        the former held in the condition set represented by the latter.
        """
        seen.add(cause)
        parents = [c for e, c in condition_causes if e == cause and c not in seen]
        local = f"required because {conditions[cause[0]]} "

        return [indent + local] + [
            c
            for parent in parents
            for c in self._get_cause_tree(
                parent, conditions, condition_causes, seen, indent=indent + "  "
            )
        ]

    def raise_if_errors(self):
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
        error_syms = [
            sym for sym in self.full_model if sym.name == "error" and len(sym.arguments) == 3
        ]
        cause_syms = [
            sym for sym in self.full_model if sym.name == "error_cause" and len(sym.arguments) == 4
        ]

        # Build causes lookup: (ErrorType_str, NodeTerm_str) -> [(cond_id, cause_id), ...]
        causes_by_error: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
        for sym in cause_syms:
            key = (str(sym.arguments[0]), str(sym.arguments[1]))
            cond_id = str(sym.arguments[2])
            cause_id = str(sym.arguments[3])
            causes_by_error.setdefault(key, []).append((cond_id, cause_id))

        # Sort errors by weight descending
        errors = sorted(
            [
                (int(str(sym.arguments[1])), sym.arguments[0], sym.arguments[2])
                for sym in error_syms
            ],
            reverse=True,
        )

        conditions: Dict[str, str] = dict(extract_args(self.full_model, "condition_reason"))
        condition_causes: List[Tuple[Tuple[str, str], Tuple[str, str]]] = list(
            ((Effect, EID), (Cause, CID))
            for Effect, EID, Cause, CID in extract_args(self.full_model, "condition_cause")
        )

        formatter = ErrorFormatter()
        try:
            messages = []
            for _weight, error_type_sym, node_sym in errors:
                try:
                    msg = formatter.format(error_type_sym, node_sym)
                except Exception as e:
                    msg = f"unknown error [{e}]"
                key = (str(error_type_sym), str(node_sym))
                seen_causes: Set[Tuple[str, str]] = set()
                for cond_id, cause_id in causes_by_error.get(key, []):
                    cause = (cond_id, cause_id)
                    if cause not in seen_causes:
                        seen_causes.add(cause)
                        for line in self._get_cause_tree(
                            cause, conditions, condition_causes, set()
                        ):
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
