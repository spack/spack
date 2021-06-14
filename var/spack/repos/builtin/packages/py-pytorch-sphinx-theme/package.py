# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytorchSphinxTheme(PythonPackage):
    """PyTorch Sphinx Theme."""

    homepage = "https://github.com/pytorch/pytorch_sphinx_theme"
    pypi     = "pytorch_sphinx_theme/pytorch_sphinx_theme-0.0.19.tar.gz"

    version('0.0.19', sha256='9c0472a82fc72e5b4c4c5202fc9cdd6de8f1de6050a98f4ace75707ebb184bfd')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx', type=('build', 'run'))
