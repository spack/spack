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

    # No dependencies

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
