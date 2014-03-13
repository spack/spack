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
"""
This package contains relationships that can be defined among packages.
Relations are functions that can be called inside a package definition,
for example:

    class OpenMPI(Package):
        depends_on("hwloc")
        provides("mpi")
        ...

The available relations are:

depends_on
    Above, the OpenMPI package declares that it "depends on" hwloc.  This means
    that the hwloc package needs to be installed before OpenMPI can be
    installed.  When a user runs 'spack install openmpi', spack will fetch
    hwloc and install it first.

provides
    This is useful when more than one package can satisfy a dependence.  Above,
    OpenMPI declares that it "provides" mpi.  Other implementations of the MPI
    interface, like mvapich and mpich, also provide mpi, e.g.:

        class Mvapich(Package):
            provides("mpi")
            ...

        class Mpich(Package):
            provides("mpi")
            ...

    Instead of depending on openmpi, mvapich, or mpich, another package can
    declare that it depends on "mpi":

        class Mpileaks(Package):
            depends_on("mpi")
            ...

    Now the user can pick which MPI they would like to build with when they
    install mpileaks.  For example, the user could install 3 instances of
    mpileaks, one for each MPI version, by issuing these three commands:

        spack install mpileaks ^openmpi
        spack install mpileaks ^mvapich
        spack install mpileaks ^mpich
"""
import re
import inspect
import importlib

from llnl.util.lang import *

import spack
import spack.spec
import spack.error

from spack.patch import Patch
from spack.spec import Spec, parse_anonymous_spec
from spack.packages import packages_module


"""Adds a dependencies local variable in the locals of
   the calling class, based on args. """
def depends_on(*specs):
    pkg = get_calling_package_name()

    dependencies = caller_locals().setdefault('dependencies', {})
    for string in specs:
        for spec in spack.spec.parse(string):
            if pkg == spec.name:
                raise CircularReferenceError('depends_on', pkg)
            dependencies[spec.name] = spec


def provides(*specs, **kwargs):
    """Allows packages to provide a virtual dependency.  If a package provides
       'mpi', other packages can declare that they depend on "mpi", and spack
       can use the providing package to satisfy the dependency.
    """
    pkg = get_calling_package_name()
    spec_string = kwargs.get('when', pkg)
    provider_spec = parse_anonymous_spec(spec_string, pkg)

    provided = caller_locals().setdefault("provided", {})
    for string in specs:
        for provided_spec in spack.spec.parse(string):
            if pkg == provided_spec.name:
                raise CircularReferenceError('depends_on', pkg)
            provided[provided_spec] = provider_spec


def patch(url_or_filename, **kwargs):
    """Packages can declare patches to apply to source.  You can
       optionally provide a when spec to indicate that a particular
       patch should only be applied when the package's spec meets
       certain conditions (e.g. a particular version).
    """
    pkg = get_calling_package_name()
    level = kwargs.get('level', 1)
    when_spec = parse_anonymous_spec(kwargs.get('when', pkg), pkg)

    patches = caller_locals().setdefault('patches', {})
    if when_spec not in patches:
        patches[when_spec] = [Patch(pkg, url_or_filename, level)]
    else:
        # if this spec is identical to some other, then append this
        # patch to the existing list.
        patches[when_spec].append(Patch(pkg, url_or_filename, level))


def conflicts(*specs):
    """Packages can declare conflicts with other packages.
       This can be as specific as you like: use regular spec syntax.

       NOT YET IMPLEMENTED.
    """
    # TODO: implement conflicts
    pass


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
