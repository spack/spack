# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyMeldmd(PythonPackage, CudaPackage):
    """MELD is a tool for inferring the structure of
    biomolecules from sparse, ambiguous, or noisy data."""

    homepage = "http://meldmd.org/"
    url      = "https://github.com/maccallumlab/meld/archive/refs/tags/0.4.20.tar.gz"

    version('0.4.20', sha256='8c8d2b713f8dc0ecc137d19945b3957e12063c8dda569696e47c8820eeac6c92')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('amber')
    depends_on('openmm')
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-parmed', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))
