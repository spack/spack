from spack import *

class PyProj(Package):
    """Python interface to the PROJ.4 Library."""
    homepage = "http://jswhit.github.io/pyproj/"
    url      = "https://github.com/jswhit/pyproj/tarball/v1.9.5.1rel"

    # This is not a tagged release of pyproj.
    # The changes in this "version" fix some bugs, especially with Python3 use.
    version('1.9.5.1.1', 'd035e4bc704d136db79b43ab371b27d2',
        url='https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f')

    version('1.9.5.1', 'a4b80d7170fc82aee363d7f980279835')

    extends('python')

    depends_on('py-cython')
    depends_on('py-setuptools')

    # NOTE: py-proj does NOT depends_on('proj').
    # The py-proj git repo actually includes the correct version of PROJ.4,
    # which is built internally as part of the py-proj build.
    # Adding depends_on('proj') will cause mysterious build errors.

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
