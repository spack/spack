# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install blitz
#
# You can always get back here to change things with:
#
#     spack edit blitz
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Blitz(Package):
    """N-dimensional arrays for C++"""
    homepage = "http://github.com/blitzpp/blitz"

# This version doesn't have the configure script generated yet.
    url      = "https://github.com/blitzpp/blitz/tarball/1.0.0"
#http://prdownloads.sourceforge.net/%(namelower)s

    version('1.0.0', '9f040b9827fe22228a892603671a77af')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        # FIXME: Spack couldn't guess one, so here are some options:
        configure('--prefix=%s' % prefix)
        # cmake('.', *std_cmake_args)

        # FIXME: Add logic to build and install here
        make()
        make("install")
