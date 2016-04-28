from spack import *

class Graphviz(Package):
    """Graph Visualization Software"""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    # By default disable optional Perl language support to prevent build issues
    # related to missing Perl packages. If spack begins support for Perl in the
    # future, this package can be updated to depend_on('perl') and the
    # ncecessary devel packages.
    variant('perl', default=False, description='Enable if you need the optional Perl language bindings.')

    parallel = False

    depends_on("swig")
    depends_on("python")
    depends_on("ghostscript")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        if not '+perl' in spec:
            options.append('--disable-perl')

        configure(*options)
        make()
        make("install")
