import os
from llnl.util.lang import memoized

import spack.error
from spack.version import Version
from spack.util.executable import Executable




def _verify_executables(*paths):
    for path in paths:
        if not os.path.isfile(path) and os.access(path, os.X_OK):
            raise InvalidCompilerPathError(path)


class Compiler(object):
    """This class encapsulates a Spack "compiler", which includes C,
       C++, and Fortran compilers.  Subclasses should implement
       support for specific compilers, their possible names, arguments,
       and how to identify the particular type of compiler."""

    # Subclasses use possible names of C compiler
    cc_names = []

    # Subclasses use possible names of C++ compiler
    cxx_names = []

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = []

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = []

    # Names of generic arguments used by this compiler
    arg_version = '-dumpversion'
    arg_rpath   = '-Wl,-rpath,%s'


    def __init__(self, cc, cxx, f77, fc):
        _verify_executables(cc, cxx, f77, fc)

        self.cc  = Executable(cc)
        self.cxx = Executable(cxx)
        self.f77 = Executable(f77)
        self.fc  = Executable(fc)

    @property
    @memoized
    def version(self):
        v = self.cc(arg_version)
        return Version(v)


class InvalidCompilerPathError(spack.error.SpackError):
    def __init__(self, path):
        super(InvalidCompilerPathError, self).__init__(
            "'%s' is not a valid compiler." % path)
