# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTenacity(PythonPackage):
    """Retrying library for Python"""

    homepage = "https://github.com/jd/tenacity"
    pypi = "tenacity/tenacity-6.3.1.tar.gz"

    version("8.0.1", sha256="43242a20e3e73291a28bcbcacfd6e000b02d3857a9a9fff56b297a27afdc932f")
    version("6.3.1", sha256="e14d191fb0a309b563904bbc336582efe2037de437e543b38da749769b544d7f")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@8:")

    depends_on("py-setuptools@21:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

    depends_on("py-six@1.9.0:", type=("build", "run"), when="@:7")
