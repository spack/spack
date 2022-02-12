# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyJupyterlabPygments(PythonPackage):
    """Pygments theme using JupyterLab CSS variables."""

    homepage = "https://jupyter.org/"
    pypi = "jupyterlab-pygments/jupyterlab_pygments-0.1.1.tar.gz"

    version('0.1.2', sha256='cfcda0873626150932f438eccf0f8bf22bfa92345b814890ab360d666b254146')
    version('0.1.1', sha256='19a0ccde7daddec638363cd3d60b63a4f6544c9181d65253317b2fb492a797b9')

    depends_on('py-setuptools', type='build')
    depends_on('py-pygments@2.4.1:2', type=('build', 'run'))
