# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-python-fmask
#
# You can edit this file again by typing:
#
#     spack edit py-python-fmask
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class PyPythonFmask(PythonPackage):
    """A set of command line utilities and Python modules that implement 
       the FMASK algorithm for Landsat and Sentinel-2"""

    homepage = "http://pythonfmask.org"
    url      = "https://bitbucket.org/chchrsc/python-fmask/downloads/python-fmask-0.5.3.tar.gz"

    version('0.5.3', '6923320282860ea7e2cdeed2192e2923')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-rios', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    
    phases = ['install']
    
    """
    def install(self, spec, prefix):
        import subprocess
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
    """


