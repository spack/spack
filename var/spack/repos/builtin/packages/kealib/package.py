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

class Kealib(Package):
    """An HDF5 Based Raster File Format
    
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
    homepage = "http://kealib.org/"
    url      = "https://bitbucket.org/chchrsc/kealib/get/kealib-1.4.5.tar.gz"

    version('1.4.5', '112e9c42d980b2d2987a3c15d0833a5d')

    depends_on("hdf5")

    def install(self, spec, prefix):
        with working_dir('trunk', create=False):
            cmake_args = []
            cmake_args.append("-DCMAKE_INSTALL_PREFIX=%s" % prefix)
            cmake_args.append("-DHDF5_INCLUDE_DIR=%s" % spec['hdf5'].prefix.include)
            cmake_args.append("-DHDF5_LIB_PATH=%s" % spec['hdf5'].prefix.lib)
            cmake('.', *cmake_args)

            make()
            make("install")
