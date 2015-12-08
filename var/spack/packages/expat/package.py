from spack import *

class Expat(Package):
    """<eXpat/> is an XML parser library written in C"""
    homepage = "http://expat.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/expat/expat/2.1.0/expat-2.1.0.tar.gz"

    version('2.1.0', 'dd7dab7a5fea97d2a6a43f511449b7cd')


    def install(self, spec, prefix):

        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make('install')

