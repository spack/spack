from spack import *
from spack.pkg.builtin.hadoop import Hadoop as BuiltinHadoop


class Hadoop(BuiltinHadoop):
    patch("hadoop-shell-quoting.patch")
