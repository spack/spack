# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAutotune(PythonPackage):
    """Common interface for autotuning search space and method definition."""

    maintainers = ['Kerilk']

    homepage = "https://github.com/ytopt-team/autotune"
    url = "https://github.com/ytopt-team/autotune/archive/refs/tags/v1.0.0.tar.gz"

    version('1.0.0', sha256='13f10594156a7a220561467fdbee52173238ea82c07e8188fdf6584d4524f46f')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
