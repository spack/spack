# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterPackaging(PythonPackage):
    """Jupyter Packaging Utilities."""

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi     = "jupyter_packaging/jupyter_packaging-0.10.4.tar.gz"

    version('0.10.4', sha256='589db027cb85a92612f9bcfaeecaa8a9072ac8a4bddaf827f648664258e587c4')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@46.4.0:', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))
    depends_on('py-tomlkit', type=('build', 'run'))
    depends_on('py-wheel', type=('build', 'run'))
    depends_on('py-deprecation', type=('build', 'run'))
