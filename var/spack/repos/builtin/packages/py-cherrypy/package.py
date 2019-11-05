from spack import *


class PyCherrypy(PythonPackage):
    """CherryPy is a pythonic, object-oriented HTTP framework."""

    homepage = "https://cherrypy.org/"
    url      = "https://pypi.io/packages/source/C/CherryPy/CherryPy-18.1.1.tar.gz"

    version('18.1.1', '76e5d3c6b7be845345f871c604cfdf58')

    depends_on('py-setuptools', type='build')
    depends_on('py-more-itertools',    type=('build', 'run'))
    depends_on('py-zc-buildout',       type=('build', 'run'))
    depends_on('py-zc-lockfile',       type=('build', 'run'))
    depends_on('py-cheroot@6.2.4:', type=('build', 'run'))
    depends_on('py-tempora',           type=('build', 'run'))
    depends_on('py-portend',           type=('build', 'run'))
