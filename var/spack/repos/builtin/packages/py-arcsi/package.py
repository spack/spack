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
#     spack install py-arcsi
#
# You can edit this file again by typing:
#
#     spack edit py-arcsi
#
# See the Spack documentation for more information on packaging.
#

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
    version('3.1.6', '85b2ece361750f27ca1416ec8b0463c5')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-six', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('rsgislib', type=('build', 'run'))
    depends_on('py-py6s', type=('build', 'run'))
    depends_on('py-rios', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    
    def install(self, spec, prefix):
        import subprocess
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)

