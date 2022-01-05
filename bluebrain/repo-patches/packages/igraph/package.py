from spack import *
from spack.pkg.builtin.igraph import Igraph as BuiltinIgraph


class Igraph(BuiltinIgraph):
    version('0.8.2', sha256='718a471e7b8cbf02e3e8006153b7be6a22f85bb804283763a0016280e8a60e95')
