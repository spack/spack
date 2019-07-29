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
#     spack install py-rios
#
# You can edit this file again by typing:
#
#     spack edit py-rios
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import subprocess

class PyRios(PythonPackage):
    """Raster I/O Simplification. A set of python modules which makes it easy to 
       write raster processing code in Python. Built on top of GDAL, it handles 
       the details of opening and closing files, checking alignment of projection 
       and raster grid, stepping through the raster in small blocks, etc., allowing 
       the programmer to concentrate on the processing involved."""

    # Add a proper url for your package's homepage here.
    homepage = "http://rioshome.org"
    url      = "https://bitbucket.org/chchrsc/rios/downloads/rios-1.4.8.tar.gz"

    version('1.4.8', '5a18c0618e1b5f0f646932924a682206')
    version('1.4.6', 'b7a0840c3eeac1d2bd2563f08d433247')
    version('1.4.5', '1e71c533524a9436ed1b5bd3ec91f4a9')
    version('1.4.4', '14dae098d1a0100c81bfc270b7d9d226')
    version('1.4.3', '156cce39c3e406517f9e829d3fe59210')
    version('1.4.2', 'a179f34d527c51dac99945bf24c7899d')
    version('1.4.1', '14aceafa555a504c7facec62e8805ed4')
    version('1.4.0', 'b9cef075390b79f195ec6f1340292081')
    version('1.3.1', 'e45d157f31b10cc77171b21f55a1198a')
    version('1.3.0', '8770ffb90bd050e991a95e0b9889a8aa')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-six', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
        
    def install(self, spec, prefix):
        subprocess.call('export RIOS_NOCMDLINE=1', shell=True)
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        
    
    

