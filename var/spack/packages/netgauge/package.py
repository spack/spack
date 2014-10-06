# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install netgauge
#
# You can always get back here to change things with:
#
#     spack edit netgauge
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Netgauge(Package):
    """Netgauge is a high-precision network parameter measurement
    tool. It supports benchmarking of many different network protocols
    and communication patterns. The main focus lies on accuracy,
    statistical analysis and easy extensibility.
    """
    homepage = "http://unixer.de/research/netgauge/"
    url      = "http://unixer.de/research/netgauge/netgauge-2.4.6.tar.gz"

    version('2.4.6', 'e0e040ec6452e93ca21ccc54deac1d7f')

    depends_on("mpi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
