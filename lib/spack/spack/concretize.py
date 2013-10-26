"""
Functions here are used to take abstract specs and make them concrete.
For example, if a spec asks for a version between 1.8 and 1.9, these
functions might take will take the most recent 1.9 version of the
package available.  Or, if the user didn't specify a compiler for a
spec, then this will assign a compiler to the spec based on defaults
or user preferences.

TODO: make this customizable and allow users to configure
      concretization  policies.
"""
import spack.arch
import spack.compilers
from spack.version import *
from spack.spec import *


def concretize_version(spec):
    """If the spec is already concrete, return.  Otherwise take
       the most recent available version, and default to the package's
       version if there are no avaialble versions.
    """
    # return if already concrete.
    if spec.versions.concrete:
        return

    pkg = spec.package

    # If there are known avaialble versions, return the most recent
    available_versions = pkg.available_versions
    if available_versions:
        spec.versions = ver([available_versions[-1]])
    else:
        spec.versions = ver([pkg.version])


def concretize_architecture(spec):
    """If the spec already had an architecture, return.  Otherwise if
       the root of the DAG has an architecture, then use that.
       Otherwise take the system's default architecture.

       Intuition: Architectures won't be set a lot, and generally you
       want the host system's architecture.  When architectures are
       mised in a spec, it is likely because the tool requries a
       cross-compiled component, e.g. for tools that run on BlueGene
       or Cray machines.  These constraints will likely come directly
       from packages, so require the user to be explicit if they want
       to mess with the architecture, and revert to the default when
       they're not explicit.
    """
    if spec.architecture is not None:
        return

    if spec.root.architecture:
        spec.architecture = spec.root.architecture
    else:
        spec.architecture = spack.arch.sys_type()


def concretize_compiler(spec):
    """Currently just sets the compiler to gcc or throws an exception
       if the compiler is set to something else.

       TODO: implement below description.

       If the spec already has a compiler, we're done.  If not, then
       take the compiler used for the nearest ancestor with a concrete
       compiler, or use the system default if there is no ancestor
       with a compiler.

       Intuition: Use the system default if no package that depends on
       this one has a strict compiler requirement.  Otherwise, try to
       build with the compiler that will be used by libraries that
       link to this one, to maximize compatibility.
    """
    if spec.compiler and spec.compiler.concrete:
        if spec.compiler != spack.compilers.default_compiler():
            raise spack.spec.UnknownCompilerError(str(spec.compiler))
    else:
        spec.compiler = spack.compilers.default_compiler()
