# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-rios
#
# You can edit this file again by typing:
#
#     spack edit py-rios
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class PyRios(PythonPackage):
    """Raster I/O Simplification. A set of python modules which makes it easy to 
       write raster processing code in Python. Built on top of GDAL, it handles 
       the details of opening and closing files, checking alignment of projection 
       and raster grid, stepping through the raster in small blocks, etc., allowing 
       the programmer to concentrate on the processing involved."""

    homepage = "http://rioshome.org"
    url      = "https://bitbucket.org/chchrsc/rios/downloads/rios-1.4.8.tar.gz"

    version('1.4.8', '5a18c0618e1b5f0f646932924a682206')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-six', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    
    phases = ['install']
    
    """    
    def install(self, spec, prefix):
        import subprocess
        subprocess.call('export RIOS_NOCMDLINE=1', shell=True)
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True) 
    """
    

