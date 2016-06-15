from spack import *


class LibpthreadStubs(Package):
    """libpthread-stubs provides stub functions for pthreads as weak aliases for
    platforms on which libc does not provide these stubs. Linking to both libc
    and libpthread-stubs will always provide a full set of pthread stubs,
    allowing programs and libraries to portably use pthreads when linked to
    pthreads and improve single-threaded performance when not linked to
    pthreads."""

    homepage = "https://xcb.freedesktop.org"
    url      = "https://xcb.freedesktop.org/dist/libpthread-stubs-0.3.tar.gz"

    version('0.3', 'a09d928c4af54fe5436002345ef71138')
    version('0.2', 'e73ed50befe69ecb406c6bbddee928e7')
    version('0.1', '5e3e75160ab6a8c212d0ecd82aa04651')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
