# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVoxcell(PythonPackage):
    """Python library for handling volumetric data"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/voxcell"
    git      = "ssh://bbpcode.epfl.ch/nse/voxcell"

    version('develop', branch='master')
    version('2.6.0', tag='voxcell-v2.6.0', preferred=True)
    version('2.5.6', tag='voxcell-v2.5.6')

    depends_on('py-setuptools', type='build')

    depends_on('py-future@0.16:', type='run')
    depends_on('py-h5py~mpi@2.3:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-pynrrd@0.2:0.2.99', type='run')
    depends_on('py-requests@2.18:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-six@1.0:', type='run')

    depends_on('py-libsonata@0.0.2:', type='run')
