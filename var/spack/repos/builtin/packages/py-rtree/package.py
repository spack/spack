from spack import *
import os

class PyRtree(Package):
    """Python interface to the RTREE.4 Library."""
    homepage = "http://toblerity.org/rtree/"
    url      = "https://github.com/Toblerity/rtree/tarball/0.8.2"


    # Not an official release yet.  But changes in here are required to work with Spack
    # (Spack installs libspatialindex installed in a non-standard location).
    version('0.8.2.1', '394696ca849dd9f3a5ef24fb02a41ef4',
        url='https://github.com/citibeth/rtree/tarball/3a87d86f66a3955676b2507d3bf424ade938a22b')

    # Does not work with Spack
    # version('0.8.2', '593c7ac6babc397b8ba58f1636c1e0a0')

    # For testing/development purposes
    # version('bakedenv', branch='160529-efischer/BakedInEnv', git='https://github.com/citibeth/rtree.git')

    extends('python')

    depends_on('libspatialindex')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        lib = os.path.join(spec['libspatialindex'].prefix, 'lib')
        os.environ['SPATIALINDEX_LIBRARY'] = os.path.join(lib, 'libspatialindex.%s' % dso_suffix)
        os.environ['SPATIALINDEX_C_LIBRARY'] = os.path.join(lib, 'libspatialindex_c.%s' % dso_suffix)

        python('setup.py', 'install', '--prefix=%s' % prefix)
