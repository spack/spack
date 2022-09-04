# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxThemeBuilder(PythonPackage):
    """A tool for authoring Sphinx themes with a simple (opinionated) workflow."""

    homepage = "https://github.com/pradyunsg/sphinx-theme-builder"
    pypi = "sphinx-theme-builder/sphinx-theme-builder-0.2.0b1.tar.gz"

    maintainers = ["JBlaschke"]

    version("0.2.0b1", sha256="e9bb4a0a8516bab8769b9ddf003b70e5878611113319eb1fdb690af84a3a595f")

    depends_on("py-setuptools", type="build")
    depends_on("py-flit-core", type="build")

    def global_options(self, spec, prefix):
        options = []
        return options

    def install_options(self, spec, prefix):
        options = []
        return options
