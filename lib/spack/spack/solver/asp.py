# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import division, print_function

import collections
import collections.abc
import copy
import itertools
import os
import pprint
import re
import types
import warnings

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
import spack.util.path
import spack.util.timer
import spack.variant
import spack.version

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
    control.configuration.solve.models = 0
    control.configuration.solver.heuristic = "Domain"
    control.configuration.solve.parallel_mode = "1"
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

#: Order of precedence for version origins. Topmost types are preferred.
version_origin_fields = [
    "spec",
    "dev_spec",
    "external",
    "packages_yaml",
    "package_py",
    "installed",
]

#: Look up version precedence strings by enum id
version_origin_str = {i: name for i, name in enumerate(version_origin_fields)}

#: Enumeration like object to mark version provenance
version_provenance = collections.namedtuple(  # type: ignore
    "VersionProvenance", version_origin_fields
)(**{name: i for i, name in enumerate(version_origin_fields)})

#: Named tuple to contain information on declared versions
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


def packagize(pkg):
    if isinstance(pkg, str):
        return spack.repo.path.get_pkg_class(pkg)
    else:
        return pkg


def specify(spec):
    if isinstance(spec, spack.spec.Spec):
        return spec
    return spack.spec.Spec(spec)


class AspObject(object):
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
    def __init__(self, name, args=None):
        self.name = name
        self.args = () if args is None else tuple(args)

    def _cmp_key(self):
        return (self.name, self.args)

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
            else:
                return clingo.String(str(arg))

        return clingo.Function(self.name, [argify(arg) for arg in self.args], positive=positive)

    def __str__(self):
        return "%s(%s)" % (self.name, ", ".join(str(_id(arg)) for arg in self.args))

    def __repr__(self):
        return str(self)


class AspFunctionBuilder(object):
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


def check_packages_exist(specs):
    """Ensure all packages mentioned in specs exist."""
    repo = spack.repo.path
    for spec in specs:
        for s in spec.traverse():
            try:
                check_passed = repo.exists(s.name) or repo.is_virtual(s.name)
            except Exception as e:
                msg = "Cannot find package: {0}".format(str(e))
                check_passed = False
                tty.debug(msg)

            if not check_passed:
                raise spack.repo.UnknownPackageError(str(s.fullname))


class Result(object):
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
            key = input_spec.name
            if input_spec.virtual:
                providers = [spec.name for spec in answer.values() if spec.package.provides(key)]
                key = providers[0]
            candidate = answer.get(key)

            if candidate and candidate.intersects(input_spec):
                self._concrete_specs.append(answer[key])
                self._concrete_specs_by_input[input_spec] = answer[key]
            else:
                self._unsolved_specs.append(input_spec)


def _normalize_packages_yaml(packages_yaml):
    normalized_yaml = copy.copy(packages_yaml)
    for pkg_name in packages_yaml:
        is_virtual = spack.repo.path.is_virtual(pkg_name)
        if pkg_name == "all" or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = normalized_yaml.pop(pkg_name)
        is_buildable = data.get("buildable", True)
        if not is_buildable:
            for provider in spack.repo.path.providers_for(pkg_name):
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


def stringify(sym):
    """Stringify symbols from clingo models.

    This will turn a ``clingo.Symbol`` into a string, or a sequence of ``clingo.Symbol``
    objects into a tuple of strings.

    """
    # TODO: simplify this when we no longer have to support older clingo versions.
    if isinstance(sym, (list, tuple)):
        return tuple(stringify(a) for a in sym)

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

    Pull out all the predicates with name ``predicate_name`` from the model, and return
    their stringified arguments as tuples.
    """
    return [stringify(sym.arguments) for sym in model if sym.name == predicate_name]


class PyclingoDriver(object):
    def __init__(self, cores=True):
        """Driver for the Python clingo interface.

        Arguments:
            cores (bool): whether to generate unsatisfiable cores for better
                error reporting.
        """
        bootstrap_clingo()

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

        self.out.write("%s.\n" % str(symbol))

        atom = self.backend.add_atom(symbol)

        # Only functions relevant for constructing bug reports for bad error messages
        # are assumptions, and only when using cores.
        choice = self.cores and symbol.name == "internal_error"
        self.backend.add_rule([atom], [], choice=choice)
        if choice:
            self.assumptions.append(atom)

    def handle_error(self, msg, *args):
        """Handle an error state derived by the solver."""
        msg = msg.format(*args)

        # For variant formatting, we sometimes have to construct specs
        # to format values properly. Find/replace all occurances of
        # Spec(...) with the string representation of the spec mentioned
        specs_to_construct = re.findall(r"Spec\(([^)]*)\)", msg)
        for spec_str in specs_to_construct:
            msg = msg.replace("Spec(%s)" % spec_str, str(spack.spec.Spec(spec_str)))

        # TODO: this raises early -- we should handle multiple errors if there are any.
        raise UnsatisfiableSpecError(msg)

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
            setup.setup(self, specs, reuse=reuse)
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
        self.control.load(os.path.join(parent_dir, "os_compatibility.lp"))
        self.control.load(os.path.join(parent_dir, "display.lp"))
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
        timer.stop("solve")

        # once done, construct the solve result
        result.satisfiable = solve_result.satisfiable

        if result.satisfiable:
            # get the best model
            builder = SpecBuilder(specs, hash_lookup=setup.reusable_and_possible)
            min_cost, best_model = min(models)

            # first check for errors
            error_args = extract_args(best_model, "error")
            errors = sorted((int(priority), msg, args) for priority, msg, *args in error_args)
            for _, msg, args in errors:
                self.handle_error(msg, *args)

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
                        "UNKNOWN SYMBOL: %s(%s)" % (sym.name, ", ".join(stringify(sym.arguments)))
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


class SpackSolverSetup(object):
    """Class to set up and run a Spack concretization solve."""

    def __init__(self, tests=False):
        self.gen = None  # set by setup()

        self.declared_versions = {}
        self.possible_versions = {}
        self.deprecated_versions = {}

        self.possible_virtuals = None
        self.possible_compilers = []
        self.possible_oses = set()
        self.variant_values_from_specs = set()
        self.version_constraints = set()
        self.target_constraints = set()
        self.default_targets = []
        self.compiler_version_constraints = set()
        self.post_facts = []

        # hashes we've already added facts for
        self.seen_hashes = set()
        self.reusable_and_possible = {}

        # id for dummy variables
        self._condition_id_counter = itertools.count()

        # Caches to optimize the setup phase of the solver
        self.target_specs_cache = None

        # whether to add installed/binary hashes to the solve
        self.tests = tests

        # If False allows for input specs that are not solved
        self.concretize_everything = True

        # Set during the call to setup
        self.pkgs = None

    def pkg_version_rules(self, pkg):
        """Output declared versions of a package.

        This uses self.declared_versions so that we include any versions
        that arise from a spec.
        """

        def key_fn(version):
            # Origins are sorted by precedence defined in `version_origin_str`,
            # then by order added.
            return version.origin, version.idx

        pkg = packagize(pkg)
        declared_versions = self.declared_versions[pkg.name]
        partially_sorted_versions = sorted(set(declared_versions), key=key_fn)

        most_to_least_preferred = []
        for _, group in itertools.groupby(partially_sorted_versions, key=key_fn):
            most_to_least_preferred.extend(
                list(sorted(group, reverse=True, key=lambda x: spack.version.ver(x.version)))
            )

        for weight, declared_version in enumerate(most_to_least_preferred):
            self.gen.fact(
                fn.version_declared(
                    pkg.name,
                    declared_version.version,
                    weight,
                    version_origin_str[declared_version.origin],
                )
            )

        for v in most_to_least_preferred:
            # There are two paths for creating the ref_version in GitVersions.
            # The first uses a lookup to supply a tag and distance as a version.
            # The second is user specified and can be resolved as a standard version.
            # This second option is constrained such that the user version must be known to Spack
            if (
                isinstance(v.version, spack.version.GitVersion)
                and v.version.user_supplied_reference
            ):
                ref_version = spack.version.Version(v.version.ref_version_str)
                self.gen.fact(fn.version_equivalent(pkg.name, v.version, ref_version))
                # disqualify any git supplied version from user if they weren't already known
                # versions in spack
                if not any(ref_version == dv.version for dv in most_to_least_preferred if v != dv):
                    msg = (
                        "The reference version '{version}' for package '{package}' is not defined."
                        " Either choose another reference version or define '{version}' in your"
                        " version preferences or package.py file for {package}.".format(
                            package=pkg.name, version=str(ref_version)
                        )
                    )

                    raise UnsatisfiableSpecError(msg)

        # Declare deprecated versions for this package, if any
        deprecated = self.deprecated_versions[pkg.name]
        for v in sorted(deprecated):
            self.gen.fact(fn.deprecated_version(pkg.name, v))

    def spec_versions(self, spec):
        """Return list of clauses expressing spec's version constraints."""
        spec = specify(spec)
        msg = "Internal Error: spec with no name occured. Please report to the spack maintainers."
        assert spec.name, msg

        if spec.concrete:
            return [fn.attr("version", spec.name, spec.version)]

        if spec.versions == spack.version.ver(":"):
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
        default_msg = "{0} '{1}' conflicts with '{2}'"
        no_constraint_msg = "{0} conflicts with '{1}'"
        for trigger, constraints in pkg.conflicts.items():
            trigger_msg = "conflict trigger %s" % str(trigger)
            trigger_id = self.condition(spack.spec.Spec(trigger), name=pkg.name, msg=trigger_msg)

            for constraint, conflict_msg in constraints:
                if conflict_msg is None:
                    if constraint == spack.spec.Spec():
                        conflict_msg = no_constraint_msg.format(pkg.name, trigger)
                    else:
                        conflict_msg = default_msg.format(pkg.name, trigger, constraint)
                constraint_msg = "conflict constraint %s" % str(constraint)
                constraint_id = self.condition(constraint, name=pkg.name, msg=constraint_msg)
                self.gen.fact(fn.conflict(pkg.name, trigger_id, constraint_id, conflict_msg))
                self.gen.newline()

    def available_compilers(self):
        """Facts about available compilers."""

        self.gen.h2("Available compilers")
        compilers = self.possible_compilers

        compiler_versions = collections.defaultdict(lambda: set())
        for compiler in compilers:
            compiler_versions[compiler.name].add(compiler.version)

        for compiler in sorted(compiler_versions):
            for v in sorted(compiler_versions[compiler]):
                self.gen.fact(fn.compiler_version(compiler, v))

            self.gen.newline()

    def compiler_defaults(self):
        """Set compiler defaults, given a list of possible compilers."""
        self.gen.h2("Default compiler preferences")

        compiler_list = self.possible_compilers.copy()
        compiler_list = sorted(compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs("all", "compiler", all=False)
        matches = sorted(compiler_list, key=ppk)

        for i, cspec in enumerate(matches):
            f = fn.default_compiler_preference(cspec.name, cspec.version, i)
            self.gen.fact(f)

        # Enumerate target families. This may be redundant, but compilers with
        # custom versions will be able to concretize properly.
        for entry in spack.compilers.all_compilers_config():
            compiler_entry = entry["compiler"]
            cspec = spack.spec.CompilerSpec(compiler_entry["spec"])
            if not compiler_entry.get("target", None):
                continue

            self.gen.fact(
                fn.compiler_supports_target(cspec.name, cspec.version, compiler_entry["target"])
            )

    def compiler_supports_os(self):
        compilers_yaml = spack.compilers.all_compilers_config()
        for entry in compilers_yaml:
            c = spack.spec.CompilerSpec(entry["compiler"]["spec"])
            operating_system = entry["compiler"]["operating_system"]
            self.gen.fact(fn.compiler_supports_os(c.name, c.version, operating_system))

    def package_compiler_defaults(self, pkg):
        """Facts about packages' compiler prefs."""

        packages = spack.config.get("packages")
        pkg_prefs = packages.get(pkg.name)
        if not pkg_prefs or "compiler" not in pkg_prefs:
            return

        compiler_list = self.possible_compilers.copy()
        compiler_list = sorted(compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs(pkg.name, "compiler", all=False)
        matches = sorted(compiler_list, key=ppk)

        for i, cspec in enumerate(reversed(matches)):
            self.gen.fact(
                fn.node_compiler_preference(pkg.name, cspec.name, cspec.version, -i * 100)
            )

    def package_requirement_rules(self, pkg):
        pkg_name = pkg.name
        config = spack.config.get("packages")
        requirements, raise_on_failure = config.get(pkg_name, {}).get("require", []), True
        if not requirements:
            requirements, raise_on_failure = config.get("all", {}).get("require", []), False
        rules = self._rules_from_requirements(pkg_name, requirements)
        self.emit_facts_from_requirement_rules(
            rules, virtual=False, raise_on_failure=raise_on_failure
        )

    def _rules_from_requirements(self, pkg_name, requirements):
        """Manipulate requirements from packages.yaml, and return a list of tuples
        with a uniform structure (name, policy, requirements).
        """
        if isinstance(requirements, str):
            rules = [(pkg_name, "one_of", [requirements])]
        else:
            rules = []
            for requirement in requirements:
                for policy in ("one_of", "any_of"):
                    if policy in requirement:
                        rules.append((pkg_name, policy, requirement[policy]))
        return rules

    def pkg_rules(self, pkg, tests):
        pkg = packagize(pkg)

        # versions
        self.pkg_version_rules(pkg)
        self.gen.newline()

        # variants
        for name, entry in sorted(pkg.variants.items()):
            variant, when = entry

            if spack.spec.Spec() in when:
                # unconditional variant
                self.gen.fact(fn.variant(pkg.name, name))
            else:
                # conditional variant
                for w in when:
                    msg = "%s has variant %s" % (pkg.name, name)
                    if str(w):
                        msg += " when %s" % w

                    cond_id = self.condition(w, name=pkg.name, msg=msg)
                    self.gen.fact(fn.variant_condition(cond_id, pkg.name, name))

            single_value = not variant.multi
            if single_value:
                self.gen.fact(fn.variant_single_value(pkg.name, name))
                self.gen.fact(
                    fn.variant_default_value_from_package_py(pkg.name, name, variant.default)
                )
            else:
                spec_variant = variant.make_default()
                defaults = spec_variant.value
                for val in sorted(defaults):
                    self.gen.fact(fn.variant_default_value_from_package_py(pkg.name, name, val))

            values = variant.values
            if values is None:
                values = []
            elif isinstance(values, spack.variant.DisjointSetsOfValues):
                union = set()
                # Encode the disjoint sets in the logic program
                for sid, s in enumerate(values.sets):
                    for value in s:
                        self.gen.fact(
                            fn.variant_value_from_disjoint_sets(pkg.name, name, value, sid)
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
                        self.gen.fact(fn.conflict(pkg.name, trigger_id, constraint_id, msg))
                    else:
                        imposed = spack.spec.Spec(value.when)
                        imposed.name = pkg.name

                        self.condition(
                            required_spec=condition_spec,
                            imposed_spec=imposed,
                            name=pkg.name,
                            msg="%s variant %s value %s when %s" % (pkg.name, name, value, when),
                        )
                self.gen.fact(fn.variant_possible_value(pkg.name, name, value))

            if variant.sticky:
                self.gen.fact(fn.variant_sticky(pkg.name, name))

            self.gen.newline()

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
            pkg.name, lambda v, p, i: self.gen.fact(fn.pkg_provider_preference(pkg.name, v, p, i))
        )

        self.package_requirement_rules(pkg)

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
        assert named_cond.name, "must provide name for anonymous condtions!"

        # Check if we can emit the requirements before updating the condition ID counter.
        # In this way, if a condition can't be emitted but the exception is handled in the caller,
        # we won't emit partial facts.
        requirements = self.spec_clauses(named_cond, body=True, required_from=name)

        condition_id = next(self._condition_id_counter)
        self.gen.fact(fn.condition(condition_id, msg))
        for pred in requirements:
            self.gen.fact(fn.condition_requirement(condition_id, *pred.args))

        if imposed_spec:
            self.impose(condition_id, imposed_spec, node=node, name=name)

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
            self.gen.fact(fn.possible_provider(pkg.name, provider_name))

        for provided, whens in pkg.provided.items():
            for when in whens:
                msg = "%s provides %s when %s" % (pkg.name, provided, when)
                condition_id = self.condition(when, provided, pkg.name, msg)
                self.gen.fact(fn.provider_condition(condition_id, when.name, provided.name))
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

                condition_id = self.condition(cond, dep.spec, pkg.name, msg)
                self.gen.fact(fn.dependency_condition(condition_id, pkg.name, dep.spec.name))

                for t in sorted(deptypes):
                    # there is a declared dependency of type t
                    self.gen.fact(fn.dependency_type(condition_id, t))

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

    def provider_defaults(self):
        self.gen.h2("Default virtual providers")
        msg = (
            "Internal Error: possible_virtuals is not populated. Please report to the spack"
            " maintainers"
        )
        assert self.possible_virtuals is not None, msg
        self.virtual_preferences(
            "all", lambda v, p, i: self.gen.fact(fn.default_provider_preference(v, p, i))
        )

    def provider_requirements(self):
        self.gen.h2("Requirements on virtual providers")
        msg = (
            "Internal Error: possible_virtuals is not populated. Please report to the spack"
            " maintainers"
        )
        packages_yaml = spack.config.config.get("packages")
        assert self.possible_virtuals is not None, msg
        for virtual_str in sorted(self.possible_virtuals):
            requirements = packages_yaml.get(virtual_str, {}).get("require", [])
            rules = self._rules_from_requirements(virtual_str, requirements)
            self.emit_facts_from_requirement_rules(rules, virtual=True)

    def emit_facts_from_requirement_rules(self, rules, *, virtual=False, raise_on_failure=True):
        """Generate facts to enforce requirements from packages.yaml.

        Args:
            rules: rules for which we want facts to be emitted
            virtual: if True the requirements are on a virtual spec
            raise_on_failure: if True raise an exception when a requirement condition is invalid
                for the current spec. If False, just skip that condition
        """
        for requirement_grp_id, (pkg_name, policy, requirement_grp) in enumerate(rules):
            self.gen.fact(fn.requirement_group(pkg_name, requirement_grp_id))
            self.gen.fact(fn.requirement_policy(pkg_name, requirement_grp_id, policy))
            requirement_weight = 0
            for spec_str in requirement_grp:
                spec = spack.spec.Spec(spec_str)
                if not spec.name:
                    spec.name = pkg_name
                when_spec = spec
                if virtual:
                    when_spec = spack.spec.Spec(pkg_name)

                try:
                    member_id = self.condition(
                        required_spec=when_spec, imposed_spec=spec, name=pkg_name, node=virtual
                    )
                except Exception as e:
                    if raise_on_failure:
                        raise RuntimeError("cannot emit requirements for the solver") from e
                    continue

                self.gen.fact(fn.requirement_group_member(member_id, pkg_name, requirement_grp_id))
                self.gen.fact(fn.requirement_has_weight(member_id, requirement_weight))
                requirement_weight += 1

    def external_packages(self):
        """Facts on external packages, as read from packages.yaml"""
        # Read packages.yaml and normalize it, so that it
        # will not contain entries referring to virtual
        # packages.
        packages_yaml = spack.config.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml)

        self.gen.h1("External packages")
        for pkg_name, data in packages_yaml.items():
            if pkg_name == "all":
                continue

            # This package does not appear in any repository
            if pkg_name not in spack.repo.path:
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
            external_specs = [spack.spec.Spec(x["spec"]) for x in externals]

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
                    DeclaredVersion(version=version, idx=idx, origin=version_provenance.external)
                )

            # Declare external conditions with a local index into packages.yaml
            for local_idx, spec in enumerate(external_specs):
                msg = "%s available as external when satisfying %s" % (spec.name, spec)
                condition_id = self.condition(spec, msg=msg)
                self.gen.fact(fn.possible_external(condition_id, pkg_name, local_idx))
                self.possible_versions[spec.name].add(spec.version)
                self.gen.newline()

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
                fn.target_weight(pkg_name, str(preferred.architecture.target), i + offset)
            )

    def flag_defaults(self):
        self.gen.h2("Compiler flag defaults")

        # types of flags that can be on specs
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            self.gen.fact(fn.flag_type(flag))
        self.gen.newline()

        # flags from compilers.yaml
        compilers = all_compilers_in_config()
        seen = set()
        for compiler in compilers:
            # if there are multiple with the same spec, only use the first
            if compiler.spec in seen:
                continue
            seen.add(compiler.spec)
            for name, flags in compiler.flags.items():
                for flag in flags:
                    self.gen.fact(
                        fn.compiler_version_flag(compiler.name, compiler.version, name, flag)
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
        class Head(object):
            node = fn.attr("node")
            virtual_node = fn.attr("virtual_node")
            node_platform = fn.attr("node_platform_set")
            node_os = fn.attr("node_os_set")
            node_target = fn.attr("node_target_set")
            variant_value = fn.attr("variant_set")
            node_compiler = fn.attr("node_compiler_set")
            node_compiler_version = fn.attr("node_compiler_version_set")
            node_flag = fn.attr("node_flag_set")
            node_flag_propagate = fn.attr("node_flag_propagate")
            variant_propagate = fn.attr("variant_propagate")

        class Body(object):
            node = fn.attr("node")
            virtual_node = fn.attr("virtual_node")
            node_platform = fn.attr("node_platform")
            node_os = fn.attr("node_os")
            node_target = fn.attr("node_target")
            variant_value = fn.attr("variant_value")
            node_compiler = fn.attr("node_compiler")
            node_compiler_version = fn.attr("node_compiler_version")
            node_flag = fn.attr("node_flag")
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
                        pkg_cls = spack.repo.path.get_pkg_class(spec.name)
                        try:
                            variant_def, _ = pkg_cls.variants[vname]
                        except KeyError:
                            msg = 'variant "{0}" not found in package "{1}"'
                            raise RuntimeError(msg.format(vname, spec.name))
                        else:
                            variant_def.validate_or_raise(
                                variant, spack.repo.path.get_pkg_class(spec.name)
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

                            # Ensure Spack will not coconcretize this with another provider
                            # for the same virtual
                            for virtual in dep.package.virtuals_provided:
                                clauses.append(fn.attr("virtual_node", virtual.name))
                                clauses.append(fn.provider(dep.name, virtual.name))

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
        self.declared_versions = collections.defaultdict(list)
        self.possible_versions = collections.defaultdict(set)
        self.deprecated_versions = collections.defaultdict(set)

        packages_yaml = spack.config.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml)
        for pkg_name in possible_pkgs:
            pkg_cls = spack.repo.path.get_pkg_class(pkg_name)

            # All the versions from the corresponding package.py file. Since concepts
            # like being a "develop" version or being preferred exist only at a
            # package.py level, sort them in this partial list here
            def key_fn(item):
                version, info = item
                # When COMPARING VERSIONS, the '@develop' version is always
                # larger than other versions. BUT when CONCRETIZING, the largest
                # NON-develop version is selected by default.
                return info.get("preferred", False), not version.isdevelop(), version

            for idx, item in enumerate(sorted(pkg_cls.versions.items(), key=key_fn, reverse=True)):
                v, version_info = item
                self.possible_versions[pkg_name].add(v)
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=v, idx=idx, origin=version_provenance.package_py)
                )
                deprecated = version_info.get("deprecated", False)
                if deprecated:
                    self.deprecated_versions[pkg_name].add(v)

            # All the preferred version from packages.yaml, versions in external
            # specs will be computed later
            version_preferences = packages_yaml.get(pkg_name, {}).get("version", [])
            for idx, v in enumerate(version_preferences):
                # v can be a string so force it into an actual version for comparisons
                ver = spack.version.Version(v)
                self.declared_versions[pkg_name].append(
                    DeclaredVersion(version=ver, idx=idx, origin=version_provenance.packages_yaml)
                )

    def add_concrete_versions_from_specs(self, specs, origin):
        """Add concrete versions to possible versions from lists of CLI/dev specs."""
        for spec in specs:
            for dep in spec.traverse():
                if not dep.versions.concrete:
                    continue

                known_versions = self.possible_versions[dep.name]
                if not isinstance(dep.version, spack.version.GitVersion) and any(
                    v.satisfies(dep.version) for v in known_versions
                ):
                    # some version we know about satisfies this constraint, so we
                    # should use that one. e.g, if the user asks for qt@5 and we
                    # know about qt@5.5. This ensures we don't add under-specified
                    # versions to the solver
                    #
                    # For git versions, we know the version is already fully specified
                    # so we don't have to worry about whether it's an under-specified
                    # version
                    continue

                # if there is a concrete version on the CLI *that we know nothing
                # about*, add it to the known versions. Use idx=0, which is the
                # best possible, so they're guaranteed to be used preferentially.
                self.declared_versions[dep.name].append(
                    DeclaredVersion(version=dep.version, idx=0, origin=origin)
                )
                self.possible_versions[dep.name].add(dep.version)

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

        compilers = self.possible_compilers

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

        best_targets = set([uarch.family.name])
        for compiler in sorted(compilers):
            supported = self._supported_targets(compiler.name, compiler.version, candidate_targets)

            # If we can't find supported targets it may be due to custom
            # versions in the spec, e.g. gcc@foo. Try to match the
            # real_version from the compiler object to get more accurate
            # results.
            if not supported:
                compiler_obj = spack.compilers.compilers_for_spec(compiler)
                compiler_obj = compiler_obj[0]
                supported = self._supported_targets(
                    compiler.name, compiler_obj.real_version, candidate_targets
                )

            if not supported:
                continue

            for target in supported:
                best_targets.add(target.name)
                self.gen.fact(
                    fn.compiler_supports_target(compiler.name, compiler.version, target.name)
                )

            self.gen.fact(
                fn.compiler_supports_target(compiler.name, compiler.version, uarch.family.name)
            )

        i = 0  # TODO compute per-target offset?
        for target in candidate_targets:
            self.gen.fact(fn.target(target.name))
            self.gen.fact(fn.target_family(target.name, target.family.name))
            for parent in sorted(target.parents):
                self.gen.fact(fn.target_parent(target.name, parent.name))

            # prefer best possible targets; weight others poorly so
            # they're not used unless set explicitly
            # these are stored to be generated as facts later offset by the
            # number of preferred targets
            if target.name in best_targets:
                self.default_targets.append((i, target.name))
                i += 1
            else:
                self.default_targets.append((100, target.name))

            self.default_targets = list(sorted(set(self.default_targets)))
            self.gen.newline()

    def virtual_providers(self):
        self.gen.h2("Virtual providers")
        msg = (
            "Internal Error: possible_virtuals is not populated. Please report to the spack"
            " maintainers"
        )
        assert self.possible_virtuals is not None, msg

        # what provides what
        for vspec in sorted(self.possible_virtuals):
            self.gen.fact(fn.virtual(vspec))
        self.gen.newline()

    def generate_possible_compilers(self, specs):
        compilers = all_compilers_in_config()
        cspecs = set([c.spec for c in compilers])

        # add compiler specs from the input line to possibilities if we
        # don't require compilers to exist.
        strict = spack.concretize.Concretizer().check_for_compiler_existence
        for spec in specs:
            for s in spec.traverse():
                # we don't need to validate compilers for already-built specs
                if s.concrete:
                    continue

                if not s.compiler or not s.compiler.concrete:
                    continue

                if strict and s.compiler not in cspecs:
                    if not s.concrete:
                        raise spack.concretize.UnavailableCompilerVersionError(s.compiler)
                    # Allow unknown compilers to exist if the associated spec
                    # is already built
                else:
                    cspecs.add(s.compiler)
                    self.gen.fact(fn.allow_compiler(s.compiler.name, s.compiler.version))

        return cspecs

    def define_version_constraints(self):
        """Define what version_satisfies(...) means in ASP logic."""
        for pkg_name, versions in sorted(self.version_constraints):
            # version must be *one* of the ones the spec allows.
            allowed_versions = [
                v for v in sorted(self.possible_versions[pkg_name]) if v.intersects(versions)
            ]

            # This is needed to account for a variable number of
            # numbers e.g. if both 1.0 and 1.0.2 are possible versions
            exact_match = [v for v in allowed_versions if v == versions]
            if exact_match:
                allowed_versions = exact_match

            # generate facts for each package constraint and the version
            # that satisfies it
            for v in allowed_versions:
                self.gen.fact(fn.version_satisfies(pkg_name, versions, v))

            self.gen.newline()

    def define_virtual_constraints(self):
        """Define versions for constraints on virtuals.

        Must be called before define_version_constraints().
        """
        # aggregate constraints into per-virtual sets
        constraint_map = collections.defaultdict(lambda: set())
        for pkg_name, versions in self.version_constraints:
            if not spack.repo.path.is_virtual(pkg_name):
                continue
            constraint_map[pkg_name].add(versions)

        # extract all the real versions mentioned in version ranges
        def versions_for(v):
            if isinstance(v, spack.version.VersionBase):
                return [v]
            elif isinstance(v, spack.version.VersionRange):
                result = [v.start] if v.start else []
                result += [v.end] if v.end else []
                return result
            elif isinstance(v, spack.version.VersionList):
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
        compiler_list = spack.compilers.all_compiler_specs()
        compiler_list = list(sorted(set(compiler_list)))
        for constraint in sorted(self.compiler_version_constraints):
            for compiler in compiler_list:
                if compiler.satisfies(constraint):
                    self.gen.fact(
                        fn.compiler_version_satisfies(
                            constraint.name, constraint.versions, compiler.version
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
            self.gen.fact(fn.variant_possible_value(pkg, variant, value))

    def _facts_from_concrete_spec(self, spec, possible):
        # tell the solver about any installed packages that could
        # be dependencies (don't tell it about the others)
        h = spec.dag_hash()
        if spec.name in possible and h not in self.seen_hashes:
            self.reusable_and_possible[h] = spec
            try:
                # Only consider installed packages for repo we know
                spack.repo.path.get(spec)
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
                    DeclaredVersion(
                        version=dep.version, idx=0, origin=version_provenance.installed
                    )
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

    def setup(self, driver, specs, reuse=None):
        """Generate an ASP program with relevant constraints for specs.

        This calls methods on the solve driver to set up the problem with
        facts and rules from all possible dependencies of the input
        specs, as well as constraints from the specs themselves.

        Arguments:
            driver (PyclingoDriver): driver instance of this solve
            specs (list): list of Specs to solve
            reuse (None or list): list of concrete specs that can be reused
        """
        self._condition_id_counter = itertools.count()

        # preliminary checks
        check_packages_exist(specs)

        # get list of all possible dependencies
        self.possible_virtuals = set(x.name for x in specs if x.virtual)
        possible = spack.package_base.possible_dependencies(
            *specs, virtuals=self.possible_virtuals, deptype=spack.dependency.all_deptypes
        )

        # Fail if we already know an unreachable node is requested
        for spec in specs:
            missing_deps = [
                str(d) for d in spec.traverse() if d.name not in possible and not d.virtual
            ]
            if missing_deps:
                raise spack.spec.InvalidDependencyError(spec.name, missing_deps)

        self.pkgs = set(possible)

        # driver is used by all the functions below to add facts and
        # rules to generate an ASP program.
        self.gen = driver

        # Calculate develop specs
        # they will be used in addition to command line specs
        # in determining known versions/targets/os
        dev_specs = ()
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

        # traverse all specs and packages to build dict of possible versions
        self.build_version_dict(possible)
        self.add_concrete_versions_from_specs(specs, version_provenance.spec)
        self.add_concrete_versions_from_specs(dev_specs, version_provenance.dev_spec)

        self.gen.h1("Concrete input spec definitions")
        self.define_concrete_input_specs(specs, possible)

        if reuse:
            self.gen.h1("Reusable specs")
            self.gen.fact(fn.optimize_for_reuse())
            for reusable_spec in reuse:
                self._facts_from_concrete_spec(reusable_spec, possible)

        self.gen.h1("General Constraints")
        self.available_compilers()
        self.compiler_defaults()
        self.compiler_supports_os()

        # architecture defaults
        self.platform_defaults()
        self.os_defaults(specs + dev_specs)
        self.target_defaults(specs + dev_specs)

        self.virtual_providers()
        self.provider_defaults()
        self.provider_requirements()
        self.external_packages()
        self.flag_defaults()

        self.gen.h1("Package Constraints")
        for pkg in sorted(self.pkgs):
            self.gen.h2("Package rules: %s" % pkg)
            self.pkg_rules(pkg, tests=self.tests)
            self.gen.h2("Package preferences: %s" % pkg)
            self.preferred_variants(pkg)
            self.target_preferences(pkg)

        # Inject dev_path from environment
        for ds in dev_specs:
            self.condition(spack.spec.Spec(ds.name), ds, msg="%s is a develop spec" % ds.name)

        self.gen.h1("Spec Constraints")
        self.literal_specs(specs)

        self.gen.h1("Variant Values defined in specs")
        self.define_variant_values()

        self.gen.h1("Virtual Constraints")
        self.define_virtual_constraints()

        self.gen.h1("Version Constraints")
        self.define_version_constraints()

        self.gen.h1("Compiler Version Constraints")
        self.define_compiler_version_constraints()

        self.gen.h1("Target Constraints")
        self.define_target_constraints()

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
            self.gen.fact(fn.concretize_everything())


class SpecBuilder(object):
    """Class with actions to rebuild a spec from ASP results."""

    #: Regex for attributes that don't need actions b/c they aren't used to construct specs.
    ignored_attributes = re.compile(
        "|".join(
            [
                r"^.*_propagate$",
                r"^.*_satisfies$",
                r"^.*_set$",
                r"^package_hash$",
                r"^root$",
                r"^virtual_node$",
                r"^virtual_root$",
            ]
        )
    )

    def __init__(self, specs, hash_lookup=None):
        self._specs = {}
        self._result = None
        self._command_line_specs = specs
        self._flag_sources = collections.defaultdict(lambda: set())
        self._flag_compiler_defaults = set()

        # Pass in as arguments reusable specs and plug them in
        # from this dictionary during reconstruction
        self._hash_lookup = hash_lookup or {}

    def hash(self, pkg, h):
        if pkg not in self._specs:
            self._specs[pkg] = self._hash_lookup[h]

    def node(self, pkg):
        if pkg not in self._specs:
            self._specs[pkg] = spack.spec.Spec(pkg)

    def _arch(self, pkg):
        arch = self._specs[pkg].architecture
        if not arch:
            arch = spack.spec.ArchSpec()
            self._specs[pkg].architecture = arch
        return arch

    def node_platform(self, pkg, platform):
        self._arch(pkg).platform = platform

    def node_os(self, pkg, os):
        self._arch(pkg).os = os

    def node_target(self, pkg, target):
        self._arch(pkg).target = target

    def variant_value(self, pkg, name, value):
        # FIXME: is there a way not to special case 'dev_path' everywhere?
        if name == "dev_path":
            self._specs[pkg].variants.setdefault(
                name, spack.variant.SingleValuedVariant(name, value)
            )
            return

        if name == "patches":
            self._specs[pkg].variants.setdefault(
                name, spack.variant.MultiValuedVariant(name, value)
            )
            return

        self._specs[pkg].update_variant_validate(name, value)

    def version(self, pkg, version):
        self._specs[pkg].versions = spack.version.ver([version])

    def node_compiler(self, pkg, compiler):
        self._specs[pkg].compiler = spack.spec.CompilerSpec(compiler)

    def node_compiler_version(self, pkg, compiler, version):
        self._specs[pkg].compiler.versions = spack.version.VersionList([version])

    def node_flag_compiler_default(self, pkg):
        self._flag_compiler_defaults.add(pkg)

    def node_flag(self, pkg, flag_type, flag):
        self._specs[pkg].compiler_flags.add_flag(flag_type, flag, False)

    def node_flag_source(self, pkg, flag_type, source):
        self._flag_sources[(pkg, flag_type)].add(source)

    def no_flags(self, pkg, flag_type):
        self._specs[pkg].compiler_flags[flag_type] = []

    def external_spec_selected(self, pkg, idx):
        """This means that the external spec and index idx
        has been selected for this package.
        """
        packages_yaml = spack.config.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml)
        spec_info = packages_yaml[pkg]["externals"][int(idx)]
        self._specs[pkg].external_path = spec_info.get("prefix", None)
        self._specs[pkg].external_modules = spack.spec.Spec._format_module_list(
            spec_info.get("modules", None)
        )
        self._specs[pkg].extra_attributes = spec_info.get("extra_attributes", {})

        # If this is an extension, update the dependencies to include the extendee
        package = self._specs[pkg].package_class(self._specs[pkg])
        extendee_spec = package.extendee_spec
        if extendee_spec:
            package.update_external_dependencies(self._specs.get(extendee_spec.name, None))

    def depends_on(self, pkg, dep, type):
        dependencies = self._specs[pkg].edges_to_dependencies(name=dep)

        # TODO: assertion to be removed when cross-compilation is handled correctly
        msg = "Current solver does not handle multiple dependency edges of the same name"
        assert len(dependencies) < 2, msg

        if not dependencies:
            self._specs[pkg].add_dependency_edge(self._specs[dep], deptypes=(type,))
        else:
            # TODO: This assumes that each solve unifies dependencies
            dependencies[0].add_type(type)

    def reorder_flags(self):
        """Order compiler flags on specs in predefined order.

        We order flags so that any node's flags will take priority over
        those of its dependents.  That is, the deepest node in the DAG's
        flags will appear last on the compile line, in the order they
        were specified.

        The solver determines wihch flags are on nodes; this routine
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
                source_key = (spec.name, flag_type)
                if source_key in self._flag_sources:
                    order = [s.name for s in spec.traverse(order="post", direction="parents")]
                    sorted_sources = sorted(
                        self._flag_sources[source_key], key=lambda s: order.index(s)
                    )

                    # add flags from each source, lowest to highest precedence
                    for source_name in sorted_sources:
                        source = cmd_specs[source_name]
                        extend_flag_list(from_sources, source.compiler_flags.get(flag_type, []))

                # compiler flags from compilers config are lowest precedence
                ordered_compiler_flags = from_compiler + from_sources
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
        node_compiler attributes are handled next to ensure they come before node_compiler_version
        external_spec_selected attributes are handled last, so that external extensions can find
        the concrete specs on which they depend because all nodes are fully constructed before we
        consider which ones are external.
        """
        name = function_tuple[0]
        if name == "hash":
            return (-5, 0)
        elif name == "node":
            return (-4, 0)
        elif name == "node_compiler":
            return (-3, 0)
        elif name == "node_flag":
            return (-2, 0)
        elif name == "external_spec_selected":
            return (0, 0)  # note out of order so this goes last
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
                pkg = args[0]
                if spack.repo.path.is_virtual(pkg):
                    continue

                # if we've already gotten a concrete spec for this pkg,
                # do not bother calling actions on it.
                spec = self._specs.get(pkg)
                if spec and spec.concrete:
                    continue

            action(*args)

        # namespace assignment is done after the fact, as it is not
        # currently part of the solve
        for spec in self._specs.values():
            if spec.namespace:
                continue
            repo = spack.repo.path.repo_for_pkg(spec)
            spec.namespace = repo.namespace

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
                if isinstance(spec.version, spack.version.GitVersion):
                    spec.version.generate_git_lookup(spec.fullname)

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


class Solver(object):
    """This is the main external interface class for solving.

    It manages solver configuration and preferences in one place. It sets up the solve
    and passes the setup method to the driver, as well.

    Properties of interest:

      ``reuse (bool)``
        Whether to try to reuse existing installs/binaries

    """

    def __init__(self):
        self.driver = PyclingoDriver()

        # These properties are settable via spack configuration, and overridable
        # by setting them directly as properties.
        self.reuse = spack.config.get("concretizer:reuse", False)

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

    def _reusable_specs(self):
        reusable_specs = []
        if self.reuse:
            # Specs from the local Database
            with spack.store.db.read_transaction():
                reusable_specs.extend(
                    [
                        s
                        for s in spack.store.db.query(installed=True)
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
        return reusable_specs

    def solve(self, specs, out=None, timers=False, stats=False, tests=False, setup_only=False):
        """
        Arguments:
          specs (list): List of ``Spec`` objects to solve for.
          out: Optionally write the generate ASP program to a file-like object.
          timers (bool): Print out coarse fimers for different solve phases.
          stats (bool): Print out detailed stats from clingo.
          tests (bool or tuple): If True, concretize test dependencies for all packages.
            If a tuple of package names, concretize test dependencies for named
            packages (defaults to False: do not concretize test dependencies).
          setup_only (bool): if True, stop after setup and don't solve (default False).
        """
        # Check upfront that the variants are admissible
        reusable_specs = self._check_input_and_extract_concrete_specs(specs)
        reusable_specs.extend(self._reusable_specs())
        setup = SpackSolverSetup(tests=tests)
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
        reusable_specs = self._check_input_and_extract_concrete_specs(specs)
        reusable_specs.extend(self._reusable_specs())
        setup = SpackSolverSetup(tests=tests)

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
        indented = ["  %s\n" % conflict for conflict in conflicts]
        error_msg = "".join(indented)
        msg = "Spack concretizer internal error. Please submit a bug report"
        msg += "\n    Please include the command, environment if applicable,"
        msg += "\n    and the following error message."
        msg = "\n        %s is unsatisfiable, errors are:\n%s" % (provided, error_msg)

        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)

        self.provided = provided

        # Add attribute expected of the superclass interface
        self.required = None
        self.constraint_type = None
