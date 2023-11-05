# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpydoc(PythonPackage):
    """numpydoc - Numpy's Sphinx extensions"""

    homepage = "https://github.com/numpy/numpydoc"
    pypi = "numpydoc/numpydoc-0.6.0.tar.gz"

    version("1.5.0", sha256="b0db7b75a32367a0e25c23b397842c65e344a1206524d16c8069f0a1c91b5f4c")
    version("1.1.0", sha256="c36fd6cb7ffdc9b4e165a43f67bf6271a7b024d0bb6b00ac468c9e2bfc76448e")
    version("0.6.0", sha256="1ec573e91f6d868a9940d90a6599f3e834a2d6c064030fbe078d922ee21dcfa1")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@4.2:", type=("build", "run"), when="@1.5:")
    depends_on("py-sphinx@1.6.5:", type=("build", "run"), when="@1.1.0")
    depends_on("py-sphinx@1.0.1:1.6.7", type=("build", "run"), when="@0.6.0")
    depends_on("py-jinja2@2.10:", type=("build", "run"), when="@1.3.0:")
    depends_on("py-jinja2@2.3:", type=("build", "run"), when="@1.1.0")
