# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVascpy(PythonPackage):
    """Python library for reading, writing, and manipulating large-scale vasculature
    datasets """

    homepage = "https://github.com/BlueBrain/vascpy"
    url      = "https://pypi.io/packages/source/v/vascpy/vascpy-0.1.0.tar.gz"

    version("develop", branch="main")
    version("0.1.0", sha256="0d6aa4faebe75bce36f44bd6f884d015a8f24e1dc76977d8c7fd6be7ea8e725b")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type="build")

    depends_on("py-numpy@1.17.0:", type="run")
    depends_on("py-scipy@1.0.0:", type="run")
    depends_on("py-h5py@3.5.0:", type="run")
    depends_on("py-pandas@1.0.0:", type="run")
    depends_on("py-morphio@3.0.0:", type="run")
    depends_on("py-libsonata@0.1.8:", type="run")
    depends_on("py-click@8.0.0:", type="run")
