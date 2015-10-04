from spack import *
import os

class PyBasemap(Package):
    """The matplotlib basemap toolkit is a library for plotting 2D data on maps in Python."""
    homepage = "http://matplotlib.org/basemap/"
    url      = "https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz"

    version('1.0.7', '48c0557ced9e2c6e440b28b3caff2de8')

    extends('python')
    depends_on('py-setuptools')
    depends_on('py-numpy')
    depends_on('py-matplotlib')
    depends_on('py-pil')
    depends_on("geos")

    def install(self, spec, prefix):
        env['GEOS_DIR'] = spec['geos'].prefix
        python('setup.py', 'install', '--prefix=%s' % prefix)
