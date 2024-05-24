# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import copy
import enum
import functools
import itertools
import os
import pathlib
import pprint
import re
import sys
import types
import typing
import warnings
from contextlib import contextmanager
from typing import Callable, Dict, Iterator, List, NamedTuple, Optional, Set, Tuple, Type, Union

import archspec.cpu

import llnl.util.lang
import llnl.util.tty as tty

import spack
import spack.binary_distribution
import spack.cmd
import spack.compilers
import spack.config
import spack.config as sc
import spack.deptypes as dt
import spack.directives
import spack.environment as ev
import spack.error
import spack.package_base
import spack.package_prefs
import spack.parser
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.util.crypto
import spack.util.elf
import spack.util.libc
import spack.util.path
import spack.util.timer
import spack.variant
import spack.version as vn
import spack.version.git_ref_lookup
from spack import traverse

from .core import (
    AspFunction,
    NodeArgument,
    ast_sym,
    ast_type,
    clingo,
    clingo_cffi,
    extract_args,
    fn,
    parse_files,
    parse_term,
)
from .counter import FullDuplicatesCounter, MinimalDuplicatesCounter, NoDuplicatesCounter

GitOrStandardVersion = Union[spack.version.GitVersion, spack.version.StandardVersion]

TransformFunction = Callable[["spack.spec.Spec", List[AspFunction]], List[AspFunction]]

#: Enable the addition of a runtime node
WITH_RUNTIME = sys.platform != "win32"

#: Data class that contain configuration on what a
#: clingo solve should output.
#:
#: Args:
#:     timers (bool):  Print out coarse timers for different solve phases.
#:     stats (bool): Whether to output Clingo's internal solver statistics.
#:     out: Optional output stream for the generated ASP program.
#:     setup_only (bool): if True, stop after setup and don't solve (default False).
OutputConfiguration = collections.namedtuple(
    "OutputConfiguration", ["timers", "stats", "out", "setup_only"]
)

#: Default output configuration for a solve
DEFAULT_OUTPUT_CONFIGURATION = OutputConfiguration(
    timers=False, stats=False, out=None, setup_only=False
)


def default_clingo_control():
    """Return a control object with the default settings used in Spack"""
    control = clingo().Control()
    control.configuration.configuration = "tweety"
    control.configuration.solver.heuristic = "Domain"
    control.configuration.solver.opt_strategy = "usc,one"
    return control


class Provenance(enum.IntEnum):
    """Enumeration of the possible provenances of a version."""

    # A spec literal
    SPEC = enum.auto()
    # A dev spec literal
    DEV_SPEC = enum.auto()
    # An external spec declaration
    EXTERNAL = enum.auto()
    # The 'packages' section of the configuration
    PACKAGES_YAML = enum.auto()
    # A package requirement
    PACKAGE_REQUIREMENT = enum.auto()
    # A 'package.py' file
    PACKAGE_PY = enum.auto()
    # An installed spec
    INSTALLED = enum.auto()
    # A runtime injected from another package (e.g. a compiler)
    RUNTIME = enum.auto()

    def __str__(self):
        return f"{self._name_.lower()}"


@contextmanager
def spec_with_name(spec, name):
    """Context manager to temporarily set the name of a spec"""
    old_name = spec.name
    spec.name = name
    try:
        yield spec
    finally:
        spec.name = old_name


class RequirementKind(enum.Enum):
    """Purpose / provenance of a requirement"""

    #: Default requirement expressed under the 'all' attribute of packages.yaml
    DEFAULT = enum.auto()
    #: Requirement expressed on a virtual package
    VIRTUAL = enum.auto()
    #: Requirement expressed on a specific package
    PACKAGE = enum.auto()


class DeclaredVersion(NamedTuple):
    """Data class to contain information on declared versions used in the solve"""

    #: String representation of the version
    version: str
    #: Unique index assigned to this version
    idx: int
    #: Provenance of the version
    origin: Provenance


# Below numbers are used to map names of criteria to the order
# they appear in the solution. See concretize.lp

# The space of possible priorities for optimization targets
# is partitioned in the following ranges:
#
# [0-100) Optimization criteria for software being reused
# [100-200) Fixed criteria that are higher priority than reuse, but lower than build
# [200-300) Optimization criteria for software being built
# [300-1000) High-priority fixed criteria
# [1000-inf) Error conditions
#
# Each optimization target is a minimization with optimal value 0.

#: High fixed priority offset for criteria that supersede all build criteria
high_fixed_priority_offset = 300

#: Priority offset for "build" criteria (regular criterio shifted to
#: higher priority for specs we have to build)
build_priority_offset = 200

#: Priority offset of "fixed" criteria (those w/o build criteria)
fixed_priority_offset = 100


def build_criteria_names(costs, arg_tuples):
    """Construct an ordered mapping from criteria names to costs."""
    # pull optimization criteria names out of the solution
    priorities_names = []

    num_fixed = 0
    num_high_fixed = 0
    for args in arg_tuples:
        priority, name = args[:2]
        priority = int(priority)

        # add the priority of this opt criterion and its name
        priorities_names.append((priority, name))

        # if the priority is less than fixed_priority_offset, then it
        # has an associated build priority -- the same criterion but for
        # nodes that we have to build.
        if priority < fixed_priority_offset:
            build_priority = priority + build_priority_offset
            priorities_names.append((build_priority, name))
        elif priority >= high_fixed_priority_offset:
            num_high_fixed += 1
        else:
            num_fixed += 1

    # sort the criteria by priority
    priorities_names = sorted(priorities_names, reverse=True)

    # We only have opt-criterion values for non-error types
    # error type criteria are excluded (they come first)
    error_criteria = len(costs) - len(priorities_names)
    costs = costs[error_criteria:]

    # split list into three parts: build criteria, fixed criteria, non-build criteria
    num_criteria = len(priorities_names)
    num_build = (num_criteria - num_fixed - num_high_fixed) // 2

    build_start_idx = num_high_fixed
    fixed_start_idx = num_high_fixed + num_build
    installed_start_idx = num_high_fixed + num_build + num_fixed

    high_fixed = priorities_names[:build_start_idx]
    build = priorities_names[build_start_idx:fixed_start_idx]
    fixed = priorities_names[fixed_start_idx:installed_start_idx]
    installed = priorities_names[installed_start_idx:]

    # mapping from priority to index in cost list
    indices = dict((p, i) for i, (p, n) in enumerate(priorities_names))

    # make a list that has each name with its build and non-build costs
    criteria = [(cost, None, name) for cost, (p, name) in zip(costs[:build_start_idx], high_fixed)]
    criteria += [
        (cost, None, name)
        for cost, (p, name) in zip(costs[fixed_start_idx:installed_start_idx], fixed)
    ]

    for (i, name), (b, _) in zip(installed, build):
        criteria.append((costs[indices[i]], costs[indices[b]], name))

    return criteria


def issequence(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, (collections.abc.Sequence, types.GeneratorType))


def listify(args):
    if len(args) == 1 and issequence(args[0]):
        return list(args[0])
    return list(args)


def packagize(pkg):
    if isinstance(pkg, str):
        return spack.repo.PATH.get_pkg_class(pkg)
    else:
        return pkg


def specify(spec):
    if isinstance(spec, spack.spec.Spec):
        return spec
    return spack.spec.Spec(spec)


def remove_node(spec: spack.spec.Spec, facts: List[AspFunction]) -> List[AspFunction]:
    """Transformation that removes all "node" and "virtual_node" from the input list of facts."""
    return list(filter(lambda x: x.args[0] not in ("node", "virtual_node"), facts))


def _create_counter(specs: List[spack.spec.Spec], tests: bool):
    strategy = spack.config.CONFIG.get("concretizer:duplicates:strategy", "none")
    if strategy == "full":
        return FullDuplicatesCounter(specs, tests=tests)
    if strategy == "minimal":
        return MinimalDuplicatesCounter(specs, tests=tests)
    return NoDuplicatesCounter(specs, tests=tests)


def all_compilers_in_config(configuration):
    return spack.compilers.all_compilers_from(configuration)


def all_libcs() -> Set[spack.spec.Spec]:
    """Return a set of all libc specs targeted by any configured compiler. If none, fall back to
    libc determined from the current Python process if dynamically linked."""

    libcs = {
        c.default_libc for c in all_compilers_in_config(spack.config.CONFIG) if c.default_libc
    }

    if libcs:
        return libcs

    libc = spack.util.libc.libc_from_current_python_process()
    return {libc} if libc else set()


def libc_is_compatible(lhs: spack.spec.Spec, rhs: spack.spec.Spec) -> List[spack.spec.Spec]:
    return (
        lhs.name == rhs.name
        and lhs.external_path == rhs.external_path
        and lhs.version >= rhs.version
    )


def using_libc_compatibility() -> bool:
    """Returns True if we are currently using libc compatibility"""
    return spack.platforms.host().name == "linux"


def extend_flag_list(flag_list, new_flags):
    """Extend a list of flags, preserving order and precedence.

    Add new_flags at the end of flag_list.  If any flags in new_flags are
    already in flag_list, they are moved to the end so that they take
    higher precedence on the compile line.

    """
    for flag in new_flags:
        if flag in flag_list:
            flag_list.remove(flag)
        flag_list.append(flag)


def check_packages_exist(specs):
    """Ensure all packages mentioned in specs exist."""
    repo = spack.repo.PATH
    for spec in specs:
        for s in spec.traverse():
            try:
                check_passed = repo.repo_for_pkg(s).exists(s.name) or repo.is_virtual(s.name)
            except Exception as e:
                msg = "Cannot find package: {0}".format(str(e))
                check_passed = False
                tty.debug(msg)

            if not check_passed:
                raise spack.repo.UnknownPackageError(str(s.fullname))


class Result:
    """Result of an ASP solve."""

    def __init__(self, specs, asp=None):
        self.asp = asp
        self.satisfiable = None
        self.optimal = None
        self.warnings = None
        self.nmodels = 0

        # Saved control object for reruns when necessary
        self.control = None

        # specs ordered by optimization level
        self.answers = []
        self.cores = []

        # names of optimization criteria
        self.criteria = []

        # Abstract user requests
        self.abstract_specs = specs

        # Concrete specs
        self._concrete_specs_by_input = None
        self._concrete_specs = None
        self._unsolved_specs = None

    def format_core(self, core):
        """
        Format an unsatisfiable core for human readability

        Returns a list of strings, where each string is the human readable
        representation of a single fact in the core, including a newline.

        Modeled after traceback.format_stack.
        """
        error_msg = (
            "Internal Error: ASP Result.control not populated. Please report to the spack"
            " maintainers"
        )
        assert self.control, error_msg

        symbols = dict((a.literal, a.symbol) for a in self.control.symbolic_atoms)

        core_symbols = []
        for atom in core:
            sym = symbols[atom]
            core_symbols.append(sym)

        return sorted(str(symbol) for symbol in core_symbols)

    def minimize_core(self, core):
        """
        Return a subset-minimal subset of the core.

        Clingo cores may be thousands of lines when two facts are sufficient to
        ensure unsatisfiability. This algorithm reduces the core to only those
        essential facts.
        """
        error_msg = (
            "Internal Error: ASP Result.control not populated. Please report to the spack"
            " maintainers"
        )
        assert self.control, error_msg

        min_core = core[:]
        for fact in core:
            # Try solving without this fact
            min_core.remove(fact)
            ret = self.control.solve(assumptions=min_core)
            if not ret.unsatisfiable:
                min_core.append(fact)
        return min_core

    def minimal_cores(self):
        """
        Return a list of subset-minimal unsatisfiable cores.
        """
        return [self.minimize_core(core) for core in self.cores]

    def format_minimal_cores(self):
        """List of facts for each core

        Separate cores are separated by an empty line
        """
        string_list = []
        for core in self.minimal_cores():
            if string_list:
                string_list.append("\n")
            string_list.extend(self.format_core(core))
        return string_list

    def format_cores(self):
        """List of facts for each core

        Separate cores are separated by an empty line
        Cores are not minimized
        """
        string_list = []
        for core in self.cores:
            if string_list:
                string_list.append("\n")
            string_list.extend(self.format_core(core))
        return string_list

    def raise_if_unsat(self):
        """
        Raise an appropriate error if the result is unsatisfiable.

        The error is an SolverError, and includes the minimized cores
        resulting from the solve, formatted to be human readable.
        """
        if self.satisfiable:
            return

        constraints = self.abstract_specs
        if len(constraints) == 1:
            constraints = constraints[0]

        conflicts = self.format_minimal_cores()
        raise SolverError(constraints, conflicts=conflicts)

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
    def specs_by_input(self):
        if self._concrete_specs_by_input is None:
            self._compute_specs_from_answer_set()
        return self._concrete_specs_by_input

    def _compute_specs_from_answer_set(self):
        if not self.satisfiable:
            self._concrete_specs = []
            self._unsolved_specs = list((x, None) for x in self.abstract_specs)
            self._concrete_specs_by_input = {}
            return

        self._concrete_specs, self._unsolved_specs = [], []
        self._concrete_specs_by_input = {}
        best = min(self.answers)
        opt, _, answer = best
        for input_spec in self.abstract_specs:
            node = SpecBuilder.make_node(pkg=input_spec.name)
            if input_spec.virtual:
                providers = [
                    spec.name for spec in answer.values() if spec.package.provides(input_spec.name)
                ]
                node = SpecBuilder.make_node(pkg=providers[0])
            candidate = answer.get(node)

            if candidate and candidate.satisfies(input_spec):
                self._concrete_specs.append(answer[node])
                self._concrete_specs_by_input[input_spec] = answer[node]
            else:
                self._unsolved_specs.append((input_spec, candidate))

    @staticmethod
    def format_unsolved(unsolved_specs):
        """Create a message providing info on unsolved user specs and for
        each one show the associated candidate spec from the solver (if
        there is one).
        """
        msg = "Unsatisfied input specs:"
        for input_spec, candidate in unsolved_specs:
            msg += f"\n\tInput spec: {str(input_spec)}"
            if candidate:
                msg += f"\n\tCandidate spec: {str(candidate)}"
            else:
                msg += "\n\t(No candidate specs from solver)"
        return msg


def _normalize_packages_yaml(packages_yaml):
    normalized_yaml = copy.copy(packages_yaml)
    for pkg_name in packages_yaml:
        is_virtual = spack.repo.PATH.is_virtual(pkg_name)
        if pkg_name == "all" or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = normalized_yaml.pop(pkg_name)
        is_buildable = data.get("buildable", True)
        if not is_buildable:
            for provider in spack.repo.PATH.providers_for(pkg_name):
                entry = normalized_yaml.setdefault(provider.name, {})
                entry["buildable"] = False

        externals = data.get("externals", [])

        def keyfn(x):
            return spack.spec.Spec(x["spec"]).name

        for provider, specs in itertools.groupby(externals, key=keyfn):
            entry = normalized_yaml.setdefault(provider, {})
            entry.setdefault("externals", []).extend(specs)

    return normalized_yaml


def _is_checksummed_git_version(v):
    return isinstance(v, vn.GitVersion) and v.is_commit


def _is_checksummed_version(version_info: Tuple[GitOrStandardVersion, dict]):
    """Returns true iff the version is not a moving target"""
    version, info = version_info
    if isinstance(version, spack.version.StandardVersion):
        if any(h in info for h in spack.util.crypto.hashes.keys()) or "checksum" in info:
            return True
        return "commit" in info and len(info["commit"]) == 40
    return _is_checksummed_git_version(version)


def _concretization_version_order(version_info: Tuple[GitOrStandardVersion, dict]):
    """Version order key for concretization, where preferred > not preferred,
    not deprecated > deprecated, finite > any infinite component; only if all are
    the same, do we use default version ordering."""
    version, info = version_info
    return (
        info.get("preferred", False),
        not info.get("deprecated", False),
        not version.isdevelop(),
        not version.is_prerelease(),
        version,
    )


def _spec_with_default_name(spec_str, name):
    """Return a spec with a default name if none is provided, used for requirement specs"""
    spec = spack.spec.Spec(spec_str)
    if not spec.name:
        spec.name = name
    return spec


def _external_config_with_implicit_externals(configuration):
    # Read packages.yaml and normalize it, so that it will not contain entries referring to
    # virtual packages.
    packages_yaml = _normalize_packages_yaml(configuration.get("packages"))

    # Add externals for libc from compilers on Linux
    if not using_libc_compatibility():
        return packages_yaml

    for compiler in all_compilers_in_config(configuration):
        libc = compiler.default_libc
        if libc:
            entry = {"spec": f"{libc} %{compiler.spec}", "prefix": libc.external_path}
            packages_yaml.setdefault(libc.name, {}).setdefault("externals", []).append(entry)
    return packages_yaml


class ErrorHandler:
    def __init__(self, model):
        self.model = model
        self.full_model = None

    def multiple_values_error(self, attribute, pkg):
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

    def no_value_error(self, attribute, pkg):
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

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
        local = "required because %s " % conditions[cause[0]]

        return [indent + local] + [
            c
            for parent in parents
            for c in self._get_cause_tree(
                parent, conditions, condition_causes, seen, indent=indent + "  "
            )
        ]

    def get_cause_tree(self, cause: Tuple[str, str]) -> List[str]:
        """
        Get the cause tree associated with the given cause.

        Arguments:
            cause: The root cause of the tree (final condition)

        Returns:
            A list of strings describing the causes, formatted to display tree structure.
        """
        conditions: Dict[str, str] = dict(extract_args(self.full_model, "condition_reason"))
        condition_causes: List[Tuple[Tuple[str, str], Tuple[str, str]]] = list(
            ((Effect, EID), (Cause, CID))
            for Effect, EID, Cause, CID in extract_args(self.full_model, "condition_cause")
        )
        return self._get_cause_tree(cause, conditions, condition_causes, set())

    def handle_error(self, msg, *args):
        """Handle an error state derived by the solver."""
        if msg == "multiple_values_error":
            return self.multiple_values_error(*args)

        if msg == "no_value_error":
            return self.no_value_error(*args)

        try:
            idx = args.index("startcauses")
        except ValueError:
            msg_args = args
            causes = []
        else:
            msg_args = args[:idx]
            cause_args = args[idx + 1 :]
            cause_args_conditions = cause_args[::2]
            cause_args_ids = cause_args[1::2]
            causes = list(zip(cause_args_conditions, cause_args_ids))

        msg = msg.format(*msg_args)

        # For variant formatting, we sometimes have to construct specs
        # to format values properly. Find/replace all occurances of
        # Spec(...) with the string representation of the spec mentioned
        specs_to_construct = re.findall(r"Spec\(([^)]*)\)", msg)
        for spec_str in specs_to_construct:
            msg = msg.replace("Spec(%s)" % spec_str, str(spack.spec.Spec(spec_str)))

        for cause in set(causes):
            for c in self.get_cause_tree(cause):
                msg += f"\n{c}"

        return msg

    def message(self, errors) -> str:
        messages = [
            f"  {idx+1: 2}. {self.handle_error(msg, *args)}"
            for idx, (_, msg, args) in enumerate(errors)
        ]
        header = "concretization failed for the following reasons:\n"
        return "\n".join([header] + messages)

    def raise_if_errors(self):
        initial_error_args = extract_args(self.model, "error")
        if not initial_error_args:
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

        # No choices so there will be only one model
        error_args = extract_args(self.full_model, "error")
        errors = sorted(
            [(int(priority), msg, args) for priority, msg, *args in error_args], reverse=True
        )
        try:
            msg = self.message(errors)
        except Exception as e:
            msg = (
                f"unexpected error during concretization [{str(e)}]. "
                f"Please report a bug at https://github.com/spack/spack/issues"
            )
            raise spack.error.SpackError(msg)
        raise UnsatisfiableSpecError(msg)


class RequirementRule(NamedTuple):
    """Data class to collect information on a requirement"""

    pkg_name: str
    policy: str
    requirements: List["spack.spec.Spec"]
    condition: "spack.spec.Spec"
    kind: RequirementKind
    message: Optional[str]


class KnownCompiler(NamedTuple):
    """Data class to collect information on compilers"""

    spec: "spack.spec.Spec"
    os: str
    target: str
    available: bool
    compiler_obj: Optional["spack.compiler.Compiler"]

    def _key(self):
        return self.spec, self.os, self.target

    def __eq__(self, other: object):
        if not isinstance(other, KnownCompiler):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())


class PyclingoDriver:
    def __init__(self, cores=True):
        """Driver for the Python clingo interface.

        Arguments:
            cores (bool): whether to generate unsatisfiable cores for better
                error reporting.
        """
        self.cores = cores
        # This attribute will be reset at each call to solve
        self.control = None

    def solve(self, setup, specs, reuse=None, output=None, control=None, allow_deprecated=False):
        """Set up the input and solve for dependencies of ``specs``.

        Arguments:
            setup (SpackSolverSetup): An object to set up the ASP problem.
            specs (list): List of ``Spec`` objects to solve for.
            reuse (None or list): list of concrete specs that can be reused
            output (None or OutputConfiguration): configuration object to set
                the output of this solve.
            control (clingo.Control): configuration for the solver. If None,
                default values will be used
            allow_deprecated: if True, allow deprecated versions in the solve

        Return:
            A tuple of the solve result, the timer for the different phases of the
            solve, and the internal statistics from clingo.
        """
        # avoid circular import
        import spack.bootstrap

        output = output or DEFAULT_OUTPUT_CONFIGURATION
        timer = spack.util.timer.Timer()

        # Initialize the control object for the solver
        self.control = control or default_clingo_control()

        # ensure core deps are present on Windows
        # needs to modify active config scope, so cannot be run within
        # bootstrap config scope
        if sys.platform == "win32":
            tty.debug("Ensuring basic dependencies {win-sdk, wgl} available")
            spack.bootstrap.core.ensure_winsdk_external_or_raise()

        timer.start("setup")
        asp_problem = setup.setup(specs, reuse=reuse, allow_deprecated=allow_deprecated)
        if output.out is not None:
            output.out.write(asp_problem)
        if output.setup_only:
            return Result(specs), None, None
        timer.stop("setup")

        timer.start("load")
        # Add the problem instance
        self.control.add("base", [], asp_problem)
        # Load the file itself
        parent_dir = os.path.dirname(__file__)
        self.control.load(os.path.join(parent_dir, "concretize.lp"))
        self.control.load(os.path.join(parent_dir, "heuristic.lp"))
        if spack.config.CONFIG.get("concretizer:duplicates:strategy", "none") != "none":
            self.control.load(os.path.join(parent_dir, "heuristic_separate.lp"))
        self.control.load(os.path.join(parent_dir, "display.lp"))
        if not setup.concretize_everything:
            self.control.load(os.path.join(parent_dir, "when_possible.lp"))

        # Binary compatibility is based on libc on Linux, and on the os tag elsewhere
        if using_libc_compatibility():
            self.control.load(os.path.join(parent_dir, "libc_compatibility.lp"))
        else:
            self.control.load(os.path.join(parent_dir, "os_compatibility.lp"))

        timer.stop("load")

        # Grounding is the first step in the solve -- it turns our facts
        # and first-order logic rules into propositional logic.
        timer.start("ground")
        self.control.ground([("base", [])])
        timer.stop("ground")

        # With a grounded program, we can run the solve.
        models = []  # stable models if things go well
        cores = []  # unsatisfiable cores if they do not

        def on_model(model):
            models.append((model.cost, model.symbols(shown=True, terms=True)))

        solve_kwargs = {
            "assumptions": setup.assumptions,
            "on_model": on_model,
            "on_core": cores.append,
        }

        if clingo_cffi():
            solve_kwargs["on_unsat"] = cores.append

        timer.start("solve")
        solve_result = self.control.solve(**solve_kwargs)
        timer.stop("solve")

        # once done, construct the solve result
        result = Result(specs)
        result.satisfiable = solve_result.satisfiable

        if result.satisfiable:
            # get the best model
            builder = SpecBuilder(specs, hash_lookup=setup.reusable_and_possible)
            min_cost, best_model = min(models)

            # first check for errors
            error_handler = ErrorHandler(best_model)
            error_handler.raise_if_errors()

            # build specs from spec attributes in the model
            spec_attrs = [(name, tuple(rest)) for name, *rest in extract_args(best_model, "attr")]
            answers = builder.build_specs(spec_attrs)

            # add best spec to the results
            result.answers.append((list(min_cost), 0, answers))

            # get optimization criteria
            criteria_args = extract_args(best_model, "opt_criterion")
            result.criteria = build_criteria_names(min_cost, criteria_args)

            # record the number of models the solver considered
            result.nmodels = len(models)

            # record the possible dependencies in the solve
            result.possible_dependencies = setup.pkgs

        elif cores:
            result.control = self.control
            result.cores.extend(cores)

        if output.timers:
            timer.write_tty()
            print()

        if output.stats:
            print("Statistics:")
            pprint.pprint(self.control.statistics)

        result.raise_if_unsat()

        if result.satisfiable and result.unsolved_specs and setup.concretize_everything:
            unsolved_str = Result.format_unsolved(result.unsolved_specs)
            raise InternalConcretizerError(
                "Internal Spack error: the solver completed but produced specs"
                " that do not satisfy the request. Please report a bug at "
                f"https://github.com/spack/spack/issues\n\t{unsolved_str}"
            )

        return result, timer, self.control.statistics


class ConcreteSpecsByHash(collections.abc.Mapping):
    """Mapping containing concrete specs keyed by DAG hash.

    The mapping is ensured to be consistent, i.e. if a spec in the mapping has a dependency with
    hash X, it is ensured to be the same object in memory as the spec keyed by X.
    """

    def __init__(self) -> None:
        self.data: Dict[str, spack.spec.Spec] = {}
        self.explicit: Set[str] = set()

    def __getitem__(self, dag_hash: str) -> spack.spec.Spec:
        return self.data[dag_hash]

    def explicit_items(self) -> Iterator[Tuple[str, spack.spec.Spec]]:
        """Iterate on items that have been added explicitly, and not just as a dependency
        of other nodes.
        """
        for h, s in self.items():
            # We need to make an exception for gcc-runtime, until we can splice it.
            if h in self.explicit or s.name == "gcc-runtime":
                yield h, s

    def add(self, spec: spack.spec.Spec) -> bool:
        """Adds a new concrete spec to the mapping. Returns True if the spec was just added,
        False if the spec was already in the mapping.

        Calling this function marks the spec as added explicitly.

        Args:
            spec: spec to be added

        Raises:
            ValueError: if the spec is not concrete
        """
        if not spec.concrete:
            msg = (
                f"trying to store the non-concrete spec '{spec}' in a container "
                f"that only accepts concrete"
            )
            raise ValueError(msg)

        dag_hash = spec.dag_hash()
        self.explicit.add(dag_hash)
        if dag_hash in self.data:
            return False

        # Here we need to iterate on the input and rewire the copy.
        self.data[spec.dag_hash()] = spec.copy(deps=False)
        nodes_to_reconstruct = [spec]

        while nodes_to_reconstruct:
            input_parent = nodes_to_reconstruct.pop()
            container_parent = self.data[input_parent.dag_hash()]

            for edge in input_parent.edges_to_dependencies():
                input_child = edge.spec
                container_child = self.data.get(input_child.dag_hash())
                # Copy children that don't exist yet
                if container_child is None:
                    container_child = input_child.copy(deps=False)
                    self.data[input_child.dag_hash()] = container_child
                    nodes_to_reconstruct.append(input_child)

                # Rewire edges
                container_parent.add_dependency_edge(
                    dependency_spec=container_child, depflag=edge.depflag, virtuals=edge.virtuals
                )
        return True

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


# types for condition caching in solver setup
ConditionSpecKey = Tuple[str, Optional[TransformFunction]]
ConditionIdFunctionPair = Tuple[int, List[AspFunction]]
ConditionSpecCache = Dict[str, Dict[ConditionSpecKey, ConditionIdFunctionPair]]


class SpackSolverSetup:
    """Class to set up and run a Spack concretization solve."""

    def __init__(self, tests: bool = False):
        # these are all initialized in setup()
        self.gen: "ProblemInstanceBuilder" = ProblemInstanceBuilder()
        self.possible_virtuals: Set[str] = set()

        self.assumptions: List[Tuple["clingo.Symbol", bool]] = []  # type: ignore[name-defined]
        self.declared_versions: Dict[str, List[DeclaredVersion]] = collections.defaultdict(list)
        self.possible_versions: Dict[str, Set[GitOrStandardVersion]] = collections.defaultdict(set)
        self.deprecated_versions: Dict[str, Set[GitOrStandardVersion]] = collections.defaultdict(
            set
        )

        self.possible_compilers: List = []
        self.possible_oses: Set = set()
        self.variant_values_from_specs: Set = set()
        self.version_constraints: Set = set()
        self.target_constraints: Set = set()
        self.default_targets: List = []
        self.compiler_version_constraints: Set = set()
        self.post_facts: List = []

        self.reusable_and_possible: ConcreteSpecsByHash = ConcreteSpecsByHash()

        self._id_counter: Iterator[int] = itertools.count()
        self._trigger_cache: ConditionSpecCache = collections.defaultdict(dict)
        self._effect_cache: ConditionSpecCache = collections.defaultdict(dict)

        # Caches to optimize the setup phase of the solver
        self.target_specs_cache = None

        # whether to add installed/binary hashes to the solve
        self.tests = tests

        # If False allows for input specs that are not solved
        self.concretize_everything = True

        # Set during the call to setup
        self.pkgs: Set[str] = set()
        self.explicitly_required_namespaces: Dict[str, str] = {}

        # list of unique libc specs targeted by compilers (or an educated guess if no compiler)
        self.libcs: List[spack.spec.Spec] = []

    def pkg_version_rules(self, pkg):
        """Output declared versions of a package.

        This uses self.declared_versions so that we include any versions
        that arise from a spec.
        """

        def key_fn(version):
            # Origins are sorted by "provenance" first, see the Provenance enumeration above
            return version.origin, version.idx

        if isinstance(pkg, str):
            pkg = self.pkg_class(pkg)

        declared_versions = self.declared_versions[pkg.name]
        partially_sorted_versions = sorted(set(declared_versions), key=key_fn)

        most_to_least_preferred = []
        for _, group in itertools.groupby(partially_sorted_versions, key=key_fn):
            most_to_least_preferred.extend(
                list(sorted(group, reverse=True, key=lambda x: vn.ver(x.version)))
            )

        for weight, declared_version in enumerate(most_to_least_preferred):
            self.gen.fact(
                fn.pkg_fact(
                    pkg.name,
                    fn.version_declared(
                        declared_version.version, weight, str(declared_version.origin)
                    ),
                )
            )

        # Declare deprecated versions for this package, if any
        deprecated = self.deprecated_versions[pkg.name]
        for v in sorted(deprecated):
            self.gen.fact(fn.pkg_fact(pkg.name, fn.deprecated_version(v)))

    def spec_versions(self, spec):
        """Return list of clauses expressing spec's version constraints."""
        spec = specify(spec)
        msg = "Internal Error: spec with no name occured. Please report to the spack maintainers."
        assert spec.name, msg

        if spec.concrete:
            return [fn.attr("version", spec.name, spec.version)]

        if spec.versions == vn.any_version:
            return []

        # record all version constraints for later
        self.version_constraints.add((spec.name, spec.versions))
        return [fn.attr("node_version_satisfies", spec.name, spec.versions)]

    def target_ranges(self, spec, single_target_fn):
        target = spec.architecture.target

        # Check if the target is a concrete target
        if str(target) in archspec.cpu.TARGETS:
            return [single_target_fn(spec.name, target)]

        self.target_constraints.add(target)
        return [fn.attr("node_target_satisfies", spec.name, target)]

    def conflict_rules(self, pkg):
        for when_spec, conflict_specs in pkg.conflicts.items():
            when_spec_msg = "conflict constraint %s" % str(when_spec)
            when_spec_id = self.condition(when_spec, name=pkg.name, msg=when_spec_msg)

            for conflict_spec, conflict_msg in conflict_specs:
                conflict_spec = spack.spec.Spec(conflict_spec)
                if conflict_msg is None:
                    conflict_msg = f"{pkg.name}: "
                    if when_spec == spack.spec.Spec():
                        conflict_msg += f"conflicts with '{conflict_spec}'"
                    else:
                        conflict_msg += f"'{conflict_spec}' conflicts with '{when_spec}'"

                spec_for_msg = conflict_spec
                if conflict_spec == spack.spec.Spec():
                    spec_for_msg = spack.spec.Spec(pkg.name)
                conflict_spec_msg = f"conflict is triggered when {str(spec_for_msg)}"
                conflict_spec_id = self.condition(
                    conflict_spec, name=conflict_spec.name or pkg.name, msg=conflict_spec_msg
                )
                self.gen.fact(
                    fn.pkg_fact(
                        pkg.name, fn.conflict(conflict_spec_id, when_spec_id, conflict_msg)
                    )
                )
                self.gen.newline()

    def package_languages(self, pkg):
        for when_spec, languages in pkg.languages.items():
            condition_msg = f"{pkg.name} needs the {', '.join(sorted(languages))} language"
            if when_spec != spack.spec.Spec():
                condition_msg += f" when {when_spec}"
            condition_id = self.condition(when_spec, name=pkg.name, msg=condition_msg)
            for language in sorted(languages):
                self.gen.fact(fn.pkg_fact(pkg.name, fn.language(condition_id, language)))
        self.gen.newline()

    def config_compatible_os(self):
        """Facts about compatible os's specified in configs"""
        self.gen.h2("Compatible OS from concretizer config file")
        os_data = spack.config.get("concretizer:os_compatible", {})
        for recent, reusable in os_data.items():
            for old in reusable:
                self.gen.fact(fn.os_compatible(recent, old))
                self.gen.newline()

    def compiler_facts(self):
        """Facts about available compilers."""

        self.gen.h2("Available compilers")
        for compiler_id, compiler in enumerate(self.possible_compilers):
            self.gen.fact(fn.compiler_id(compiler_id))
            self.gen.fact(fn.compiler_name(compiler_id, compiler.spec.name))
            self.gen.fact(fn.compiler_version(compiler_id, compiler.spec.version))

            if compiler.os:
                self.gen.fact(fn.compiler_os(compiler_id, compiler.os))

            if compiler.target is not None:
                self.gen.fact(fn.compiler_target(compiler_id, compiler.target))

            if compiler.compiler_obj is not None:
                c = compiler.compiler_obj
                for flag_type, flags in c.flags.items():
                    for flag in flags:
                        self.gen.fact(fn.compiler_flag(compiler_id, flag_type, flag))

            if compiler.available:
                self.gen.fact(fn.compiler_available(compiler_id))

            self.gen.fact(fn.compiler_weight(compiler_id, compiler_id))
            self.gen.newline()

    def package_requirement_rules(self, pkg):
        parser = RequirementParser(spack.config.CONFIG)
        self.emit_facts_from_requirement_rules(parser.rules(pkg))

    def pkg_rules(self, pkg, tests):
        pkg = self.pkg_class(pkg)

        # Namespace of the package
        self.gen.fact(fn.pkg_fact(pkg.name, fn.namespace(pkg.namespace)))

        # versions
        self.pkg_version_rules(pkg)
        self.gen.newline()

        # languages
        self.package_languages(pkg)

        # variants
        self.variant_rules(pkg)

        # conflicts
        self.conflict_rules(pkg)

        # virtuals
        self.package_provider_rules(pkg)

        # dependencies
        self.package_dependencies_rules(pkg)

        # virtual preferences
        self.virtual_preferences(
            pkg.name,
            lambda v, p, i: self.gen.fact(fn.pkg_fact(pkg.name, fn.provider_preference(v, p, i))),
        )

        self.package_requirement_rules(pkg)

        # trigger and effect tables
        self.trigger_rules()
        self.effect_rules()

    def trigger_rules(self):
        """Flushes all the trigger rules collected so far, and clears the cache."""
        if not self._trigger_cache:
            return

        self.gen.h2("Trigger conditions")
        for name in self._trigger_cache:
            cache = self._trigger_cache[name]
            for (spec_str, _), (trigger_id, requirements) in cache.items():
                self.gen.fact(fn.pkg_fact(name, fn.trigger_id(trigger_id)))
                self.gen.fact(fn.pkg_fact(name, fn.trigger_msg(spec_str)))
                for predicate in requirements:
                    self.gen.fact(fn.condition_requirement(trigger_id, *predicate.args))
                self.gen.newline()
        self._trigger_cache.clear()

    def effect_rules(self):
        """Flushes all the effect rules collected so far, and clears the cache."""
        if not self._effect_cache:
            return

        self.gen.h2("Imposed requirements")
        for name in self._effect_cache:
            cache = self._effect_cache[name]
            for (spec_str, _), (effect_id, requirements) in cache.items():
                self.gen.fact(fn.pkg_fact(name, fn.effect_id(effect_id)))
                self.gen.fact(fn.pkg_fact(name, fn.effect_msg(spec_str)))
                for predicate in requirements:
                    self.gen.fact(fn.imposed_constraint(effect_id, *predicate.args))
                self.gen.newline()
        self._effect_cache.clear()

    def variant_rules(self, pkg):
        for name, entry in sorted(pkg.variants.items()):
            variant, when = entry

            if spack.spec.Spec() in when:
                # unconditional variant
                self.gen.fact(fn.pkg_fact(pkg.name, fn.variant(name)))
            else:
                # conditional variant
                for w in when:
                    msg = "%s has variant %s" % (pkg.name, name)
                    if str(w):
                        msg += " when %s" % w

                    cond_id = self.condition(w, name=pkg.name, msg=msg)
                    self.gen.fact(fn.pkg_fact(pkg.name, fn.conditional_variant(cond_id, name)))

            single_value = not variant.multi
            if single_value:
                self.gen.fact(fn.pkg_fact(pkg.name, fn.variant_single_value(name)))
                self.gen.fact(
                    fn.pkg_fact(
                        pkg.name, fn.variant_default_value_from_package_py(name, variant.default)
                    )
                )
            else:
                spec_variant = variant.make_default()
                defaults = spec_variant.value
                for val in sorted(defaults):
                    self.gen.fact(
                        fn.pkg_fact(pkg.name, fn.variant_default_value_from_package_py(name, val))
                    )

            values = variant.values
            if values is None:
                values = []
            elif isinstance(values, spack.variant.DisjointSetsOfValues):
                union = set()
                # Encode the disjoint sets in the logic program
                for sid, s in enumerate(values.sets):
                    for value in s:
                        self.gen.fact(
                            fn.pkg_fact(
                                pkg.name, fn.variant_value_from_disjoint_sets(name, value, sid)
                            )
                        )
                    union.update(s)
                values = union

            # make sure that every variant has at least one possible value
            if not values:
                values = [variant.default]

            for value in sorted(values):
                if getattr(value, "when", True) is not True:  # when=True means unconditional
                    condition_spec = spack.spec.Spec("{0}={1}".format(name, value))
                    if value.when is False:
                        # This value is a conflict
                        # Cannot just prevent listing it as a possible value because it could
                        # also come in as a possible value from the command line
                        trigger_id = self.condition(
                            condition_spec,
                            name=pkg.name,
                            msg="invalid variant value {0}={1}".format(name, value),
                        )
                        constraint_id = self.condition(
                            spack.spec.Spec(),
                            name=pkg.name,
                            msg="empty (total) conflict constraint",
                        )
                        msg = "variant {0}={1} is conditionally disabled".format(name, value)
                        self.gen.fact(
                            fn.pkg_fact(pkg.name, fn.conflict(trigger_id, constraint_id, msg))
                        )
                    else:
                        imposed = spack.spec.Spec(value.when)
                        imposed.name = pkg.name

                        self.condition(
                            required_spec=condition_spec,
                            imposed_spec=imposed,
                            name=pkg.name,
                            msg="%s variant %s value %s when %s" % (pkg.name, name, value, when),
                        )
                self.gen.fact(fn.pkg_fact(pkg.name, fn.variant_possible_value(name, value)))

            if variant.sticky:
                self.gen.fact(fn.pkg_fact(pkg.name, fn.variant_sticky(name)))

            self.gen.newline()

    def _get_condition_id(
        self,
        named_cond: spack.spec.Spec,
        cache: ConditionSpecCache,
        body: bool,
        transform: Optional[TransformFunction] = None,
    ) -> int:
        """Get the id for one half of a condition (either a trigger or an imposed constraint).

        Construct a key from the condition spec and any associated transformation, and
        cache the ASP functions that they imply. The saved functions will be output
        later in ``trigger_rules()`` and ``effect_rules()``.

        Returns:
            The id of the cached trigger or effect.

        """
        pkg_cache = cache[named_cond.name]

        named_cond_key = (str(named_cond), transform)
        result = pkg_cache.get(named_cond_key)
        if result:
            return result[0]

        cond_id = next(self._id_counter)
        requirements = self.spec_clauses(named_cond, body=body)
        if transform:
            requirements = transform(named_cond, requirements)
        pkg_cache[named_cond_key] = (cond_id, requirements)

        return cond_id

    def condition(
        self,
        required_spec: spack.spec.Spec,
        imposed_spec: Optional[spack.spec.Spec] = None,
        name: Optional[str] = None,
        msg: Optional[str] = None,
        transform_required: Optional[TransformFunction] = None,
        transform_imposed: Optional[TransformFunction] = remove_node,
    ):
        """Generate facts for a dependency or virtual provider condition.

        Arguments:
            required_spec: the constraints that triggers this condition
            imposed_spec: the constraints that are imposed when this condition is triggered
            name: name for `required_spec` (required if required_spec is anonymous, ignored if not)
            msg: description of the condition
            transform_required: transformation applied to facts from the required spec. Defaults
                to leave facts as they are.
            transform_imposed: transformation applied to facts from the imposed spec. Defaults
                to removing "node" and "virtual_node" facts.
        Returns:
            int: id of the condition created by this function
        """
        name = required_spec.name or name
        if not name:
            raise ValueError(f"Must provide a name for anonymous condition: '{required_spec}'")

        with spec_with_name(required_spec, name):
            # Check if we can emit the requirements before updating the condition ID counter.
            # In this way, if a condition can't be emitted but the exception is handled in the
            # caller, we won't emit partial facts.

            condition_id = next(self._id_counter)
            self.gen.fact(fn.pkg_fact(required_spec.name, fn.condition(condition_id)))
            self.gen.fact(fn.condition_reason(condition_id, msg))

            trigger_id = self._get_condition_id(
                required_spec, cache=self._trigger_cache, body=True, transform=transform_required
            )
            self.gen.fact(
                fn.pkg_fact(required_spec.name, fn.condition_trigger(condition_id, trigger_id))
            )

            if not imposed_spec:
                return condition_id

            effect_id = self._get_condition_id(
                imposed_spec, cache=self._effect_cache, body=False, transform=transform_imposed
            )
            self.gen.fact(
                fn.pkg_fact(required_spec.name, fn.condition_effect(condition_id, effect_id))
            )

            return condition_id

    def impose(self, condition_id, imposed_spec, node=True, name=None, body=False):
        imposed_constraints = self.spec_clauses(imposed_spec, body=body, required_from=name)
        for pred in imposed_constraints:
            # imposed "node"-like conditions are no-ops
            if not node and pred.args[0] in ("node", "virtual_node"):
                continue
            self.gen.fact(fn.imposed_constraint(condition_id, *pred.args))

    def package_provider_rules(self, pkg):
        for vpkg_name in pkg.provided_virtual_names():
            if vpkg_name not in self.possible_virtuals:
                continue
            self.gen.fact(fn.pkg_fact(pkg.name, fn.possible_provider(vpkg_name)))

        for when, provided in pkg.provided.items():
            for vpkg in provided:
                if vpkg.name not in self.possible_virtuals:
                    continue

                msg = f"{pkg.name} provides {vpkg} when {when}"
                condition_id = self.condition(when, vpkg, pkg.name, msg)
                self.gen.fact(
                    fn.pkg_fact(when.name, fn.provider_condition(condition_id, vpkg.name))
                )
            self.gen.newline()

        for when, sets_of_virtuals in pkg.provided_together.items():
            condition_id = self.condition(
                when, name=pkg.name, msg="Virtuals are provided together"
            )
            for set_id, virtuals_together in enumerate(sets_of_virtuals):
                for name in virtuals_together:
                    self.gen.fact(
                        fn.pkg_fact(pkg.name, fn.provided_together(condition_id, set_id, name))
                    )
            self.gen.newline()

    def package_dependencies_rules(self, pkg):
        """Translate 'depends_on' directives into ASP logic."""
        for cond, deps_by_name in sorted(pkg.dependencies.items()):
            for _, dep in sorted(deps_by_name.items()):
                depflag = dep.depflag
                # Skip test dependencies if they're not requested
                if not self.tests:
                    depflag &= ~dt.TEST

                # ... or if they are requested only for certain packages
                elif not isinstance(self.tests, bool) and pkg.name not in self.tests:
                    depflag &= ~dt.TEST

                # if there are no dependency types to be considered
                # anymore, don't generate the dependency
                if not depflag:
                    continue

                msg = f"{pkg.name} depends on {dep.spec}"
                if cond != spack.spec.Spec():
                    msg += f" when {cond}"
                else:
                    pass

                def track_dependencies(input_spec, requirements):
                    return requirements + [fn.attr("track_dependencies", input_spec.name)]

                def dependency_holds(input_spec, requirements):
                    return remove_node(input_spec, requirements) + [
                        fn.attr(
                            "dependency_holds", pkg.name, input_spec.name, dt.flag_to_string(t)
                        )
                        for t in dt.ALL_FLAGS
                        if t & depflag
                    ]

                self.condition(
                    cond,
                    dep.spec,
                    name=pkg.name,
                    msg=msg,
                    transform_required=track_dependencies,
                    transform_imposed=dependency_holds,
                )

                self.gen.newline()

    def virtual_preferences(self, pkg_name, func):
        """Call func(vspec, provider, i) for each of pkg's provider prefs."""
        config = spack.config.get("packages")
        pkg_prefs = config.get(pkg_name, {}).get("providers", {})
        for vspec, providers in pkg_prefs.items():
            if vspec not in self.possible_virtuals:
                continue

            for i, provider in enumerate(providers):
                provider_name = spack.spec.Spec(provider).name
                func(vspec, provider_name, i)
            self.gen.newline()

    def provider_defaults(self):
        self.gen.h2("Default virtual providers")
        self.virtual_preferences(
            "all", lambda v, p, i: self.gen.fact(fn.default_provider_preference(v, p, i))
        )

    def provider_requirements(self):
        self.gen.h2("Requirements on virtual providers")
        parser = RequirementParser(spack.config.CONFIG)
        for virtual_str in sorted(self.possible_virtuals):
            rules = parser.rules_from_virtual(virtual_str)
            if rules:
                self.emit_facts_from_requirement_rules(rules)
                self.trigger_rules()
                self.effect_rules()

    def emit_facts_from_requirement_rules(self, rules: List[RequirementRule]):
        """Generate facts to enforce requirements.

        Args:
            rules: rules for which we want facts to be emitted
        """
        for requirement_grp_id, rule in enumerate(rules):
            virtual = rule.kind == RequirementKind.VIRTUAL

            pkg_name, policy, requirement_grp = rule.pkg_name, rule.policy, rule.requirements
            requirement_weight = 0

            # Write explicitly if a requirement is conditional or not
            if rule.condition != spack.spec.Spec():
                msg = f"condition to activate requirement {requirement_grp_id}"
                try:
                    main_condition_id = self.condition(rule.condition, name=pkg_name, msg=msg)
                except Exception as e:
                    if rule.kind != RequirementKind.DEFAULT:
                        raise RuntimeError(
                            "cannot emit requirements for the solver: " + str(e)
                        ) from e
                    continue

                self.gen.fact(
                    fn.requirement_conditional(pkg_name, requirement_grp_id, main_condition_id)
                )

            self.gen.fact(fn.requirement_group(pkg_name, requirement_grp_id))
            self.gen.fact(fn.requirement_policy(pkg_name, requirement_grp_id, policy))
            if rule.message:
                self.gen.fact(fn.requirement_message(pkg_name, requirement_grp_id, rule.message))
            self.gen.newline()

            for input_spec in requirement_grp:
                spec = spack.spec.Spec(input_spec)
                if not spec.name:
                    spec.name = pkg_name
                spec.attach_git_version_lookup()

                when_spec = spec
                if virtual:
                    when_spec = spack.spec.Spec(pkg_name)

                try:
                    # With virtual we want to emit "node" and "virtual_node" in imposed specs
                    transform: Optional[TransformFunction] = remove_node
                    if virtual:
                        transform = None

                    member_id = self.condition(
                        required_spec=when_spec,
                        imposed_spec=spec,
                        name=pkg_name,
                        transform_imposed=transform,
                        msg=f"{input_spec} is a requirement for package {pkg_name}",
                    )
                except Exception as e:
                    # Do not raise if the rule comes from the 'all' subsection, since usability
                    # would be impaired. If a rule does not apply for a specific package, just
                    # discard it.
                    if rule.kind != RequirementKind.DEFAULT:
                        raise RuntimeError(
                            "cannot emit requirements for the solver: " + str(e)
                        ) from e
                    continue

                self.gen.fact(fn.requirement_group_member(member_id, pkg_name, requirement_grp_id))
                self.gen.fact(fn.requirement_has_weight(member_id, requirement_weight))
                self.gen.newline()
                requirement_weight += 1

    def external_packages(self):
        """Facts on external packages, from packages.yaml and implicit externals."""
        packages_yaml = _external_config_with_implicit_externals(spack.config.CONFIG)

        self.gen.h1("External packages")
        spec_filters = []
        concretizer_yaml = spack.config.get("concretizer")
        reuse_yaml = concretizer_yaml.get("reuse")
        if isinstance(reuse_yaml, typing.Mapping):
            default_include = reuse_yaml.get("include", [])
            default_exclude = reuse_yaml.get("exclude", [])
            libc_externals = list(all_libcs())
            for source in reuse_yaml.get("from", []):
                if source["type"] != "external":
                    continue

                include = source.get("include", default_include)
                if include:
                    # Since libcs are implicit externals, we need to implicitly include them
                    include = include + libc_externals
                exclude = source.get("exclude", default_exclude)
                spec_filters.append(
                    SpecFilter(
                        factory=lambda: [],
                        is_usable=lambda x: True,
                        include=include,
                        exclude=exclude,
                    )
                )

        for pkg_name, data in packages_yaml.items():
            if pkg_name == "all":
                continue

            # This package does not appear in any repository
            if pkg_name not in spack.repo.PATH:
                continue

            # Check if the external package is buildable. If it is
            # not then "external(<pkg>)" is a fact, unless we can
            # reuse an already installed spec.
            external_buildable = data.get("buildable", True)
            if not external_buildable:
                self.gen.fact(fn.buildable_false(pkg_name))

            # Read a list of all the specs for this package
            externals = data.get("externals", [])
            candidate_specs = [
                spack.spec.parse_with_version_concrete(x["spec"]) for x in externals
            ]

            external_specs = []
            if spec_filters:
                for current_filter in spec_filters:
                    current_filter.factory = lambda: candidate_specs
                    external_specs.extend(current_filter.selected_specs())
            else:
                external_specs.extend(candidate_specs)

            # Order the external versions to prefer more recent versions
            # even if specs in packages.yaml are not ordered that way
            external_versions = [
                (x.version, external_id) for external_id, x in enumerate(external_specs)
            ]
            external_versions = [
                (v, idx, external_id)
                for idx, (v, external_id) in enumerate(sorted(external_versions, reverse=True))
            ]
            for version, idx, external_id in external_versions:
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=version, idx=idx, origin=Provenance.EXTERNAL)
                )

            # Declare external conditions with a local index into packages.yaml
            for local_idx, spec in enumerate(external_specs):
                msg = "%s available as external when satisfying %s" % (spec.name, spec)

                def external_imposition(input_spec, requirements):
                    return requirements + [
                        fn.attr("external_conditions_hold", input_spec.name, local_idx)
                    ]

                self.condition(spec, spec, msg=msg, transform_imposed=external_imposition)
                self.possible_versions[spec.name].add(spec.version)
                self.gen.newline()

            self.trigger_rules()
            self.effect_rules()

    def preferred_variants(self, pkg_name):
        """Facts on concretization preferences, as read from packages.yaml"""
        preferences = spack.package_prefs.PackagePrefs
        preferred_variants = preferences.preferred_variants(pkg_name)
        if not preferred_variants:
            return

        for variant_name in sorted(preferred_variants):
            variant = preferred_variants[variant_name]
            values = variant.value

            if not isinstance(values, tuple):
                values = (values,)

            # perform validation of the variant and values
            spec = spack.spec.Spec(pkg_name)
            try:
                spec.update_variant_validate(variant_name, values)
            except (spack.variant.InvalidVariantValueError, KeyError, ValueError) as e:
                tty.debug(
                    f"[SETUP]: rejected {str(variant)} as a preference for {pkg_name}: {str(e)}"
                )
                continue

            for value in values:
                self.variant_values_from_specs.add((pkg_name, variant.name, value))
                self.gen.fact(
                    fn.variant_default_value_from_packages_yaml(pkg_name, variant.name, value)
                )

    def target_preferences(self):
        key_fn = spack.package_prefs.PackagePrefs("all", "target")

        if not self.target_specs_cache:
            self.target_specs_cache = [
                spack.spec.Spec("target={0}".format(target_name))
                for _, target_name in self.default_targets
            ]

        package_targets = self.target_specs_cache[:]
        package_targets.sort(key=key_fn)
        for i, preferred in enumerate(package_targets):
            self.gen.fact(fn.target_weight(str(preferred.architecture.target), i))

    def spec_clauses(
        self,
        spec: spack.spec.Spec,
        *,
        body: bool = False,
        transitive: bool = True,
        expand_hashes: bool = False,
        concrete_build_deps=False,
        required_from: Optional[str] = None,
    ) -> List[AspFunction]:
        """Wrap a call to `_spec_clauses()` into a try/except block with better error handling.

        Arguments are as for ``_spec_clauses()`` except ``required_from``.

        Arguments:
            required_from: name of package that caused this call.
        """
        try:
            clauses = self._spec_clauses(
                spec,
                body=body,
                transitive=transitive,
                expand_hashes=expand_hashes,
                concrete_build_deps=concrete_build_deps,
            )
        except RuntimeError as exc:
            msg = str(exc)
            if required_from:
                msg += f" [required from package '{required_from}']"
            raise RuntimeError(msg)
        return clauses

    def _spec_clauses(
        self,
        spec: spack.spec.Spec,
        *,
        body: bool = False,
        transitive: bool = True,
        expand_hashes: bool = False,
        concrete_build_deps: bool = False,
    ) -> List[AspFunction]:
        """Return a list of clauses for a spec mandates are true.

        Arguments:
            spec: the spec to analyze
            body: if True, generate clauses to be used in rule bodies (final values) instead
                of rule heads (setters).
            transitive: if False, don't generate clauses from dependencies (default True)
            expand_hashes: if True, descend into hashes of concrete specs (default False)
            concrete_build_deps: if False, do not include pure build deps of concrete specs
                (as they have no effect on runtime constraints)

        Normally, if called with ``transitive=True``, ``spec_clauses()`` just generates
        hashes for the dependency requirements of concrete specs. If ``expand_hashes``
        is ``True``, we'll *also* output all the facts implied by transitive hashes,
        which are redundant during a solve but useful outside of one (e.g.,
        for spec ``diff``).
        """
        clauses = []

        f: Union[Type[_Head], Type[_Body]] = _Body if body else _Head

        if spec.name:
            clauses.append(f.node(spec.name) if not spec.virtual else f.virtual_node(spec.name))

        clauses.extend(self.spec_versions(spec))

        # seed architecture at the root (we'll propagate later)
        # TODO: use better semantics.
        arch = spec.architecture
        if arch:
            if arch.platform:
                clauses.append(f.node_platform(spec.name, arch.platform))
            if arch.os:
                clauses.append(f.node_os(spec.name, arch.os))
            if arch.target:
                clauses.extend(self.target_ranges(spec, f.node_target))

        # variants
        for vname, variant in sorted(spec.variants.items()):
            values = variant.value
            if not isinstance(values, (list, tuple)):
                values = [values]

            for value in values:
                # * is meaningless for concretization -- just for matching
                if value == "*":
                    continue

                # validate variant value only if spec not concrete
                if not spec.concrete:
                    reserved_names = spack.directives.reserved_names
                    if not spec.virtual and vname not in reserved_names:
                        pkg_cls = self.pkg_class(spec.name)
                        try:
                            variant_def, _ = pkg_cls.variants[vname]
                        except KeyError:
                            msg = 'variant "{0}" not found in package "{1}"'
                            raise RuntimeError(msg.format(vname, spec.name))
                        else:
                            variant_def.validate_or_raise(
                                variant, spack.repo.PATH.get_pkg_class(spec.name)
                            )

                clauses.append(f.variant_value(spec.name, vname, value))

                if variant.propagate:
                    clauses.append(
                        f.variant_propagation_candidate(spec.name, vname, value, spec.name)
                    )

                # Tell the concretizer that this is a possible value for the
                # variant, to account for things like int/str values where we
                # can't enumerate the valid values
                self.variant_values_from_specs.add((spec.name, vname, value))

        # compiler and compiler version
        if spec.compiler:
            clauses.append(f.node_compiler(spec.name, spec.compiler.name))

            if spec.compiler.concrete:
                clauses.append(
                    f.node_compiler_version(spec.name, spec.compiler.name, spec.compiler.version)
                )

            elif spec.compiler.versions and spec.compiler.versions != vn.any_version:
                # The condition above emits a facts only if we have an actual constraint
                # on the compiler version, and avoids emitting them if any version is fine
                clauses.append(
                    fn.attr(
                        "node_compiler_version_satisfies",
                        spec.name,
                        spec.compiler.name,
                        spec.compiler.versions,
                    )
                )
                self.compiler_version_constraints.add(spec.compiler)

        # compiler flags
        for flag_type, flags in spec.compiler_flags.items():
            for flag in flags:
                clauses.append(f.node_flag(spec.name, flag_type, flag))
                clauses.append(f.node_flag_source(spec.name, flag_type, spec.name))
                if not spec.concrete and flag.propagate is True:
                    clauses.append(f.node_flag_propagate(spec.name, flag_type))

        # dependencies
        if spec.concrete:
            # older specs do not have package hashes, so we have to do this carefully
            package_hash = getattr(spec, "_package_hash", None)
            if package_hash:
                clauses.append(fn.attr("package_hash", spec.name, package_hash))
            clauses.append(fn.attr("hash", spec.name, spec.dag_hash()))

        edges = spec.edges_from_dependents()
        virtuals = [x for x in itertools.chain.from_iterable([edge.virtuals for edge in edges])]
        if not body:
            for virtual in virtuals:
                clauses.append(fn.attr("provider_set", spec.name, virtual))
                clauses.append(fn.attr("virtual_node", virtual))
        else:
            for virtual in virtuals:
                clauses.append(fn.attr("virtual_on_incoming_edges", spec.name, virtual))

        # add all clauses from dependencies
        if transitive:
            # TODO: Eventually distinguish 2 deps on the same pkg (build and link)
            for dspec in spec.edges_to_dependencies():
                dep = dspec.spec

                if spec.concrete:
                    # GCC runtime is solved again by clingo, even on concrete specs, to give
                    # the possibility to reuse specs built against a different runtime.
                    if dep.name == "gcc-runtime":
                        continue

                    # libc is also solved again by clingo, but in this case the compatibility
                    # is not encoded in the parent node - so we need to emit explicit facts
                    if "libc" in dspec.virtuals:
                        for libc in self.libcs:
                            if libc_is_compatible(libc, dep):
                                clauses.append(
                                    fn.attr("compatible_libc", spec.name, libc.name, libc.version)
                                )
                        continue

                    # We know dependencies are real for concrete specs. For abstract
                    # specs they just mean the dep is somehow in the DAG.
                    for dtype in dt.ALL_FLAGS:
                        if not dspec.depflag & dtype:
                            continue
                        # skip build dependencies of already-installed specs
                        if concrete_build_deps or dtype != dt.BUILD:
                            clauses.append(
                                fn.attr(
                                    "depends_on", spec.name, dep.name, dt.flag_to_string(dtype)
                                )
                            )
                            for virtual_name in dspec.virtuals:
                                clauses.append(
                                    fn.attr("virtual_on_edge", spec.name, dep.name, virtual_name)
                                )
                                clauses.append(fn.attr("virtual_node", virtual_name))

                    # imposing hash constraints for all but pure build deps of
                    # already-installed concrete specs.
                    if concrete_build_deps or dspec.depflag != dt.BUILD:
                        clauses.append(fn.attr("hash", dep.name, dep.dag_hash()))

                # if the spec is abstract, descend into dependencies.
                # if it's concrete, then the hashes above take care of dependency
                # constraints, but expand the hashes if asked for.
                if not spec.concrete or expand_hashes:
                    clauses.extend(
                        self._spec_clauses(
                            dep,
                            body=body,
                            expand_hashes=expand_hashes,
                            concrete_build_deps=concrete_build_deps,
                        )
                    )

        return clauses

    def define_package_versions_and_validate_preferences(
        self, possible_pkgs: Set[str], *, require_checksum: bool, allow_deprecated: bool
    ):
        """Declare any versions in specs not declared in packages."""
        packages_yaml = spack.config.get("packages")
        for pkg_name in possible_pkgs:
            pkg_cls = self.pkg_class(pkg_name)

            # All the versions from the corresponding package.py file. Since concepts
            # like being a "develop" version or being preferred exist only at a
            # package.py level, sort them in this partial list here
            package_py_versions = sorted(
                pkg_cls.versions.items(), key=_concretization_version_order, reverse=True
            )

            if require_checksum and pkg_cls.has_code:
                package_py_versions = [
                    x for x in package_py_versions if _is_checksummed_version(x)
                ]

            for idx, (v, version_info) in enumerate(package_py_versions):
                if version_info.get("deprecated", False):
                    self.deprecated_versions[pkg_name].add(v)
                    if not allow_deprecated:
                        continue

                self.possible_versions[pkg_name].add(v)
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=v, idx=idx, origin=Provenance.PACKAGE_PY)
                )

            if pkg_name not in packages_yaml or "version" not in packages_yaml[pkg_name]:
                continue

            version_defs: List[GitOrStandardVersion] = []

            for vstr in packages_yaml[pkg_name]["version"]:
                v = vn.ver(vstr)

                if isinstance(v, vn.GitVersion):
                    if not require_checksum or v.is_commit:
                        version_defs.append(v)
                else:
                    matches = [x for x in self.possible_versions[pkg_name] if x.satisfies(v)]
                    matches.sort(reverse=True)
                    if not matches:
                        raise spack.config.ConfigError(
                            f"Preference for version {v} does not match any known "
                            f"version of {pkg_name} (in its package.py or any external)"
                        )
                    version_defs.extend(matches)

            for weight, vdef in enumerate(llnl.util.lang.dedupe(version_defs)):
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=vdef, idx=weight, origin=Provenance.PACKAGES_YAML)
                )
                self.possible_versions[pkg_name].add(vdef)

    def define_ad_hoc_versions_from_specs(
        self, specs, origin, *, allow_deprecated: bool, require_checksum: bool
    ):
        """Add concrete versions to possible versions from lists of CLI/dev specs."""
        for s in traverse.traverse_nodes(specs):
            # If there is a concrete version on the CLI *that we know nothing
            # about*, add it to the known versions. Use idx=0, which is the
            # best possible, so they're guaranteed to be used preferentially.
            version = s.versions.concrete

            if version is None or any(v == version for v in self.possible_versions[s.name]):
                continue

            if require_checksum and not _is_checksummed_git_version(version):
                raise UnsatisfiableSpecError(
                    s.format("No matching version for constraint {name}{@versions}")
                )

            if not allow_deprecated and version in self.deprecated_versions[s.name]:
                continue

            declared = DeclaredVersion(version=version, idx=0, origin=origin)
            self.declared_versions[s.name].append(declared)
            self.possible_versions[s.name].add(version)

    def _supported_targets(self, compiler_name, compiler_version, targets):
        """Get a list of which targets are supported by the compiler.

        Results are ordered most to least recent.
        """
        supported = []

        for target in targets:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    target.optimization_flags(compiler_name, str(compiler_version))
                supported.append(target)
            except archspec.cpu.UnsupportedMicroarchitecture:
                continue
            except ValueError:
                continue

        return sorted(supported, reverse=True)

    def platform_defaults(self):
        self.gen.h2("Default platform")
        platform = spack.platforms.host()
        self.gen.fact(fn.node_platform_default(platform))
        self.gen.fact(fn.allowed_platform(platform))

    def os_defaults(self, specs):
        self.gen.h2("Possible operating systems")
        platform = spack.platforms.host()

        # create set of OS's to consider
        buildable = set(platform.operating_sys.keys())

        # Consider any OS's mentioned on the command line. We need this to
        # cross-concretize in CI, and for some tests.
        # TODO: OS should really be more than just a label -- rework this.
        for spec in specs:
            if spec.architecture and spec.architecture.os:
                buildable.add(spec.architecture.os)

        # make directives for buildable OS's
        for build_os in sorted(buildable):
            self.gen.fact(fn.buildable_os(build_os))
            if os.environ.get("SPACKOS_BOOTSTRAP"):
                self.gen.fact(fn.os_compatible("spack0", build_os))


        def keyfun(os):
            return (
                os == platform.default_os,  # prefer default
                os not in buildable,  # then prefer buildables
                os,  # then sort by name
            )

        all_oses = buildable.union(self.possible_oses)
        ordered_oses = sorted(all_oses, key=keyfun, reverse=True)

        # output the preference order of OS's for the concretizer to choose
        for i, os_name in enumerate(ordered_oses):
            self.gen.fact(fn.os(os_name, i))

    def target_defaults(self, specs):
        """Add facts about targets and target compatibility."""
        self.gen.h2("Default target")

        platform = spack.platforms.host()
        uarch = archspec.cpu.TARGETS.get(platform.default)

        self.gen.h2("Target compatibility")

        # Construct the list of targets which are compatible with the host
        candidate_targets = [uarch] + uarch.ancestors

        # Get configuration options
        granularity = spack.config.get("concretizer:targets:granularity")
        host_compatible = spack.config.get("concretizer:targets:host_compatible")

        # Add targets which are not compatible with the current host
        if not host_compatible:
            additional_targets_in_family = sorted(
                [
                    t
                    for t in archspec.cpu.TARGETS.values()
                    if (t.family.name == uarch.family.name and t not in candidate_targets)
                ],
                key=lambda x: len(x.ancestors),
                reverse=True,
            )
            candidate_targets += additional_targets_in_family

        # Check if we want only generic architecture
        if granularity == "generic":
            candidate_targets = [t for t in candidate_targets if t.vendor == "generic"]

        # Add targets explicitly requested from specs
        for spec in specs:
            if not spec.architecture or not spec.architecture.target:
                continue

            target = archspec.cpu.TARGETS.get(spec.target.name)
            if not target:
                self.target_ranges(spec, None)
                continue

            if target not in candidate_targets and not host_compatible:
                candidate_targets.append(target)
                for ancestor in target.ancestors:
                    if ancestor not in candidate_targets:
                        candidate_targets.append(ancestor)

        best_targets = {uarch.family.name}
        for compiler_id, known_compiler in enumerate(self.possible_compilers):
            if not known_compiler.available:
                continue

            compiler = known_compiler.compiler_obj
            # Stub support for cross-compilation, to be expanded later
            if known_compiler.target is not None and compiler.target not in (
                str(uarch.family),
                "any",
            ):
                self.gen.fact(fn.compiler_supports_target(compiler_id, compiler.target))
                self.gen.newline()
                continue

            supported = self._supported_targets(compiler.name, compiler.version, candidate_targets)

            # If we can't find supported targets it may be due to custom
            # versions in the spec, e.g. gcc@foo. Try to match the
            # real_version from the compiler object to get more accurate
            # results.
            if not supported:
                supported = self._supported_targets(
                    compiler.name, compiler.real_version, candidate_targets
                )

            if not supported:
                continue

            for target in supported:
                best_targets.add(target.name)
                self.gen.fact(fn.compiler_supports_target(compiler_id, target.name))

            self.gen.fact(fn.compiler_supports_target(compiler_id, uarch.family.name))
            self.gen.newline()

        i = 0  # TODO compute per-target offset?
        for target in candidate_targets:
            self.gen.fact(fn.target(target.name))
            self.gen.fact(fn.target_family(target.name, target.family.name))
            self.gen.fact(fn.target_compatible(target.name, target.name))
            # Code for ancestor can run on target
            for ancestor in target.ancestors:
                self.gen.fact(fn.target_compatible(target.name, ancestor.name))

            # prefer best possible targets; weight others poorly so
            # they're not used unless set explicitly
            # these are stored to be generated as facts later offset by the
            # number of preferred targets
            if target.name in best_targets:
                self.default_targets.append((i, target.name))
                i += 1
            else:
                self.default_targets.append((100, target.name))
            self.gen.newline()

        self.default_targets = list(sorted(set(self.default_targets)))

        self.target_preferences()

    def virtual_providers(self):
        self.gen.h2("Virtual providers")
        for vspec in sorted(self.possible_virtuals):
            self.gen.fact(fn.virtual(vspec))
        self.gen.newline()

    def define_version_constraints(self):
        """Define what version_satisfies(...) means in ASP logic."""
        for pkg_name, versions in sorted(self.version_constraints):
            # generate facts for each package constraint and the version
            # that satisfies it
            for v in sorted(v for v in self.possible_versions[pkg_name] if v.satisfies(versions)):
                self.gen.fact(fn.pkg_fact(pkg_name, fn.version_satisfies(versions, v)))

            self.gen.newline()

    def collect_virtual_constraints(self):
        """Define versions for constraints on virtuals.

        Must be called before define_version_constraints().
        """
        # aggregate constraints into per-virtual sets
        constraint_map = collections.defaultdict(lambda: set())
        for pkg_name, versions in self.version_constraints:
            if not spack.repo.PATH.is_virtual(pkg_name):
                continue
            constraint_map[pkg_name].add(versions)

        # extract all the real versions mentioned in version ranges
        def versions_for(v):
            if isinstance(v, vn.StandardVersion):
                return [v]
            elif isinstance(v, vn.ClosedOpenRange):
                return [v.lo, vn._prev_version(v.hi)]
            elif isinstance(v, vn.VersionList):
                return sum((versions_for(e) for e in v), [])
            else:
                raise TypeError("expected version type, found: %s" % type(v))

        # define a set of synthetic possible versions for virtuals, so
        # that `version_satisfies(Package, Constraint, Version)` has the
        # same semantics for virtuals as for regular packages.
        for pkg_name, versions in sorted(constraint_map.items()):
            possible_versions = set(sum([versions_for(v) for v in versions], []))
            for version in sorted(possible_versions):
                self.possible_versions[pkg_name].add(version)

    def define_compiler_version_constraints(self):
        for constraint in sorted(self.compiler_version_constraints):
            for compiler_id, compiler in enumerate(self.possible_compilers):
                if compiler.spec.satisfies(constraint):
                    self.gen.fact(
                        fn.compiler_version_satisfies(
                            constraint.name, constraint.versions, compiler_id
                        )
                    )
        self.gen.newline()

    def define_target_constraints(self):
        def _all_targets_satisfiying(single_constraint):
            allowed_targets = []

            if ":" not in single_constraint:
                return [single_constraint]

            t_min, _, t_max = single_constraint.partition(":")
            for test_target in archspec.cpu.TARGETS.values():
                # Check lower bound
                if t_min and not t_min <= test_target:
                    continue

                # Check upper bound
                if t_max and not t_max >= test_target:
                    continue

                allowed_targets.append(test_target)
            return allowed_targets

        cache = {}
        for target_constraint in sorted(self.target_constraints):
            # Construct the list of allowed targets for this constraint
            allowed_targets = []
            for single_constraint in str(target_constraint).split(","):
                if single_constraint not in cache:
                    cache[single_constraint] = _all_targets_satisfiying(single_constraint)
                allowed_targets.extend(cache[single_constraint])

            for target in allowed_targets:
                self.gen.fact(fn.target_satisfies(target_constraint, target))
            self.gen.newline()

    def define_variant_values(self):
        """Validate variant values from the command line.

        Also add valid variant values from the command line to the
        possible values for a variant.

        """
        # Tell the concretizer about possible values from specs we saw in
        # spec_clauses(). We might want to order these facts by pkg and name
        # if we are debugging.
        for pkg, variant, value in self.variant_values_from_specs:
            self.gen.fact(fn.pkg_fact(pkg, fn.variant_possible_value(variant, value)))

    def register_concrete_spec(self, spec, possible):
        # tell the solver about any installed packages that could
        # be dependencies (don't tell it about the others)
        if spec.name not in possible:
            return

        try:
            # Only consider installed packages for repo we know
            spack.repo.PATH.get(spec)
        except (spack.repo.UnknownNamespaceError, spack.repo.UnknownPackageError) as e:
            tty.debug(f"[REUSE] Issues when trying to reuse {spec.short_spec}: {str(e)}")
            return

        self.reusable_and_possible.add(spec)

    def concrete_specs(self):
        """Emit facts for reusable specs"""
        for h, spec in self.reusable_and_possible.explicit_items():
            # this indicates that there is a spec like this installed
            self.gen.fact(fn.installed_hash(spec.name, h))
            # this describes what constraints it imposes on the solve
            self.impose(h, spec, body=True)
            self.gen.newline()
            # Declare as possible parts of specs that are not in package.py
            # - Add versions to possible versions
            # - Add OS to possible OS's
            for dep in spec.traverse():
                self.possible_versions[dep.name].add(dep.version)
                self.declared_versions[dep.name].append(
                    DeclaredVersion(version=dep.version, idx=0, origin=Provenance.INSTALLED)
                )
                self.possible_oses.add(dep.os)

    def define_concrete_input_specs(self, specs, possible):
        # any concrete specs in the input spec list
        for input_spec in specs:
            for spec in input_spec.traverse():
                if spec.concrete:
                    self.register_concrete_spec(spec, possible)

    def setup(
        self,
        specs: List[spack.spec.Spec],
        *,
        reuse: Optional[List[spack.spec.Spec]] = None,
        allow_deprecated: bool = False,
    ) -> str:
        """Generate an ASP program with relevant constraints for specs.

        This calls methods on the solve driver to set up the problem with
        facts and rules from all possible dependencies of the input
        specs, as well as constraints from the specs themselves.

        Arguments:
            specs: list of Specs to solve
            reuse: list of concrete specs that can be reused
            allow_deprecated: if True adds deprecated versions into the solve
        """
        check_packages_exist(specs)

        node_counter = _create_counter(specs, tests=self.tests)
        self.possible_virtuals = node_counter.possible_virtuals()
        self.pkgs = node_counter.possible_dependencies()
        self.libcs = sorted(all_libcs())  # type: ignore[type-var]

        # Fail if we already know an unreachable node is requested
        for spec in specs:
            missing_deps = [
                str(d) for d in spec.traverse() if d.name not in self.pkgs and not d.virtual
            ]
            if missing_deps:
                raise spack.spec.InvalidDependencyError(spec.name, missing_deps)

        for node in traverse.traverse_nodes(specs):
            if node.namespace is not None:
                self.explicitly_required_namespaces[node.name] = node.namespace

        self.gen = ProblemInstanceBuilder()
        compiler_parser = CompilerParser(configuration=spack.config.CONFIG).with_input_specs(specs)

        if using_libc_compatibility():
            for libc in self.libcs:
                self.gen.fact(fn.allowed_libc(libc.name, libc.version))

        if not allow_deprecated:
            self.gen.fact(fn.deprecated_versions_not_allowed())

        # Calculate develop specs
        # they will be used in addition to command line specs
        # in determining known versions/targets/os
        dev_specs: Tuple[spack.spec.Spec, ...] = ()
        env = ev.active_environment()
        if env:
            dev_specs = tuple(
                spack.spec.Spec(info["spec"]).constrained(
                    "dev_path=%s"
                    % spack.util.path.canonicalize_path(info["path"], default_wd=env.path)
                )
                for name, info in env.dev_specs.items()
            )
        specs = tuple(specs)  # ensure compatible types to add

        self.gen.h1("Reusable concrete specs")
        self.define_concrete_input_specs(specs, self.pkgs)
        if reuse:
            self.gen.fact(fn.optimize_for_reuse())
            for reusable_spec in reuse:
                compiler_parser.add_compiler_from_concrete_spec(reusable_spec)
                self.register_concrete_spec(reusable_spec, self.pkgs)
        self.concrete_specs()

        self.possible_compilers = compiler_parser.possible_compilers()

        self.gen.h1("Generic statements on possible packages")
        node_counter.possible_packages_facts(self.gen, fn)

        self.gen.h1("Possible flags on nodes")
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            self.gen.fact(fn.flag_type(flag))
        self.gen.newline()

        self.gen.h1("General Constraints")
        self.config_compatible_os()
        self.compiler_facts()

        # architecture defaults
        self.platform_defaults()
        self.os_defaults(specs + dev_specs)
        self.target_defaults(specs + dev_specs)

        self.virtual_providers()
        self.provider_defaults()
        self.provider_requirements()
        self.external_packages()

        # TODO: make a config option for this undocumented feature
        checksummed = "SPACK_CONCRETIZER_REQUIRE_CHECKSUM" in os.environ
        self.define_package_versions_and_validate_preferences(
            self.pkgs, allow_deprecated=allow_deprecated, require_checksum=checksummed
        )
        self.define_ad_hoc_versions_from_specs(
            specs, Provenance.SPEC, allow_deprecated=allow_deprecated, require_checksum=checksummed
        )
        self.define_ad_hoc_versions_from_specs(
            dev_specs,
            Provenance.DEV_SPEC,
            allow_deprecated=allow_deprecated,
            require_checksum=checksummed,
        )
        self.validate_and_define_versions_from_requirements(
            allow_deprecated=allow_deprecated, require_checksum=checksummed
        )

        self.gen.h1("Package Constraints")
        for pkg in sorted(self.pkgs):
            self.gen.h2("Package rules: %s" % pkg)
            self.pkg_rules(pkg, tests=self.tests)
            self.gen.h2("Package preferences: %s" % pkg)
            self.preferred_variants(pkg)

        self.gen.h1("Develop specs")
        # Inject dev_path from environment
        for ds in dev_specs:
            self.condition(spack.spec.Spec(ds.name), ds, msg="%s is a develop spec" % ds.name)
            self.trigger_rules()
            self.effect_rules()

        self.gen.h1("Spec Constraints")
        self.literal_specs(specs)

        self.gen.h1("Variant Values defined in specs")
        self.define_variant_values()

        if WITH_RUNTIME:
            self.gen.h1("Runtimes")
            self.define_runtime_constraints()

        self.gen.h1("Version Constraints")
        self.collect_virtual_constraints()
        self.define_version_constraints()

        self.gen.h1("Compiler Version Constraints")
        self.define_compiler_version_constraints()

        self.gen.h1("Target Constraints")
        self.define_target_constraints()

        self.gen.h1("Internal errors")
        self.internal_errors()

        return self.gen.value()

    def internal_errors(self):
        parent_dir = os.path.dirname(__file__)

        def visit(node):
            if ast_type(node) == clingo().ast.ASTType.Rule:
                for term in node.body:
                    if ast_type(term) == clingo().ast.ASTType.Literal:
                        if ast_type(term.atom) == clingo().ast.ASTType.SymbolicAtom:
                            name = ast_sym(term.atom).name
                            if name == "internal_error":
                                arg = ast_sym(ast_sym(term.atom).arguments[0])
                                symbol = AspFunction(name)(arg.string)
                                self.assumptions.append((parse_term(str(symbol)), True))
                                self.gen.asp_problem.append(f"{{ {symbol} }}.\n")

        path = os.path.join(parent_dir, "concretize.lp")
        parse_files([path], visit)

    def define_runtime_constraints(self):
        """Define the constraints to be imposed on the runtimes"""
        recorder = RuntimePropertyRecorder(self)

        for compiler in self.possible_compilers:
            compiler_with_different_cls_names = {
                "oneapi": "intel-oneapi-compilers",
                "clang": "llvm",
            }
            compiler_cls_name = compiler_with_different_cls_names.get(
                compiler.spec.name, compiler.spec.name
            )
            try:
                compiler_cls = spack.repo.PATH.get_pkg_class(compiler_cls_name)
                if hasattr(compiler_cls, "runtime_constraints"):
                    compiler_cls.runtime_constraints(spec=compiler.spec, pkg=recorder)
            except spack.repo.UnknownPackageError:
                pass

            # Inject libc from available compilers, on Linux
            if not compiler.available:
                continue

            current_libc = compiler.compiler_obj.default_libc
            # If this is a compiler yet to be built (config:install_missing_compilers:true)
            # infer libc from the Python process
            if not current_libc and compiler.compiler_obj.cc is None:
                current_libc = spack.util.libc.libc_from_current_python_process()

            if using_libc_compatibility() and current_libc:
                recorder("*").depends_on(
                    "libc", when=f"%{compiler.spec}", type="link", description="Add libc"
                )
                recorder("*").depends_on(
                    str(current_libc),
                    when=f"%{compiler.spec}",
                    type="link",
                    description="Add libc",
                )

        recorder.consume_facts()

    def literal_specs(self, specs):
        for spec in specs:
            self.gen.h2("Spec: %s" % str(spec))
            condition_id = next(self._id_counter)
            trigger_id = next(self._id_counter)

            # Special condition triggered by "literal_solved"
            self.gen.fact(fn.literal(trigger_id))
            self.gen.fact(fn.pkg_fact(spec.name, fn.condition_trigger(condition_id, trigger_id)))
            self.gen.fact(fn.condition_reason(condition_id, f"{spec} requested explicitly"))

            imposed_spec_key = str(spec), None
            cache = self._effect_cache[spec.name]
            if imposed_spec_key in cache:
                effect_id, requirements = cache[imposed_spec_key]
            else:
                effect_id = next(self._id_counter)
                requirements = self.spec_clauses(spec)
            root_name = spec.name
            for clause in requirements:
                clause_name = clause.args[0]
                if clause_name == "variant_set":
                    requirements.append(
                        fn.attr("variant_default_value_from_cli", *clause.args[1:])
                    )
                elif clause_name in ("node", "virtual_node", "hash"):
                    # These facts are needed to compute the "condition_set" of the root
                    pkg_name = clause.args[1]
                    self.gen.fact(fn.mentioned_in_literal(trigger_id, root_name, pkg_name))

            requirements.append(fn.attr("virtual_root" if spec.virtual else "root", spec.name))
            cache[imposed_spec_key] = (effect_id, requirements)
            self.gen.fact(fn.pkg_fact(spec.name, fn.condition_effect(condition_id, effect_id)))

            if self.concretize_everything:
                self.gen.fact(fn.solve_literal(trigger_id))

        self.effect_rules()

    def validate_and_define_versions_from_requirements(
        self, *, allow_deprecated: bool, require_checksum: bool
    ):
        """If package requirements mention concrete versions that are not mentioned
        elsewhere, then we need to collect those to mark them as possible
        versions. If they are abstract and statically have no match, then we
        need to throw an error. This function assumes all possible versions are already
        registered in self.possible_versions."""
        for pkg_name, d in spack.config.get("packages").items():
            if pkg_name == "all" or "require" not in d:
                continue

            for s in traverse.traverse_nodes(self._specs_from_requires(pkg_name, d["require"])):
                name, versions = s.name, s.versions

                if name not in self.pkgs or versions == spack.version.any_version:
                    continue

                s.attach_git_version_lookup()
                v = versions.concrete

                if not v:
                    # If the version is not concrete, check it's statically concretizable. If
                    # not throw an error, which is just so that users know they need to change
                    # their config, instead of getting a hard to decipher concretization error.
                    if not any(x for x in self.possible_versions[name] if x.satisfies(versions)):
                        raise spack.config.ConfigError(
                            f"Version requirement {versions} on {pkg_name} for {name} "
                            f"cannot match any known version from package.py or externals"
                        )
                    continue

                if v in self.possible_versions[name]:
                    continue

                if not allow_deprecated and v in self.deprecated_versions[name]:
                    continue

                # If concrete an not yet defined, conditionally define it, like we do for specs
                # from the command line.
                if not require_checksum or _is_checksummed_git_version(v):
                    self.declared_versions[name].append(
                        DeclaredVersion(version=v, idx=0, origin=Provenance.PACKAGE_REQUIREMENT)
                    )
                    self.possible_versions[name].add(v)

    def _specs_from_requires(self, pkg_name, section):
        """Collect specs from a requirement rule"""
        if isinstance(section, str):
            yield _spec_with_default_name(section, pkg_name)
            return

        for spec_group in section:
            if isinstance(spec_group, str):
                yield _spec_with_default_name(spec_group, pkg_name)
                continue

            # Otherwise it is an object. The object can contain a single
            # "spec" constraint, or a list of them with "any_of" or
            # "one_of" policy.
            if "spec" in spec_group:
                yield _spec_with_default_name(spec_group["spec"], pkg_name)
                continue

            key = "one_of" if "one_of" in spec_group else "any_of"
            for s in spec_group[key]:
                yield _spec_with_default_name(s, pkg_name)

    def pkg_class(self, pkg_name: str) -> typing.Type["spack.package_base.PackageBase"]:
        request = pkg_name
        if pkg_name in self.explicitly_required_namespaces:
            namespace = self.explicitly_required_namespaces[pkg_name]
            request = f"{namespace}.{pkg_name}"
        return spack.repo.PATH.get_pkg_class(request)


class _Head:
    """ASP functions used to express spec clauses in the HEAD of a rule"""

    node = fn.attr("node")
    virtual_node = fn.attr("virtual_node")
    node_platform = fn.attr("node_platform_set")
    node_os = fn.attr("node_os_set")
    node_target = fn.attr("node_target_set")
    variant_value = fn.attr("variant_set")
    node_compiler = fn.attr("node_compiler_set")
    node_compiler_version = fn.attr("node_compiler_version_set")
    node_flag = fn.attr("node_flag_set")
    node_flag_source = fn.attr("node_flag_source")
    node_flag_propagate = fn.attr("node_flag_propagate")
    variant_propagation_candidate = fn.attr("variant_propagation_candidate")


class _Body:
    """ASP functions used to express spec clauses in the BODY of a rule"""

    node = fn.attr("node")
    virtual_node = fn.attr("virtual_node")
    node_platform = fn.attr("node_platform")
    node_os = fn.attr("node_os")
    node_target = fn.attr("node_target")
    variant_value = fn.attr("variant_value")
    node_compiler = fn.attr("node_compiler")
    node_compiler_version = fn.attr("node_compiler_version")
    node_flag = fn.attr("node_flag")
    node_flag_source = fn.attr("node_flag_source")
    node_flag_propagate = fn.attr("node_flag_propagate")
    variant_propagation_candidate = fn.attr("variant_propagation_candidate")


class ProblemInstanceBuilder:
    """Provides an interface to construct a problem instance.

    Once all the facts and rules have been added, the problem instance can be retrieved with:

    >>> builder = ProblemInstanceBuilder()
    >>> ...
    >>> problem_instance = builder.value()

    The problem instance can be added directly to the "control" structure of clingo.
    """

    def __init__(self):
        self.asp_problem = []

    def fact(self, atom: AspFunction) -> None:
        symbol = atom.symbol() if hasattr(atom, "symbol") else atom
        self.asp_problem.append(f"{str(symbol)}.\n")

    def append(self, rule: str) -> None:
        self.asp_problem.append(rule)

    def title(self, header: str, char: str) -> None:
        self.asp_problem.append("\n")
        self.asp_problem.append("%" + (char * 76))
        self.asp_problem.append("\n")
        self.asp_problem.append(f"% {header}\n")
        self.asp_problem.append("%" + (char * 76))
        self.asp_problem.append("\n")

    def h1(self, header: str) -> None:
        self.title(header, "=")

    def h2(self, header: str) -> None:
        self.title(header, "-")

    def newline(self):
        self.asp_problem.append("\n")

    def value(self) -> str:
        return "".join(self.asp_problem)


class RequirementParser:
    """Parses requirements from package.py files and configuration, and returns rules."""

    def __init__(self, configuration):
        self.config = configuration

    def rules(self, pkg: "spack.package_base.PackageBase") -> List[RequirementRule]:
        result = []
        result.extend(self.rules_from_package_py(pkg))
        result.extend(self.rules_from_require(pkg))
        result.extend(self.rules_from_prefer(pkg))
        result.extend(self.rules_from_conflict(pkg))
        return result

    def rules_from_package_py(self, pkg) -> List[RequirementRule]:
        rules = []
        for when_spec, requirement_list in pkg.requirements.items():
            for requirements, policy, message in requirement_list:
                rules.append(
                    RequirementRule(
                        pkg_name=pkg.name,
                        policy=policy,
                        requirements=requirements,
                        kind=RequirementKind.PACKAGE,
                        condition=when_spec,
                        message=message,
                    )
                )
        return rules

    def rules_from_virtual(self, virtual_str: str) -> List[RequirementRule]:
        requirements = self.config.get("packages", {}).get(virtual_str, {}).get("require", [])
        return self._rules_from_requirements(
            virtual_str, requirements, kind=RequirementKind.VIRTUAL
        )

    def rules_from_require(self, pkg: "spack.package_base.PackageBase") -> List[RequirementRule]:
        kind, requirements = self._raw_yaml_data(pkg, section="require")
        return self._rules_from_requirements(pkg.name, requirements, kind=kind)

    def rules_from_prefer(self, pkg: "spack.package_base.PackageBase") -> List[RequirementRule]:
        result = []
        kind, preferences = self._raw_yaml_data(pkg, section="prefer")
        for item in preferences:
            spec, condition, message = self._parse_prefer_conflict_item(item)
            result.append(
                # A strong preference is defined as:
                #
                # require:
                # - any_of: [spec_str, "@:"]
                RequirementRule(
                    pkg_name=pkg.name,
                    policy="any_of",
                    requirements=[spec, spack.spec.Spec("@:")],
                    kind=kind,
                    message=message,
                    condition=condition,
                )
            )
        return result

    def rules_from_conflict(self, pkg: "spack.package_base.PackageBase") -> List[RequirementRule]:
        result = []
        kind, conflicts = self._raw_yaml_data(pkg, section="conflict")
        for item in conflicts:
            spec, condition, message = self._parse_prefer_conflict_item(item)
            result.append(
                # A conflict is defined as:
                #
                # require:
                # - one_of: [spec_str, "@:"]
                RequirementRule(
                    pkg_name=pkg.name,
                    policy="one_of",
                    requirements=[spec, spack.spec.Spec("@:")],
                    kind=kind,
                    message=message,
                    condition=condition,
                )
            )
        return result

    def _parse_prefer_conflict_item(self, item):
        # The item is either a string or an object with at least a "spec" attribute
        if isinstance(item, str):
            spec = sc.parse_spec_from_yaml_string(item)
            condition = spack.spec.Spec()
            message = None
        else:
            spec = sc.parse_spec_from_yaml_string(item["spec"])
            condition = spack.spec.Spec(item.get("when"))
            message = item.get("message")
        return spec, condition, message

    def _raw_yaml_data(self, pkg: "spack.package_base.PackageBase", *, section: str):
        config = self.config.get("packages")
        data = config.get(pkg.name, {}).get(section, [])
        kind = RequirementKind.PACKAGE
        if not data:
            data = config.get("all", {}).get(section, [])
            kind = RequirementKind.DEFAULT
        return kind, data

    def _rules_from_requirements(
        self, pkg_name: str, requirements, *, kind: RequirementKind
    ) -> List[RequirementRule]:
        """Manipulate requirements from packages.yaml, and return a list of tuples
        with a uniform structure (name, policy, requirements).
        """
        if isinstance(requirements, str):
            requirements = [requirements]

        rules = []
        for requirement in requirements:
            # A string is equivalent to a one_of group with a single element
            if isinstance(requirement, str):
                requirement = {"one_of": [requirement]}

            for policy in ("spec", "one_of", "any_of"):
                if policy not in requirement:
                    continue

                constraints = requirement[policy]
                # "spec" is for specifying a single spec
                if policy == "spec":
                    constraints = [constraints]
                    policy = "one_of"

                # validate specs from YAML first, and fail with line numbers if parsing fails.
                constraints = [
                    sc.parse_spec_from_yaml_string(constraint) for constraint in constraints
                ]
                when_str = requirement.get("when")
                when = sc.parse_spec_from_yaml_string(when_str) if when_str else spack.spec.Spec()

                constraints = [
                    x
                    for x in constraints
                    if not self.reject_requirement_constraint(pkg_name, constraint=x, kind=kind)
                ]
                if not constraints:
                    continue

                rules.append(
                    RequirementRule(
                        pkg_name=pkg_name,
                        policy=policy,
                        requirements=constraints,
                        kind=kind,
                        message=requirement.get("message"),
                        condition=when,
                    )
                )
        return rules

    def reject_requirement_constraint(
        self, pkg_name: str, *, constraint: spack.spec.Spec, kind: RequirementKind
    ) -> bool:
        """Returns True if a requirement constraint should be rejected"""
        if kind == RequirementKind.DEFAULT:
            # Requirements under all: are applied only if they are satisfiable considering only
            # package rules, so e.g. variants must exist etc. Otherwise, they are rejected.
            try:
                s = spack.spec.Spec(pkg_name)
                s.constrain(constraint)
                s.validate_or_raise()
            except spack.error.SpackError as e:
                tty.debug(
                    f"[SETUP] Rejecting the default '{constraint}' requirement "
                    f"on '{pkg_name}': {str(e)}",
                    level=2,
                )
                return True
        return False


class CompilerParser:
    """Parses configuration files, and builds a list of possible compilers for the solve."""

    def __init__(self, configuration) -> None:
        self.compilers: Set[KnownCompiler] = set()
        for c in all_compilers_in_config(configuration):
            if using_libc_compatibility() and not c.default_libc:
                warnings.warn(
                    f"cannot detect libc from {c.spec}. The compiler will not be used "
                    f"during concretization."
                )
                continue

            target = c.target if c.target != "any" else None
            candidate = KnownCompiler(
                spec=c.spec, os=c.operating_system, target=target, available=True, compiler_obj=c
            )
            if candidate in self.compilers:
                warnings.warn(
                    f"duplicate found for {c.spec} on {c.operating_system}/{c.target}. "
                    f"Edit your compilers.yaml configuration to remove it."
                )
                continue

            self.compilers.add(candidate)

    def with_input_specs(self, input_specs: List["spack.spec.Spec"]) -> "CompilerParser":
        """Accounts for input specs when building the list of possible compilers.

        Args:
            input_specs: specs to be concretized
        """
        strict = spack.concretize.Concretizer().check_for_compiler_existence
        default_os = str(spack.platforms.host().default_os)
        default_target = str(archspec.cpu.host().family)
        for s in traverse.traverse_nodes(input_specs):
            # we don't need to validate compilers for already-built specs
            if s.concrete or not s.compiler:
                continue

            version = s.compiler.versions.concrete

            if not version or any(item.spec.satisfies(s.compiler) for item in self.compilers):
                continue

            # Error when a compiler is not found and strict mode is enabled
            if strict:
                raise spack.concretize.UnavailableCompilerVersionError(s.compiler)

            # Make up a compiler matching the input spec. This is for bootstrapping.
            compiler_cls = spack.compilers.class_for_compiler_name(s.compiler.name)
            compiler_obj = compiler_cls(
                s.compiler, operating_system=default_os, target=default_target, paths=[None] * 4
            )
            self.compilers.add(
                KnownCompiler(
                    spec=s.compiler,
                    os=default_os,
                    target=default_target,
                    available=True,
                    compiler_obj=compiler_obj,
                )
            )

        return self

    def add_compiler_from_concrete_spec(self, spec: "spack.spec.Spec") -> None:
        """Account for compilers that are coming from concrete specs, through reuse.

        Args:
            spec: concrete spec to be reused
        """
        assert spec.concrete, "the spec argument must be concrete"
        candidate = KnownCompiler(
            spec=spec.compiler,
            os=str(spec.architecture.os),
            target=str(spec.architecture.target.microarchitecture.family),
            available=False,
            compiler_obj=None,
        )
        self.compilers.add(candidate)

    def possible_compilers(self) -> List[KnownCompiler]:
        # Here we have to sort two times, first sort by name and ascending version
        result = sorted(self.compilers, key=lambda x: (x.spec.name, x.spec.version), reverse=True)
        # Then stable sort to prefer available compilers and account for preferences
        ppk = spack.package_prefs.PackagePrefs("all", "compiler", all=False)
        result.sort(key=lambda x: (not x.available, ppk(x.spec)))
        return result


class RuntimePropertyRecorder:
    """An object of this class is injected in callbacks to compilers, to let them declare
    properties of the runtimes they support and of the runtimes they provide, and to add
    runtime dependencies to the nodes using said compiler.

    The usage of the object is the following. First, a runtime package name or the wildcard
    "*" are passed as an argument to __call__, to set which kind of package we are referring to.
    Then we can call one method with a directive-like API.

    Examples:
        >>> pkg = RuntimePropertyRecorder(setup)
        >>> # Every package compiled with %gcc has a link dependency on 'gcc-runtime'
        >>> pkg("*").depends_on(
        ...     "gcc-runtime",
        ...     when="%gcc",
        ...     type="link",
        ...     description="If any package uses %gcc, it depends on gcc-runtime"
        ... )
        >>> # The version of gcc-runtime is the same as the %gcc used to "compile" it
        >>> pkg("gcc-runtime").requires("@=9.4.0", when="%gcc@=9.4.0")
    """

    def __init__(self, setup):
        self._setup = setup
        self.rules = []
        self.runtime_conditions = set()
        # State of this object set in the __call__ method, and reset after
        # each directive-like method
        self.current_package = None

    def __call__(self, package_name: str) -> "RuntimePropertyRecorder":
        """Sets a package name for the next directive-like method call"""
        assert self.current_package is None, f"state was already set to '{self.current_package}'"
        self.current_package = package_name
        return self

    def reset(self):
        """Resets the current state."""
        self.current_package = None

    def depends_on(
        self,
        dependency_str: str,
        *,
        when: str,
        type: str,
        description: str,
        languages: Optional[List[str]] = None,
    ) -> None:
        """Injects conditional dependencies on packages.

        Conditional dependencies can be either "real" packages or virtual dependencies.

        Args:
            dependency_str: the dependency spec to inject
            when: anonymous condition to be met on a package to have the dependency
            type: dependency type
            languages: languages needed by the package for the dependency to be considered
            description: human-readable description of the rule for adding the dependency
        """
        # TODO: The API for this function is not final, and is still subject to change. At
        # TODO: the moment, we implemented only the features strictly needed for the
        # TODO: functionality currently provided by Spack, and we assert nothing else is required.
        msg = "the 'depends_on' method can be called only with pkg('*')"
        assert self.current_package == "*", msg

        when_spec = spack.spec.Spec(when)
        assert when_spec.name is None, "only anonymous when specs are accepted"

        dependency_spec = spack.spec.Spec(dependency_str)
        if dependency_spec.versions != vn.any_version:
            self._setup.version_constraints.add((dependency_spec.name, dependency_spec.versions))

        placeholder = "XXX"
        node_variable = "node(ID, Package)"
        when_spec.name = placeholder

        body_clauses = self._setup.spec_clauses(when_spec, body=True)
        body_str = (
            f"  {f',{os.linesep}  '.join(str(x) for x in body_clauses)},\n"
            f"  not external({node_variable}),\n"
            f"  not runtime(Package)"
        ).replace(f'"{placeholder}"', f"{node_variable}")
        if languages:
            body_str += ",\n"
            for language in languages:
                body_str += f'  attr("language", {node_variable}, "{language}")'

        head_clauses = self._setup.spec_clauses(dependency_spec, body=False)

        runtime_pkg = dependency_spec.name

        is_virtual = head_clauses[0].args[0] == "virtual_node"
        main_rule = (
            f"% {description}\n"
            f'1 {{ attr("depends_on", {node_variable}, node(0..X-1, "{runtime_pkg}"), "{type}") :'
            f' max_dupes("{runtime_pkg}", X)}} 1:-\n'
            f"{body_str}.\n\n"
        )
        if is_virtual:
            main_rule = (
                f"% {description}\n"
                f'attr("dependency_holds", {node_variable}, "{runtime_pkg}", "{type}") :-\n'
                f"{body_str}.\n\n"
            )

        self.rules.append(main_rule)
        for clause in head_clauses:
            if clause.args[0] == "node":
                continue
            runtime_node = f'node(RuntimeID, "{runtime_pkg}")'
            head_str = str(clause).replace(f'"{runtime_pkg}"', runtime_node)
            depends_on_constraint = (
                f'  attr("depends_on", {node_variable}, {runtime_node}, "{type}"),\n'
            )
            if is_virtual:
                depends_on_constraint = (
                    f'  attr("depends_on", {node_variable}, ProviderNode, "{type}"),\n'
                    f"  provider(ProviderNode, {runtime_node}),\n"
                )

            rule = f"{head_str} :-\n" f"{depends_on_constraint}" f"{body_str}.\n\n"
            self.rules.append(rule)

        self.reset()

    def requires(self, impose: str, *, when: str):
        """Injects conditional requirements on a given package.

        Args:
            impose: constraint to be imposed
            when: condition triggering the constraint
        """
        msg = "the 'requires' method cannot be called with pkg('*') or without setting the package"
        assert self.current_package is not None and self.current_package != "*", msg

        imposed_spec = spack.spec.Spec(f"{self.current_package}{impose}")
        when_spec = spack.spec.Spec(f"{self.current_package}{when}")

        assert imposed_spec.versions.concrete, f"{impose} must have a concrete version"
        assert when_spec.compiler.concrete, f"{when} must have a concrete compiler"

        # Add versions to possible versions
        for s in (imposed_spec, when_spec):
            if not s.versions.concrete:
                continue
            self._setup.possible_versions[s.name].add(s.version)
            self._setup.declared_versions[s.name].append(
                DeclaredVersion(version=s.version, idx=0, origin=Provenance.RUNTIME)
            )

        self.runtime_conditions.add((imposed_spec, when_spec))
        self.reset()

    def consume_facts(self):
        """Consume the facts collected by this object, and emits rules and
        facts for the runtimes.
        """
        self._setup.gen.h2("Runtimes: rules")
        self._setup.gen.newline()
        for rule in self.rules:
            self._setup.gen.append(rule)

        self._setup.gen.h2("Runtimes: conditions")
        for runtime_pkg in spack.repo.PATH.packages_with_tags("runtime"):
            self._setup.gen.fact(fn.runtime(runtime_pkg))
            self._setup.gen.fact(fn.possible_in_link_run(runtime_pkg))
            self._setup.gen.newline()
            # Inject version rules for runtimes (versions are declared based
            # on the available compilers)
            self._setup.pkg_version_rules(runtime_pkg)

        for imposed_spec, when_spec in self.runtime_conditions:
            msg = f"{when_spec} requires {imposed_spec} at runtime"
            _ = self._setup.condition(when_spec, imposed_spec=imposed_spec, msg=msg)

        self._setup.trigger_rules()
        self._setup.effect_rules()


class SpecBuilder:
    """Class with actions to rebuild a spec from ASP results."""

    #: Regex for attributes that don't need actions b/c they aren't used to construct specs.
    ignored_attributes = re.compile(
        "|".join(
            [
                r"^.*_propagate$",
                r"^.*_satisfies$",
                r"^.*_set$",
                r"^compatible_libc$",
                r"^dependency_holds$",
                r"^external_conditions_hold$",
                r"^node_compiler$",
                r"^package_hash$",
                r"^root$",
                r"^track_dependencies$",
                r"^variant_default_value_from_cli$",
                r"^virtual_node$",
                r"^virtual_on_incoming_edges$",
                r"^virtual_root$",
            ]
        )
    )

    @staticmethod
    def make_node(*, pkg: str) -> NodeArgument:
        """Given a package name, returns the string representation of the "min_dupe_id" node in
        the ASP encoding.

        Args:
            pkg: name of a package
        """
        return NodeArgument(id="0", pkg=pkg)

    def __init__(self, specs, hash_lookup=None):
        self._specs = {}
        self._result = None
        self._command_line_specs = specs
        self._flag_sources = collections.defaultdict(lambda: set())
        self._flag_compiler_defaults = set()

        # Pass in as arguments reusable specs and plug them in
        # from this dictionary during reconstruction
        self._hash_lookup = hash_lookup or {}

    def hash(self, node, h):
        if node not in self._specs:
            self._specs[node] = self._hash_lookup[h]

    def node(self, node):
        if node not in self._specs:
            self._specs[node] = spack.spec.Spec(node.pkg)

    def _arch(self, node):
        arch = self._specs[node].architecture
        if not arch:
            arch = spack.spec.ArchSpec()
            self._specs[node].architecture = arch
        return arch

    def namespace(self, node, namespace):
        self._specs[node].namespace = namespace

    def node_platform(self, node, platform):
        self._arch(node).platform = platform

    def node_os(self, node, os):
        self._arch(node).os = os

    def node_target(self, node, target):
        self._arch(node).target = target

    def variant_value(self, node, name, value):
        # FIXME: is there a way not to special case 'dev_path' everywhere?
        if name == "dev_path":
            self._specs[node].variants.setdefault(
                name, spack.variant.SingleValuedVariant(name, value)
            )
            return

        if name == "patches":
            self._specs[node].variants.setdefault(
                name, spack.variant.MultiValuedVariant(name, value)
            )
            return

        self._specs[node].update_variant_validate(name, value)

    def version(self, node, version):
        self._specs[node].versions = vn.VersionList([vn.Version(version)])

    def node_compiler_version(self, node, compiler, version):
        self._specs[node].compiler = spack.spec.CompilerSpec(compiler)
        self._specs[node].compiler.versions = vn.VersionList([vn.Version(version)])

    def node_flag_compiler_default(self, node):
        self._flag_compiler_defaults.add(node)

    def node_flag(self, node, flag_type, flag):
        self._specs[node].compiler_flags.add_flag(flag_type, flag, False)

    def node_flag_source(self, node, flag_type, source):
        self._flag_sources[(node, flag_type)].add(source)

    def no_flags(self, node, flag_type):
        self._specs[node].compiler_flags[flag_type] = []

    def external_spec_selected(self, node, idx):
        """This means that the external spec and index idx has been selected for this package."""
        packages_yaml = _external_config_with_implicit_externals(spack.config.CONFIG)
        spec_info = packages_yaml[node.pkg]["externals"][int(idx)]
        self._specs[node].external_path = spec_info.get("prefix", None)
        self._specs[node].external_modules = spack.spec.Spec._format_module_list(
            spec_info.get("modules", None)
        )
        self._specs[node].extra_attributes = spec_info.get("extra_attributes", {})

        # If this is an extension, update the dependencies to include the extendee
        package = self._specs[node].package_class(self._specs[node])
        extendee_spec = package.extendee_spec

        if extendee_spec:
            extendee_node = SpecBuilder.make_node(pkg=extendee_spec.name)
            package.update_external_dependencies(self._specs.get(extendee_node, None))

    def depends_on(self, parent_node, dependency_node, type):
        dependency_spec = self._specs[dependency_node]
        edges = self._specs[parent_node].edges_to_dependencies(name=dependency_spec.name)
        edges = [x for x in edges if id(x.spec) == id(dependency_spec)]
        depflag = dt.flag_from_string(type)

        if not edges:
            self._specs[parent_node].add_dependency_edge(
                self._specs[dependency_node], depflag=depflag, virtuals=()
            )
        else:
            edges[0].update_deptypes(depflag=depflag)

    def virtual_on_edge(self, parent_node, provider_node, virtual):
        dependencies = self._specs[parent_node].edges_to_dependencies(name=(provider_node.pkg))
        provider_spec = self._specs[provider_node]
        dependencies = [x for x in dependencies if id(x.spec) == id(provider_spec)]
        assert len(dependencies) == 1, f"{virtual}: {provider_node.pkg}"
        dependencies[0].update_virtuals((virtual,))

    def reorder_flags(self):
        """Order compiler flags on specs in predefined order.

        We order flags so that any node's flags will take priority over
        those of its dependents.  That is, the deepest node in the DAG's
        flags will appear last on the compile line, in the order they
        were specified.

        The solver determines which flags are on nodes; this routine
        imposes order afterwards.
        """
        # reverse compilers so we get highest priority compilers that share a spec
        compilers = dict(
            (c.spec, c) for c in reversed(all_compilers_in_config(spack.config.CONFIG))
        )
        cmd_specs = dict((s.name, s) for spec in self._command_line_specs for s in spec.traverse())

        for spec in self._specs.values():
            # if bootstrapping, compiler is not in config and has no flags
            flagmap_from_compiler = {}
            if spec.compiler in compilers:
                flagmap_from_compiler = compilers[spec.compiler].flags

            for flag_type in spec.compiler_flags.valid_compiler_flags():
                from_compiler = flagmap_from_compiler.get(flag_type, [])
                from_sources = []

                # order is determined by the  DAG. A spec's flags come after any of its ancestors
                # on the compile line
                node = SpecBuilder.make_node(pkg=spec.name)
                source_key = (node, flag_type)
                if source_key in self._flag_sources:
                    order = [
                        SpecBuilder.make_node(pkg=s.name)
                        for s in spec.traverse(order="post", direction="parents")
                    ]
                    sorted_sources = sorted(
                        self._flag_sources[source_key], key=lambda s: order.index(s)
                    )

                    # add flags from each source, lowest to highest precedence
                    for node in sorted_sources:
                        all_src_flags = list()
                        per_pkg_sources = [self._specs[node]]
                        if node.pkg in cmd_specs:
                            per_pkg_sources.append(cmd_specs[node.pkg])
                        for source in per_pkg_sources:
                            all_src_flags.extend(source.compiler_flags.get(flag_type, []))
                        extend_flag_list(from_sources, all_src_flags)

                # compiler flags from compilers config are lowest precedence
                ordered_compiler_flags = list(llnl.util.lang.dedupe(from_compiler + from_sources))
                compiler_flags = spec.compiler_flags.get(flag_type, [])

                msg = "%s does not equal %s" % (set(compiler_flags), set(ordered_compiler_flags))
                assert set(compiler_flags) == set(ordered_compiler_flags), msg

                spec.compiler_flags.update({flag_type: ordered_compiler_flags})

    def deprecated(self, node: NodeArgument, version: str) -> None:
        tty.warn(f'using "{node.pkg}@{version}" which is a deprecated version')

    @staticmethod
    def sort_fn(function_tuple):
        """Ensure attributes are evaluated in the correct order.

        hash attributes are handled first, since they imply entire concrete specs
        node attributes are handled next, since they instantiate nodes
        external_spec_selected attributes are handled last, so that external extensions can find
        the concrete specs on which they depend because all nodes are fully constructed before we
        consider which ones are external.
        """
        name = function_tuple[0]
        if name == "hash":
            return (-5, 0)
        elif name == "node":
            return (-4, 0)
        elif name == "node_flag":
            return (-2, 0)
        elif name == "external_spec_selected":
            return (0, 0)  # note out of order so this goes last
        elif name == "virtual_on_edge":
            return (1, 0)
        else:
            return (-1, 0)

    def build_specs(self, function_tuples):
        # Functions don't seem to be in particular order in output.  Sort
        # them here so that directives that build objects (like node and
        # node_compiler) are called in the right order.
        self.function_tuples = sorted(set(function_tuples), key=self.sort_fn)

        self._specs = {}
        for name, args in self.function_tuples:
            if SpecBuilder.ignored_attributes.match(name):
                continue

            action = getattr(self, name, None)

            # print out unknown actions so we can display them for debugging
            if not action:
                msg = 'UNKNOWN SYMBOL: attr("%s", %s)' % (name, ", ".join(str(a) for a in args))
                tty.debug(msg)
                continue

            msg = (
                "Internal Error: Uncallable action found in asp.py.  Please report to the spack"
                " maintainers."
            )
            assert action and callable(action), msg

            # ignore predicates on virtual packages, as they're used for
            # solving but don't construct anything. Do not ignore error
            # predicates on virtual packages.
            if name != "error":
                node = args[0]
                pkg = node.pkg
                if spack.repo.PATH.is_virtual(pkg):
                    continue

                # if we've already gotten a concrete spec for this pkg,
                # do not bother calling actions on it except for node_flag_source,
                # since node_flag_source is tracking information not in the spec itself
                spec = self._specs.get(args[0])
                if spec and spec.concrete:
                    if name != "node_flag_source":
                        continue

            action(*args)

        # fix flags after all specs are constructed
        self.reorder_flags()

        # inject patches -- note that we' can't use set() to unique the
        # roots here, because the specs aren't complete, and the hash
        # function will loop forever.
        roots = [spec.root for spec in self._specs.values() if not spec.root.installed]
        roots = dict((id(r), r) for r in roots)
        for root in roots.values():
            spack.spec.Spec.inject_patches_variant(root)

        # Add external paths to specs with just external modules
        for s in self._specs.values():
            spack.spec.Spec.ensure_external_path_if_external(s)

        for s in self._specs.values():
            _develop_specs_from_env(s, ev.active_environment())

        # mark concrete and assign hashes to all specs in the solve
        for root in roots.values():
            root._finalize_concretization()

        for s in self._specs.values():
            spack.spec.Spec.ensure_no_deprecated(s)

        # Add git version lookup info to concrete Specs (this is generated for
        # abstract specs as well but the Versions may be replaced during the
        # concretization process)
        for root in self._specs.values():
            for spec in root.traverse():
                if isinstance(spec.version, vn.GitVersion):
                    spec.version.attach_lookup(
                        spack.version.git_ref_lookup.GitRefLookup(spec.fullname)
                    )

        return self._specs


def _develop_specs_from_env(spec, env):
    dev_info = env.dev_specs.get(spec.name, {}) if env else {}
    if not dev_info:
        return

    path = spack.util.path.canonicalize_path(dev_info["path"], default_wd=env.path)

    if "dev_path" in spec.variants:
        error_msg = (
            "Internal Error: The dev_path for spec {name} is not connected to a valid environment"
            "path. Please note that develop specs can only be used inside an environment"
            "These paths should be the same:\n\tdev_path:{dev_path}\n\tenv_based_path:{env_path}"
        ).format(name=spec.name, dev_path=spec.variants["dev_path"], env_path=path)

        assert spec.variants["dev_path"].value == path, error_msg
    else:
        spec.variants.setdefault("dev_path", spack.variant.SingleValuedVariant("dev_path", path))
    spec.constrain(dev_info["spec"])


def _is_reusable(spec: spack.spec.Spec, packages, local: bool) -> bool:
    """A spec is reusable if it's not a dev spec, it's imported from the cray manifest, it's not
    external, or it's external with matching packages.yaml entry. The latter prevents two issues:

    1. Externals in build caches: avoid installing an external on the build machine not
       available on the target machine
    2. Local externals: avoid reusing an external if the local config changes. This helps in
       particular when a user removes an external from packages.yaml, and expects that that
       takes effect immediately.

    Arguments:
        spec: the spec to check
        packages: the packages configuration
    """
    if "dev_path" in spec.variants:
        return False

    if not spec.external:
        return _has_runtime_dependencies(spec)

    # Cray external manifest externals are always reusable
    if local:
        _, record = spack.store.STORE.db.query_by_spec_hash(spec.dag_hash())
        if record and record.origin == "external-db":
            return True

    try:
        provided = spack.repo.PATH.get(spec).provided_virtual_names()
    except spack.repo.RepoError:
        provided = []

    for name in {spec.name, *provided}:
        for entry in packages.get(name, {}).get("externals", []):
            if (
                spec.satisfies(entry["spec"])
                and spec.external_path == entry.get("prefix")
                and spec.external_modules == entry.get("modules")
            ):
                return True

    return False


def _has_runtime_dependencies(spec: spack.spec.Spec) -> bool:
    if not WITH_RUNTIME:
        return True

    if spec.compiler.name == "gcc" and not spec.dependencies("gcc-runtime"):
        return False

    if spec.compiler.name == "oneapi" and not spec.dependencies("intel-oneapi-runtime"):
        return False

    return True


class SpecFilter:
    """Given a method to produce a list of specs, this class can filter them according to
    different criteria.
    """

    def __init__(
        self,
        factory: Callable[[], List[spack.spec.Spec]],
        is_usable: Callable[[spack.spec.Spec], bool],
        include: List[str],
        exclude: List[str],
    ) -> None:
        """
        Args:
            factory: factory to produce a list of specs
            is_usable: predicate that takes a spec in input and returns False if the spec
                should not be considered for this filter, True otherwise.
            include: if present, a "good" spec must match at least one entry in the list
            exclude: if present, a "good" spec must not match any entry in the list
        """
        self.factory = factory
        self.is_usable = is_usable
        self.include = include
        self.exclude = exclude

    def is_selected(self, s: spack.spec.Spec) -> bool:
        if not self.is_usable(s):
            return False

        if self.include and not any(s.satisfies(c) for c in self.include):
            return False

        if self.exclude and any(s.satisfies(c) for c in self.exclude):
            return False

        return True

    def selected_specs(self) -> List[spack.spec.Spec]:
        return [s for s in self.factory() if self.is_selected(s)]

    @staticmethod
    def from_store(configuration, include, exclude) -> "SpecFilter":
        """Constructs a filter that takes the specs from the current store."""
        packages = _external_config_with_implicit_externals(configuration)
        is_reusable = functools.partial(_is_reusable, packages=packages, local=True)
        factory = functools.partial(_specs_from_store, configuration=configuration)
        return SpecFilter(factory=factory, is_usable=is_reusable, include=include, exclude=exclude)

    @staticmethod
    def from_buildcache(configuration, include, exclude) -> "SpecFilter":
        """Constructs a filter that takes the specs from the configured buildcaches."""
        packages = _external_config_with_implicit_externals(configuration)
        is_reusable = functools.partial(_is_reusable, packages=packages, local=False)
        return SpecFilter(
            factory=_specs_from_mirror, is_usable=is_reusable, include=include, exclude=exclude
        )


def _specs_from_store(configuration):
    store = spack.store.create(configuration)
    with store.db.read_transaction():
        return store.db.query(installed=True)


def _specs_from_mirror():
    try:
        return spack.binary_distribution.update_cache_and_get_specs()
    except (spack.binary_distribution.FetchCacheError, IndexError):
        # this is raised when no mirrors had indices.
        # TODO: update mirror configuration so it can indicate that the
        # TODO: source cache (or any mirror really) doesn't have binaries.
        return []


class ReuseStrategy(enum.Enum):
    ROOTS = enum.auto()
    DEPENDENCIES = enum.auto()
    NONE = enum.auto()


class ReusableSpecsSelector:
    """Selects specs that can be reused during concretization."""

    def __init__(self, configuration: spack.config.Configuration) -> None:
        self.configuration = configuration
        self.store = spack.store.create(configuration)
        self.reuse_strategy = ReuseStrategy.ROOTS

        reuse_yaml = self.configuration.get("concretizer:reuse", False)
        self.reuse_sources = []
        if not isinstance(reuse_yaml, typing.Mapping):
            if reuse_yaml is False:
                self.reuse_strategy = ReuseStrategy.NONE
            if reuse_yaml == "dependencies":
                self.reuse_strategy = ReuseStrategy.DEPENDENCIES
            self.reuse_sources.extend(
                [
                    SpecFilter.from_store(
                        configuration=self.configuration, include=[], exclude=[]
                    ),
                    SpecFilter.from_buildcache(
                        configuration=self.configuration, include=[], exclude=[]
                    ),
                ]
            )
        else:
            roots = reuse_yaml.get("roots", True)
            if roots is True:
                self.reuse_strategy = ReuseStrategy.ROOTS
            else:
                self.reuse_strategy = ReuseStrategy.DEPENDENCIES
            default_include = reuse_yaml.get("include", [])
            default_exclude = reuse_yaml.get("exclude", [])
            default_sources = [{"type": "local"}, {"type": "buildcache"}]
            for source in reuse_yaml.get("from", default_sources):
                include = source.get("include", default_include)
                exclude = source.get("exclude", default_exclude)
                if source["type"] == "local":
                    self.reuse_sources.append(
                        SpecFilter.from_store(self.configuration, include=include, exclude=exclude)
                    )
                elif source["type"] == "buildcache":
                    self.reuse_sources.append(
                        SpecFilter.from_buildcache(
                            self.configuration, include=include, exclude=exclude
                        )
                    )

    def reusable_specs(self, specs: List[spack.spec.Spec]) -> List[spack.spec.Spec]:
        if self.reuse_strategy == ReuseStrategy.NONE:
            return []

        result = []
        for reuse_source in self.reuse_sources:
            result.extend(reuse_source.selected_specs())

        # If we only want to reuse dependencies, remove the root specs
        if self.reuse_strategy == ReuseStrategy.DEPENDENCIES:
            result = [spec for spec in result if not any(root in spec for root in specs)]

        return result


class Solver:
    """This is the main external interface class for solving.

    It manages solver configuration and preferences in one place. It sets up the solve
    and passes the setup method to the driver, as well.
    """

    def __init__(self):
        self.driver = PyclingoDriver()
        self.selector = ReusableSpecsSelector(configuration=spack.config.CONFIG)
        if spack.platforms.host().name == "cray":
            msg = (
                "The Cray platform, i.e. 'platform=cray', will be removed in Spack v0.23. "
                "All Cray machines will be then detected as 'platform=linux'."
            )
            warnings.warn(msg)

    @staticmethod
    def _check_input_and_extract_concrete_specs(specs):
        reusable = []
        for root in specs:
            for s in root.traverse():
                if s.virtual:
                    continue
                if s.concrete:
                    reusable.append(s)
                spack.spec.Spec.ensure_valid_variants(s)
        return reusable

    def solve(
        self,
        specs,
        out=None,
        timers=False,
        stats=False,
        tests=False,
        setup_only=False,
        allow_deprecated=False,
    ):
        """
        Arguments:
          specs (list): List of ``Spec`` objects to solve for.
          out: Optionally write the generate ASP program to a file-like object.
          timers (bool): Print out coarse timers for different solve phases.
          stats (bool): Print out detailed stats from clingo.
          tests (bool or tuple): If True, concretize test dependencies for all packages.
            If a tuple of package names, concretize test dependencies for named
            packages (defaults to False: do not concretize test dependencies).
          setup_only (bool): if True, stop after setup and don't solve (default False).
          allow_deprecated (bool): allow deprecated version in the solve
        """
        # Check upfront that the variants are admissible
        specs = [s.lookup_hash() for s in specs]
        reusable_specs = self._check_input_and_extract_concrete_specs(specs)
        reusable_specs.extend(self.selector.reusable_specs(specs))
        setup = SpackSolverSetup(tests=tests)
        output = OutputConfiguration(timers=timers, stats=stats, out=out, setup_only=setup_only)
        result, _, _ = self.driver.solve(
            setup, specs, reuse=reusable_specs, output=output, allow_deprecated=allow_deprecated
        )
        return result

    def solve_in_rounds(
        self, specs, out=None, timers=False, stats=False, tests=False, allow_deprecated=False
    ):
        """Solve for a stable model of specs in multiple rounds.

        This relaxes the assumption of solve that everything must be consistent and
        solvable in a single round. Each round tries to maximize the reuse of specs
        from previous rounds.

        The function is a generator that yields the result of each round.

        Arguments:
            specs (list): list of Specs to solve.
            out: Optionally write the generate ASP program to a file-like object.
            timers (bool): print timing if set to True
            stats (bool): print internal statistics if set to True
            tests (bool): add test dependencies to the solve
            allow_deprecated (bool): allow deprecated version in the solve
        """
        specs = [s.lookup_hash() for s in specs]
        reusable_specs = self._check_input_and_extract_concrete_specs(specs)
        reusable_specs.extend(self.selector.reusable_specs(specs))
        setup = SpackSolverSetup(tests=tests)

        # Tell clingo that we don't have to solve all the inputs at once
        setup.concretize_everything = False

        input_specs = specs
        output = OutputConfiguration(timers=timers, stats=stats, out=out, setup_only=False)
        while True:
            result, _, _ = self.driver.solve(
                setup,
                input_specs,
                reuse=reusable_specs,
                output=output,
                allow_deprecated=allow_deprecated,
            )
            yield result

            # If we don't have unsolved specs we are done
            if not result.unsolved_specs:
                break

            if not result.specs:
                # This is also a problem: no specs were solved for, which
                # means we would be in a loop if we tried again
                unsolved_str = Result.format_unsolved(result.unsolved_specs)
                raise InternalConcretizerError(
                    "Internal Spack error: a subset of input specs could not"
                    f" be solved for.\n\t{unsolved_str}"
                )

            input_specs = list(x for (x, y) in result.unsolved_specs)
            for spec in result.specs:
                reusable_specs.extend(spec.traverse())


class UnsatisfiableSpecError(spack.error.UnsatisfiableSpecError):
    """There was an issue with the spec that was requested (i.e. a user error)."""

    def __init__(self, msg):
        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)
        self.provided = None
        self.required = None
        self.constraint_type = None


class InternalConcretizerError(spack.error.UnsatisfiableSpecError):
    """Errors that indicate a bug in Spack."""

    def __init__(self, msg):
        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)
        self.provided = None
        self.required = None
        self.constraint_type = None


class SolverError(InternalConcretizerError):
    """For cases where the solver is unable to produce a solution.

    Such cases are unexpected because we allow for solutions with errors,
    so for example user specs that are over-constrained should still
    get a solution.
    """

    def __init__(self, provided, conflicts):
        msg = (
            "Spack concretizer internal error. Please submit a bug report and include the "
            "command, environment if applicable and the following error message."
            f"\n    {provided} is unsatisfiable"
        )

        if conflicts:
            msg += ", errors are:" + "".join([f"\n    {conflict}" for conflict in conflicts])

        super().__init__(msg)

        self.provided = provided

        # Add attribute expected of the superclass interface
        self.required = None
        self.constraint_type = None
