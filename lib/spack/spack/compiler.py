import os
import re
import itertools

from llnl.util.lang import memoized
from llnl.util.filesystem import join_path

import spack.error
import spack.spec
from spack.version import Version
from spack.util.executable import Executable, which
from spack.compilation import get_path

_default_order = ['']

def _verify_executables(*paths):
    for path in paths:
        if not os.path.isfile(path) and os.access(path, os.X_OK):
            raise CompilerAccessError(path)

@memoized
def get_compiler_version(compiler, version_arg):
    return compiler(version_arg, return_output=True)


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

    # Optional prefix regexes for searching for this type of compiler.
    # Prefixes are sometimes used for toolchains, e.g. 'powerpc-bgq-linux-'
    prefixes = []

    # Optional suffix regexes for searching for this type of compiler.
    # Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    # version suffix for gcc.
    suffixes = []

    # Names of generic arguments used by this compiler
    arg_version = '-dumpversion'
    arg_rpath   = '-Wl,-rpath,%s'


    def __init__(self, cc, cxx, f77, fc):
        def make_exe(exe):
            if exe is None:
                return None
            _verify_executables(exe)
            return Executable(exe)

        self.cc  = make_exe(cc)
        self.cxx = make_exe(cxx)
        self.f77 = make_exe(f77)
        self.fc  = make_exe(fc)


    def _tuple(self):
        return (self.cc, self.cxx, self.f77, self.fc)


    @property
    def version(self):
        for comp in self._tuple():
            if comp is not None:
                v = get_compiler_version(comp, self.arg_version)
                return Version(v)
        raise InvalidCompilerError()


    @property
    def spec(self):
        return spack.spec.CompilerSpec(self.name, self.version)


    @classmethod
    def _find_matches_in_path(cls, compiler_names, *path):
        """Try to find compilers with the supplied names in any of the suppled
           paths.  Searches for all combinations of each name with the
           compiler's specified prefixes and suffixes.  Compilers are
           returned in a dict from (prefix, suffix) tuples to paths to
           the compilers with those prefixes and suffixes.
        """
        if not path:
            path = get_path('PATH')

        matches = {}
        ps_pairs = [p for p in itertools.product(
            [''] + cls.prefixes, [''] + cls.suffixes)]

        for directory in path:
            files = os.listdir(directory)

            for pre_re, suf_re in ps_pairs:
                for compiler_name in compiler_names:
                    regex = r'^(%s)%s(%s)$' % (
                        pre_re, re.escape(compiler_name), suf_re)

                    for exe in files:
                        match = re.match(regex, exe)
                        if match:
                            pair = match.groups()
                            if pair not in matches:
                                matches[pair] = join_path(directory, exe)

        return matches

    @classmethod
    def find(cls, *path):
        """Try to find this type of compiler in the user's environment. For
           each set of compilers found, this returns a 4-tuple with
           the cc, cxx, f77, and fc paths.

           This will search for compilers with the names in cc_names,
           cxx_names, etc. and it will group 4-tuples if they have
           common prefixes and suffixes.  e.g., gcc-mp-4.7 would be
           grouped with g++-mp-4.7 and gfortran-mp-4.7.

           Example return values::

               [ ('/usr/bin/gcc',      '/usr/bin/g++',
                  '/usr/bin/gfortran', '/usr/bin/gfortran'),

                 ('/usr/bin/gcc-mp-4.5',      '/usr/bin/g++-mp-4.5',
                  '/usr/bin/gfortran-mp-4.5', '/usr/bin/gfortran-mp-4.5') ]

        """
        pair_names = [cls._find_matches_in_path(names, *path) for names in (
            cls.cc_names, cls.cxx_names, cls.f77_names, cls.fc_names)]

        keys = set()
        for p in pair_names:
            keys.update(p)

        return [ tuple(pn[k] if k in pn else None for pn in pair_names)
                 for k in keys ]


    def __repr__(self):
        """Return a string represntation of the compiler toolchain."""
        return self.__str__()


    def __str__(self):
        """Return a string represntation of the compiler toolchain."""
        def p(path):
            return ' '.join(path.exe) if path else None
        return "%s(%s, %s, %s, %s)" % (
            self.name,
            p(self.cc), p(self.cxx), p(self.f77), p(self.fc))


class CompilerAccessError(spack.error.SpackError):
    def __init__(self, path):
        super(CompilerAccessError, self).__init__(
            "'%s' is not a valid compiler." % path)


class InvalidCompilerError(spack.error.SpackError):
    def __init__(self):
        super(InvalidCompilerError, self).__init__(
            "Compiler has no executables.")
