# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyJupyterPackaging7(PythonPackage):
    """Jupyter Packaging Utilities, version 7."""

    # TODO: This package only exists because different packages in the Jupyter ecosystem
    # require different versions of jupyter_packaging. Once the concretizer is capable
    # of concretizing build dependencies separately, this package should be removed.

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi     = "jupyter_packaging/jupyter-packaging-0.7.12.tar.gz"

    version('0.7.12', sha256='b140325771881a7df7b7f2d14997b619063fe75ae756b9025852e4346000bbb8')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
