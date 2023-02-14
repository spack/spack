# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgv(PythonPackage):
    """Validate configuration and produce human readable error messages."""

    homepage = "https://github.com/asottile/cfgv/"
    pypi = "cfgv/cfgv-2.0.1.tar.gz"

    version("3.3.1", sha256="f5a830efb9ce7a445376bb66ec94c638a9787422f96264c98edc6bdeed8ab736")
    version("2.0.1", sha256="edb387943b665bf9c434f717bf630fa78aecd53d5900d2e05da6ad6048553144")

    depends_on("python@3.6.1:", when="@3.1:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", when="@:2", type=("build", "run"))
