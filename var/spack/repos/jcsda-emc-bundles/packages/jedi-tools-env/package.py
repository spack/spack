# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediToolsEnv(BundlePackage):
    """Development environment for jedi-tools"""

    homepage = "https://github.com/JCSDA-internal/jedi-tools"
    git = "https://github.com/JCSDA-internal/jedi-tools.git"

    maintainers = ["climbfuji", "srherbener"]

    version("1.0.0")

    variant("latex", default=False, description="Enable building LaTeX documentation with Sphinx")

    depends_on("awscli", type="run")
    # Only old versions - new versions have terrible dependencies
    # depends_on("aws-parallelcluster", type="run")
    # npm is needed for aws-parallelcluster, even when installed
    # via pip in venv - however, several build errors in npm and
    # node-js - install all of this outside of spack-stack for now
    # depends_on("npm", type="run")
    depends_on("py-click", type="run")
    depends_on("py-openpyxl", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pygithub", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-sphinx", type="run")
    depends_on("py-sphinxcontrib-bibtex", when="+latex", type="run")
    depends_on("texlive", when="+latex", type="run")

    conflicts("%intel", msg="jedi-tools-env does not build with Intel")

    # There is no need for install() since there is no code.
