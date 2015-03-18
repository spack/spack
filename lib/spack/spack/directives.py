##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
"""This package contains directives that can be used within a package.

Directives are functions that can be called inside a package
definition to modify the package, for example:

    class OpenMpi(Package):
        depends_on("hwloc")
        provides("mpi")
        ...

``provides`` and ``depends_on`` are spack directives.

The available directives are:

  * ``version``
  * ``depends_on``
  * ``provides``
  * ``extends``
  * ``patch``

"""
__all__ = [ 'depends_on', 'extends', 'provides', 'patch', 'version' ]

import re
import inspect

from llnl.util.lang import *

import spack
import spack.spec
import spack.error
import spack.url
from spack.version import Version
from spack.patch import Patch
from spack.spec import Spec, parse_anonymous_spec


def directive(fun):
    """Decorator that allows a function to be called while a class is
       being constructed, and to modify the class.

       Adds the class scope as an initial parameter when called, like
       a class method would.
    """
    def directive_function(*args, **kwargs):
        pkg      = DictWrapper(caller_locals())
        pkg.name = get_calling_module_name()
        return fun(pkg, *args, **kwargs)
    return directive_function


@directive
def version(pkg, ver, checksum=None, **kwargs):
    """Adds a version and metadata describing how to fetch it.
       Metadata is just stored as a dict in the package's versions
       dictionary.  Package must turn it into a valid fetch strategy
       later.
    """
    versions = pkg.setdefault('versions', {})

    # special case checksum for backward compatibility
    if checksum:
        kwargs['md5'] = checksum

    # Store the kwargs for the package to use later when constructing
    # a fetch strategy.
    versions[Version(ver)] = kwargs


@directive
def depends_on(pkg, *specs):
    """Adds a dependencies local variable in the locals of
       the calling class, based on args. """
    dependencies = pkg.setdefault('dependencies', {})

    for string in specs:
        for spec in spack.spec.parse(string):
            if pkg.name == spec.name:
                raise CircularReferenceError('depends_on', pkg.name)
            dependencies[spec.name] = spec


@directive
def extends(pkg, spec, **kwargs):
    """Same as depends_on, but dependency is symlinked into parent prefix.

    This is for Python and other language modules where the module
    needs to be installed into the prefix of the Python installation.
    Spack handles this by installing modules into their own prefix,
    but allowing ONE module version to be symlinked into a parent
    Python install at a time.

    keyword arguments can be passed to extends() so that extension
    packages can pass parameters to the extendee's extension
    mechanism.

    """
    dependencies = pkg.setdefault('dependencies', {})
    extendees = pkg.setdefault('extendees', {})
    if extendees:
        raise RelationError("Packages can extend at most one other package.")

    spec = Spec(spec)
    if pkg.name == spec.name:
        raise CircularReferenceError('extends', pkg.name)
    dependencies[spec.name] = spec
    extendees[spec.name] = (spec, kwargs)


@directive
def provides(pkg, *specs, **kwargs):
    """Allows packages to provide a virtual dependency.  If a package provides
       'mpi', other packages can declare that they depend on "mpi", and spack
       can use the providing package to satisfy the dependency.
    """
    spec_string = kwargs.get('when', pkg.name)
    provider_spec = parse_anonymous_spec(spec_string, pkg.name)

    provided = pkg.setdefault("provided", {})
    for string in specs:
        for provided_spec in spack.spec.parse(string):
            if pkg.name == provided_spec.name:
                raise CircularReferenceError('depends_on', pkg.name)
            provided[provided_spec] = provider_spec


@directive
def patch(pkg, url_or_filename, **kwargs):
    """Packages can declare patches to apply to source.  You can
       optionally provide a when spec to indicate that a particular
       patch should only be applied when the package's spec meets
       certain conditions (e.g. a particular version).
    """
    level = kwargs.get('level', 1)
    when  = kwargs.get('when', pkg.name)

    patches = pkg.setdefault('patches', {})

    when_spec = parse_anonymous_spec(when, pkg.name)
    if when_spec not in patches:
        patches[when_spec] = [Patch(pkg.name, url_or_filename, level)]
    else:
        # if this spec is identical to some other, then append this
        # patch to the existing list.
        patches[when_spec].append(Patch(pkg.name, url_or_filename, level))


class RelationError(spack.error.SpackError):
    """This is raised when something is wrong with a package relation."""
    def __init__(self, relation, message):
        super(RelationError, self).__init__(message)
        self.relation = relation


class ScopeError(RelationError):
    """This is raised when a relation is called from outside a spack package."""
    def __init__(self, relation):
        super(ScopeError, self).__init__(
            relation,
            "Must invoke '%s' from inside a class definition!" % relation)


class CircularReferenceError(RelationError):
    """This is raised when something depends on itself."""
    def __init__(self, relation, package):
        super(CircularReferenceError, self).__init__(
            relation,
            "Package '%s' cannot pass itself to %s." % (package, relation))
        self.package = package
