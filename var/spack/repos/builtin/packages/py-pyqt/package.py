from spack import *

class PyPyqt(Package):
    """PyQt is a set of Python v2 and v3 bindings for Digia's Qt
       application framework and runs on all platforms supported by Qt
       including Windows, MacOS/X and Linux."""
    homepage = "http://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz"

    version('4.11.3', '997c3e443165a89a559e0d96b061bf70')

    extends('python')
    depends_on('py-sip')

    # TODO: allow qt5 when conditional deps are supported.
    # TODO: Fix version matching so that @4 works like @:4
    depends_on('qt@:4')

    def install(self, spec, prefix):
        python('configure.py',
               '--confirm-license',
               '--destdir=%s' % site_packages_dir)
        make()
        make('install')
