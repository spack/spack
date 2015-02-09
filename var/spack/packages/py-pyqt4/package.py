from spack import *

class PyPyqt4(Package):
    """PyQt is a set of Python v2 and v3 bindings for Digia's Qt application framework and runs on all platforms supported by Qt including Windows, MacOS/X and Linux."""
    homepage = "http://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz"

    version('4.11.3', '997c3e443165a89a559e0d96b061bf70')

    extends('python')
    depends_on('qt')
    depends_on('py-sip')

    def install(self, spec, prefix):
        version_array = str(spec['python'].version).split('.')
        python('configure.py', '--confirm-license', '--destdir=%s/python%s.%s/site-packages' %(self.prefix.lib, version_array[0], version_array[1]))
        make()
        make('install')
