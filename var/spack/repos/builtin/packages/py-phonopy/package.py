from spack import *

class PyPhonopy(Package):
    """Phonopy is an open source package for phonon
    calculations at harmonic and quasi-harmonic levels."""
    homepage = "http://atztogo.github.io/phonopy/index.html"
    url      = "http://sourceforge.net/projects/phonopy/files/phonopy/phonopy-1.10/phonopy-1.10.0.tar.gz"

    version('1.10.0', '973ed1bcea46e21b9bf747aab9061ff6')

    extends('python')
    depends_on('py-numpy')
    depends_on('py-scipy')
    depends_on('py-matplotlib')
    depends_on('py-pyyaml')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--home=%s' % prefix)
