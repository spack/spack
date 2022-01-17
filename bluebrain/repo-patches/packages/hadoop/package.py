from spack import *
from spack.pkg.builtin.hadoop import Hadoop as BuiltinHadoop


class Hadoop(BuiltinHadoop):
    __doc__ = BuiltinHadoop.__doc__

    patch("hadoop-shell-quoting.patch")
