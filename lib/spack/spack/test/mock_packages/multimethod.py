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



    #
    # Use these to test whether the default method is called when no
    # match is found.  This also tests whether we can switch methods
    # on compilers
    #
    def has_a_default(self):
        return 'default'

    @when('%gcc')
    def has_a_default(self):
        return 'gcc'

    @when('%intel')
    def has_a_default(self):
        return 'intel'



    #
    # Make sure we can switch methods on different architectures
    #
    @when('=x86_64')
    def different_by_architecture(self):
        return 'x86_64'

    @when('=ppc64')
    def different_by_architecture(self):
        return 'ppc64'

    @when('=ppc32')
    def different_by_architecture(self):
        return 'ppc32'

    @when('=arm64')
    def different_by_architecture(self):
        return 'arm64'


    #
    # Make sure we can switch methods on different dependencies
    #
    @when('^mpich')
    def different_by_dep(self):
        return 'mpich'

    @when('^zmpi')
    def different_by_dep(self):
        return 'zmpi'


    #
    # Make sure we can switch on virtual dependencies
    #
    @when('^mpi@2:')
    def different_by_virtual_dep(self):
        return 'mpi@2:'

    @when('^mpi@:1')
    def different_by_virtual_dep(self):
        return 'mpi@:1'
