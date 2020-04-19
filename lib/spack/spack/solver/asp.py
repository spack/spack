# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import collections
import pkgutil
import re
import sys
import tempfile
import time
import types
from six import string_types

import llnl.util.cpu
import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack
import spack.cmd
import spack.config
import spack.dependency
import spack.spec
import spack.package
import spack.package_prefs
import spack.repo
from spack.util.executable import which
from spack.version import ver


#: max line length for ASP programs in characters
_max_line = 80


def issequence(obj):
    if isinstance(obj, string_types):
        return False
    return isinstance(obj, (collections.Sequence, types.GeneratorType))


def listify(args):
    if len(args) == 1 and issequence(args[0]):
        return list(args[0])
    return list(args)


def packagize(pkg):
    if isinstance(pkg, string_types):
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


class AspFunction(AspObject):
    def __init__(self, name, args=None):
        self.name = name
        self.args = [] if args is None else args

    def __call__(self, *args):
        return AspFunction(self.name, args)

    def __getitem___(self, *args):
        self.args[:] = args
        return self

    def __str__(self):
        return "%s(%s)" % (
            self.name, ', '.join(str(_id(arg)) for arg in self.args))

    def __repr__(self):
        return str(self)


class AspAnd(AspObject):
    def __init__(self, *args):
        args = listify(args)
        self.args = args

    def __str__(self):
        s = ", ".join(str(arg) for arg in self.args)
        return s


class AspOr(AspObject):
    def __init__(self, *args):
        args = listify(args)
        self.args = args

    def __str__(self):
        return " | ".join(str(arg) for arg in self.args)


class AspNot(AspObject):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "not %s" % self.arg


class AspOneOf(AspObject):
    def __init__(self, *args):
        args = listify(args)
        self.args = args

    def __str__(self):
        body = "; ".join(str(arg) for arg in self.args)
        return "1 { %s } 1" % body


class AspFunctionBuilder(object):
    def __getattr__(self, name):
        return AspFunction(name)


fn = AspFunctionBuilder()


def default_arch():
    return spack.spec.ArchSpec(spack.architecture.sys_type())


def compilers_for_default_arch():
    return spack.compilers.compilers_for_arch(default_arch())


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


def check_same_flags(flag_dict_1, flag_dict_2):
    """Return True if flag dicts contain the same flags regardless of order."""
    types = set(flag_dict_1.keys()).union(set(flag_dict_2.keys()))
    for t in types:
        values1 = set(flag_dict_1.get(t, []))
        values2 = set(flag_dict_2.get(t, []))
        assert values1 == values2


def check_packages_exist(specs):
    """Ensure all packages mentioned in specs exist."""
    repo = spack.repo.path
    for spec in specs:
        for s in spec.traverse():
            if not (repo.exists(s.name) or repo.is_virtual(s)):
                raise spack.repo.UnknownPackageError(s.name)


class AspGenerator(object):
    def __init__(self, out):
        self.out = out
        self.func = AspFunctionBuilder()
        self.possible_versions = {}
        self.possible_virtuals = None
        self.possible_compilers = []

    def title(self, name, char):
        self.out.write('\n')
        self.out.write("%" + (char * 76))
        self.out.write('\n')
        self.out.write("%% %s\n" % name)
        self.out.write("%" + (char * 76))
        self.out.write('\n')

    def h1(self, name):
        self.title(name, "=")

    def h2(self, name):
        self.title(name, "-")

    def section(self, name):
        self.out.write("\n")
        self.out.write("%\n")
        self.out.write("%% %s\n" % name)
        self.out.write("%\n")

    def one_of(self, *args):
        return AspOneOf(*args)

    def _or(self, *args):
        return AspOr(*args)

    def _and(self, *args):
        return AspAnd(*args)

    def _not(self, arg):
        return AspNot(arg)

    def fact(self, head):
        """ASP fact (a rule without a body)."""
        self.out.write("%s.\n" % head)

    def rule(self, head, body):
        """ASP rule (an implication)."""
        rule_line = "%s :- %s.\n" % (head, body)
        if len(rule_line) > _max_line:
            rule_line = re.sub(r' \| ', "\n| ", rule_line)
        self.out.write(rule_line)

    def constraint(self, body):
        """ASP integrity constraint (rule with no head; can't be true)."""
        self.out.write(":- %s.\n" % body)

    def pkg_version_rules(self, pkg):
        """Output declared versions of a package.

        This uses self.possible_versions so that we include any versions
        that arise from a spec.
        """
        pkg = packagize(pkg)

        config = spack.config.get("packages")
        version_prefs = config.get(pkg.name, {}).get("version", {})
        priority = dict((v, i) for i, v in enumerate(version_prefs))

        # The keys below show the order of precedence of factors used
        # to select a version when concretizing.  The item with
        # the "largest" key will be selected.
        #
        # NOTE: When COMPARING VERSIONS, the '@develop' version is always
        #       larger than other versions.  BUT when CONCRETIZING,
        #       the largest NON-develop version is selected by default.
        keyfn = lambda v: (
            # ------- Special direction from the user
            # Respect order listed in packages.yaml
            -priority.get(v, 0),

            # The preferred=True flag (packages or packages.yaml or both?)
            pkg.versions.get(v).get('preferred', False),

            # ------- Regular case: use latest non-develop version by default.
            # Avoid @develop version, which would otherwise be the "largest"
            # in straight version comparisons
            not v.isdevelop(),

            # Compare the version itself
            # This includes the logic:
            #    a) develop > everything (disabled by "not v.isdevelop() above)
            #    b) numeric > non-numeric
            #    c) Numeric or string comparison
            v)

        most_to_least_preferred = sorted(
            self.possible_versions[pkg.name], key=keyfn, reverse=True
        )

        for i, v in enumerate(most_to_least_preferred):
            self.fact(fn.version_declared(pkg.name, v, i))

    def spec_versions(self, spec):
        """Return list of clauses expressing spec's version constraints."""
        spec = specify(spec)
        assert spec.name

        if spec.concrete:
            return [fn.version(spec.name, spec.version)]

        # version must be *one* of the ones the spec allows.
        allowed_versions = [
            v for v in sorted(self.possible_versions[spec.name])
            if v.satisfies(spec.versions)
        ]

        # don't bother restricting anything if all versions are allowed
        if len(allowed_versions) == len(self.possible_versions[spec.name]):
            return []

        predicates = [fn.version(spec.name, v) for v in allowed_versions]

        # conflict with any versions that do not satisfy the spec
        if predicates:
            return [self.one_of(*predicates)]
        return []

    def available_compilers(self):
        """Facts about available compilers."""

        self.h2("Available compilers")
        compilers = self.possible_compilers

        compiler_versions = collections.defaultdict(lambda: set())
        for compiler in compilers:
            compiler_versions[compiler.name].add(compiler.version)

        for compiler in sorted(compiler_versions):
            self.fact(fn.compiler(compiler))
            self.rule(
                self._or(
                    fn.compiler_version(compiler, v)
                    for v in sorted(compiler_versions[compiler])),
                fn.compiler(compiler))

    def compiler_defaults(self):
        """Set compiler defaults, given a list of possible compilers."""
        self.h2("Default compiler preferences")

        compiler_list = self.possible_compilers.copy()
        compiler_list = sorted(
            compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs("all", 'compiler', all=False)
        matches = sorted(compiler_list, key=ppk)

        for i, cspec in enumerate(matches):
            f = fn.default_compiler_preference(cspec.name, cspec.version, i)
            self.fact(f)

    def package_compiler_defaults(self, pkg):
        """Facts about packages' compiler prefs."""

        packages = spack.config.get("packages")
        pkg_prefs = packages.get(pkg)
        if not pkg_prefs or "compiler" not in pkg_prefs:
            return

        compiler_list = self.possible_compilers.copy()
        compiler_list = sorted(
            compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs(pkg.name, 'compiler', all=False)
        matches = sorted(compiler_list, key=ppk)

        for i, cspec in enumerate(matches):
            self.fact(fn.node_compiler_preference(
                pkg.name, cspec.name, cspec.version, i))

    def pkg_rules(self, pkg):
        pkg = packagize(pkg)

        # versions
        self.pkg_version_rules(pkg)
        self.out.write('\n')

        # variants
        for name, variant in sorted(pkg.variants.items()):
            self.fact(fn.variant(pkg.name, name))

            single_value = not variant.multi
            single = fn.variant_single_value(pkg.name, name)
            if single_value:
                self.fact(single)
                self.fact(
                    fn.variant_default_value(pkg.name, name, variant.default))
            else:
                self.fact(self._not(single))
                defaults = variant.default.split(',')
                for val in sorted(defaults):
                    self.fact(fn.variant_default_value(pkg.name, name, val))

            values = variant.values
            if values is None:
                values = []
            elif isinstance(values, spack.variant.DisjointSetsOfValues):
                union = set()
                for s in values.sets:
                    union.update(s)
                values = union

            # make sure that every variant has at least one posisble value
            if not values:
                values = [variant.default]

            for value in sorted(values):
                self.fact(fn.variant_possible_value(pkg.name, name, value))

            self.out.write('\n')

        # default compilers for this package
        self.package_compiler_defaults(pkg)

        # dependencies
        for name, conditions in sorted(pkg.dependencies.items()):
            for cond, dep in sorted(conditions.items()):
                named_cond = cond.copy()
                if not named_cond.name:
                    named_cond.name = pkg.name

                if cond == spack.spec.Spec():
                    for t in sorted(dep.type):
                        self.fact(
                            fn.declared_dependency(
                                dep.pkg.name, dep.spec.name, t
                            )
                        )
                else:
                    for t in sorted(dep.type):
                        self.rule(
                            fn.declared_dependency(
                                dep.pkg.name, dep.spec.name, t
                            ),
                            self._and(
                                *self.spec_clauses(named_cond, body=True)
                            )
                        )

                # add constraints on the dependency from dep spec.
                for clause in self.spec_clauses(dep.spec):
                    self.rule(
                        clause,
                        self._and(
                            fn.depends_on(dep.pkg.name, dep.spec.name),
                            *self.spec_clauses(named_cond, body=True)
                        )
                    )
            self.out.write('\n')

        # virtual preferences
        self.virtual_preferences(
            pkg.name,
            lambda v, p, i: self.fact(
                fn.pkg_provider_preference(pkg.name, v, p, i)
            )
        )

    def virtual_preferences(self, pkg_name, func):
        """Call func(vspec, provider, i) for each of pkg's provider prefs."""
        config = spack.config.get("packages")
        pkg_prefs = config.get(pkg_name, {}).get("providers", {})
        for vspec, providers in pkg_prefs.items():
            if vspec not in self.possible_virtuals:
                continue

            for i, provider in enumerate(providers):
                func(vspec, provider, i)

    def provider_defaults(self):
        self.h2("Default virtual providers")
        assert self.possible_virtuals is not None
        self.virtual_preferences(
            "all",
            lambda v, p, i: self.fact(fn.default_provider_preference(v, p, i))
        )

    def flag_defaults(self):
        self.h2("Compiler flag defaults")

        # types of flags that can be on specs
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            self.fact(fn.flag_type(flag))
        self.out.write("\n")

        # flags from compilers.yaml
        compilers = compilers_for_default_arch()
        for compiler in compilers:
            for name, flags in compiler.flags.items():
                for flag in flags:
                    self.fact(fn.compiler_version_flag(
                        compiler.name, compiler.version, name, flag))

    def spec_clauses(self, spec, body=False):
        """Return a list of clauses for a spec mandates are true.

        Arguments:
            spec (Spec): the spec to analyze
            body (bool): if True, generate clauses to be used in rule bodies
                (final values) instead of rule heads (setters).
        """
        clauses = []

        # TODO: do this with consistent suffixes.
        class Head(object):
            node = fn.node
            node_platform = fn.node_platform_set
            node_os = fn.node_os_set
            node_target = fn.node_target_set
            variant = fn.variant_set
            node_compiler = fn.node_compiler
            node_compiler_version = fn.node_compiler_version

        class Body(object):
            node = fn.node
            node_platform = fn.node_platform
            node_os = fn.node_os
            node_target = fn.node_target
            variant = fn.variant_value
            node_compiler = fn.node_compiler
            node_compiler_version = fn.node_compiler_version

        f = Body if body else Head

        if spec.name:
            clauses.append(f.node(spec.name))

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
                clauses.append(f.node_target(spec.name, arch.target))

        # variants
        for vname, variant in sorted(spec.variants.items()):
            value = variant.value
            if isinstance(value, tuple):
                for v in value:
                    clauses.append(f.variant(spec.name, vname, v))
            else:
                clauses.append(f.variant(spec.name, vname, variant.value))

        # compiler and compiler version
        if spec.compiler:
            clauses.append(f.node_compiler(spec.name, spec.compiler.name))
            clauses.append(
                fn.node_compiler_hard(spec.name, spec.compiler.name))

            if spec.compiler.concrete:
                clauses.append(f.node_compiler_version(
                    spec.name, spec.compiler.name, spec.compiler.version))

            elif spec.compiler.versions:
                compiler_list = spack.compilers.all_compiler_specs()
                possible_compiler_versions = [
                    f.node_compiler_version(
                        spec.name, spec.compiler.name, compiler.version
                    )
                    for compiler in compiler_list
                    if compiler.satisfies(spec.compiler)
                ]
                clauses.append(self.one_of(*possible_compiler_versions))
                for version in possible_compiler_versions:
                    clauses.append(
                        fn.node_compiler_version_hard(
                            spec.name, spec.compiler.name, version))

        # compiler flags
        for flag_type, flags in spec.compiler_flags.items():
            for flag in flags:
                self.fact(fn.node_flag_set(spec.name, flag_type, flag))

        # TODO
        # external_path
        # external_module
        # namespace

        return clauses

    def build_version_dict(self, possible_pkgs, specs):
        """Declare any versions in specs not declared in packages."""
        self.possible_versions = collections.defaultdict(lambda: set())

        for pkg_name in possible_pkgs:
            pkg = spack.repo.get(pkg_name)
            for v in pkg.versions:
                self.possible_versions[pkg_name].add(v)

        for spec in specs:
            for dep in spec.traverse():
                if dep.versions.concrete:
                    self.possible_versions[dep.name].add(dep.version)

    def _supported_targets(self, compiler, targets):
        """Get a list of which targets are supported by the compiler.

        Results are ordered most to least recent.
        """
        supported = []

        for target in targets:
            compiler_info = target.compilers.get(compiler.name)
            if not compiler_info:
                # if we don't know, we assume it's supported and leave it
                # to the user to debug
                supported.append(target)
                continue

            if not isinstance(compiler_info, list):
                compiler_info = [compiler_info]

            for info in compiler_info:
                version = ver(info['versions'])
                if compiler.version.satisfies(version):
                    supported.append(target)

        return sorted(supported, reverse=True)

    def platform_defaults(self):
        self.h2('Default platform')
        default = default_arch()
        self.fact(fn.node_platform_default(default.platform))

    def os_defaults(self, specs):
        self.h2('Default operating system')
        default = default_arch()
        self.fact(fn.node_os_default(default.os))

    def target_defaults(self, specs):
        """Add facts about targets and target compatibility."""
        self.h2('Default target')
        default = default_arch()
        self.fact(fn.node_target_default(default_arch().target))

        uarch = default.target.microarchitecture

        self.h2('Target compatibility')

        # listing too many targets can be slow, at least with our current
        # encoding. To reduce the number of options to consider, only
        # consider the *best* target that each compiler supports, along
        # with the family.
        compatible_targets = [uarch] + uarch.ancestors
        compilers = self.possible_compilers

        # this loop can be used to limit the number of targets
        # considered. Right now we consider them all, but it seems that
        # many targets can make things slow.
        # TODO: investigate this.
        best_targets = set([uarch.family.name])
        for compiler in compilers:
            supported = self._supported_targets(compiler, compatible_targets)
            if not supported:
                continue

            for target in supported:
                best_targets.add(target.name)
                self.fact(fn.compiler_supports_target(
                    compiler.name, compiler.version, target.name))
                self.fact(fn.compiler_supports_target(
                    compiler.name, compiler.version, uarch.family.name))

        # add any targets explicitly mentioned in specs
        for spec in specs:
            if not spec.architecture or not spec.architecture.target:
                continue

            target = llnl.util.cpu.targets.get(spec.target.name)
            if not target:
                raise ValueError("Invalid target: ", spec.target.name)
            if target not in compatible_targets:
                compatible_targets.append(target)

        i = 0
        for target in compatible_targets:
            self.fact(fn.target(target.name))
            self.fact(fn.target_family(target.name, target.family.name))
            for parent in sorted(target.parents):
                self.fact(fn.target_parent(target.name, parent.name))

            # prefer best possible targets; weight others poorly so
            # they're not used unless set explicitly
            if target.name in best_targets:
                self.fact(fn.target_weight(target.name, i))
                i += 1
            else:
                self.fact(fn.target_weight(target.name, 100))

            self.out.write("\n")

    def virtual_providers(self):
        self.h2("Virtual providers")
        assert self.possible_virtuals is not None

        # what provides what
        for vspec in sorted(self.possible_virtuals):
            self.fact(fn.virtual(vspec))
            for provider in sorted(spack.repo.path.providers_for(vspec)):
                # TODO: handle versioned and conditional virtuals
                self.fact(fn.provides_virtual(provider.name, vspec))

    def generate_possible_compilers(self, specs):
        default_arch = spack.spec.ArchSpec(spack.architecture.sys_type())
        compilers = spack.compilers.compilers_for_arch(default_arch)
        cspecs = set([c.spec for c in compilers])

        # add compiler specs from the input line to possibilities if we
        # don't require compilers to exist.
        strict = spack.concretize.Concretizer.check_for_compiler_existence
        for spec in specs:
            for s in spec.traverse():
                if (not s.compiler
                    or s.compiler in cspecs
                    or not s.compiler.concrete):
                    continue

                if strict:
                    raise spack.concretize.UnavailableCompilerVersionError(
                        s.compiler)
                else:
                    cspecs.add(s.compiler)

        return cspecs

    def generate_asp_program(self, specs):
        """Write an ASP program for specs.

        Writes to this AspGenerator's output stream.

        Arguments:
            specs (list): list of Specs to solve
        """
        # preliminary checks
        check_packages_exist(specs)

        # get list of all possible dependencies
        self.possible_virtuals = set()
        possible = spack.package.possible_dependencies(
            *specs,
            virtuals=self.possible_virtuals,
            deptype=("build", "link", "run")
        )
        pkgs = set(possible)

        # get possible compilers
        self.possible_compilers = self.generate_possible_compilers(specs)

        # read the main ASP program from concrtize.lp
        concretize_lp = pkgutil.get_data('spack.solver', 'concretize.lp')
        self.out.write(concretize_lp.decode("utf-8"))

        # traverse all specs and packages to build dict of possible versions
        self.build_version_dict(possible, specs)

        self.h1('General Constraints')
        self.available_compilers()
        self.compiler_defaults()

        # architecture defaults
        self.platform_defaults()
        self.os_defaults(specs)
        self.target_defaults(specs)

        self.virtual_providers()
        self.provider_defaults()
        self.flag_defaults()

        self.h1('Package Constraints')
        for pkg in sorted(pkgs):
            self.h2('Package: %s' % pkg)
            self.pkg_rules(pkg)

        self.h1('Spec Constraints')
        for spec in sorted(specs):
            self.fact(fn.root(spec.name))
            for dep in spec.traverse():
                self.h2('Spec: %s' % str(dep))

                if dep.virtual:
                    self.fact(fn.virtual_node(dep.name))
                else:
                    for clause in self.spec_clauses(dep):
                        self.fact(clause)

        self.out.write('\n')
        display_lp = pkgutil.get_data('spack.solver', 'display.lp')
        self.out.write(display_lp.decode("utf-8"))


class ResultParser(object):
    """Class with actions that can re-parse a spec from ASP."""
    def __init__(self, specs):
        self._result = None

        self._command_line_specs = specs
        self._flag_sources = collections.defaultdict(lambda: set())
        self._flag_compiler_defaults = set()

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
        pkg_class = spack.repo.path.get_pkg_class(pkg)

        variant = self._specs[pkg].variants.get(name)
        if variant:
            # it's multi-valued
            variant.append(value)
        else:
            variant = pkg_class.variants[name].make_variant(value)
            self._specs[pkg].variants[name] = variant

    def version(self, pkg, version):
        self._specs[pkg].versions = ver([version])

    def node_compiler(self, pkg, compiler):
        self._specs[pkg].compiler = spack.spec.CompilerSpec(compiler)

    def node_compiler_version(self, pkg, compiler, version):
        self._specs[pkg].compiler.versions = spack.version.VersionList(
            [version])

    def node_flag_compiler_default(self, pkg):
        self._flag_compiler_defaults.add(pkg)

    def node_flag(self, pkg, flag_type, flag):
        self._specs[pkg].compiler_flags.setdefault(flag_type, []).append(flag)

    def node_flag_source(self, pkg, source):
        self._flag_sources[pkg].add(source)

    def no_flags(self, pkg, flag_type):
        self._specs[pkg].compiler_flags[flag_type] = []

    def depends_on(self, pkg, dep, type):
        dependency = self._specs[pkg]._dependencies.get(dep)
        if not dependency:
            self._specs[pkg]._add_dependency(
                self._specs[dep], (type,))
        else:
            dependency.add_type(type)

    def reorder_flags(self):
        """Order compiler flags on specs in predefined order.

        We order flags so that any node's flags will take priority over
        those of its dependents.  That is, the deepest node in the DAG's
        flags will appear last on the compile line, in the order they
        were specified.

        The solver determines wihch flags are on nodes; this routine
        imposes order afterwards.
        """
        # nodes with no flags get flag order from compiler
        compilers = dict((c.spec, c) for c in compilers_for_default_arch())
        for pkg in self._flag_compiler_defaults:
            spec = self._specs[pkg]
            compiler_flags = compilers[spec.compiler].flags
            check_same_flags(spec.compiler_flags, compiler_flags)
            spec.compiler_flags.update(compiler_flags)

        # index of all specs (and deps) from the command line by name
        cmd_specs = dict(
            (s.name, s)
            for spec in self._command_line_specs
            for s in spec.traverse())

        # iterate through specs with specified flaggs
        for pkg, sources in self._flag_sources.items():
            spec = self._specs[pkg]

            # order is determined by the DAG.  A spec's flags come after
            # any from its ancestors on the compile line.
            order = [
                s.name
                for s in spec.traverse(order='post', direction='parents')]

            # sort the sources in our DAG order
            sorted_sources = sorted(
                sources, key=lambda s: order.index(s))

            # add flags from each source, lowest to highest precedence
            flags = collections.defaultdict(lambda: [])
            for source_name in sorted_sources:
                source = cmd_specs[source_name]
                for name, flag_list in source.compiler_flags.items():
                    extend_flag_list(flags[name], flag_list)

            check_same_flags(spec.compiler_flags, flags)
            spec.compiler_flags.update(flags)

    def call_actions_for_functions(self, function_strings):
        function_re = re.compile(r'(\w+)\(([^)]*)\)')

        # parse functions out of ASP output
        functions = []
        for string in function_strings:
            m = function_re.match(string)
            name, arg_string = m.groups()
            args = re.split(r'\s*,\s*', arg_string)
            args = [s.strip('"') if s.startswith('"') else int(s)
                    for s in args]
            functions.append((name, args))

        # Functions don't seem to be in particular order in output.  Sort
        # them here so that directives that build objects (like node and
        # node_compiler) are called in the right order.
        functions.sort(key=lambda f: {
            "node": -2,
            "node_compiler": -1,
        }.get(f[0], 0))

        self._specs = {}
        for name, args in functions:
            action = getattr(self, name, None)
            if not action:
                print("%s(%s)" % (name, ", ".join(str(a) for a in args)))
                continue

            assert action and callable(action)
            action(*args)

    def parse_json(self, data, result):
        """Parse Clingo's JSON output format, which can give a lot of answers.

        This can be slow, espeically if Clingo comes back having explored
        a lot of models.
        """
        if data["Result"] == "UNSATISFIABLE":
            result.satisfiable = False
            return

        result.satisfiable = True
        if data["Result"] == "OPTIMUM FOUND":
            result.optimal = True

        nmodels = data["Models"]["Number"]
        best_model_number = nmodels - 1
        best_model = data["Call"][0]["Witnesses"][best_model_number]
        opt = list(best_model["Costs"])

        functions = best_model["Value"]

        self.call_actions_for_functions(functions)
        self.reorder_flags()
        result.answers.append((opt, best_model_number, self._specs))

    def parse_best(self, output, result):
        """Parse Clingo's competition output format, which gives one answer."""
        best_model_number = 0
        for line in output:
            match = re.match(r"% Answer: (\d+)", line)
            if match:
                best_model_number = int(match.group(1))

            if re.match("INCONSISTENT", line):
                result.satisfiable = False
                return

            if re.match("ANSWER", line):
                result.satisfiable = True

                answer = next(output)
                functions = [
                    f.rstrip(".") for f in re.split(r"\s+", answer.strip())
                ]
                self.call_actions_for_functions(functions)

                costs = re.split(r"\s+", next(output).strip())
                opt = [int(x) for x in costs[1:]]

                for spec in self._specs.values():
                    # namespace assignment can be done after the fact, as
                    # it is not part of the solve
                    repo = spack.repo.path.repo_for_pkg(spec)
                    spec.namespace = repo.namespace

                    # once this is done, everything is concrete
                    spec._mark_concrete()

                self.reorder_flags()
                result.answers.append((opt, best_model_number, self._specs))


class Result(object):
    def __init__(self, asp):
        self.asp = asp
        self.satisfiable = None
        self.optimal = None
        self.warnings = None

        # specs ordered by optimization level
        self.answers = []


def highlight(string):
    """Syntax highlighting for ASP programs"""
    # variables
    string = re.sub(r'\b([A-Z])\b', r'@y{\1}', string)

    # implications
    string = re.sub(r':-', r'@*G{:-}', string)

    # final periods
    string = re.sub(r'^([^%].*)\.$', r'\1@*G{.}', string, flags=re.MULTILINE)

    # directives
    string = re.sub(
        r'(#\w*)( (?:\w*)?)((?:/\d+)?)', r'@*B{\1}@c{\2}\3', string)

    # functions
    string = re.sub(r'(\w[\w-]+)\(([^)]*)\)', r'@C{\1}@w{(}\2@w{)}', string)

    # comments
    string = re.sub(r'(%.*)$', r'@w\1@.', string, flags=re.MULTILINE)

    # strings
    string = re.sub(r'("[^"]*")', r'@m{\1}', string)

    # result
    string = re.sub(r'\bUNSATISFIABLE', "@R{UNSATISFIABLE}", string)
    string = re.sub(r'\bINCONSISTENT', "@R{INCONSISTENT}", string)
    string = re.sub(r'\bSATISFIABLE', "@G{SATISFIABLE}", string)
    string = re.sub(r'\bOPTIMUM FOUND', "@G{OPTIMUM FOUND}", string)

    return string


class Timer(object):
    def __init__(self):
        self.start = time.time()
        self.last = self.start
        self.phases = {}

    def phase(self, name):
        last = self.last
        now = time.time()
        self.phases[name] = now - last
        self.last = now

    def write(self, out=sys.stdout):
        now = time.time()
        out.write("Time:\n")
        for phase, t in self.phases.items():
            out.write("    %-15s%.4f\n" % (phase + ":", t))
        out.write("Total: %.4f\n" % (now - self.start))


#
# These are handwritten parts for the Spack ASP model.
#
def solve(specs, dump=None, models=0, timers=False):
    """Solve for a stable model of specs.

    Arguments:
        specs (list): list of Specs to solve.
        dump (tuple): what to dump
        models (int): number of models to search (default: 0)
    """
    clingo = which('clingo', required=True)
    parser = ResultParser(specs)

    def colorize(string):
        color.cprint(highlight(color.cescape(string)))

    timer = Timer()
    with tempfile.TemporaryFile("w+") as program:
        generator = AspGenerator(program)
        generator.generate_asp_program(specs)
        timer.phase("generate")
        program.seek(0)

        result = Result(program.read())
        program.seek(0)

        if dump and 'asp' in dump:
            if sys.stdout.isatty():
                tty.msg('ASP program:')

            if dump == ['asp']:
                print(result.asp)
                return
            else:
                colorize(result.asp)
            timer.phase("dump")

        with tempfile.TemporaryFile("w+") as output:
            with tempfile.TemporaryFile() as warnings:
                clingo(
                    '--models=%d' % models,
                    # 1 is "competition" format with just optimal answer
                    # 2 is JSON format with all explored answers
                    '--outf=1',
                    # Use a highest priority criteria-first optimization
                    # strategy, which means we'll explore recent
                    # versions, preferred packages first.  This works
                    # well because Spack solutions are pretty easy to
                    # find -- there are just a lot of them.  Without
                    # this, it can take a VERY long time to find good
                    # solutions, and a lot of models are explored.
                    '--opt-strategy=bb,hier',
                    input=program,
                    output=output,
                    error=warnings,
                    fail_on_error=False)
                timer.phase("solve")

                warnings.seek(0)
                result.warnings = warnings.read().decode("utf-8")

                # dump any warnings generated by the solver
                if result.warnings:
                    if sys.stdout.isatty():
                        tty.msg('Clingo gave the following warnings:')
                    colorize(result.warnings)

                output.seek(0)
                result.output = output.read()
                timer.phase("read")

                # dump the raw output of the solver
                if dump and 'output' in dump:
                    if sys.stdout.isatty():
                        tty.msg('Clingo output:')
                    print(result.output)

                    if 'solutions' not in dump:
                        return

                output.seek(0)
                parser.parse_best(output, result)
                timer.phase("parse")

        if timers:
            timer.write()
            print()

    return result
