##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class Gdl(CMakePackage):
    """A free and open-source IDL/PV-WAVE compiler.

    GNU Data Language (GDL) is a free/libre/open source incremental compiler
    compatible with IDL and to some extent with PV-WAVE.
    """

    homepage = "https://github.com/gnudatalanguage/gdl"
    url      = "https://github.com/gnudatalanguage/gdl/archive/v0.9.8.tar.gz"

    version('0.9.8', '447b0362e1df5ea8af814a969e89d3ec')

    variant(
            'graphicsmagick',
            default=False,
            description='Enable GraphicsMagick'
           )
    variant('hdf4', default=False, description='Enable HDF4')
    variant('hdf5', default=True, description='Enable HDF5')
    variant('openmp', default=True, description='Enable OpenMP')
    variant('proj', default=True, description='Enable LIBPROJ4')
    variant('python', default=False, description='Enable Python')
    variant('wx', default=False, description='Enable WxWidgets')
    variant('x11', default=False, description='Enable X11')

    extends('python', when='+python')

    depends_on('graphicsmagick', when='+graphicsmagick')
    depends_on('hdf', when='+hdf4')
    depends_on('hdf5', when='+hdf5')
    depends_on('libx11', when='+x11')
    depends_on('plplot+wx', when='+wx@:5.11')
    depends_on('plplot+wx+wxold', when='+wx@5.12:')
    depends_on('plplot~wx', when='~wx')
    depends_on('proj', when='+proj')
    depends_on('py-numpy', type=('build', 'run'), when='+python')
    depends_on('python@2.7:2.8', type=('build', 'run'), when='+python')
    depends_on('wx', when='+wx')

    depends_on('eigen')
    depends_on('fftw')
    depends_on('gsl')
    depends_on('jpeg')
    depends_on('libice')
    depends_on('libsm')
    depends_on('libxinerama')
    depends_on('libxxf86vm')
    depends_on('netcdf')
    depends_on('pslib')
    depends_on('readline')

    def cmake_args(self):
        args = []

        # GraphicsMagick covers the same features as ImageMagick and
        # only version 6 of ImageMagick is supported (version 7 is packaged)
        args += ['-DMAGICK=OFF']

        if '+graphicsmagick' in self.spec:
            args += ['-DGRAPHICSMAGICK=ON']
        else:
            args += ['-DGRAPHICSMAGICK=OFF']

        if '+hdf4' in self.spec:
            args += ['-DHDF=ON']
        else:
            args += ['-DHDF=OFF']

        if '+hdf5' in self.spec:
            args += ['-DHDF5=ON']
        else:
            args += ['-DHDF5=OFF']

        if '+openmp' in self.spec:
            args += ['-DOPENMP=ON']
        else:
            args += ['-DOPENMP=OFF']

        if '+proj' in self.spec:
            args += [
                '-DLIBPROJ4=ON',
                '-DLIBPROJ4DIR={0}'.format(self.spec['proj'].prefix)
            ]
        else:
            args += ['-DLIBPROJ4=OFF']

        if '+python' in self.spec:
            args += ['-DPYTHON=ON']
        else:
            args += ['-DPYTHON=OFF']

        if '+wx' in self.spec:
            args += ['-DWXWIDGETS=ON']
        else:
            args += ['-DWXWIDGETS=OFF']

        if '+x11' in self.spec:
            args += ['-DX11=ON']
        else:
            args += ['-DX11=OFF']

        return args
