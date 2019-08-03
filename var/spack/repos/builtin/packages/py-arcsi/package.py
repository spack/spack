# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-arcsi
#
# You can edit this file again by typing:
#
#     spack edit py-arcsi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyArcsi(PythonPackage):
    """The Atmospheric and Radiometric Correction of Satellite Imagery (ARCSI) 
       software provides a command line tool for the generation of Analysis Ready 
       Data (ARD) optical data including atmospheric correction, cloud masking, 
       topographic correction etc. of Earth Observation optical imagery (Blue-SWIR). 
       The aim of ARCSI is to provide as automatic as possible method of generating 
       Analysis Ready Data (ARD)."""

    homepage = "https://www.arcsi.remotesensing.info"
    url      = "https://bitbucket.org/petebunting/arcsi/downloads/arcsi-3.1.6.tar.gz"

    maintainers = ['petebunting']

    version('3.2.3a', '177aacacdae897b43c4a717c88e95ea7')

    # Add dependencies if required.
    #depends_on('py-setuptools', type='build')
    #depends_on('py-wheel', type='build')
    #depends_on('py-six', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('rsgislib', type=('build', 'run'))
    depends_on('py-py6s', type=('build', 'run'))
    depends_on('py-rios', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    
    #phases = ['install']
    
    """
    def install(self, spec, prefix):
        import subprocess
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
    """
