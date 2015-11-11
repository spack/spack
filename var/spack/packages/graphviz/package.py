from spack import *

class Graphviz(Package):
    """graph visualization software."""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')
    version('2.36.0', '1f41664dba0c93109ac8b71216bf2b57')

    depends_on("cairo@1.1.10")
    depends_on("freetype@2.1.10")
    depends_on("fontconfig")
    depends_on("zlib@1.2.3")
    # depends_on("libpng@1.2.10")
    # depends_on("expat@2.0.0")
    # depends_on("gd@2.0.34")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
