# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQsymm(PythonPackage):
    """Qsymm is a symmetry finder and symmetric Hamiltonian generator.
    It automatically generates model Hamiltonians from symmetry
    constraints and finds the full symmetry group of your Hamiltonian."""

    homepage = "https://gitlab.kwant-project.org/qt/qsymm"
    #url = "https://downloads.kwant-project.org/tinyarray/tinyarray-1.2.3.tar.gz"
    git = "https://gitlab.kwant-project.org/qt/qsymm.git"

    # Add a list of GitHub accounts to notify when the
    # package is updated
    maintainers = ['payerle']

    version('1.2.7', commit='b0362829887dee187029f62192d42e666dedb11a')
    version('1.2.6', commit='6256f3db38800a4106ec968c7bac8ca9e65bc2e6')
    version('1.2.5', commit='4d983163d472e1c2735193cd4d0bb016e1338025')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
