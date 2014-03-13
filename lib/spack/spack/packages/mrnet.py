# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install mrnet
#
# You can always get back here to change things with:
#
#     spack edit mrnet
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Mrnet(Package):
    """The MRNet Multi-Cast Reduction Network."""
    homepage = "http://paradyn.org/mrnet"
    url      = "ftp://ftp.cs.wisc.edu/paradyn/mrnet/mrnet_4.0.0.tar.gz"

    versions = { '4.0.0' : 'd00301c078cba57ef68613be32ceea2f', }

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" %prefix, "--enable-shared")

        # FIXME: Add logic to build and install here
        make(parallel=False)
        make("install", parallel=False)
