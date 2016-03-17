from spack import *

class Graphviz(Package):
    """Graph Visualization Software"""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    variant('perl', default=True, description='Disable if you have problems with the optional script language bindings')
    variant('shared', default=True, description='Building static is required on AIX')

    parallel = False

    depends_on("swig")
    depends_on("python")
    depends_on("ghostscript")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        if '~perl' in spec:
            options.append('--disable-perl')
        if '~shared' in spec:
            options.append('--enable-shared=no')

        configure(*options)
        make()
        make("install")
