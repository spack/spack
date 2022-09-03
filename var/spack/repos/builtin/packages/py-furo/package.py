# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuro(PythonPackage):
    """A clean customisable Sphinx documentation theme."""

    homepage = "https://github.com/pradyunsg/furo"
    pypi = "furo/furo-2022.6.21.tar.gz"

    maintainers = ["JBlaschke"]

    version("2022.6.21", sha256="9aa983b7488a4601d13113884bfb7254502c8729942e073a0acb87a5512af223")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx-theme-builder", type="build")
    depends_on("py-rich", type="build")
    depends_on("py-pyproject-metadata", type="build")
    depends_on("py-tomli", type="build")
    depends_on("py-nodeenv", type="build")


    def global_options(self, spec, prefix):
        options = []
        return options

    def install_options(self, spec, prefix):
        options = []
        return options
