from spack import *
import os

class Tcsh(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "ftp://ftp.astron.com/pub/tcsh/tcsh-6.18.01.tar.gz"

    version('6.18.01', '6eed09dbd4223ab5b6955378450d228a')

    def setup_dependent_environment(self, module, spec, dep_spec):
        os.environ['PATH'] = self.prefix.bin + ':' + os.environ['PATH']

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
        symlink('%s/tcsh' % prefix.bin , '%s/csh' % prefix.bin)
