# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestAsyncio(PythonPackage):
    """pytest-asyncio is an Apache2 licensed library, written in Python,
    for testing asyncio code with pytest."""

    homepage = "https://github.com/pytest-dev/pytest-asyncio"
    pypi = "pytest-asyncio/pytest-asyncio-0.18.3.tar.gz"

    version("0.18.3", sha256="7659bdb0a9eb9c6e3ef992eef11a2b3e69697800ad02fb06374a210d85b29f91")
    version("0.9.0", sha256="fbd92c067c16111174a1286bfb253660f1e564e5146b39eeed1133315cf2c2cf")

    depends_on("python@3.7:", when="@0.18.3:", type=("build", "run"))
    depends_on("python@3.5:", when="@0.9.0:", type=("build", "run"))
    depends_on("py-setuptools@51.0:", when="@0.18.3:", type="build")
    depends_on("py-setuptools", when="@0.9.0:", type="build")
    depends_on("py-wheel@0.36:", when="@0.18.3:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", when="@0.18.3:", type="build")
    depends_on("py-pytest@6.1.0:", when="@0.18.3:", type=("build", "run"))
    depends_on("py-pytest@3.0.6:", when="@0.9.0:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.2:", when="@0.18.3:^python@:3.7", type=("build", "run"))
