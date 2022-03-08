from spack import *
from spack.pkg.builtin.py_pyspark import PyPyspark as BuiltinPyPyspark


class PyPyspark(BuiltinPyPyspark):
    __doc__ = BuiltinPyPyspark.__doc__

    version('3.2.1', sha256='0b81359262ec6e9ac78c353344e7de026027d140c6def949ff0d80ab70f89a54')
    version('3.1.3', sha256='39ac641ef5559a3d1286154779fc990316e9934520853615ae4785c1af52d14b')
    version('3.1.2', sha256='5e25ebb18756e9715f4d26848cc7e558035025da74b4fc325a0ebc05ff538e65')

    depends_on('py-py4j@0.10.9', when='@3.1.2', type=('build', 'run'))
    depends_on('py-py4j@0.10.9', when='@3.1.3', type=('build', 'run'))
    depends_on('py-py4j@0.10.9.3', when='@3.2.1', type=('build', 'run'))

    def setup_run_environment(self, env):
        env.set('PYSPARK_PYTHON', self.spec['python'].command.path)
        env.set('PYSPARK_DRIVER_PYTHON', self.spec['python'].command.path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('PYSPARK_PYTHON', self.spec['python'].command.path)
        env.set('PYSPARK_DRIVER_PYTHON', self.spec['python'].command.path)
