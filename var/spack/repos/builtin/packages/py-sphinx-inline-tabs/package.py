# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxInlineTabs(PythonPackage):
    """Add inline tabbed content to your Sphinx documentation."""

    homepage = "https://github.com/pradyunsg/sphinx-inline-tabs"
    pypi = "sphinx_inline_tabs/sphinx_inline_tabs-2022.1.2b11.tar.gz"

    maintainers = ["JBlaschke"]

    version("2022.1.2b11", sha256="afb9142772ec05ccb07f05d8181b518188fc55631b26ee803c694e812b3fdd73")

    depends_on("py-setuptools", type="build")
    depends_on("py-flit-core", type="build")

    def global_options(self, spec, prefix):
        options = []
        return options

    def install_options(self, spec, prefix):
        options = []
        return options
