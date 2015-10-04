from spack import *

class PyEmcee(Package):
    """Kick ass affine-invariant ensemble MCMC sampling"""
    homepage = "http://dan.iel.fm/emcee/"
    version("2.1.0", "c6b6fad05c824d40671d4a4fc58dfff7",
            url="https://pypi.python.org/packages/source/e/emcee/emcee-2.1.0.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
