from spack import *

class PyAstroid(Package):
    homepage = "https://www.astroid.org/"
    url      = "https://github.com/PyCQA/astroid/archive/astroid-1.4.5.tar.gz"

    version('1.4.5', '7adfc55809908297ef430efe4ea20ac3')
    version('1.4.4', '8ae6f63f6a2b260bb7f647dafccbc796')
    version('1.4.3', '4647159de7d4d0c4b1de23ecbfb8e246')
    version('1.4.2', '677f7965840f375af51b0e86403bee6a')
    version('1.4.1', 'ed70bfed5e4b25be4292e7fe72da2c02')

    extends('python')
    depends_on('py-logilab-common')
    depends_on('py-setuptools')
    depends_on('py-six')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

