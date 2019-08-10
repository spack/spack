# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import collections
import re
import sys
import tempfile
import types
from six import string_types

import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack
import spack.cmd
import spack.spec
import spack.package
import spack.repo
from spack.util.executable import which
from spack.version import ver


#: generate the problem space, establish cardinality constraints
_generate = """\
% One version, arch, etc. per package
{ version(P, V) : version(P, V) } = 1             :- node(P).
{ arch_platform(P, A) : arch_platform(P, A) } = 1 :- node(P).
{ arch_os(P, A) : arch_os(P, A) } = 1             :- node(P).
{ arch_target(P, T) : arch_target(P, T) } = 1     :- node(P).

% one variant value for single-valued variants.
{ variant_value(P, V, X) : variant_value(P, V, X) } = 1
    :- node(P), variant(P, V), not variant_single_value(P, V).
"""

#: define the rules of Spack concretization
_define = """\
% dependencies imply new nodes.
node(D) :- node(P), depends_on(P, D).

% propagate platform, os, target downwards
arch_platform(D, A) :- node(D), depends_on(P, D), arch_platform(P, A).
arch_os(D, A) :- node(D), depends_on(P, D), arch_os(P, A).
arch_target(D, A) :- node(D), depends_on(P, D), arch_target(P, A).

% if a variant is set to anything, it is considered "set".
variant_set(P, V) :- variant_set(P, V, _).

% variant_set is an explicitly set variant value. If it's not "set",
% we revert to the default value. If it is set, we force the set value
variant_value(P, V, X) :- node(P), variant(P, V), variant_set(P, V, X).
"""

#: what parts of the model to display to read models back in
_display = """\
#show node/1.
#show depends_on/2.
#show version/2.
#show variant_value/3.
#show arch_platform/2.
#show arch_os/2.
#show arch_target/2.
"""


def _id(thing):
    """Quote string if needed for it to be a valid identifier."""
    return '"%s"' % str(thing)


def issequence(obj):
    if isinstance(obj, string_types):
        return False
    return isinstance(obj, (collections.Sequence, types.GeneratorType))


def listify(args):
    if len(args) == 1 and issequence(args[0]):
        return list(args[0])
    return list(args)


def packagize(pkg):
    if isinstance(pkg, spack.package.PackageMeta):
        return pkg
    return spack.repo.path.get_pkg_class(pkg)


def specify(spec):
    if isinstance(spec, spack.spec.Spec):
        return spec
    return spack.spec.Spec(spec)


class AspFunction(object):
    def __init__(self, name):
        self.name = name
        self.args = []

    def __call__(self, *args):
        self.args[:] = args
        return self

    def __str__(self):
        return "%s(%s)" % (
            self.name, ', '.join(_id(arg) for arg in self.args))


class AspAnd(object):
    def __init__(self, *args):
        args = listify(args)
        self.args = args

    def __str__(self):
        s = ", ".join(str(arg) for arg in self.args)
        return s


class AspOr(object):
    def __init__(self, *args):
        args = listify(args)
        self.args = args

    def __str__(self):
        return " | ".join(str(arg) for arg in self.args)


class AspNot(object):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "not %s" % self.arg


class AspFunctionBuilder(object):
    def __getattr__(self, name):
        return AspFunction(name)


fn = AspFunctionBuilder()


class AspGenerator(object):
    def __init__(self, out):
        self.out = out
        self.func = AspFunctionBuilder()

    def title(self, name):
        self.out.write('\n')
        self.out.write("%% %s\n" % name)
        self.out.write("% -----------------------------------------\n")

    def section(self, name):
        self.out.write("\n")
        self.out.write("%\n")
        self.out.write("%% %s\n" % name)
        self.out.write("%\n")

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
        self.out.write("%s :- %s.\n" % (head, body))

    def constraint(self, body):
        """ASP integrity constraint (rule with no head; can't be true)."""
        self.out.write(":- %s.\n" % body)

    def pkg_version_rules(self, pkg):
        pkg = packagize(pkg)
        self.rule(
            self._or(fn.version(pkg.name, v) for v in pkg.versions),
            fn.node(pkg.name))

    def spec_versions(self, spec):
        spec = specify(spec)

        if spec.concrete:
            self.rule(fn.version(spec.name, spec.version),
                      fn.node(spec.name))
        else:
            version = spec.versions
            impossible, possible = [], []
            for v in spec.package.versions:
                if v.satisfies(version):
                    possible.append(v)
                else:
                    impossible.append(v)

            if impossible:
                self.rule(
                    self._and(self._not(fn.version(spec.name, v))
                              for v in impossible),
                    fn.node(spec.name))
            if possible:
                self.rule(
                    self._or(fn.version(spec.name, v) for v in possible),
                    fn.node(spec.name))

    def pkg_rules(self, pkg):
        pkg = packagize(pkg)

        # versions
        self.pkg_version_rules(pkg)

        # variants
        for name, variant in pkg.variants.items():
            self.rule(fn.variant(pkg.name, name),
                      fn.node(pkg.name))

            single_value = not variant.multi
            single = fn.variant_single_value(pkg.name, name)
            if single_value:
                self.rule(single, fn.node(pkg.name))
                self.rule(fn.variant_value(pkg.name, name, variant.default),
                          self._not(fn.variant_set(pkg.name, name)))
            else:
                self.rule(self._not(single), fn.node(pkg.name))
                defaults = variant.default.split(',')
                for val in defaults:
                    self.rule(fn.variant_value(pkg.name, name, val),
                              self._not(fn.variant_set(pkg.name, name)))

        # dependencies
        for name, conditions in pkg.dependencies.items():
            for cond, dep in conditions.items():
                self.fact(fn.depends_on(dep.pkg.name, dep.spec.name))

    def spec_rules(self, spec):
        self.fact(fn.node(spec.name))
        self.spec_versions(spec)

        # seed architecture at the root (we'll propagate later)
        # TODO: use better semantics.
        arch = spack.spec.ArchSpec(spack.architecture.sys_type())
        spec_arch = spec.architecture
        if spec_arch:
            if spec_arch.platform:
                arch.platform = spec_arch.platform
            if spec_arch.os:
                arch.os = spec_arch.os
            if spec_arch.target:
                arch.target = spec_arch.target
        self.fact(fn.arch_platform(spec.name, arch.platform))
        self.fact(fn.arch_os(spec.name, arch.os))
        self.fact(fn.arch_target(spec.name, arch.target))

        # variants
        for vname, variant in spec.variants.items():
            self.fact(fn.variant_value(spec.name, vname, variant.value))

        # TODO
        # dependencies
        # compiler
        # external_path
        # external_module
        # compiler_flags
        # namespace

    def generate_asp_program(self, specs):
        """Write an ASP program for specs.

        Writes to this AspGenerator's output stream.

        Arguments:
            specs (list): list of Specs to solve
        """
        # get list of all possible dependencies
        pkg_names = set(spec.fullname for spec in specs)
        pkgs = [spack.repo.path.get_pkg_class(name) for name in pkg_names]
        pkgs = list(set(spack.package.possible_dependencies(*pkgs))
                    | set(pkg_names))

        self.title("Generate")
        self.out.write(_generate)

        self.title("Define")
        self.out.write(_define)

        self.title("Package Constraints")
        for pkg in pkgs:
            self.section(pkg)
            self.pkg_rules(pkg)

        self.title("Spec Constraints")
        for spec in specs:
            self.section(str(spec))
            self.spec_rules(spec)

        self.title("Display")
        self.out.write(_display)
        self.out.write('\n\n')


class ResultParser(object):
    """Class with actions that can re-parse a spec from ASP."""
    def __init__(self):
        self._result = None

    def node(self, pkg):
        if pkg not in self._specs:
            self._specs[pkg] = spack.spec.Spec(pkg)

    def _arch(self, pkg):
        arch = self._specs[pkg].architecture
        if not arch:
            arch = spack.spec.ArchSpec()
            self._specs[pkg].architecture = arch
        return arch

    def arch_platform(self, pkg, platform):
        self._arch(pkg).platform = platform

    def arch_os(self, pkg, os):
        self._arch(pkg).os = os

    def arch_target(self, pkg, target):
        self._arch(pkg).target = target

    def variant_value(self, pkg, name, value):
        pkg_class = spack.repo.path.get_pkg_class(pkg)
        variant = pkg_class.variants[name].make_variant(value)
        self._specs[pkg].variants[name] = variant

    def version(self, pkg, version):
        self._specs[pkg].versions = ver([version])

    def depends_on(self, pkg, dep):
        self._specs[pkg]._add_dependency(
            self._specs[dep], ('link', 'run'))

    def parse(self, stream, result):
        for line in stream:
            match = re.match(r'SATISFIABLE', line)
            if match:
                result.satisfiable = True
                continue

            match = re.match(r'UNSATISFIABLE', line)
            if match:
                result.satisfiable = False
                continue

            match = re.match(r'Answer: (\d+)', line)
            if not match:
                continue

            answer_number = int(match.group(1))
            assert answer_number == len(result.answers) + 1

            answer = next(stream)
            tty.debug("Answer: %d" % answer_number, answer)

            self._specs = {}
            for m in re.finditer(r'(\w+)\(([^)]*)\)', answer):
                name, arg_string = m.groups()
                args = re.findall(r'"([^"]*)"', arg_string)

                action = getattr(self, name)
                assert action and callable(action)
                action(*args)

            result.answers.append(self._specs)


class Result(object):
    def __init__(self, asp):
        self.asp = asp
        self.satisfiable = None
        self.warnings = None
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
    string = re.sub(r'(%.*)$', r'@K\1@.', string, flags=re.MULTILINE)

    # strings
    string = re.sub(r'("[^"]*")', r'@m{\1}', string)

    # result
    string = re.sub(r'\bUNSATISFIABLE', "@R{UNSATISFIABLE}", string)
    string = re.sub(r'\bINCONSISTENT', "@R{INCONSISTENT}", string)
    string = re.sub(r'\bSATISFIABLE', "@G{SATISFIABLE}", string)

    return string

#
# These are handwritten parts for the Spack ASP model.
#
def solve(specs, dump=None, models=1):
    """Solve for a stable model of specs.

    Arguments:
        specs (list): list of Specs to solve.
        dump (tuple): what to dump
        models (int): number of satisfying specs to find (default: 1)
    """
    clingo = which('clingo', required=True)
    parser = ResultParser()

    def colorize(string):
        color.cprint(highlight(color.cescape(string)))

    with tempfile.TemporaryFile("w+") as program:
        generator = AspGenerator(program)
        generator.generate_asp_program(specs)
        program.seek(0)

        result = Result(program.read())
        program.seek(0)

        if 'asp' in dump:
            if sys.stdout.isatty():
                tty.msg('ASP program:')
            colorize(result.asp)

        with tempfile.TemporaryFile("w+") as output:
            with tempfile.TemporaryFile() as warnings:
                clingo(
                    '--models=%d' % models,
                    input=program,
                    output=output,
                    error=warnings,
                    fail_on_error=False)

                warnings.seek(0)
                result.warnings = warnings.read()

                # dump any warnings generated by the solver
                if 'warnings' in dump:
                    if result.warnings:
                        if sys.stdout.isatty():
                            tty.msg('Clingo gave the following warnings:')
                        colorize(result.warnings)
                    else:
                        if sys.stdout.isatty():
                            tty.msg('No warnings.')

                output.seek(0)
                result.output = output.read()

                # dump the raw output of the solver
                if 'output' in dump:
                    if sys.stdout.isatty():
                        tty.msg('Clingo output:')
                    colorize(result.output)

                output.seek(0)
                parser.parse(output, result)

    return result
