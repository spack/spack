# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import collections
import types

import spack
import spack.cmd
import spack.spec
import spack.package


def title(name):
    print()
    print("%% %s" % name)
    print("% -----------------------------------------")


def section(name):
    print()
    print("%")
    print("%% %s" % name)
    print("%")


def _id(thing):
    """Quote string if needed for it to be a valid identifier."""
    return '"%s"' % str(thing)


def issequence(obj):
    if isinstance(obj, basestring):
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


class AspBuilder(object):
    def _or(self, *args):
        return AspOr(*args)

    def _and(self, *args):
        return AspAnd(*args)

    def _not(self, arg):
        return AspNot(arg)

    def _fact(self, head):
        """ASP fact (a rule without a body)."""
        print("%s." % head)

    def _rule(self, head, body):
        """ASP rule (an implication)."""
        print("%s :- %s." % (head, body))

    def _constraint(self, body):
        """ASP integrity constraint (rule with no head; can't be true)."""
        print(":- %s." % body)

    def __getattr__(self, name):
        return AspFunction(name)


asp = AspBuilder()


def pkg_version_rules(pkg):
    pkg = packagize(pkg)
    asp._rule(
        asp._or(asp.version(pkg.name, v) for v in pkg.versions),
        asp.node(pkg.name))


def spec_versions(spec):
    spec = specify(spec)

    if spec.concrete:
        asp._rule(asp.version(spec.name, spec.version),
                  asp.node(spec.name))
    else:
        version = spec.versions
        impossible, possible = [], []
        for v in spec.package.versions:
            if v.satisfies(version):
                possible.append(v)
            else:
                impossible.append(v)

        if impossible:
            asp._rule(
                asp._and(asp._not(asp.version(spec.name, v))
                         for v in impossible),
                asp.node(spec.name))
        if possible:
            asp._rule(
                asp._or(asp.version(spec.name, v) for v in possible),
                asp.node(spec.name))


def pkg_rules(pkg):
    pkg = packagize(pkg)

    # versions
    pkg_version_rules(pkg)

    # dependencies
    for name, conditions in pkg.dependencies.items():
        for cond, dep in conditions.items():
            asp._fact(asp.depends_on(dep.pkg.name, dep.spec.name))


def spec_rules(spec):
    asp._fact(asp.node(spec.name))
    spec_versions(spec)

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
    asp._fact(asp.arch_platform(spec.name, arch.platform))
    asp._fact(asp.arch_os(spec.name, arch.os))
    asp._fact(asp.arch_target(spec.name, arch.target))

    # TODO
    # dependencies
    # compiler
    # external_path
    # external_module
    # compiler_flags
    # namespace

#
# These are handwritten parts for the Spack ASP model.
#


#: generate the problem space, establish cardinality constraints
_generate = """\
% One version, arch, etc. per package
{ version(P, V) : version(P, V) } = 1             :- node(P).
{ arch_platform(P, A) : arch_platform(P, A) } = 1 :- node(P).
{ arch_os(P, A) : arch_os(P, A) } = 1             :- node(P).
{ arch_target(P, T) : arch_target(P, T) } = 1     :- node(P).
"""

#: define the rules of Spack concretization
_define = """\
% dependencies imply new nodes.
node(D) :- node(P), depends_on(P, D).

% propagate platform, os, target downwards
arch_platform(D, A) :- node(D), depends_on(P, D), arch_platform(P, A).
arch_os(D, A) :- node(D), depends_on(P, D), arch_os(P, A).
arch_target(D, A) :- node(D), depends_on(P, D), arch_target(P, A).
"""

#: what parts of the model to display to read models back in
_display = """\
#show node/1.
#show depends_on/2.
#show version/2.
#show arch_platform/2.
#show arch_os/2.
#show arch_target/2.
"""


def solve(specs):
    """Solve for a stable model of specs.

    Arguments:
        specs (list): list of Specs to solve.
    """

    # get list of all possible dependencies
    pkg_names = set(spec.fullname for spec in specs)
    pkgs = [spack.repo.path.get_pkg_class(name) for name in pkg_names]
    pkgs = spack.package.possible_dependencies(*pkgs)

    title("Generate")
    print(_generate)

    title("Define")
    print(_define)

    title("Package Constraints")
    for pkg in pkgs:
        section(pkg)
        pkg_rules(pkg)

    title("Spec Constraints")
    for spec in specs:
        section(str(spec))
        spec_rules(spec)

    title("Display")
    print(_display)
    print()
    print()
