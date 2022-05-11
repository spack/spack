# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyJupyterPackaging11(PythonPackage):
    """Jupyter Packaging Utilities, version 11."""

    # TODO: This package only exists because different packages in the Jupyter ecosystem
    # require different versions of jupyter_packaging. Once the concretizer is capable
    # of concretizing build dependencies separately, this package should be removed.

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi     = "jupyter_packaging/jupyter_packaging-0.11.1.tar.gz"

    version('0.11.1', sha256='6f5c7eeea98f7f3c8fb41d565a94bf59791768a93f93148b3c2dfb7ebade8eec')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))
    depends_on('py-tomlkit', type=('build', 'run'))
    depends_on('py-setuptools@46.4:', type=('build', 'run'))
    depends_on('py-wheel', type=('build', 'run'))
    depends_on('py-deprecation', type=('build', 'run'))
