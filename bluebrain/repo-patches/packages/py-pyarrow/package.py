from spack import *
from spack.pkg.builtin.py_pyarrow import PyPyarrow as BuiltinPyPyarrow


class PyPyarrow(BuiltinPyPyarrow):
    __doc__ = BuiltinPyPyarrow.__doc__

    version('6.0.1', sha256='423990d56cd8f12283b67367d48e142739b789085185018eb03d05087c3c8d43')

    for v in ('@6.0.1',):
        depends_on('arrow+python' + v, when=v)
        depends_on('arrow+parquet+python' + v, when='+parquet' + v)
        depends_on('arrow+cuda' + v, when='+cuda' + v)
        depends_on('arrow+orc' + v, when='+orc' + v)
