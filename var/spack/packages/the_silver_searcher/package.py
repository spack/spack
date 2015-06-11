from spack import *

class TheSilverSearcher(Package):
    """Fast recursive grep alternative"""
    homepage = "http://geoff.greer.fm/ag/"
    url      = "http://geoff.greer.fm/ag/releases/the_silver_searcher-0.30.0.tar.gz"

    version('0.30.0', '95e2e7859fab1156c835aff7413481db')

    depends_on('pcre')
    depends_on('xz')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
