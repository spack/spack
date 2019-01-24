# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exchanger(AutotoolsPackage):
    """Exchanger is a package containing several C++ base classes. These
    classes, when customized for a solver, can provide communication channels
    between solvers. This packaged is used by CitcomS for solver coupling."""

    homepage = "https://geodynamics.org/cig/software/exchanger/"
    url      = "https://geodynamics.org/cig/software/exchanger/Exchanger-1.0.1.tar.gz"

    version('1.0.1', sha256='1e6c8311db96582bcf2c9aee16a863a5730c1aa54cb3aa7d0249239c6e0b68ee')

    depends_on('python', type=('build', 'run'))
    depends_on('py-merlin', type='build')
    depends_on('py-pythia@0.8.1.0:0.8.1.999', type=('build', 'run'))
