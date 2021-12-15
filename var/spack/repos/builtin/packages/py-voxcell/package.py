# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVoxcell(PythonPackage):
    """Python library for handling volumetric data"""

    homepage = "https://bbpgitlab.epfl.ch/nse/voxcell"
    git      = "git@bbpgitlab.epfl.ch:nse/voxcell.git"

    version('develop')
    version('3.0.2', tag='voxcell-v3.0.2')
    version('3.0.0', tag='voxcell-v3.0.0')
    version('2.7.4', tag='voxcell-v2.7.4')
    version('2.7.0', tag='voxcell-v2.7.0')
    version('2.6.2', tag='voxcell-v2.6.2')
    version('2.6.1', tag='voxcell-v2.6.1')
    version('2.6.0', tag='voxcell-v2.6.0')
    version('2.5.6', tag='voxcell-v2.5.6')

    depends_on('py-setuptools', type='build')

    depends_on('py-future@0.16:', type='run')
    depends_on('py-h5py@2.3:2.99', type='run', when='@:2.99.9')
    depends_on('py-h5py@3.1.0:', type='run', when='@3.0.0:')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@0.24.2:', type='run')
    depends_on('py-pynrrd@0.2:0.2.99', type='run', when='@:2.6.1')
    depends_on('py-pynrrd@0.4.0', type='run', when='@2.6.2:')
    depends_on('py-requests@2.18:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-six@1.0:', type='run', when='@:2.99.9')

    depends_on('py-libsonata@0.0.2:', type='run', when='@:2.7.3')
