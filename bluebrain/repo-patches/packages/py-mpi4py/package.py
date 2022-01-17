from spack.pkg.builtin.py_mpi4py import PyMpi4py as BuiltinPyMpi4py


class PyMpi4py(BuiltinPyMpi4py):
    __doc__ = BuiltinPyMpi4py.__doc__

    def setup_build_environment(self, env):
        # Python is not built with NVHPC, but the compiler flags that were used
        # to build Python are inherited by the build of py-mpi4py and passed to
        # NVHPC. This can lead to errors, but by injecting this extra flag we
        # can demote those errors to warnings.
        if self.spec.compiler.name == 'nvhpc':
            env.append_flags('SPACK_CFLAGS', '-noswitcherror')
            env.append_flags('SPACK_CXXFLAGS', '-noswitcherror')
