from spack import *

class PyArgcomplete(Package):
    """Bash tab completion for argparse."""

    homepage = "https://pypi.python.org/pypi/argcomplete"
    url      = "https://pypi.python.org/packages/source/a/argcomplete/argcomplete-1.1.1.tar.gz"

    version('1.1.1', '89a3839096c9f991ad33828e72d21abf')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
