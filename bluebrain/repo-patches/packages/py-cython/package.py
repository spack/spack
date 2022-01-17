from spack.pkg.builtin.py_cython import PyCython as BuiltinPyCython


class PyCython(BuiltinPyCython):
    __doc__ = BuiltinPyCython.__doc__

    def setup_build_environment(self, env):
        # Otherwise we get errors related to python being %gcc:
        # nvc-Error-Unknown switch: -Wno-unused-result
        # nvc-Error-Unknown switch: -fwrapv
        if self.spec.satisfies('%nvhpc'):
            for var in ['CPPFLAGS', 'CFLAGS', 'CXXFLAGS']:
                env.append_flags(var, '-noswitcherror')
