# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPoissonReconPybind(PythonPackage):
    """
    Internal Python bindings for PoissonRecon's surface reconstruction
    algorithm
    """

    homepage = "https://bbpgitlab.epfl.ch/nse/poisson-recon-pybind"
    git      = "git@bbpgitlab.epfl.ch:nse/poisson-recon-pybind.git"

    version('0.1.0', tag='poisson_recon_pybind-v0.1.0', submodules=True)

    depends_on('py-setuptools', type='build')
    depends_on('boost@1.50:')
    depends_on('cmake', type='build')
    depends_on('eigen')
    depends_on('py-numpy@1.12:', type=('build', 'run'))
