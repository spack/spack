from spack import *
import spack.package
import os

class PyPyside(Package):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/pyside"
    url      = "https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz"

    version('1.2.2', 'c45bc400c8a86d6b35f34c29e379e44d')

    extends('python')

    def install(self, spec, prefix):
        qmake_path = '/usr/lib64/qt4/bin/qmake'
        if not os.path.exists(qmake_path):
            raise spack.package.InstallError("Failed to find qmake in %s" % qmake_path)
        python('setup.py', 'install', '--prefix=%s' % prefix, '--qmake=%s' % qmake_path)
