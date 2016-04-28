from spack import *
import os

class Geos(Package):
    """GEOS (Geometry Engine - Open Source) is a C++ port of the Java
       Topology Suite (JTS). As such, it aims to contain the complete
       functionality of JTS in C++. This includes all the OpenGIS
       Simple Features for SQL spatial predicate functions and spatial
       operators, as well as specific JTS enhanced topology functions."""

    homepage = "http://trac.osgeo.org/geos/"
    url      = "http://download.osgeo.org/geos/geos-3.4.2.tar.bz2"

    # Verison 3.5.0 supports Autotools and CMake
    version('3.5.0', '136842690be7f504fba46b3c539438dd')

    # Versions through 3.4.2 have CMake, but only Autotools is supported
    version('3.4.2', 'fc5df2d926eb7e67f988a43a92683bae')
    version('3.4.1', '4c930dec44c45c49cd71f3e0931ded7e')
    version('3.4.0', 'e41318fc76b5dc764a69d43ac6b18488')
    version('3.3.9', '4794c20f07721d5011c93efc6ccb8e4e')
    version('3.3.8', '75be476d0831a2d14958fed76ca266de')
    version('3.3.7', '95ab996d22672b067d92c7dee2170460')
    version('3.3.6', '6fadfb941541875f4976f75fb0bbc800')
    version('3.3.5', '2ba61afb7fe2c5ddf642d82d7b16e75b')
    version('3.3.4', '1bb9f14d57ef06ffa41cb1d67acb55a1')
    version('3.3.3', '8454e653d7ecca475153cc88fd1daa26')

#    # Python3 is not supported.
#    variant('python', default=False, description='Enable Python support')

#    extends('python', when='+python')
#    depends_on('python', when='+python')
#    depends_on('swig', when='+python')

    def install(self, spec, prefix):
        args = ["--prefix=%s" % prefix]
#        if '+python' in spec:
#            os.environ['PYTHON'] = join_path(spec['python'].prefix, 'bin',
#                'python' if spec['python'].version[:1][0] <= 2 else 'python3')
#            os.environ['SWIG'] = join_path(spec['swig'].prefix, 'bin', 'swig')
#
#            args.append("--enable-python")

        configure(*args)
        make()
        make("install")
