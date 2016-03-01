# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install proj
#
# You can always get back here to change things with:
#
#     spack edit proj
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Proj(Package):
    """Cartographic Projections"""
    homepage = "https://github.com/OSGeo/proj.4/wiki"
    url      = "http://download.osgeo.org/proj/proj-4.9.2.tar.gz"

    version('4.9.2', '9843131676e31bbd903d60ae7dc76cf9')
    version('4.9.1', '3cbb2a964fd19a496f5f4265a717d31c')
    version('4.8.0', 'd815838c92a29179298c126effbb1537')
    version('4.7.0', '927d34623b52e0209ba2bfcca18fe8cd')
    version('4.6.1', '7dbaab8431ad50c25669fd3fb28dc493')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
