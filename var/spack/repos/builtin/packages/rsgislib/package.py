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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install rsgislib
#
# You can edit this file again by typing:
#
#     spack edit rsgislib
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import subprocess
import os

class Rsgislib(Package):
    """The Remote Sensing and GIS software library (RSGISLib) is a 
       collection of Python modules for processing remote sensing and GIS datasets.
    """

    # Add a proper url for your package's homepage here.
    homepage = "http://www.rsgislib.org"
    url      = "https://bitbucket.org/petebunting/rsgislib/downloads/rsgislib-3.7.54a.tar.gz"
    
    maintainers = ['petebunting']

    version('3.7.54a', '28bccbe06bc2ec14c3d1e4d75708d70f')
    version('3.6.14', '13dde2a575f044b41c11f973eba1de16')
    version('3.5.8', '54849d968b8f4b113c3557fbcb845334')
    version('3.5.7', '9a9e7c9f092cf92f5f4d11a3ac1e0629')

    # Add dependencies if required.
    depends_on('cmake', type='build')
    depends_on('hdf5+cxx+hl')
    depends_on('kealib')
    depends_on('xerces-c')
    depends_on('muparser')
    depends_on('gsl')
    depends_on('geos')
    depends_on('gdal')
    depends_on('cgal')
    depends_on('python')
    depends_on('boost')
    depends_on('py-numpy')
    depends_on('py-scikit-learn')
    
    extends('python')
    
    def install(self, spec, prefix):
        cmdPython = ' -DPYTHON_EXE={0}'.format(spec['python'].command.path)
        # Boost
        cmdBoostLib = ' -DBOOST_LIB_PATH={0}/lib'.format(spec['boost'].prefix)
        cmdBoostInc = ' -DBOOST_INCLUDE_PATH={0}/include'.format(spec['boost'].prefix)
        # GDAL
        cmdGDALLib = ' -DGDAL_LIB_PATH={0}/lib'.format(spec['gdal'].prefix)
        cmdGDALInc = ' -DGDAL_INCLUDE_DIR={0}/include'.format(spec['gdal'].prefix)
        # HDF5
        cmdHDF5Lib = ' -DHDF5_LIB_PATH={0}/lib'.format(spec['hdf5'].prefix)
        cmdHDF5Inc = ' -DHDF5_INCLUDE_DIR={0}/include'.format(spec['hdf5'].prefix)
        # Xerces-c
        cmdXercescLib = ' -DXERCESC_LIB_PATH={0}/lib'.format(spec['xerces-c'].prefix)
        cmdXercescInc = ' -DXERCESC_INCLUDE_DIR={0}/include'.format(spec['xerces-c'].prefix)
        # GSL
        cmdGSLLib = ' -DGSL_LIB_PATH={0}/lib'.format(spec['gsl'].prefix)
        cmdGSLInc = ' -DGSL_INCLUDE_DIR={0}/include'.format(spec['gsl'].prefix)
        # GEOS
        cmdGEOSLib = ' -DGEOS_LIB_PATH={0}/lib'.format(spec['geos'].prefix)
        cmdGEOSInc = ' -DGEOS_INCLUDE_DIR={0}/include'.format(spec['geos'].prefix)
        # MuParser
        cmdMuParserLib = ' -DMUPARSER_LIB_PATH={0}/lib'.format(spec['muparser'].prefix)
        cmdMuParserInc = ' -DMUPARSER_INCLUDE_DIR={0}/include'.format(spec['muparser'].prefix)
        # CGAL
        cmdCGALLib = ' -DCGAL_LIB_PATH={0}/lib'.format(spec['cgal'].prefix)
        cmdCGALInc = ' -DCGAL_INCLUDE_DIR={0}/include'.format(spec['cgal'].prefix)
        # GMP
        cmdGMPLib = ' -DGMP_LIB_PATH={0}/lib'.format(spec['gmp'].prefix)
        cmdGMPInc = ' -DGMP_INCLUDE_DIR={0}/include'.format(spec['gmp'].prefix)
        # MPFR
        cmdMPFRLib = ' -DMPFR_LIB_PATH={0}/lib'.format(spec['mpfr'].prefix)
        cmdMPFRInc = ' -DMPFR_INCLUDE_DIR={0}/include'.format(spec['mpfr'].prefix)
        # KEA
        cmdKEALib = ' -DKEA_LIB_PATH={0}/lib'.format(spec['kealib'].prefix)
        cmdKEAInc = ' -DKEA_INCLUDE_DIR={0}/include'.format(spec['kealib'].prefix)
        
        cmd = 'cmake -DCMAKE_INSTALL_PREFIX='+str(prefix) + cmdPython + ' -DINSTALL_PYTHON_USING_PREFIX=OFF -DCMAKE_BUILD_TYPE=Release ' + cmdBoostLib + cmdBoostInc + cmdGDALLib + cmdGDALInc + cmdHDF5Lib + cmdHDF5Inc + cmdXercescLib + cmdXercescInc + cmdGSLLib + cmdGSLInc + cmdGEOSLib + cmdGEOSInc + cmdMuParserLib + cmdMuParserInc + cmdCGALLib + cmdCGALInc + cmdGMPLib + cmdGMPInc + cmdMPFRLib + cmdMPFRInc + cmdKEAInc + cmdKEAInc + ' .. '
        
        os.mkdir('build_dir')
        os.chdir('build_dir')
        subprocess.call(cmd, shell=True)
        
        make()
        make('install')        
        
