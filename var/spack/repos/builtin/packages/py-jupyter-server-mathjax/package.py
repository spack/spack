# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyJupyterServerMathjax(PythonPackage):
    """MathJax resources as a Jupyter Server Extension."""

    homepage = "http://jupyter.org/"
    pypi     = "jupyter_server_mathjax/jupyter_server_mathjax-0.2.3.tar.gz"

    version('0.2.3', sha256='564e8d1272019c6771208f577b5f9f2b3afb02b9e2bff3b34c042cef8ed84451')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-jupyter-packaging',    type='build')
    depends_on('py-jupyter-server@1.1:1', type=('build', 'run'))
