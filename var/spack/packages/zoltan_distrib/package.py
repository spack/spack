# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install zoltan_distrib
#
# You can always get back here to change things with:
#
#     spack edit zoltan_distrib
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class ZoltanDistrib(Package):
    """FIXME: put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://www.cs.sandia.gov/~kddevin/Zoltan_Distributions/zoltan_distrib_v3.81.tar.gz"

    version('3.81', 'e0587ac69dbc3b17d28f515ed0933719')

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
