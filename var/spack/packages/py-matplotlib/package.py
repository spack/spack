from spack import *
import os

class PyMatplotlib(Package):
    """Python plotting package."""
    homepage = "https://pypi.python.org/pypi/matplotlib"
    url      = "https://pypi.python.org/packages/source/m/matplotlib/matplotlib-1.4.2.tar.gz"

    version('1.4.2', '7d22efb6cce475025733c50487bd8898')
    version('1.4.3', '86af2e3e3c61849ac7576a6f5ca44267')

    extends('python', ignore=r'bin/nosetests.*$')

    depends_on('py-pyside')
    depends_on('py-ipython')
    depends_on('py-pyparsing')
    depends_on('py-six')
    depends_on('py-dateutil')
    depends_on('py-pytz')
    depends_on('py-nose')
    depends_on('py-numpy')

    depends_on('qt')
    depends_on('bzip2')
    depends_on('tcl')
    depends_on('tk')
    depends_on('qhull')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

        if str(self.version) in ['1.4.2', '1.4.3']:
            # hack to fix configuration file
            config_file = None
            for p,d,f in os.walk(prefix.lib):
                for file in f:
                    if file.find('matplotlibrc') != -1:
                        config_file = join_path(p, 'matplotlibrc')
                        print config_file
            if config_file == None:
                raise InstallError('could not find config file')
            filter_file(r'backend      : pyside',
                        'backend      : Qt4Agg',
                        config_file)
            filter_file(r'#backend.qt4 : PyQt4',
                        'backend.qt4 : PySide',
                        config_file)
