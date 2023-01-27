from spack.package import *
from spack.pkg.builtin.py_pyarrow import PyPyarrow as BuiltinPyPyarrow


class PyPyarrow(BuiltinPyPyarrow):
    __doc__ = BuiltinPyPyarrow.__doc__

    pypi = 'pyarrow/pyarrow-9.0.0.tar.gz'

    version('9.0.0', sha256='7fb02bebc13ab55573d1ae9bb5002a6d20ba767bf8569b52fce5301d42495ab7')
    version('8.0.0', sha256='4a18a211ed888f1ac0b0ebcb99e2d9a3e913a481120ee9b1fe33d3fedb945d4e')
    version('7.0.0', sha256='da656cad3c23a2ebb6a307ab01d35fce22f7850059cffafcb90d12590f8f4f38')
    version('6.0.1', sha256='423990d56cd8f12283b67367d48e142739b789085185018eb03d05087c3c8d43')

    variant('dataset', default=True, description="Build with Dataset support")

    for v in ('@6.0.1', '@7.0.0', '@8.0.0', '@9.0.0'):
        depends_on('arrow+python' + v, when=v)
        depends_on('arrow+parquet+python' + v, when='+parquet' + v)
        depends_on('arrow+cuda' + v, when='+cuda' + v)
        depends_on('arrow+orc' + v, when='+orc' + v)

    def setup_build_environment(self, env):
        args = self.install_options(self.spec, self.prefix)
        for arg in args:
            key = arg[2:]
            if "=" in key:
                key, val = key.split("=", 1)
            else:
                val = "1"
            var = "PYARROW_" + key.replace("-", "_").upper()
            env.set(var, val)

    def install_options(self, spec, prefix):
        args = BuiltinPyPyarrow.install_options(self, spec, prefix)
        if spec.satisfies('+dataset'):
            args.append('--with-dataset')
        return args
