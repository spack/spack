from spack import *

class PyProj(Package):
    """Python interface to the PROJ.4 Library."""
    homepage = "http://jswhit.github.io/pyproj/"
    url      = "https://github.com/jswhit/pyproj/tarball/v1.9.5.1rel"


    version('1.9.5.1', 'a4b80d7170fc82aee363d7f980279835')

    # We need the benefits of this PR
    # https://github.com/jswhit/pyproj/pull/54
    version('citibeth-latlong2',
        git='https://github.com/citibeth/pyproj.git',
        branch='latlong2')

    extends('python')

    depends_on('py-cython')
    depends_on('proj')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
