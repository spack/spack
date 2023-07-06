# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEasybuildFramework(PythonPackage):
    """The core of EasyBuild, a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = "https://easybuilders.github.io/easybuild"
    pypi = "easybuild-framework/easybuild-framework-4.0.0.tar.gz"
    maintainers("boegel")

    version("4.7.0", sha256="ea51c3cb88fca27daadd2fb55ee31f5f51fc60c4e3519ee9d275954540312df8")
    version("4.0.0", sha256="f5c40345cc8b9b5750f53263ade6c9c3a8cd3dfab488d58f76ac61a8ca7c5a77")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
