# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import hashlib

import spack.directives
import spack.error
import spack.package
import spack.repo
import spack.spec
import spack.util.hash
import spack.util.naming
from spack.util.unparse import unparse


class RemoveDocstrings(ast.NodeTransformer):
    """Transformer that removes docstrings from a Python AST.

    This removes *all* strings that aren't on the RHS of an assignment statement from
    the body of functions, classes, and modules -- even if they're not directly after
    the declaration.

    """
    def remove_docstring(self, node):
        def unused_string(node):
            """Criteria for unassigned body strings."""
            return isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)

        if node.body:
            node.body = [child for child in node.body if not unused_string(child)]

        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):  # noqa
        return self.remove_docstring(node)

    def visit_ClassDef(self, node):  # noqa
        return self.remove_docstring(node)

    def visit_Module(self, node):  # noqa
        return self.remove_docstring(node)


class RemoveDirectives(ast.NodeTransformer):
    """Remove Spack directives from a package AST."""
    def __init__(self, spec):
        self.spec = spec

    def is_directive(self, node):
        """Check to determine if the node is a valid directive

        Directives are assumed to be represented in the AST as a named function
        call expression.  This means that they will NOT be represented by a
        named function call within a function call expression (e.g., as
        callbacks are sometimes represented).

        Args:
            node (ast.AST): the AST node being checked

        Returns:
            bool: ``True`` if the node represents a known directive,
                ``False`` otherwise
        """
        return (isinstance(node, ast.Expr) and
                node.value and isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Name) and
                node.value.func.id in spack.directives.directive_names)

    def is_spack_attr(self, node):
        return (isinstance(node, ast.Assign) and
                node.targets and isinstance(node.targets[0], ast.Name) and
                node.targets[0].id in spack.package.Package.metadata_attrs)

    def visit_ClassDef(self, node):  # noqa
        if node.name == spack.util.naming.mod_to_class(self.spec.name):
            node.body = [
                c for c in node.body
                if (not self.is_directive(c) and not self.is_spack_attr(c))]
        return node


class TagMultiMethods(ast.NodeVisitor):
    """Tag @when-decorated methods in a package AST."""
    def __init__(self, spec):
        self.spec = spec
        # map from function name to (implementation, condition_list) tuples
        self.methods = {}

    def visit_FunctionDef(self, func):  # noqa
        conditions = []
        for dec in func.decorator_list:
            if isinstance(dec, ast.Call) and dec.func.id == 'when':
                try:
                    # evaluate spec condition for any when's
                    cond = dec.args[0].s
                    conditions.append(self.spec.satisfies(cond, strict=True))
                except AttributeError:
                    # In this case the condition for the 'when' decorator is
                    # not a string literal (for example it may be a Python
                    # variable name). We append None because we don't know
                    # whether the constraint applies or not, and it should be included
                    # unless some other constraint is False.
                    conditions.append(None)

        # anything defined without conditions will overwrite prior definitions
        if not conditions:
            self.methods[func.name] = []

        # add all discovered conditions on this node to the node list
        impl_conditions = self.methods.setdefault(func.name, [])
        impl_conditions.append((func, conditions))

        # don't modify the AST -- return the untouched function node
        return func


class ResolveMultiMethods(ast.NodeTransformer):
    """Remove multi-methods when we know statically that they won't be used.

    Say we have multi-methods like this::

        class SomePackage:
            def foo(self): print("implementation 1")

            @when("@1.0")
            def foo(self): print("implementation 2")

            @when("@2.0")
            @when(sys.platform == "darwin")
            def foo(self): print("implementation 3")

            @when("@3.0")
            def foo(self): print("implementation 4")

    The multimethod that will be chosen at runtime depends on the package spec and on
    whether we're on the darwin platform *at build time* (the darwin condition for
    implementation 3 is dynamic). We know the package spec statically; we don't know
    statically what the runtime environment will be. We need to include things that can
    possibly affect package behavior in the package hash, and we want to exclude things
    when we know that they will not affect package behavior.

    If we're at version 4.0, we know that implementation 1 will win, because some @when
    for 2, 3, and 4 will be `False`. We should only include implementation 1.

    If we're at version 1.0, we know that implementation 2 will win, because it
    overrides implementation 1.  We should only include implementation 2.

    If we're at version 3.0, we know that implementation 4 will win, because it
    overrides implementation 1 (the default), and some @when on all others will be
    False.

    If we're at version 2.0, it's a bit more complicated. We know we can remove
    implementations 2 and 4, because their @when's will never be satisfied. But, the
    choice between implementations 1 and 3 will happen at runtime (this is a bad example
    because the spec itself has platform information, and we should prefer to use that,
    but we allow arbitrary boolean expressions in @when's, so this example suffices).
    For this case, we end up needing to include *both* implementation 1 and 3 in the
    package hash, because either could be chosen.

    """
    def __init__(self, methods):
        self.methods = methods

    def resolve(self, impl_conditions):
        """Given list of nodes and conditions, figure out which node will be chosen."""
        result = []
        default = None
        for impl, conditions in impl_conditions:
            # if there's a default implementation with no conditions, remember that.
            if not conditions:
                default = impl
                result.append(default)
                continue

            # any known-false @when means the method won't be used
            if any(c is False for c in conditions):
                continue

            # anything with all known-true conditions will be picked if it's first
            if all(c is True for c in conditions):
                if result and result[0] is default:
                    return [impl]  # we know the first MM will always win
                # if anything dynamic comes before it we don't know if it'll win,
                # so just let this result get appended

            # anything else has to be determined dynamically, so add it to a list
            result.append(impl)

        # if nothing was picked, the last definition wins.
        return result

    def visit_FunctionDef(self, func):  # noqa
        # if the function def wasn't visited on the first traversal there is a problem
        assert func.name in self.methods, "Inconsistent package traversal!"

        # if the function is a multimethod, need to resolve it statically
        impl_conditions = self.methods[func.name]

        resolutions = self.resolve(impl_conditions)
        if not any(r is func for r in resolutions):
            # multimethod did not resolve to this function; remove it
            return None

        # if we get here, this function is a possible resolution for a multi-method.
        # it might be the only one, or there might be several that have to be evaluated
        # dynamcially.  Either way, we include the function.

        # strip the when decorators (preserve the rest)
        func.decorator_list = [
            dec for dec in func.decorator_list
            if not (isinstance(dec, ast.Call) and dec.func.id == 'when')
        ]
        return func


def package_content(spec):
    return ast.dump(package_ast(spec))


def canonical_source(spec, filename=None, filter_multimethods=True):
    return unparse(
        package_ast(spec, filename, filter_multimethods),
        py_ver_consistent=True,
    )


def canonical_source_hash(spec, filename=None):
    source = canonical_source(spec, filename)
    return spack.util.hash.b32_hash(source)


def package_hash(spec, content=None):
    if content is None:
        content = package_content(spec)
    return hashlib.sha256(content.encode('utf-8')).digest().lower()


def package_ast(spec, filename=None, filter_multimethods=True):
    spec = spack.spec.Spec(spec)

    if not filename:
        filename = spack.repo.path.filename_for_package_name(spec.name)

    with open(filename) as f:
        text = f.read()
        root = ast.parse(text)

    root = RemoveDocstrings().visit(root)

    RemoveDirectives(spec).visit(root)

    if filter_multimethods:
        tagger = TagMultiMethods(spec)
        tagger.visit(root)
        root = ResolveMultiMethods(tagger.methods).visit(root)

    return root


class PackageHashError(spack.error.SpackError):
    """Raised for all errors encountered during package hashing."""
