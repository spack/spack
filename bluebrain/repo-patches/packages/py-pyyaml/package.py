from spack.pkg.builtin.py_pyyaml import PyPyyaml as BuiltinPyPyyaml


class PyPyyaml(BuiltinPyPyyaml):
    __doc__ = BuiltinPyPyyaml.__doc__

    def setup_build_environment(self, env):
        # Otherwise we get errors related to python being %gcc:
        # nvc-Error-Unknown switch: -Wno-unused-result
        # nvc-Error-Unknown switch: -fwrapv
        if self.spec.satisfies('%nvhpc'):
            for var in ['CPPFLAGS', 'CFLAGS', 'CXXFLAGS']:
                env.append_flags(var, '-noswitcherror')
