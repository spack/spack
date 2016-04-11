from spack import *

class PyTuiview(Package):
    """
       TuiView is a lightweight raster GIS with powerful raster attribute
       table manipulation abilities.
    """
    homepage = "https://bitbucket.org/chchrsc/tuiview"
    url      = "https://bitbucket.org/chchrsc/tuiview/get/tuiview-1.1.7.tar.gz"

    version('1.1.7', '4b3b38a820cc239c8ab4a181ac5d4c30')

    extends("python")
    depends_on("py-pyqt")
    depends_on("py-numpy")
    depends_on("gdal")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
