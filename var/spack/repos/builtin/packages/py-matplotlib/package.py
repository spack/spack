##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *



class PyMatplotlib(Package):
    """matplotlib is a python 2D plotting library which produces publication
    quality figures in a variety of hardcopy formats and interactive
    environments across platforms."""

    homepage = "https://pypi.python.org/pypi/matplotlib"
    url      = "https://pypi.python.org/packages/source/m/matplotlib/matplotlib-1.4.2.tar.gz"

    version('1.5.1', 'f51847d8692cb63df64cd0bd0304fd20')
    version('1.4.3', '86af2e3e3c61849ac7576a6f5ca44267')
    version('1.4.2', '7d22efb6cce475025733c50487bd8898')

    variant('gui', default=False, description='Enable GUI')
    variant('ipython', default=False, description='Enable ipython support')

    # Python 2.7, 3.4, or 3.5
    extends('python', ignore=r'bin/nosetests.*$|bin/pbr$')

    # Required dependencies
    depends_on('py-numpy@1.6:',    type=nolink)
    depends_on('py-setuptools',    type='build')
    depends_on('py-dateutil@1.1:', type=nolink)
    depends_on('py-pyparsing',     type=nolink)
    depends_on('libpng@1.2:')
    depends_on('py-pytz',          type=nolink)
    depends_on('freetype@2.3:')
    depends_on('py-cycler@0.9:',   type=nolink)

    # Optional GUI framework
    depends_on('tk@8.3:',       when='+gui')  # not 8.6.0 or 8.6.1
    depends_on('qt',            when='+gui')
    depends_on('py-pyside',     when='+gui', type=nolink)
    # TODO: Add more GUI dependencies

    # Optional external programs
    # ffmpeg/avconv or mencoder
    depends_on('ImageMagick')

    # Optional dependencies
    depends_on('py-pillow',  type=nolink)
    depends_on('pkg-config', type='build')

    # Required libraries that ship with matplotlib
    # depends_on('agg@2.4:')
    depends_on('qhull@2012.1:')
    # depends_on('ttconv')
    depends_on('py-six@1.9.0:', type=nolink)

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
