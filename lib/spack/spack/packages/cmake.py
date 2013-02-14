from spack import *

class Cmake(Package):
    homepage  = 'https://www.cmake.org'
    url       = 'http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz'
    md5       = '097278785da7182ec0aea8769d06860c'

    def install(self, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make('install')
