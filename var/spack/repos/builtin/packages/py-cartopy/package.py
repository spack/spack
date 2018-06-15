##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class PyCartopy(PythonPackage):
    """Cartopy - a cartographic python library with matplotlib support."""

    homepage = "http://scitools.org.uk/cartopy/"
    url      = "https://github.com/SciTools/cartopy/archive/v0.16.0.tar.gz"

    version('0.16.0', 'f9e2e528d7758da7c64f824548a53f32')

    depends_on('py-setuptools@0.7.2:', type='build')
    depends_on('py-cython@0.15.1:',    type='build')
    depends_on('py-numpy@1.10.0:',  type=('build', 'run'))
    depends_on('py-shapely@1.5.6:', type=('build', 'run'))
    depends_on('py-pyshp@1.1.4:',   type=('build', 'run'))
    depends_on('py-six@1.3.0:',     type=('build', 'run'))
    depends_on('geos@3.3.3:')
    depends_on('proj@4.9.0:')

    # optional dependecies
    depends_on('py-matplotlib@1.5.1:', type=('build', 'run'))
    depends_on('gdal@1.10.0:+python',  type=('build', 'run'))
    depends_on('py-pillow@1.7.8:',     type=('build', 'run'))
    depends_on('py-pyepsg@0.2.0:',     type=('build', 'run'))
    depends_on('py-scipy@0.10:',       type=('build', 'run'))
    depends_on('py-owslib@0.8.11:',    type=('build', 'run'))

    # testing dependencies
    depends_on('py-mock@1.0.1',    type='test')
    depends_on('py-pytest@3.0.0:', type='test')

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):
        args = ['-I{0}'.format(spec['proj'].prefix.include),
                '-L{0}'.format(spec['proj'].prefix.lib)
                ]
        return args
