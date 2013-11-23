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
import sys
import inspect
import spack.spec


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


def _make_relation(map_name):
    def relation_fun(*specs):
        package_map = _caller_locals().setdefault(map_name, {})
        for string in specs:
            for spec in spack.spec.parse(string):
                package_map[spec.name] = spec
    return relation_fun


"""Adds a dependencies local variable in the locals of
   the calling class, based on args. """
depends_on = _make_relation("dependencies")


"""Allows packages to provide a virtual dependency.  If a package provides
   'mpi', other packages can declare that they depend on "mpi", and spack
   can use the providing package to satisfy the dependency.
"""
provides   = _make_relation("provided")


"""Packages can declare conflicts with other packages.
   This can be as specific as you like: use regular spec syntax.
"""
conflicts  = _make_relation("conflicted")
