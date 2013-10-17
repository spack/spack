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
import spack.spec


def depends_on(*specs):
    """Adds a dependencies local variable in the locals of
       the calling class, based on args.
    """
    # Get the enclosing package's scope and add deps to it.
    locals = sys._getframe(1).f_locals
    dependencies = locals.setdefault("dependencies", {})
    for string in specs:
        for spec in spack.spec.parse(string):
            dependencies[spec.name] = spec


def provides(*args):
    """Allows packages to provide a virtual dependency.  If a package provides
       "mpi", other packages can declare that they depend on "mpi", and spack
       can use the providing package to satisfy the dependency.
    """
    # Get the enclosing package's scope and add deps to it.
    locals = sys._getframe(1).f_locals
    provides = locals.setdefault("provides", [])
    for name in args:
        provides.append(name)
