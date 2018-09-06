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


class Kealib(CMakePackage):
    """An HDF5 Based Raster File Format.

    KEALib provides an implementation of the GDAL data model.
    The format supports raster attribute tables, image pyramids,
    meta-data and in-built statistics while also handling very
    large files and compression throughout.

    Based on the HDF5 standard, it also provides a base from which
    other formats can be derived and is a good choice for long
    term data archiving. An independent software library (libkea)
    provides complete access to the KEA image format and a GDAL
    driver allowing KEA images to be used from any GDAL supported software.

    Development work on this project has been funded by Landcare Research.
    """
    homepage = "http://www.kealib.org/"
    url      = "https://bitbucket.org/chchrsc/kealib/get/kealib-1.4.10.tar.gz"
    hg       = "https://bitbucket.org/chchrsc/kealib"

    version('develop', hg=hg)
    version('1.4.10', '5684aeb2085a67a4270c73e79d4ab768')
    version('1.4.9',  'a095d0b9d6de1d609ffaf242e00cc2b6')
    version('1.4.8',  '1af2514c908f9168ff6665cc012815ad')
    version('1.4.7',  '6139e31e50f552247ddf98f489948893')

    depends_on('cmake@2.8.10:', type='build')
    depends_on('hdf5+cxx+hl')

    patch('cmake.patch', when='@1.4.7')

    @property
    def root_cmakelists_dir(self):
        if self.version >= Version('1.4.9'):
            return '.'
        else:
            return 'trunk'

    def cmake_args(self):
        spec = self.spec

        if self.version >= Version('1.4.9'):
            return [
                '-DHDF5_ROOT={0}'.format(spec['hdf5'].prefix)
            ]
        else:
            return [
                '-DHDF5_INCLUDE_DIR={0}'.format(
                    spec['hdf5'].headers.directories[0]),
                '-DHDF5_LIB_PATH={0}'.format(
                    spec['hdf5'].libs.directories[0])
            ]
