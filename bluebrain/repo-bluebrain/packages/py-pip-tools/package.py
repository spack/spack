# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPipTools(PythonPackage):
    """pip-tools keeps your pinned dependencies fresh."""

    homepage = "https://github.com/jazzband/pip-tools/"
    pypi = "pip-tools/pip-tools-6.12.3.tar.gz"

    version("6.12.3", sha256="480d44fae6e09fad3f9bd3d0a7e8423088715d10477e8ef0663440db25e3114f")

    depends_on("py-click@8:", type=("build", "run"))
    depends_on("py-setuptools@63:", type=("build", "run"))
    depends_on("py-setuptools-scm+toml@7:", type="build")
    depends_on("py-pip@22.2:", type=("build", "run"))
    depends_on("py-build", type=("build", "run"))
    depends_on("py-wheel", type=("build", "run"))
