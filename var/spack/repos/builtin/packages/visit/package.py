# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install visit
#
# You can always get back here to change things with:
#
#     spack edit visit
#
# See the spack documentation for more information on building
# packages.
#
from spack import *


class Visit(Package):
    """VisIt is an Open Source, interactive, scalable, visualization, animation and analysis tool."""
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    url = "http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz"

    version('2.10.1', '3cbca162fdb0249f17c4456605c4211e')

    depends_on("vtk@7.0")
    depends_on("qt@4.8.6")
    # FIXME: Add dependencies if this package requires them.

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        # FIXME: Spack couldn't guess one, so here are some options:
        # configure('--prefix=%s' % prefix)
        std_cmake_args = []
        cmake('.', *std_cmake_args)

        # FIXME: Add logic to build and install here
        make()
        make("install")
