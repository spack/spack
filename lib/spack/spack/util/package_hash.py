##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://software.llnl.gov/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import ast
import hashlib

import spack.repo
import spack.package
import spack.directives
import spack.error
import spack.spec
import spack.util.naming


class RemoveDocstrings(ast.NodeTransformer):
    """Transformer that removes docstrings from a Python AST."""
    def remove_docstring(self, node):
        if node.body:
            if isinstance(node.body[0], ast.Expr) and \
               isinstance(node.body[0].value, ast.Str):
                node.body.pop(0)

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
        return (isinstance(node, ast.Expr) and
                node.value and isinstance(node.value, ast.Call) and
                node.value.func.id in spack.directives.__all__)

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
    """Tag @when-decorated methods in a spec."""
    def __init__(self, spec):
        self.spec = spec
        self.methods = {}

    def visit_FunctionDef(self, node):  # noqa
        nodes = self.methods.setdefault(node.name, [])
        if node.decorator_list:
            dec = node.decorator_list[0]
            if isinstance(dec, ast.Call) and dec.func.id == 'when':
                cond = dec.args[0].s
                nodes.append((node, self.spec.satisfies(cond, strict=True)))
        else:
            nodes.append((node, None))


class ResolveMultiMethods(ast.NodeTransformer):
    """Remove methods which do not exist if their @when is not satisfied."""
    def __init__(self, methods):
        self.methods = methods

    def resolve(self, node):
        if node.name not in self.methods:
            raise PackageHashError(
                "Future traversal visited new node: %s" % node.name)

        result = None
        for n, cond in self.methods[node.name]:
            if cond:
                return n
            if cond is None:
                result = n
        return result

    def visit_FunctionDef(self, node):  # noqa
        if self.resolve(node) is node:
            node.decorator_list = []
            return node
        return None


def package_content(spec):
    return ast.dump(package_ast(spec))


def package_hash(spec, content=None):
    if content is None:
        content = package_content(spec)
    return hashlib.sha256(content.encode('utf-8')).digest().lower()


def package_ast(spec):
    spec = spack.spec.Spec(spec)

    filename = spack.repo.path.filename_for_package_name(spec.name)
    with open(filename) as f:
        text = f.read()
        root = ast.parse(text)

    root = RemoveDocstrings().visit(root)

    RemoveDirectives(spec).visit(root)

    fmm = TagMultiMethods(spec)
    fmm.visit(root)

    root = ResolveMultiMethods(fmm.methods).visit(root)
    return root


class PackageHashError(spack.error.SpackError):
    """Raised for all errors encountered during package hashing."""
