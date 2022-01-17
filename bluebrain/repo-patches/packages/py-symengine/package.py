from spack import *
from spack.pkg.builtin.py_symengine import PySymengine as BuiltinPySymengine


class PySymengine(BuiltinPySymengine):
    __doc__ = BuiltinPySymengine.__doc__

    version('0.3.0', sha256='0ecccfe5a09b25b6640afca12de62062bdb60ed2712d6c16cc47fc1ba1e851ac')

    depends_on('symengine@0.3.0:')

    def build_args(self, spec, prefix):
        return ['build_ext', '--symengine-dir={0}'.format(spec['symengine'].prefix)]
