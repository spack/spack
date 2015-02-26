from spack import *

class Ruby(Package):
    """A dynamic, open source programming language with a focus on 
    simplicity and productivity."""

    homepage = "https://www.ruby-lang.org/"
    url      = "http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz"

    version('2.2.0', 'cd03b28fd0b555970f5c4fd481700852')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
