from spack import *
import os

class Fxt(Package):
    """This library provides efficient support for recording traces"""
    homepage = "http://savannah.nongnu.org/projects/fkt"
    url      = "http://download.savannah.gnu.org/releases/fkt/fxt-0.3.1.tar.gz"

    # Install from sources
    if os.environ.has_key("MORSE_FXT_TAR") and os.environ.has_key("MORSE_FXT_TAR_MD5"):
        version('local', '%s' % os.environ['MORSE_FXT_TAR_MD5'],
                url = "file://%s" % os.environ['MORSE_FXT_TAR'])
    else:
        version('0.3.1' , '85b5829ecfe2754ba7213830c7d8f119')
        version('0.3.0' , '1aeb6807bda817163d432087b27ef855')
        version('0.2.14', '2f6bc2ce77e24be4d16523ccb372990e')
        version('0.2.13', 'c688d01cc50945a0cd6364cc39e33b95')
        version('0.2.12', 'd5d910fd818088f01fcf955eed9bc42a')


    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make(parallel=False)
        # The mkdir commands in fxt's install can fail in parallel
        make("install", parallel=False)
