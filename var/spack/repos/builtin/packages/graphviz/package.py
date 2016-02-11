from spack import *

class Graphviz(Package):
    """Graph Visualization Software"""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    parallel = False

    depends_on("swig")
    depends_on("python")
    depends_on("ghostscript")

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix)

        make()
        make("install")

