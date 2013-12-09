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

import spack
import spack.spec
from spack.spec import Spec
import spack.error
from spack.packages import packages_module


def _caller_locals():
    """This will return the locals of the *parent* of the caller.
       This allows a fucntion to insert variables into its caller's
       scope.  Yes, this is some black magic, and yes it's useful
       for implementing things like depends_on and provides.
    """
    stack = inspect.stack()
    try:
        return stack[2][0].f_locals
    finally:
        del stack


def _ensure_caller_is_spack_package():
    """Make sure that the caller is a spack package.  If it's not,
       raise ScopeError.  if it is, return its name."""
    stack = inspect.stack()
    try:
        # get calling function name (the relation)
        relation = stack[1][3]

        # Make sure locals contain __module__
        caller_locals = stack[2][0].f_locals
    finally:
        del stack

    if not '__module__' in caller_locals:
        raise ScopeError(relation)

    module_name = caller_locals['__module__']
    if not module_name.startswith(packages_module()):
        raise ScopeError(relation)

    base_name = module_name.split('.')[-1]
    return base_name


def _parse_local_spec(spec_like, pkg_name):
    """Allow the user to omit the package name part of a spec in relations.
       e.g., provides('mpi@2', when='@1.9:') says that this package provides
       MPI-3 when its version is higher than 1.9.
    """
    if type(spec_like) not in (str, Spec):
        raise TypeError('spec must be Spec or spec string.  Found %s'
                        % type(spec_like))

    if type(spec_like) == str:
        try:
            local_spec = Spec(spec_like)
        except spack.parse.ParseError:
            local_spec = Spec(pkg_name + spec_like)
            if local_spec.name != pkg_name: raise ValueError(
                    "Invalid spec for package %s: %s" % (pkg_name, spec_like))
    else:
        local_spec = spec_like

    if local_spec.name != pkg_name:
        raise ValueError("Spec name '%s' must match package name '%s'"
                         % (spec_like.name, pkg_name))

    return local_spec


"""Adds a dependencies local variable in the locals of
   the calling class, based on args. """
def depends_on(*specs):
    pkg = _ensure_caller_is_spack_package()

    dependencies = _caller_locals().setdefault('dependencies', {})
    for string in specs:
        for spec in spack.spec.parse(string):
            if pkg == spec.name:
                raise CircularDependencyError('depends_on', pkg)
            dependencies[spec.name] = spec


def provides(*specs, **kwargs):
    """Allows packages to provide a virtual dependency.  If a package provides
       'mpi', other packages can declare that they depend on "mpi", and spack
       can use the providing package to satisfy the dependency.
    """
    pkg = _ensure_caller_is_spack_package()
    spec_string = kwargs.get('when', pkg)
    provider_spec = _parse_local_spec(spec_string, pkg)

    provided = _caller_locals().setdefault("provided", {})
    for string in specs:
        for provided_spec in spack.spec.parse(string):
            provided[provided_spec] = provider_spec


"""Packages can declare conflicts with other packages.
   This can be as specific as you like: use regular spec syntax.
"""
def conflicts(*specs):
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
            "Cannot inovke '%s' from outside of a Spack package!" % relation)


class CircularDependencyError(RelationError):
    """This is raised when something depends on itself."""
    def __init__(self, relation, package):
        super(CircularDependencyError, self).__init__(
            relation, "Package %s cannot depend on itself." % package)
