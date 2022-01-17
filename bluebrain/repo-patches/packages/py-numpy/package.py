from spack.directives import conflicts
from spack.pkg.builtin.py_numpy import PyNumpy as BuiltinPyNumpy


class PyNumpy(BuiltinPyNumpy):
    __doc__ = BuiltinPyNumpy.__doc__
    # With the CPPFLAGS/CFLAGS/CXXFLAGS fix below then there does not appear
    # to be any compiler error message with NVHPC, but at least with 21.11
    # then an llc process gets stuck and eventually killed when compiling
    # loops.c
    conflicts('%nvhpc')

    def setup_build_environment(self, env):
        # Otherwise we get errors related to python being %gcc:
        # nvc-Error-Unknown switch: -Wno-unused-result
        # nvc-Error-Unknown switch: -fwrapv
        if self.spec.satisfies('%nvhpc'):
            for var in ['CPPFLAGS', 'CFLAGS', 'CXXFLAGS']:
                env.append_flags(var, '-noswitcherror')
