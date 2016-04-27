from spack import *

class PyJdcal(Package):
    """Julian dates from proleptic Gregorian and Julian calendars"""

    homepage = 'http://github.com/phn/jdcal'
    url      = "https://pypi.python.org/packages/source/j/jdcal/jdcal-1.2.tar.gz"

    version('1.2', 'ab8d5ba300fd1eb01514f363d19b1eb9')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
