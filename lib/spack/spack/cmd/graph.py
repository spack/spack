import spack
import spack.packages as packages


def graph(parser, args):
    packages.graph_dependencies()
