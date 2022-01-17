from spack import *
from spack.pkg.builtin.python import Python as BuiltinPython


class Python(BuiltinPython):
    __doc__ = BuiltinPython.__doc__

    def setup_dependent_build_environment(self, env, dependent_spec):
        super().setup_dependent_build_environment(env, dependent_spec)
        if self.spec.satisfies('%intel'):
            env.set('LDSHARED', '%s -shared' % spack_cc)
            env.set('LDCXXSHARED', '%s -shared' % spack_cxx)
