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
    version('1.4.2', '7d22efb6cce475025733c50487bd8898')
    version('1.4.3', '86af2e3e3c61849ac7576a6f5ca44267')

    variant('gui', default=False, description='Enable GUI')

    # Required dependencies
    extends('python@2.7:2.8,3.4:3.5', ignore=r'bin/nosetests.*$|bin/pbr$')
    #extends('python', ignore=r'bin/nosetests.*$|bin/pbr$')
    depends_on('py-numpy@1.6:')
    depends_on('py-setuptools')
    depends_on('py-dateutil@1.1:')
    depends_on('py-pyparsing')
    depends_on('libpng@1.2:')
    depends_on('py-pytz')
    depends_on('freetype@2.3:')
    depends_on('py-cycler@0.9:')
    # depends_on('py-tornado')

    # Optional GUI framework
    depends_on('tk@8.3:',       when='+gui')
    depends_on('py-pyqt@4.0:',  when='+gui')
    depends_on('pygtk@2.4:',    when='+gui')
    depends_on('wxPython@2.8:', when='+gui')

    # Optional external programs
    depends_on('ImageMagick')

    # Optional dependencies
    depends_on('py-pillow')
    depends_on('pkg-config')

    # Required libraries that ship with matplotlib
    # depends_on('agg@2.4:')
    depends_on('qhull@2012.1')
    # depends_on('ttconv')
    depends_on('py-six@1.9.0:')

    def install(self, spec, prefix):
        site_packages = '{0}/lib/python{1}/site-packages'.format(
            prefix, spec['python'].version.up_to(2))

        # site-packages directory must already exist
        mkdirp(site_packages)

        # PYTHONPATH must include site-packages directory
        env['PYTHONPATH'] += ':{0}'.format(site_packages)

        python('setup.py', 'install', '--prefix=%s' % prefix)
