from spack import *

class PyScikitImage(Package):
    """Image processing algorithms for SciPy, including IO, morphology, filtering, warping, color manipulation, object detection, etc."""
    homepage = "http://scikit-image.org/"
    url      = "https://pypi.python.org/packages/source/s/scikit-image/scikit-image-0.12.3.tar.gz"

    version('0.12.3', '04ea833383e0b6ad5f65da21292c25e1')

    extends('python', ignore=r'bin/.*\.py$')

    depends_on('py-dask')
    depends_on('py-pillow')
    depends_on('py-networkx')
    depends_on('py-six')
    depends_on('py-scipy')
    depends_on('py-matplotlib')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
