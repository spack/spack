from spack import *

class PyBlessings(Package):
    """A nicer, kinder way to write to the terminal """
    homepage = "https://github.com/erikrose/blessings"
    url      = "https://pypi.python.org/packages/source/b/blessings/blessings-1.6.tar.gz"

    version('1.6', '4f552a8ebcd4982693c92571beb99394')

    depends_on('py-setuptools')

    extends("python")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
