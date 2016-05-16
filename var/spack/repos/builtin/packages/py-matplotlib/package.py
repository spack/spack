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
import os

class PyMatplotlib(Package):
    """Python plotting package."""
    homepage = "https://pypi.python.org/pypi/matplotlib"
    url      = "https://pypi.python.org/packages/source/m/matplotlib/matplotlib-1.4.2.tar.gz"

    version('1.4.2', '7d22efb6cce475025733c50487bd8898')
    version('1.4.3', '86af2e3e3c61849ac7576a6f5ca44267')

    variant('gui', default=False, description='Enable GUI')
    variant('ipython', default=False, description='Enable ipython support')

    extends('python', ignore=r'bin/nosetests.*$|bin/pbr$')

    depends_on('py-pyside', when='+gui')
    depends_on('py-ipython', when='+ipython')
    depends_on('py-pyparsing')
    depends_on('py-six')
    depends_on('py-dateutil')
    depends_on('py-pytz')
    depends_on('py-nose')
    depends_on('py-numpy')
    depends_on('py-mock')
    depends_on('py-pbr')
    depends_on('py-funcsigs')

    depends_on('pkg-config')
    depends_on('freetype')
    depends_on('qt', when='+gui')
    depends_on('bzip2')
    depends_on('tcl', when='+gui')
    depends_on('tk', when='+gui')
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
