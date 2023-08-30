# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import copy
import enum
import itertools
import os
import pathlib
import pprint
import re
import types
import warnings
from typing import Dict, List, NamedTuple, Optional, Set, Tuple, Union

import archspec.cpu

try:
    import clingo  # type: ignore[import]

    # There may be a better way to detect this
    clingo_cffi = hasattr(clingo.Symbol, "_rep")
except ImportError:
    clingo = None  # type: ignore
    clingo_cffi = False

import llnl.util.lang
import llnl.util.tty as tty

import spack
import spack.binary_distribution
import spack.cmd
import spack.compilers
import spack.config
import spack.dependency
import spack.directives
import spack.environment as ev
import spack.error
import spack.package_base
import spack.package_prefs
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.target
import spack.traverse
import spack.util.path
import spack.util.timer
import spack.variant
import spack.version as vn
import spack.version.git_ref_lookup

from .counter import FullDuplicatesCounter, MinimalDuplicatesCounter, NoDuplicatesCounter

# these are from clingo.ast and bootstrapped later
ASTType = None
parse_files = None


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
    control = clingo.Control()
    control.configuration.configuration = "tweety"
    control.configuration.solver.heuristic = "Domain"
    control.configuration.solver.opt_strategy = "usc,one"
    return control


# backward compatibility functions for clingo ASTs
def ast_getter(*names):
    def getter(node):
        for name in names:
            result = getattr(node, name, None)
            if result:
                return result
        raise KeyError("node has no such keys: %s" % names)

    return getter


ast_type = ast_getter("ast_type", "type")
ast_sym = ast_getter("symbol", "term")


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

    def __str__(self):
        return f"{self._name_.lower()}"


class RequirementKind(enum.Enum):
    """Purpose / provenance of a requirement"""

    #: Default requirement expressed under the 'all' attribute of packages.yaml
    DEFAULT = enum.auto()
    #: Requirement expressed on a virtual package
    VIRTUAL = enum.auto()
    #: Requirement expressed on a specific package
    PACKAGE = enum.auto()


DeclaredVersion = collections.namedtuple("DeclaredVersion", ["version", "idx", "origin"])


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


def specify(spec):
    if isinstance(spec, spack.spec.Spec):
        return spec
    return spack.spec.Spec(spec)


class AspObject:
    """Object representing a piece of ASP code."""


def _id(thing):
    """Quote string if needed for it to be a valid identifier."""
    if isinstance(thing, AspObject):
        return thing
    elif isinstance(thing, bool):
        return '"%s"' % str(thing)
    elif isinstance(thing, int):
        return str(thing)
    else:
        return '"%s"' % str(thing)


@llnl.util.lang.key_ordering
class AspFunction(AspObject):
    __slots__ = ["name", "args"]

    def __init__(self, name, args=None):
        self.name = name
        self.args = () if args is None else tuple(args)

    def _cmp_key(self):
        return self.name, self.args

    def __call__(self, *args):
        """Return a new instance of this function with added arguments.

        Note that calls are additive, so you can do things like::

            >>> attr = AspFunction("attr")
            attr()

            >>> attr("version")
            attr("version")

            >>> attr("version")("foo")
            attr("version", "foo")

            >>> v = AspFunction("attr", "version")
            attr("version")

            >>> v("foo", "bar")
            attr("version", "foo", "bar")

        """
        return AspFunction(self.name, self.args + args)

    def symbol(self, positive=True):
        def argify(arg):
            if isinstance(arg, bool):
                return clingo.String(str(arg))
            elif isinstance(arg, int):
                return clingo.Number(arg)
            elif isinstance(arg, AspFunction):
                return clingo.Function(arg.name, [argify(x) for x in arg.args], positive=positive)
            else:
                return clingo.String(str(arg))

        return clingo.Function(self.name, [argify(arg) for arg in self.args], positive=positive)

    def __str__(self):
        return "%s(%s)" % (self.name, ", ".join(str(_id(arg)) for arg in self.args))

    def __repr__(self):
        return str(self)


class AspFunctionBuilder:
    def __getattr__(self, name):
        return AspFunction(name)


fn = AspFunctionBuilder()


def all_compilers_in_config():
    return spack.compilers.all_compilers()


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

        The error is an InternalConcretizerError, and includes the minimized cores
        resulting from the solve, formatted to be human readable.
        """
        if self.satisfiable:
            return

        constraints = self.abstract_specs
        if len(constraints) == 1:
            constraints = constraints[0]

        conflicts = self.format_minimal_cores()
        raise InternalConcretizerError(constraints, conflicts=conflicts)

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
        """List of abstract input specs that were not solved."""
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
            self._unsolved_specs = self.abstract_specs
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
                self._unsolved_specs.append(input_spec)


def _normalize_packages_yaml(packages_yaml, *, repository):
    normalized_yaml = copy.copy(packages_yaml)
    for pkg_name in packages_yaml:
        is_virtual = repository.is_virtual(pkg_name)
        if pkg_name == "all" or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = normalized_yaml.pop(pkg_name)
        is_buildable = data.get("buildable", True)
        if not is_buildable:
            for provider in repository.providers_for(pkg_name):
                entry = normalized_yaml.setdefault(provider.name, {})
                entry["buildable"] = False

        externals = data.get("externals", [])

        def keyfn(x):
            return spack.spec.Spec(x["spec"]).name

        for provider, specs in itertools.groupby(externals, key=keyfn):
            entry = normalized_yaml.setdefault(provider, {})
            entry.setdefault("externals", []).extend(specs)

    return normalized_yaml


def bootstrap_clingo():
    global clingo, ASTType, parse_files

    if not clingo:
        import spack.bootstrap

        with spack.bootstrap.ensure_bootstrap_configuration():
            spack.bootstrap.ensure_core_dependencies()
            import clingo

    from clingo.ast import ASTType

    try:
        from clingo.ast import parse_files
    except ImportError:
        # older versions of clingo have this one namespace up
        from clingo import parse_files


class NodeArgument(NamedTuple):
    id: str
    pkg: str


def intermediate_repr(sym):
    """Returns an intermediate representation of clingo models for Spack's spec builder.

    Currently, transforms symbols from clingo models either to strings or to NodeArgument objects.

    Returns:
        This will turn a ``clingo.Symbol`` into a string or NodeArgument, or a sequence of
        ``clingo.Symbol`` objects into a tuple of those objects.
    """
    # TODO: simplify this when we no longer have to support older clingo versions.
    if isinstance(sym, (list, tuple)):
        return tuple(intermediate_repr(a) for a in sym)

    try:
        if sym.name == "node":
            return NodeArgument(
                id=intermediate_repr(sym.arguments[0]), pkg=intermediate_repr(sym.arguments[1])
            )
    except RuntimeError:
        # This happens when using clingo w/ CFFI and trying to access ".name" for symbols
        # that are not functions
        pass

    if clingo_cffi:
        # Clingo w/ CFFI will throw an exception on failure
        try:
            return sym.string
        except RuntimeError:
            return str(sym)
    else:
        return sym.string or str(sym)


def extract_args(model, predicate_name):
    """Extract the arguments to predicates with the provided name from a model.

    Pull out all the predicates with name ``predicate_name`` from the model, and
    return their intermediate representation.
    """
    return [intermediate_repr(sym.arguments) for sym in model if sym.name == predicate_name]


class ErrorHandler:
    def __init__(self, model):
        self.model = model
        self.error_args = extract_args(model, "error")

    def multiple_values_error(self, attribute, pkg):
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

    def no_value_error(self, attribute, pkg):
        return f'Cannot select a single "{attribute}" for package "{pkg}"'

    def handle_error(self, msg, *args):
        """Handle an error state derived by the solver."""
        if msg == "multiple_values_error":
            return self.multiple_values_error(*args)

        if msg == "no_value_error":
            return self.no_value_error(*args)

        # For variant formatting, we sometimes have to construct specs
        # to format values properly. Find/replace all occurances of
        # Spec(...) with the string representation of the spec mentioned
        msg = msg.format(*args)
        specs_to_construct = re.findall(r"Spec\(([^)]*)\)", msg)
        for spec_str in specs_to_construct:
            msg = msg.replace("Spec(%s)" % spec_str, str(spack.spec.Spec(spec_str)))

        return msg

    def message(self, errors) -> str:
        messages = [
            f"  {idx+1: 2}. {self.handle_error(msg, *args)}"
            for idx, (_, msg, args) in enumerate(errors)
        ]
        header = "concretization failed for the following reasons:\n"
        return "\n".join([header] + messages)

    def raise_if_errors(self):
        if not self.error_args:
            return

        errors = sorted(
            [(int(priority), msg, args) for priority, msg, *args in self.error_args], reverse=True
        )
        msg = self.message(errors)
        raise UnsatisfiableSpecError(msg)


#: Data class to collect information on a requirement
RequirementRule = collections.namedtuple(
    "RequirementRule", ["pkg_name", "policy", "requirements", "condition", "kind", "message"]
)


class PyclingoDriver:
    def __init__(self, configuration: spack.config.ConfigurationType, cores: bool = True) -> None:
        """Driver for the Python clingo interface.

        Arguments:
            cores (bool): whether to generate unsatisfiable cores for better
                error reporting.
        """
        bootstrap_clingo()

        self.configuration = configuration
        self.out = llnl.util.lang.Devnull()
        self.cores = cores

        # These attributes are part of the object, but will be reset
        # at each call to solve
        self.control = None
        self.backend = None
        self.assumptions = None

    def title(self, name, char):
        self.out.write("\n")
        self.out.write("%" + (char * 76))
        self.out.write("\n")
        self.out.write("%% %s\n" % name)
        self.out.write("%" + (char * 76))
        self.out.write("\n")

    def h1(self, name):
        self.title(name, "=")

    def h2(self, name):
        self.title(name, "-")

    def newline(self):
        self.out.write("\n")

    def fact(self, head):
        """ASP fact (a rule without a body).

        Arguments:
            head (AspFunction): ASP function to generate as fact
        """
        symbol = head.symbol() if hasattr(head, "symbol") else head

        # This is commented out to avoid evaluating str(symbol) when we have no stream
        if not isinstance(self.out, llnl.util.lang.Devnull):
            self.out.write(f"{str(symbol)}.\n")

        atom = self.backend.add_atom(symbol)

        # Only functions relevant for constructing bug reports for bad error messages
        # are assumptions, and only when using cores.
        choice = self.cores and symbol.name == "internal_error"
        self.backend.add_rule([atom], [], choice=choice)
        if choice:
            self.assumptions.append(atom)

    def solve(self, setup, specs, reuse=None, output=None, control=None):
        """Set up the input and solve for dependencies of ``specs``.

        Arguments:
            setup (SpackSolverSetup): An object to set up the ASP problem.
            specs (list): List of ``Spec`` objects to solve for.
            reuse (None or list): list of concrete specs that can be reused
            output (None or OutputConfiguration): configuration object to set
                the output of this solve.
            control (clingo.Control): configuration for the solver. If None,
                default values will be used

        Return:
            A tuple of the solve result, the timer for the different phases of the
            solve, and the internal statistics from clingo.
        """
        assert setup.gen is self, "setup must be initialized with the same solver object"
        output = output or DEFAULT_OUTPUT_CONFIGURATION
        # allow solve method to override the output stream
        if output.out is not None:
            self.out = output.out

        timer = spack.util.timer.Timer()

        # Initialize the control object for the solver
        self.control = control or default_clingo_control()
        # set up the problem -- this generates facts and rules
        self.assumptions = []
        timer.start("setup")
        with self.control.backend() as backend:
            self.backend = backend
            setup.setup(specs, reuse=reuse)
        timer.stop("setup")

        timer.start("load")
        # read in the main ASP program and display logic -- these are
        # handwritten, not generated, so we load them as resources
        parent_dir = os.path.dirname(__file__)

        # extract error messages from concretize.lp by inspecting its AST
        with self.backend:

            def visit(node):
                if ast_type(node) == ASTType.Rule:
                    for term in node.body:
                        if ast_type(term) == ASTType.Literal:
                            if ast_type(term.atom) == ASTType.SymbolicAtom:
                                name = ast_sym(term.atom).name
                                if name == "internal_error":
                                    arg = ast_sym(ast_sym(term.atom).arguments[0])
                                    self.fact(AspFunction(name)(arg.string))

            self.h1("Error messages")
            path = os.path.join(parent_dir, "concretize.lp")
            parse_files([path], visit)

        # If we're only doing setup, just return an empty solve result
        if output.setup_only:
            return Result(specs), None, None

        # Load the file itself
        self.control.load(os.path.join(parent_dir, "concretize.lp"))
        self.control.load(os.path.join(parent_dir, "heuristic.lp"))
        if self.configuration.get("concretizer:duplicates:strategy", "none") != "none":
            self.control.load(os.path.join(parent_dir, "heuristic_separate.lp"))
        self.control.load(os.path.join(parent_dir, "os_compatibility.lp"))
        self.control.load(os.path.join(parent_dir, "display.lp"))
        if not setup.concretize_everything:
            self.control.load(os.path.join(parent_dir, "when_possible.lp"))
        timer.stop("load")

        # Grounding is the first step in the solve -- it turns our facts
        # and first-order logic rules into propositional logic.
        timer.start("ground")
        self.control.ground([("base", [])])
        timer.stop("ground")

        # With a grounded program, we can run the solve.
        result = Result(specs)
        models = []  # stable models if things go well
        cores = []  # unsatisfiable cores if they do not

        def on_model(model):
            models.append((model.cost, model.symbols(shown=True, terms=True)))

        solve_kwargs = {
            "assumptions": self.assumptions,
            "on_model": on_model,
            "on_core": cores.append,
        }

        if clingo_cffi:
            solve_kwargs["on_unsat"] = cores.append

        timer.start("solve")
        solve_result = self.control.solve(**solve_kwargs)

        if solve_result.satisfiable and self._model_has_cycles(models):
            tty.debug(f"cycles detected, falling back to slower algorithm [specs={specs}]")
            self.control.load(os.path.join(parent_dir, "cycle_detection.lp"))
            self.control.ground([("no_cycle", [])])
            models.clear()
            solve_result = self.control.solve(**solve_kwargs)

        timer.stop("solve")

        # once done, construct the solve result
        result.satisfiable = solve_result.satisfiable

        if result.satisfiable:
            # get the best model
            builder = SpecBuilder(
                specs=specs,
                configuration=self.configuration,
                hash_lookup=setup.reusable_and_possible,
            )
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

            # print any unknown functions in the model
            for sym in best_model:
                if sym.name not in ("attr", "error", "opt_criterion"):
                    tty.debug(
                        "UNKNOWN SYMBOL: %s(%s)"
                        % (sym.name, ", ".join(intermediate_repr(sym.arguments)))
                    )

        elif cores:
            result.control = self.control
            result.cores.extend(cores)

        if output.timers:
            timer.write_tty()
            print()

        if output.stats:
            print("Statistics:")
            pprint.pprint(self.control.statistics)

        return result, timer, self.control.statistics

    def _model_has_cycles(self, models):
        """Returns true if the best model has cycles in it"""
        cycle_detection = clingo.Control()
        parent_dir = pathlib.Path(__file__).parent
        lp_file = parent_dir / "cycle_detection.lp"

        min_cost, best_model = min(models)
        with cycle_detection.backend() as backend:
            for atom in best_model:
                if atom.name == "attr" and str(atom.arguments[0]) == '"depends_on"':
                    symbol = fn.depends_on(atom.arguments[1], atom.arguments[2])
                    atom_id = backend.add_atom(symbol.symbol())
                    backend.add_rule([atom_id], [], choice=False)

            cycle_detection.load(str(lp_file))
            cycle_detection.ground([("base", []), ("no_cycle", [])])
            cycle_result = cycle_detection.solve()

        return cycle_result.unsatisfiable


#: Set of concrete versions
VersionSet = Set[Union[vn.StandardVersion, vn.GitVersion]]


class SpackSolverSetup:
    """Class to set up and run a Spack concretization solve."""

    def __init__(self, *, driver: PyclingoDriver, tests: bool = False) -> None:
        self.gen = driver
        self.configuration = driver.configuration
        self.repository = spack.repo.create(self.configuration)

        self.declared_versions: Dict[str, List[DeclaredVersion]] = collections.defaultdict(list)
        self.possible_versions: Dict[str, VersionSet] = collections.defaultdict(set)
        self.deprecated_versions: Dict[str, VersionSet] = collections.defaultdict(set)

        self.possible_virtuals: Set[str] = set()
        self.possible_compilers: List[spack.compiler.Compiler] = []
        self.possible_oses: Set[str] = set()
        self.variant_values_from_specs: Set[Tuple[str, str, str]] = set()
        self.version_constraints: Set[Tuple[str, vn.VersionList]] = set()
        self.target_constraints: Set[spack.target.Target] = set()
        self.default_targets: List[Tuple[int, str]] = []
        self.compiler_version_constraints: Set[spack.spec.CompilerSpec] = set()

        # hashes we've already added facts for
        self.seen_hashes: Set[str] = set()
        self.reusable_and_possible: Dict[str, spack.spec.Spec] = {}

        # id for dummy variables
        self._condition_id_counter = itertools.count()
        self._trigger_id_counter = itertools.count()
        self._trigger_cache: Dict[
            str, Dict[str, Tuple[int, AspFunction]]
        ] = collections.defaultdict(dict)
        self._effect_id_counter = itertools.count()
        self._effect_cache: Dict[
            str, Dict[str, Tuple[int, AspFunction]]
        ] = collections.defaultdict(dict)

        # Caches to optimize the setup phase of the solver
        self.target_specs_cache = None

        # whether to add installed/binary hashes to the solve
        self.tests = tests

        # If False allows for input specs that are not solved
        self.concretize_everything = True

        # Set during the call to setup
        self.pkgs: Set[str] = set()

    def pkg_version_rules(self, pkg):
        """Output declared versions of a package.

        This uses self.declared_versions so that we include any versions
        that arise from a spec.
        """

        def key_fn(version):
            # Origins are sorted by "provenance" first, see the Provenance enumeration above
            return version.origin, version.idx

        pkg = self._packagize(pkg)
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

    def _packagize(self, pkg):
        if isinstance(pkg, str):
            return self.repository.get_pkg_class(pkg)
        else:
            return pkg

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
        default_msg = "{0}: '{1}' conflicts with '{2}'"
        no_constraint_msg = "{0}: conflicts with '{1}'"
        for trigger, constraints in pkg.conflicts.items():
            trigger_msg = "conflict trigger %s" % str(trigger)
            trigger_spec = spack.spec.Spec(trigger)
            trigger_id = self.condition(
                trigger_spec, name=trigger_spec.name or pkg.name, msg=trigger_msg
            )

            for constraint, conflict_msg in constraints:
                if conflict_msg is None:
                    if constraint == spack.spec.Spec():
                        conflict_msg = no_constraint_msg.format(pkg.name, trigger)
                    else:
                        conflict_msg = default_msg.format(pkg.name, trigger, constraint)
                constraint_msg = "conflict constraint %s" % str(constraint)
                constraint_id = self.condition(constraint, name=pkg.name, msg=constraint_msg)
                self.gen.fact(
                    fn.pkg_fact(pkg.name, fn.conflict(trigger_id, constraint_id, conflict_msg))
                )
                self.gen.newline()

    def compiler_facts(self):
        """Facts about available compilers."""

        self.gen.h2("Available compilers")
        indexed_possible_compilers = list(enumerate(self.possible_compilers))
        for compiler_id, compiler in indexed_possible_compilers:
            self.gen.fact(fn.compiler_id(compiler_id))
            self.gen.fact(fn.compiler_name(compiler_id, compiler.spec.name))
            self.gen.fact(fn.compiler_version(compiler_id, compiler.spec.version))

            if compiler.operating_system:
                self.gen.fact(fn.compiler_os(compiler_id, compiler.operating_system))

            if compiler.target == "any":
                compiler.target = None

            if compiler.target is not None:
                self.gen.fact(fn.compiler_target(compiler_id, compiler.target))

            for flag_type, flags in compiler.flags.items():
                for flag in flags:
                    self.gen.fact(fn.compiler_flag(compiler_id, flag_type, flag))

            self.gen.newline()

        # Set compiler defaults, given a list of possible compilers
        self.gen.h2("Default compiler preferences (CompilerID, Weight)")

        ppk = spack.package_prefs.PackagePrefs("all", "compiler", all=False)
        matches = sorted(indexed_possible_compilers, key=lambda x: ppk(x[1].spec))

        for weight, (compiler_id, cspec) in enumerate(matches):
            f = fn.default_compiler_preference(compiler_id, weight)
            self.gen.fact(f)

    def package_compiler_defaults(self, pkg):
        """Facts about packages' compiler prefs."""

        packages = self.configuration.get("packages")
        pkg_prefs = packages.get(pkg.name)
        if not pkg_prefs or "compiler" not in pkg_prefs:
            return

        compiler_list = self.possible_compilers
        compiler_list = sorted(compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs(pkg.name, "compiler", all=False)
        matches = sorted(compiler_list, key=lambda x: ppk(x.spec))

        for i, compiler in enumerate(reversed(matches)):
            self.gen.fact(
                fn.pkg_fact(
                    pkg.name,
                    fn.node_compiler_preference(
                        compiler.spec.name, compiler.spec.version, -i * 100
                    ),
                )
            )

    def package_requirement_rules(self, pkg):
        rules = self.requirement_rules_from_package_py(pkg)
        rules.extend(self.requirement_rules_from_packages_yaml(pkg))
        self.emit_facts_from_requirement_rules(rules)

    def requirement_rules_from_package_py(self, pkg):
        rules = []
        for requirements, conditions in pkg.requirements.items():
            for when_spec, policy, message in conditions:
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

    def requirement_rules_from_packages_yaml(self, pkg):
        pkg_name = pkg.name
        packages_yaml = self.configuration.get("packages")
        requirements = packages_yaml.get(pkg_name, {}).get("require", [])
        kind = RequirementKind.PACKAGE
        if not requirements:
            requirements = packages_yaml.get("all", {}).get("require", [])
            kind = RequirementKind.DEFAULT
        return self._rules_from_requirements(pkg_name, requirements, kind=kind)

    def _rules_from_requirements(self, pkg_name: str, requirements, *, kind: RequirementKind):
        """Manipulate requirements from packages.yaml, and return a list of tuples
        with a uniform structure (name, policy, requirements).
        """
        if isinstance(requirements, str):
            rules = [self._rule_from_str(pkg_name, requirements, kind)]
        else:
            rules = []
            for requirement in requirements:
                if isinstance(requirement, str):
                    # A string represents a spec that must be satisfied. It is
                    # equivalent to a one_of group with a single element
                    rules.append(self._rule_from_str(pkg_name, requirement, kind))
                else:
                    for policy in ("spec", "one_of", "any_of"):
                        if policy in requirement:
                            constraints = requirement[policy]

                            # "spec" is for specifying a single spec
                            if policy == "spec":
                                constraints = [constraints]
                                policy = "one_of"

                            rules.append(
                                RequirementRule(
                                    pkg_name=pkg_name,
                                    policy=policy,
                                    requirements=constraints,
                                    kind=kind,
                                    message=requirement.get("message"),
                                    condition=requirement.get("when"),
                                )
                            )
        return rules

    def _rule_from_str(
        self, pkg_name: str, requirements: str, kind: RequirementKind
    ) -> RequirementRule:
        return RequirementRule(
            pkg_name=pkg_name,
            policy="one_of",
            requirements=[requirements],
            kind=kind,
            condition=None,
            message=None,
        )

    def pkg_rules(self, pkg, tests):
        pkg = self._packagize(pkg)

        # versions
        self.pkg_version_rules(pkg)
        self.gen.newline()

        # variants
        self.variant_rules(pkg)

        # conflicts
        self.conflict_rules(pkg)

        # default compilers for this package
        self.package_compiler_defaults(pkg)

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
        self.gen.h2("Trigger conditions")
        for name in self._trigger_cache:
            cache = self._trigger_cache[name]
            for spec_str, (trigger_id, requirements) in cache.items():
                self.gen.fact(fn.pkg_fact(name, fn.trigger_id(trigger_id)))
                self.gen.fact(fn.pkg_fact(name, fn.trigger_msg(spec_str)))
                for predicate in requirements:
                    self.gen.fact(fn.condition_requirement(trigger_id, *predicate.args))
                self.gen.newline()
        self._trigger_cache.clear()

    def effect_rules(self):
        """Flushes all the effect rules collected so far, and clears the cache."""
        self.gen.h2("Imposed requirements")
        for name in self._effect_cache:
            cache = self._effect_cache[name]
            for spec_str, (effect_id, requirements) in cache.items():
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

    def condition(self, required_spec, imposed_spec=None, name=None, msg=None, node=False):
        """Generate facts for a dependency or virtual provider condition.

        Arguments:
            required_spec (spack.spec.Spec): the spec that triggers this condition
            imposed_spec (spack.spec.Spec or None): the spec with constraints that
                are imposed when this condition is triggered
            name (str or None): name for `required_spec` (required if
                required_spec is anonymous, ignored if not)
            msg (str or None): description of the condition
            node (bool): if False does not emit "node" or "virtual_node" requirements
                from the imposed spec
        Returns:
            int: id of the condition created by this function
        """
        named_cond = required_spec.copy()
        named_cond.name = named_cond.name or name
        assert named_cond.name, "must provide name for anonymous conditions!"

        # Check if we can emit the requirements before updating the condition ID counter.
        # In this way, if a condition can't be emitted but the exception is handled in the caller,
        # we won't emit partial facts.

        condition_id = next(self._condition_id_counter)
        self.gen.fact(fn.pkg_fact(named_cond.name, fn.condition(condition_id)))
        self.gen.fact(fn.condition_reason(condition_id, msg))

        cache = self._trigger_cache[named_cond.name]

        named_cond_key = str(named_cond)
        if named_cond_key not in cache:
            trigger_id = next(self._trigger_id_counter)
            requirements = self.spec_clauses(named_cond, body=True, required_from=name)
            cache[named_cond_key] = (trigger_id, requirements)
        trigger_id, requirements = cache[named_cond_key]
        self.gen.fact(fn.pkg_fact(named_cond.name, fn.condition_trigger(condition_id, trigger_id)))

        if not imposed_spec:
            return condition_id

        cache = self._effect_cache[named_cond.name]
        imposed_spec_key = str(imposed_spec)
        if imposed_spec_key not in cache:
            effect_id = next(self._effect_id_counter)
            requirements = self.spec_clauses(imposed_spec, body=False, required_from=name)
            if not node:
                requirements = list(
                    filter(lambda x: x.args[0] not in ("node", "virtual_node"), requirements)
                )
            cache[imposed_spec_key] = (effect_id, requirements)
        effect_id, requirements = cache[imposed_spec_key]
        self.gen.fact(fn.pkg_fact(named_cond.name, fn.condition_effect(condition_id, effect_id)))
        return condition_id

    def impose(self, condition_id, imposed_spec, node=True, name=None, body=False):
        imposed_constraints = self.spec_clauses(imposed_spec, body=body, required_from=name)
        for pred in imposed_constraints:
            # imposed "node"-like conditions are no-ops
            if not node and pred.args[0] in ("node", "virtual_node"):
                continue
            self.gen.fact(fn.imposed_constraint(condition_id, *pred.args))

    def package_provider_rules(self, pkg):
        for provider_name in sorted(set(s.name for s in pkg.provided.keys())):
            if provider_name not in self.possible_virtuals:
                continue
            self.gen.fact(fn.pkg_fact(pkg.name, fn.possible_provider(provider_name)))

        for provided, whens in pkg.provided.items():
            if provided.name not in self.possible_virtuals:
                continue
            for when in whens:
                msg = "%s provides %s when %s" % (pkg.name, provided, when)
                condition_id = self.condition(when, provided, pkg.name, msg)
                self.gen.fact(
                    fn.pkg_fact(when.name, fn.provider_condition(condition_id, provided.name))
                )
            self.gen.newline()

    def package_dependencies_rules(self, pkg):
        """Translate 'depends_on' directives into ASP logic."""
        for _, conditions in sorted(pkg.dependencies.items()):
            for cond, dep in sorted(conditions.items()):
                deptypes = dep.type.copy()
                # Skip test dependencies if they're not requested
                if not self.tests:
                    deptypes.discard("test")

                # ... or if they are requested only for certain packages
                if not isinstance(self.tests, bool) and pkg.name not in self.tests:
                    deptypes.discard("test")

                # if there are no dependency types to be considered
                # anymore, don't generate the dependency
                if not deptypes:
                    continue

                msg = "%s depends on %s" % (pkg.name, dep.spec.name)
                if cond != spack.spec.Spec():
                    msg += " when %s" % cond
                else:
                    pass

                condition_id = self.condition(cond, dep.spec, pkg.name, msg)
                self.gen.fact(
                    fn.pkg_fact(pkg.name, fn.dependency_condition(condition_id, dep.spec.name))
                )

                for t in sorted(deptypes):
                    # there is a declared dependency of type t
                    self.gen.fact(fn.dependency_type(condition_id, t))

                self.gen.newline()

    def virtual_preferences(self, pkg_name, func):
        """Call func(vspec, provider, i) for each of pkg's provider prefs."""
        packages_yaml = self.configuration.get("packages")
        pkg_prefs = packages_yaml.get(pkg_name, {}).get("providers", {})
        for vspec, providers in pkg_prefs.items():
            if vspec not in self.possible_virtuals:
                continue

            for i, provider in enumerate(providers):
                provider_name = spack.spec.Spec(provider).name
                func(vspec, provider_name, i)

    def provider_defaults(self):
        self.gen.h2("Default virtual providers")
        self.virtual_preferences(
            "all", lambda v, p, i: self.gen.fact(fn.default_provider_preference(v, p, i))
        )

    def provider_requirements(self):
        self.gen.h2("Requirements on virtual providers")
        packages_yaml = self.configuration.get("packages")
        for virtual_str in sorted(self.possible_virtuals):
            requirements = packages_yaml.get(virtual_str, {}).get("require", [])
            rules = self._rules_from_requirements(
                virtual_str, requirements, kind=RequirementKind.VIRTUAL
            )
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
            main_requirement_condition = spack.directives.make_when_spec(rule.condition)
            if main_requirement_condition is False:
                continue

            # Write explicitly if a requirement is conditional or not
            if main_requirement_condition != spack.spec.Spec():
                msg = f"condition to activate requirement {requirement_grp_id}"
                try:
                    main_condition_id = self.condition(
                        main_requirement_condition, name=pkg_name, msg=msg
                    )
                except Exception as e:
                    if rule.kind != RequirementKind.DEFAULT:
                        raise RuntimeError("cannot emit requirements for the solver") from e
                    continue

                self.gen.fact(
                    fn.requirement_conditional(pkg_name, requirement_grp_id, main_condition_id)
                )

            self.gen.fact(fn.requirement_group(pkg_name, requirement_grp_id))
            self.gen.fact(fn.requirement_policy(pkg_name, requirement_grp_id, policy))
            if rule.message:
                self.gen.fact(fn.requirement_message(pkg_name, requirement_grp_id, rule.message))
            self.gen.newline()

            for spec_str in requirement_grp:
                spec = spack.spec.Spec(spec_str)
                if not spec.name:
                    spec.name = pkg_name
                spec.attach_git_version_lookup()

                when_spec = spec
                if virtual:
                    when_spec = spack.spec.Spec(pkg_name)

                try:
                    member_id = self.condition(
                        required_spec=when_spec, imposed_spec=spec, name=pkg_name, node=virtual
                    )
                except Exception as e:
                    # Do not raise if the rule comes from the 'all' subsection, since usability
                    # would be impaired. If a rule does not apply for a specific package, just
                    # discard it.
                    if rule.kind != RequirementKind.DEFAULT:
                        raise RuntimeError("cannot emit requirements for the solver") from e
                    continue

                self.gen.fact(fn.requirement_group_member(member_id, pkg_name, requirement_grp_id))
                self.gen.fact(fn.requirement_has_weight(member_id, requirement_weight))
                self.gen.newline()
                requirement_weight += 1

    def external_packages(self):
        """Facts on external packages, as read from packages.yaml"""
        # Read packages.yaml and normalize it, so that it
        # will not contain entries referring to virtual
        # packages.
        packages_yaml = self.configuration.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml, repository=self.repository)

        self.gen.h1("External packages")
        for pkg_name, data in packages_yaml.items():
            if pkg_name == "all":
                continue

            # This package does not appear in any repository
            if pkg_name not in self.repository:
                continue

            self.gen.h2("External package: {0}".format(pkg_name))
            # Check if the external package is buildable. If it is
            # not then "external(<pkg>)" is a fact, unless we can
            # reuse an already installed spec.
            external_buildable = data.get("buildable", True)
            if not external_buildable:
                self.gen.fact(fn.buildable_false(pkg_name))

            # Read a list of all the specs for this package
            externals = data.get("externals", [])
            external_specs = [spack.spec.parse_with_version_concrete(x["spec"]) for x in externals]

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
                condition_id = self.condition(spec, msg=msg)
                self.gen.fact(fn.pkg_fact(pkg_name, fn.possible_external(condition_id, local_idx)))
                self.possible_versions[spec.name].add(spec.version)
                self.gen.newline()

            self.trigger_rules()

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
            spec.update_variant_validate(variant_name, values)

            for value in values:
                self.variant_values_from_specs.add((pkg_name, variant.name, value))
                self.gen.fact(
                    fn.variant_default_value_from_packages_yaml(pkg_name, variant.name, value)
                )

    def target_preferences(self, pkg_name):
        key_fn = spack.package_prefs.PackagePrefs(pkg_name, "target")

        if not self.target_specs_cache:
            self.target_specs_cache = [
                spack.spec.Spec("target={0}".format(target_name))
                for _, target_name in self.default_targets
            ]

        package_targets = self.target_specs_cache[:]
        package_targets.sort(key=key_fn)

        offset = 0
        best_default = self.default_targets[0][1]
        for i, preferred in enumerate(package_targets):
            if str(preferred.architecture.target) == best_default and i != 0:
                offset = 100
            self.gen.fact(
                fn.pkg_fact(
                    pkg_name, fn.target_weight(str(preferred.architecture.target), i + offset)
                )
            )

    def spec_clauses(self, *args, **kwargs):
        """Wrap a call to `_spec_clauses()` into a try/except block that
        raises a comprehensible error message in case of failure.
        """
        requestor = kwargs.pop("required_from", None)
        try:
            clauses = self._spec_clauses(*args, **kwargs)
        except RuntimeError as exc:
            msg = str(exc)
            if requestor:
                msg += ' [required from package "{0}"]'.format(requestor)
            raise RuntimeError(msg)
        return clauses

    def _spec_clauses(
        self, spec, body=False, transitive=True, expand_hashes=False, concrete_build_deps=False
    ):
        """Return a list of clauses for a spec mandates are true.

        Arguments:
            spec (spack.spec.Spec): the spec to analyze
            body (bool): if True, generate clauses to be used in rule bodies
                (final values) instead of rule heads (setters).
            transitive (bool): if False, don't generate clauses from
                dependencies (default True)
            expand_hashes (bool): if True, descend into hashes of concrete specs
                (default False)
            concrete_build_deps (bool): if False, do not include pure build deps
                of concrete specs (as they have no effect on runtime constraints)

        Normally, if called with ``transitive=True``, ``spec_clauses()`` just generates
        hashes for the dependency requirements of concrete specs. If ``expand_hashes``
        is ``True``, we'll *also* output all the facts implied by transitive hashes,
        which are redundant during a solve but useful outside of one (e.g.,
        for spec ``diff``).
        """
        clauses = []

        # TODO: do this with consistent suffixes.
        class Head:
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
            variant_propagate = fn.attr("variant_propagate")

        class Body:
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
            variant_propagate = fn.attr("variant_propagate")

        f = Body if body else Head

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
                        pkg_cls = self.repository.get_pkg_class(spec.name)
                        try:
                            variant_def, _ = pkg_cls.variants[vname]
                        except KeyError:
                            msg = 'variant "{0}" not found in package "{1}"'
                            raise RuntimeError(msg.format(vname, spec.name))
                        else:
                            variant_def.validate_or_raise(
                                variant, self.repository.get_pkg_class(spec.name)
                            )

                clauses.append(f.variant_value(spec.name, vname, value))

                if variant.propagate:
                    clauses.append(f.variant_propagate(spec.name, vname, value, spec.name))

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

            elif spec.compiler.versions:
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
            if getattr(spec, "_package_hash", None):
                clauses.append(fn.attr("package_hash", spec.name, spec._package_hash))
            clauses.append(fn.attr("hash", spec.name, spec.dag_hash()))

        # add all clauses from dependencies
        if transitive:
            # TODO: Eventually distinguish 2 deps on the same pkg (build and link)
            for dspec in spec.edges_to_dependencies():
                dep = dspec.spec

                if spec.concrete:
                    # We know dependencies are real for concrete specs. For abstract
                    # specs they just mean the dep is somehow in the DAG.
                    for dtype in dspec.deptypes:
                        # skip build dependencies of already-installed specs
                        if concrete_build_deps or dtype != "build":
                            clauses.append(fn.attr("depends_on", spec.name, dep.name, dtype))
                            for virtual_name in dspec.virtuals:
                                clauses.append(
                                    fn.attr("virtual_on_edge", spec.name, dep.name, virtual_name)
                                )
                                clauses.append(fn.attr("virtual_node", virtual_name))

                    # imposing hash constraints for all but pure build deps of
                    # already-installed concrete specs.
                    if concrete_build_deps or dspec.deptypes != ("build",):
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

    def build_version_dict(self, possible_pkgs):
        """Declare any versions in specs not declared in packages."""
        packages_yaml = self.configuration.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml, repository=self.repository)
        for pkg_name in possible_pkgs:
            pkg_cls = self.repository.get_pkg_class(pkg_name)

            # All the versions from the corresponding package.py file. Since concepts
            # like being a "develop" version or being preferred exist only at a
            # package.py level, sort them in this partial list here
            def key_fn(item):
                version, info = item
                # When COMPARING VERSIONS, the '@develop' version is always
                # larger than other versions. BUT when CONCRETIZING, the largest
                # NON-develop version is selected by default.
                return (
                    info.get("preferred", False),
                    not info.get("deprecated", False),
                    not version.isdevelop(),
                    version,
                )

            for idx, item in enumerate(sorted(pkg_cls.versions.items(), key=key_fn, reverse=True)):
                v, version_info = item
                self.possible_versions[pkg_name].add(v)
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=v, idx=idx, origin=Provenance.PACKAGE_PY)
                )
                deprecated = version_info.get("deprecated", False)
                if deprecated:
                    self.deprecated_versions[pkg_name].add(v)

            # All the preferred version from packages.yaml, versions in external
            # specs will be computed later
            version_preferences = packages_yaml.get(pkg_name, {}).get("version", [])
            version_defs = []
            pkg_class = self.repository.get_pkg_class(pkg_name)
            for vstr in version_preferences:
                v = vn.ver(vstr)
                if isinstance(v, vn.GitVersion):
                    version_defs.append(v)
                else:
                    satisfying_versions = self._check_for_defined_matching_versions(pkg_class, v)
                    # Amongst all defined versions satisfying this specific
                    # preference, the highest-numbered version is the
                    # most-preferred: therefore sort satisfying versions
                    # from greatest to least
                    version_defs.extend(sorted(satisfying_versions, reverse=True))

            for weight, vdef in enumerate(llnl.util.lang.dedupe(version_defs)):
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=vdef, idx=weight, origin=Provenance.PACKAGES_YAML)
                )
                self.possible_versions[pkg_name].add(vdef)

    def _check_for_defined_matching_versions(self, pkg_class, v):
        """Given a version specification (which may be a concrete version,
        range, etc.), determine if any package.py version declarations
        or externals define a version which satisfies it.

        This is primarily for determining whether a version request (e.g.
        version preferences, which should not themselves define versions)
        refers to a defined version.

        This function raises an exception if no satisfying versions are
        found.
        """
        pkg_name = pkg_class.name
        satisfying_versions = list(x for x in pkg_class.versions if x.satisfies(v))
        satisfying_versions.extend(x for x in self.possible_versions[pkg_name] if x.satisfies(v))
        if not satisfying_versions:
            raise spack.config.ConfigError(
                "Preference for version {0} does not match any version"
                " defined for {1} (in its package.py or any external)".format(str(v), pkg_name)
            )
        return satisfying_versions

    def add_concrete_versions_from_specs(self, specs, origin):
        """Add concrete versions to possible versions from lists of CLI/dev specs."""
        for s in spack.traverse.traverse_nodes(specs):
            # If there is a concrete version on the CLI *that we know nothing
            # about*, add it to the known versions. Use idx=0, which is the
            # best possible, so they're guaranteed to be used preferentially.
            version = s.versions.concrete

            if version is None or any(v == version for v in self.possible_versions[s.name]):
                continue

            self.declared_versions[s.name].append(
                DeclaredVersion(version=version, idx=0, origin=origin)
            )
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
                    target.optimization_flags(compiler_name, compiler_version)
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
        granularity = self.configuration.get("concretizer:targets:granularity")
        host_compatible = self.configuration.get("concretizer:targets:host_compatible")

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
        for compiler_id, compiler in enumerate(self.possible_compilers):
            # Stub support for cross-compilation, to be expanded later
            if compiler.target is not None and compiler.target != str(uarch.family):
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

    def virtual_providers(self):
        self.gen.h2("Virtual providers")
        for vspec in sorted(self.possible_virtuals):
            self.gen.fact(fn.virtual(vspec))
        self.gen.newline()

    def generate_possible_compilers(self, specs):
        compilers = all_compilers_in_config()

        # Search for compilers which differs only by aspects that are
        # not selectable by users using the spec syntax
        seen, sanitized_list = set(), []
        for compiler in compilers:
            key = compiler.spec, compiler.operating_system, compiler.target
            if key in seen:
                warnings.warn(
                    f"duplicate found for {compiler.spec} on "
                    f"{compiler.operating_system}/{compiler.target}. "
                    f"Edit your compilers.yaml configuration to remove it."
                )
                continue
            sanitized_list.append(compiler)
            seen.add(key)

        cspecs = set([c.spec for c in compilers])

        # add compiler specs from the input line to possibilities if we
        # don't require compilers to exist.
        strict = spack.concretize.Concretizer().check_for_compiler_existence
        for s in spack.traverse.traverse_nodes(specs):
            # we don't need to validate compilers for already-built specs
            if s.concrete or not s.compiler:
                continue

            version = s.compiler.versions.concrete

            if not version or any(c.satisfies(s.compiler) for c in cspecs):
                continue

            # Error when a compiler is not found and strict mode is enabled
            if strict:
                raise spack.concretize.UnavailableCompilerVersionError(s.compiler)

            # Make up a compiler matching the input spec. This is for bootstrapping.
            compiler_cls = spack.compilers.class_for_compiler_name(s.compiler.name)
            compilers.append(
                compiler_cls(s.compiler, operating_system=None, target=None, paths=[None] * 4)
            )
            self.gen.fact(fn.allow_compiler(s.compiler.name, version))

        return list(
            sorted(
                compilers,
                key=lambda compiler: (compiler.spec.name, compiler.spec.version),
                reverse=True,
            )
        )

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
            if not self.repository.is_virtual(pkg_name):
                continue
            constraint_map[pkg_name].add(versions)

        # extract all the real versions mentioned in version ranges
        def versions_for(v):
            if isinstance(v, vn.StandardVersion):
                return [v]
            elif isinstance(v, vn.ClosedOpenRange):
                return [v.lo, vn.prev_version(v.hi)]
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

    def _facts_from_concrete_spec(self, spec, possible):
        # tell the solver about any installed packages that could
        # be dependencies (don't tell it about the others)
        h = spec.dag_hash()
        if spec.name in possible and h not in self.seen_hashes:
            self.reusable_and_possible[h] = spec
            try:
                # Only consider installed packages for repo we know
                self.repository.get(spec)
            except (spack.repo.UnknownNamespaceError, spack.repo.UnknownPackageError):
                return

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

            # add the hash to the one seen so far
            self.seen_hashes.add(h)

    def define_concrete_input_specs(self, specs, possible):
        # any concrete specs in the input spec list
        for input_spec in specs:
            for spec in input_spec.traverse():
                if spec.concrete:
                    self._facts_from_concrete_spec(spec, possible)

    def setup(
        self, specs: List[spack.spec.Spec], reuse: Optional[List[spack.spec.Spec]] = None
    ) -> None:
        """Generate an ASP program with relevant constraints for specs.

        This calls methods on the solve driver to set up the problem with
        facts and rules from all possible dependencies of the input
        specs, as well as constraints from the specs themselves.

        Arguments:
            driver: driver instance of this solve
            specs: list of Specs to solve
            reuse: list of concrete specs that can be reused
        """
        self._condition_id_counter = itertools.count()

        # preliminary checks
        self.check_packages_exist(specs)

        # get list of all possible dependencies
        self.possible_virtuals = set(x.name for x in specs if x.virtual)

        node_counter = self._create_counter(specs, tests=self.tests)
        self.possible_virtuals = node_counter.possible_virtuals()
        self.pkgs = node_counter.possible_dependencies()

        # Fail if we already know an unreachable node is requested
        for spec in specs:
            missing_deps = [
                str(d) for d in spec.traverse() if d.name not in self.pkgs and not d.virtual
            ]
            if missing_deps:
                raise spack.spec.InvalidDependencyError(spec.name, missing_deps)

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

        # get possible compilers
        self.possible_compilers = self.generate_possible_compilers(specs)

        self.gen.h1("Concrete input spec definitions")
        self.define_concrete_input_specs(specs, self.pkgs)

        if reuse is not None:
            self.gen.h1("Reusable specs")
            self.gen.fact(fn.optimize_for_reuse())
            for reusable_spec in reuse:
                self._facts_from_concrete_spec(reusable_spec, self.pkgs)

        self.gen.h1("Generic statements on possible packages")
        node_counter.possible_packages_facts(self.gen, fn)

        self.gen.h1("Possible flags on nodes")
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            self.gen.fact(fn.flag_type(flag))
        self.gen.newline()

        self.gen.h1("General Constraints")
        self.compiler_facts()

        # architecture defaults
        self.platform_defaults()
        self.os_defaults(specs + dev_specs)
        self.target_defaults(specs + dev_specs)

        self.virtual_providers()
        self.provider_defaults()
        self.provider_requirements()
        self.external_packages()

        # traverse all specs and packages to build dict of possible versions
        self.build_version_dict(self.pkgs)
        self.add_concrete_versions_from_specs(specs, Provenance.SPEC)
        self.add_concrete_versions_from_specs(dev_specs, Provenance.DEV_SPEC)

        req_version_specs = self._get_versioned_specs_from_pkg_requirements()
        self.add_concrete_versions_from_specs(req_version_specs, Provenance.PACKAGE_REQUIREMENT)

        self.gen.h1("Package Constraints")
        for pkg in sorted(self.pkgs):
            self.gen.h2("Package rules: %s" % pkg)
            self.pkg_rules(pkg, tests=self.tests)
            self.gen.h2("Package preferences: %s" % pkg)
            self.preferred_variants(pkg)
            self.target_preferences(pkg)

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

        self.gen.h1("Version Constraints")
        self.collect_virtual_constraints()
        self.define_version_constraints()

        self.gen.h1("Compiler Version Constraints")
        self.define_compiler_version_constraints()

        self.gen.h1("Target Constraints")
        self.define_target_constraints()

    def check_packages_exist(self, specs):
        """Ensure all packages mentioned in specs exist."""
        for spec in specs:
            for s in spec.traverse():
                try:
                    check_passed = self.repository.exists(s.name) or self.repository.is_virtual(
                        s.name
                    )
                except Exception as e:
                    msg = "Cannot find package: {0}".format(str(e))
                    check_passed = False
                    tty.debug(msg)

                if not check_passed:
                    raise spack.repo.UnknownPackageError(str(s.fullname))

    def literal_specs(self, specs):
        for idx, spec in enumerate(specs):
            self.gen.h2("Spec: %s" % str(spec))
            self.gen.fact(fn.literal(idx))

            self.gen.fact(fn.literal(idx, "virtual_root" if spec.virtual else "root", spec.name))
            for clause in self.spec_clauses(spec):
                self.gen.fact(fn.literal(idx, *clause.args))
                if clause.args[0] == "variant_set":
                    self.gen.fact(
                        fn.literal(idx, "variant_default_value_from_cli", *clause.args[1:])
                    )

            if self.concretize_everything:
                self.gen.fact(fn.solve_literal(idx))

    def _get_versioned_specs_from_pkg_requirements(self):
        """If package requirements mention versions that are not mentioned
        elsewhere, then we need to collect those to mark them as possible
        versions.
        """
        req_version_specs = list()
        config = self.configuration.get("packages")
        for pkg_name, d in config.items():
            if pkg_name == "all":
                continue
            if "require" in d:
                req_version_specs.extend(self._specs_from_requires(pkg_name, d["require"]))
        return req_version_specs

    def _specs_from_requires(self, pkg_name, section):
        """Collect specs from requirements which define versions (i.e. those that
        have a concrete version). Requirements can define *new* versions if
        they are included as part of an equivalence (hash=number) but not
        otherwise.
        """
        if isinstance(section, str):
            spec = spack.spec.Spec(section)
            if not spec.name:
                spec.name = pkg_name
            extracted_specs = [spec]
        else:
            spec_strs = []
            for spec_group in section:
                if isinstance(spec_group, str):
                    spec_strs.append(spec_group)
                else:
                    # Otherwise it is an object. The object can contain a single
                    # "spec" constraint, or a list of them with "any_of" or
                    # "one_of" policy.
                    if "spec" in spec_group:
                        new_constraints = [spec_group["spec"]]
                    else:
                        key = "one_of" if "one_of" in spec_group else "any_of"
                        new_constraints = spec_group[key]
                    spec_strs.extend(new_constraints)

            extracted_specs = []
            for spec_str in spec_strs:
                spec = spack.spec.Spec(spec_str)
                if not spec.name:
                    spec.name = pkg_name
                extracted_specs.append(spec)

        version_specs = []
        for spec in extracted_specs:
            if spec.versions.concrete:
                # Note: this includes git versions
                version_specs.append(spec)
                continue

            # Prefer spec's name if it exists, in case the spec is
            # requiring a specific implementation inside of a virtual section
            # e.g. packages:mpi:require:openmpi@4.0.1
            pkg_class = self.repository.get_pkg_class(spec.name or pkg_name)
            satisfying_versions = self._check_for_defined_matching_versions(
                pkg_class, spec.versions
            )

            # Version ranges ("@1.3" without the "=", "@1.2:1.4") and lists
            # will end up here
            ordered_satisfying_versions = sorted(satisfying_versions, reverse=True)
            vspecs = list(spack.spec.Spec("@{0}".format(x)) for x in ordered_satisfying_versions)
            version_specs.extend(vspecs)

        for spec in version_specs:
            spec.attach_git_version_lookup()
        return version_specs

    def _create_counter(self, specs, tests):
        strategy = self.configuration.get("concretizer:duplicates:strategy", "none")
        if strategy == "full":
            return FullDuplicatesCounter(specs, repository=self.repository, tests=tests)
        if strategy == "minimal":
            return MinimalDuplicatesCounter(specs, repository=self.repository, tests=tests)
        return NoDuplicatesCounter(specs, repository=self.repository, tests=tests)


class SpecBuilder:
    """Class with actions to rebuild a spec from ASP results."""

    #: Regex for attributes that don't need actions b/c they aren't used to construct specs.
    ignored_attributes = re.compile(
        "|".join(
            [
                r"^.*_propagate$",
                r"^.*_satisfies$",
                r"^.*_set$",
                r"^node_compiler$",
                r"^package_hash$",
                r"^root$",
                r"^virtual_node$",
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

    def __init__(self, *, specs, configuration, hash_lookup=None):
        self._specs = {}
        self._result = None
        self._command_line_specs = specs
        self._hash_specs = []
        self._flag_sources = collections.defaultdict(lambda: set())
        self._flag_compiler_defaults = set()

        # Pass in as arguments reusable specs and plug them in
        # from this dictionary during reconstruction
        self._hash_lookup = hash_lookup or {}
        self.configuration = configuration
        self.repository = spack.repo.create(self.configuration)

    def hash(self, node, h):
        if node not in self._specs:
            self._specs[node] = self._hash_lookup[h]
        self._hash_specs.append(node)

    def node(self, node):
        if node not in self._specs:
            self._specs[node] = spack.spec.Spec(node.pkg)

    def _arch(self, node):
        arch = self._specs[node].architecture
        if not arch:
            arch = spack.spec.ArchSpec()
            self._specs[node].architecture = arch
        return arch

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
        """This means that the external spec and index idx
        has been selected for this package.
        """

        packages_yaml = self.configuration.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml, repository=self.repository)
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

        if not edges:
            self._specs[parent_node].add_dependency_edge(
                self._specs[dependency_node], deptypes=(type,), virtuals=()
            )
        else:
            edges[0].update_deptypes(deptypes=(type,))

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
        compilers = dict((c.spec, c) for c in reversed(all_compilers_in_config()))
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

    def deprecated(self, pkg, version):
        msg = 'using "{0}@{1}" which is a deprecated version'
        tty.warn(msg.format(pkg, version))

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
                if self.repository.is_virtual(pkg):
                    continue

                # if we've already gotten a concrete spec for this pkg,
                # do not bother calling actions on it except for node_flag_source,
                # since node_flag_source is tracking information not in the spec itself
                spec = self._specs.get(args[0])
                if spec and spec.concrete:
                    if name != "node_flag_source":
                        continue

            action(*args)

        # namespace assignment is done after the fact, as it is not
        # currently part of the solve
        for spec in self._specs.values():
            if spec.namespace:
                continue
            repo = self.repository.repo_for_pkg(spec)
            spec.namespace = repo.namespace

        # fix flags after all specs are constructed
        self.reorder_flags()

        # cycle detection
        roots = [spec.root for spec in self._specs.values() if not spec.root.installed]

        # inject patches -- note that we' can't use set() to unique the
        # roots here, because the specs aren't complete, and the hash
        # function will loop forever.
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


class Solver:
    """This is the main external interface class for solving.

    It manages solver configuration and preferences in one place. It sets up the solve
    and passes the setup method to the driver, as well.

    Properties of interest:

      ``reuse (bool)``
        Whether to try to reuse existing installs/binaries

    """

    def __init__(self, configuration: spack.config.ConfigurationType) -> None:
        self.configuration = configuration
        self.driver = PyclingoDriver(configuration=self.configuration)

        # These properties are settable via spack configuration, and overridable
        # by setting them directly as properties.
        self.reuse = self.configuration.get("concretizer:reuse", False)

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

    def _reusable_specs(self, specs):
        reusable_specs = []
        current_store = spack.store.create(self.configuration)
        if self.reuse:
            # Specs from the local Database
            with current_store.db.read_transaction():
                reusable_specs.extend(
                    [
                        s
                        for s in current_store.db.query(installed=True)
                        if not s.satisfies("dev_path=*")
                    ]
                )

            # Specs from buildcaches
            try:
                index = spack.binary_distribution.update_cache_and_get_specs()
                reusable_specs.extend(index)
            except (spack.binary_distribution.FetchCacheError, IndexError):
                # this is raised when no mirrors had indices.
                # TODO: update mirror configuration so it can indicate that the
                # TODO: source cache (or any mirror really) doesn't have binaries.
                pass

        # If we only want to reuse dependencies, remove the root specs
        if self.reuse == "dependencies":
            reusable_specs = [
                spec for spec in reusable_specs if not any(root in spec for root in specs)
            ]

        return reusable_specs

    def solve(self, specs, out=None, timers=False, stats=False, tests=False, setup_only=False):
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
        """
        # Check upfront that the variants are admissible
        specs = [s.lookup_hash() for s in specs]
        reusable_specs = self._check_input_and_extract_concrete_specs(specs)
        reusable_specs.extend(self._reusable_specs(specs))
        setup = SpackSolverSetup(driver=self.driver, tests=tests)
        output = OutputConfiguration(timers=timers, stats=stats, out=out, setup_only=setup_only)
        result, _, _ = self.driver.solve(setup, specs, reuse=reusable_specs, output=output)
        return result

    def solve_in_rounds(self, specs, out=None, timers=False, stats=False, tests=False):
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
        """
        specs = [s.lookup_hash() for s in specs]
        reusable_specs = self._check_input_and_extract_concrete_specs(specs)
        reusable_specs.extend(self._reusable_specs(specs))
        setup = SpackSolverSetup(driver=self.driver, tests=tests)

        # Tell clingo that we don't have to solve all the inputs at once
        setup.concretize_everything = False

        input_specs = specs
        output = OutputConfiguration(timers=timers, stats=stats, out=out, setup_only=False)
        while True:
            result, _, _ = self.driver.solve(
                setup, input_specs, reuse=reusable_specs, output=output
            )
            yield result

            # If we don't have unsolved specs we are done
            if not result.unsolved_specs:
                break

            # This means we cannot progress with solving the input
            if not result.satisfiable or not result.specs:
                break

            input_specs = result.unsolved_specs
            for spec in result.specs:
                reusable_specs.extend(spec.traverse())


class UnsatisfiableSpecError(spack.error.UnsatisfiableSpecError):
    """
    Subclass for new constructor signature for new concretizer
    """

    def __init__(self, msg):
        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)
        self.provided = None
        self.required = None
        self.constraint_type = None


class InternalConcretizerError(spack.error.UnsatisfiableSpecError):
    """
    Subclass for new constructor signature for new concretizer
    """

    def __init__(self, provided, conflicts):
        msg = (
            "Spack concretizer internal error. Please submit a bug report and include the "
            "command, environment if applicable and the following error message."
            f"\n    {provided} is unsatisfiable, errors are:"
        )

        msg += "".join([f"\n    {conflict}" for conflict in conflicts])

        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)

        self.provided = provided

        # Add attribute expected of the superclass interface
        self.required = None
        self.constraint_type = None
