from spack import *

import os


class HashTest1(Package):
    """Used to test package hashing
    """

    homepage = "http://www.hashtest1.org"
    url = "http://www.hashtest1.org/downloads/hashtest1-1.1.tar.bz2"

    version('1.1', 'a' * 32)
    version('1.2', 'b' * 32)
    version('1.3', 'c' * 32)
    version('1.4', 'd' * 32)

    patch('patch1.patch', when="@1.1")
    patch('patch2.patch', when="@1.4")

    variant('variantx', default=False, description='Test variant X')
    variant('varianty', default=False, description='Test variant Y')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        pass

    @when('@:1.4')
    def install(self, spec, prefix):
        print("install 1")
        os.listdir(os.getcwd())

    @when('@1.5')
    def install(self, spec, prefix):
        os.listdir(os.getcwd())
