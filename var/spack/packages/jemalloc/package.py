from spack import *

class Jemalloc(Package):
    """jemalloc is a general purpose malloc(3) implementation that emphasizes fragmentation avoidance and scalable concurrency support."""
    homepage = "http://www.canonware.com/jemalloc/"
    url      = "https://github.com/jemalloc/jemalloc/releases/download/4.0.4/jemalloc-4.0.4.tar.bz2"

    version('4.0.4', '687c5cc53b9a7ab711ccd680351ff988')

    variant('stats', default=False, description='Enable heap statistics')
    variant('prof', default=False, description='Enable heap profiling')

    def install(self, spec, prefix):
        configure_args = ['--prefix=%s' % prefix,]

        if '+stats' in spec:
            configure_args.append('--enable-stats')
        if '+prof' in spec:
            configure_args.append('--enable-prof')

        configure(*configure_args)

        make()
        make("install")
