# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySphinxBasicNg(PythonPackage):
    """A modernised skeleton for Sphinx themes."""

    homepage = "https://github.com/pradyunsg/sphinx-basic-ng"
    pypi = "sphinx_basic_ng/sphinx_basic_ng-0.0.1a12.tar.gz"

    maintainers = ["JBlaschke"]

    version("0.0.1a12", sha256="cffffb14914ddd26c94b1330df1d72dab5a42e220aaeb5953076a40b9c50e801")

    depends_on("py-setuptools", type="build")

    def global_options(self, spec, prefix):
        options = []
        return options

    def install_options(self, spec, prefix):
        options = []
        return options
