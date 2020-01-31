# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHpccm(PythonPackage):
    """HPC Container Maker (HPCCM - pronounced H-P-see-M) is an open source
    tool to make it easier to generate container specification files."""

    homepage = "https://github.com/NVIDIA/hpc-container-maker"
    url      = "https://github.com/NVIDIA/hpc-container-maker/archive/v19.2.0.tar.gz"

    version('19.2.0', sha256='99eb0f48cfbdfb29815aed8bcd0fa8c5a857fd912a2bb9658b217b0712ca4af5')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
