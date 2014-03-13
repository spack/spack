# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install v
#
# You can always get back here to change things with:
#
#     spack edit v
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Graphlib(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/lee218llnl/graphlib/archive/v2.0.0.tar.gz"

    versions = { '2.0.0' : '43c6df84f1d38ba5a5dce0ae19371a70', }

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        cmake(".", *std_cmake_args)

        # FIXME: Add logic to build and install here
        make()
        make("install")
