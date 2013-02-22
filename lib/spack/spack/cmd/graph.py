import spack
import spack.packages as packages

description = "Write out inter-package dependencies in dot graph format"

def graph(parser, args):
    packages.graph_dependencies()
