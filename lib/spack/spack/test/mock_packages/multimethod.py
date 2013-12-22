from spack import *


class Multimethod(Package):
    """This package is designed for use with Spack's multimethod test.
       It has a bunch of test cases for the @when decorator that the
       test uses.
    """

    homepage = 'http://www.example.com/'
    url      = 'http://www.example.com/example-1.0.tar.gz'

    #
    # These functions are only valid for versions 1, 2, and 3.
    #
    @when('@1.0')
    def no_version_2(self):
        return 1

    @when('@3.0')
    def no_version_2(self):
        return 3

    @when('@4.0')
    def no_version_2(self):
        return 4


    #
    # These functions overlap too much, so there is ambiguity
    #
    @when('@:4')
    def version_overlap(self):
        pass

    @when('@2:')
    def version_overlap(self):
        pass

