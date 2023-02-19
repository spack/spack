#!/usr/bin/env spack-python

import ast
import contextlib

from io import StringIO
from typing import Dict, List, Optional

import spack.directives
import spack.repo
import spack.util.package_hash as ph


def is_directive(node):
    return (
        hasattr(node, "value")
        and node.value
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id in spack.directives.directive_names
    )


class NameDescriptor(object):
    """Name in a scope, with global/nonlocal and const information."""

    name: str
    const: bool
    isglobal: bool
    isnonlocal: bool

    def __init__(self, name: str, const: bool, isglobal: bool, isnonlocal: bool):
        self.name = name
        self.const = const
        self.isglobal = isglobal
        self.isnonlocal = isnonlocal


class ScopeStack(object):
    """Simple implementation of a stack of lexical scopes.

    We use this for very simple constant tracking in packages.

    """

    scopes: List[Dict[str, NameDescriptor]]

    def __init__(self):
        self.scopes = []

    def push(self, name):
        """Add a scope with a name for debugging."""
        self.scopes.append((name, {}))

    def pop(self, name):
        """Remove the top scope."""
        key, scope = self.scopes.pop()
        assert name == key
        return scope

    @contextlib.contextmanager
    def scope(self, name):
        try:
            self.push(name)
            yield self.top
        finally:
            self.pop(name)

    @property
    def top(self):
        """Get the top scope on the stack"""
        assert self.scopes
        _, scope = self.scopes[-1]
        return scope

    def define(self, name: str, const=None, isglobal=None, isnonlocal=None):
        # type: NameDescriptor -> None
        self.top[name] = NameDescriptor(name, const, isglobal, isnonlocal)

    def assign(self, name: str, const=None, isglobal=None, isnonlocal=None):

        self.top.add(name)

    def scope_for(self, name: str) -> Optional[Dict[str, NameDescriptor]]:
        for _, scope in reversed(self.scopes):
            if name in scope:
                return scope
        else:
            return None

    def get(self, name):
        # type: str -> Optional[NameDescriptor]
        scope = self.scope_for(name)
        return scope[name] if scope else None

    def delete(self, name):
        """Delete name from scope it lives in."""
        scope = self.scope_for(name)
        if not scope:
            raise KeyError("No name '%s' in any scope" % name)

        del scope[name]

    def __str__(self):
        out = StringIO()

        out.write("-" * 78)
        out.write("\n")

        for scope_name, scope in self.scopes:
            out.write(f"[{scope_name}]\n")
            for name, desc in scope.items():
                out.write("    ")
                out.write(f"{name:20}")
                out.write("C" if desc.const else "-")
                out.write("G" if desc.isglobal else "-")
                out.write("N" if desc.isnonlocal else "-")
                out.write("\n")

        out.write("-" * 78)
        out.write("\n")

        return out.getvalue()


def target_names(node, names=None):
    """Get names of values targeted by assignment.

    This does a naive thing and digs any and all names out of the assignment.
    TODO: We may need to be smarter about this analysis.

    """
    if names is None:
        names = set()

    if isinstance(node, ast.Name):
        print("  added", node.id)
        names.add(node.id)

    elif isinstance(node, (ast.List, ast.Tuple)):
        print("  adding from", node.elts)
        for elt in node.elts:
            names += target_names(elt)

    elif isinstance(node, (ast.Attribute, ast.Subscript, ast.Starred)):
        print("  adding from", node.value)
        names += target_names(node.value)
        # TODO: handle the attr in an Attribute to figure out if it's a variable in a
        # TODO: scope somewhere

    else:
        print("WHAT IS THIS: ", type(node))

    print(names)
    return names


def constexpr(node):
    if isinstance(node, ast.Constant):
        return True

    elif isinstance(node, (list, tuple)):
        return all(constexpr(arg) for arg in node)

    elif isinstance(node, (ast.Tuple, ast.List)):
        return all(constexpr(arg) for arg in node.elts)

    elif isinstance(node, ast.BinOp):
        return constexpr(node.left) and constexpr(node.right)

    elif isinstance(node, ast.Compare):
        return constexpr(node.left) and constexpr(node.right)

    #    elif isinstance(node, ast.Call):
    #        # allow some function calls in packages to be constexpr
    #        if isinstance(node.func, ast.Name):
    #            name = node.func.id
    #        elif isinstance(node.func, ast.Attribute):
    #            name =
    #            # common directives
    #            # TODO: we should really check that they're actually Spack's functions
    #            # and not some overridden name
    #            return node.func.id in (
    #                "any_combination_of",
    #                "auto_or_any_combination_of",
    #                "bool",
    #                "conditional",
    #                "disjoint_sets",
    #                "join_path",
    #                "str",
    #                "tuple",
    #                "patch",
    #            )

    else:
        return False


class ConstTracker(ast.NodeVisitor):
    """AST traversal that tracks the const-ness of variables defined in scopes."""

    def __init__(self, name=None):
        self.name = name or "<module>"
        self.scopes = ScopeStack()

    # These constructs create/destroy scopes and may define names

    def visit_Module(self, node):
        with self.scopes.scope("module:%s" % self.name):
            self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.scopes.define(node.name, const=False)

        with self.scopes.scope("class:%s" % node.name):
            self.generic_visit(node)

    def visit_AsyncClassDef(self, node):
        self.visit_ClassDef(node)

    def visit_FunctionDef(self, node):
        self.scopes.define(node.name, const=False)

        with self.scopes.scope("func:%s" % node.name):
            self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_GeneratorExp(self, node, leak=False):
        """Visitor used for generator expressions and comprehensions.

        Arguments:
            node (ast.Node): AST node to visit
            leak (bool): whether generator's targets leak into an outer scope

        In Python 2, Generator expressions do not leak but comprehensions do.
        In Python 3, none of these leak.
        """
        for comp in node.generators:
            if not leak:
                self.scopes.push("<generatorexp>")

            self.generic_visit(comp.iter)

            # We currently only test if the entire iter expression is const.
            #
            # TODO: if we need this to handle different targets separately, e.g. x and y in:
            #
            #    [(x, y) for x, y in [(a, 1), (b, 2), (c, 3)]]
            #
            # Then this needs to understand unpacking. Currently it's either all const or not,
            # So both x and y would be non-const here.
            const = constexpr(comp.iter)

            print(self.scopes)

            names = target_names(comp.target)
            for name in target_names(comp.target):
                # self.scopes.
                # self.scopes.define(name.id, const=const)
                pass

        # visit element expressions once the generator clauses are done
        self.generic_visit(node.elt)

        if not leak:
            for comp in reversed(node.generators):
                self.scopes.pop("<generatorexp>")

        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.visit_GeneratorExp(node)

    def visit_SetComp(self, node):
        self.visit_GeneratorExp(node)

    def visit_DictComp(self, node):
        self.visit_GeneratorExp(node)

    def visit_Lambda(self, node):
        self.generic_visit(node)

    # These constructs define names in scopes

    def visit_Assign(self, node):
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        """Operators like +="""
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.generic_visit(node)

    def visit_NamedExpr(self, node):
        """Walrus operator :="""
        self.generic_visit(node)

    def visit_withitem(self, node):
        self.generic_visit(node)

    def visit_For(self, node):
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.generic_visit(node)

    def visit_Import(self, node):
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.generic_visit(node)

    def visit_Delete(self, node):
        self.generic_visit(node)

    # these change the scope of names
    def visit_Global(self, node):
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        self.generic_visit(node)


class ConstDirectives(ConstTracker):
    def __init__(self, name):
        super(ConstDirectives, self).__init__(name)

        self.const = True
        self.name = name
        self.in_classdef = False

        self.issues = []

    def visit_Expr(self, node):
        # Directives are represented in the AST as named function call expressions (as
        # opposed to function calls through a variable callback).
        if is_directive(node):

            print(node.value.args[0].value)

            for arg in node.value.args:
                if not constexpr(arg):
                    #                    self.issues.append("ARG:   %s" % ast.dump(arg))
                    self.issues.append("ISSUE: " + ast.dump(arg))
                    self.const = False

            for k in node.value.keywords:
                if not constexpr(k.value):
                    # self.issues.append("KWARG: %s=%s" % (k.arg, ast.dump(k.value)))
                    self.issues.append("ISSUE: " + ast.dump(k.value))
                    self.const = False


for pkg_name in spack.repo.all_package_names():
    # for pkg_name in ["boost"]:
    filename = spack.repo.path.filename_for_package_name(pkg_name)
    with open(filename) as f:
        source = f.read()

    root = ast.parse(source)
    const = ConstDirectives(pkg_name)

    print("PACKAGE:", pkg_name)

    const.visit(root)
    if not const.const:
        for issue in const.issues:
            print("    ", issue)
