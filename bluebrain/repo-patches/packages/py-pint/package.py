from spack import *
from spack.pkg.builtin.py_pint import PyPint as BuiltinPyPint


class PyPint(BuiltinPyPint):
    __doc__ = BuiltinPyPint.__doc__

    version('0.18', sha256='8c4bce884c269051feb7abc69dbfd18403c0c764abc83da132e8a7222f8ba801')

    depends_on('python@3.7:', type=('build', 'run'), when='@0.18:')
