from spack import *
from spack.pkg.builtin.hadoop import Hadoop as BuiltinHadoop


class Hadoop(BuiltinHadoop):
    __doc__ = BuiltinHadoop.__doc__

    version('3.3.1', sha256='ad770ae3293c8141cc074df4b623e40d79782d952507f511ef0a6b0fa3097bac')

    patch("hadoop-shell-quoting.patch", when='@2')
