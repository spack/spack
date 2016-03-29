from spack import *

class Cmocka(Package):
    """Unit-testing framework in pure C"""
    homepage = "https://cmocka.org/"
    url      = "https://cmocka.org/files/1.0/cmocka-1.0.1.tar.xz"

    version('1.0.1', 'ed861e501a21a92b2af63e466df2015e')
    parallel = False

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
	    which('cmake')('..', *std_cmake_args)

	    make()
	    make("install")
