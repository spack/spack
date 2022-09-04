# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxextOpengraph(PythonPackage):
    """Sphinx Extension to enable OGP support"""

    homepage = "https://github.com/wpilibsuite/sphinxext-opengraph"
    pypi = "sphinxext-opengraph/sphinxext-opengraph-0.6.3.tar.gz"

    maintainers = ["JBlaschke"]

    version("0.6.3", sha256="cd89e13cc7a44739f81b64ee57c1c20ef0c05dda5d1d8201d31ec2f34e4c29db")

    depends_on("py-setuptools", type="build")

    def global_options(self, spec, prefix):
        options = []
        return options

    def install_options(self, spec, prefix):
        options = []
        return options
