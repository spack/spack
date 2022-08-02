# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgv(PythonPackage):
    """Validate configuration and produce human readable error messages."""

    homepage = "https://github.com/asottile/cfgv/"
    pypi = "cfgv/cfgv-2.0.1.tar.gz"

    version("3.3.1", sha256="f5a830efb9ce7a445376bb66ec94c638a9787422f96264c98edc6bdeed8ab736")
    version("3.3.0", sha256="9e600479b3b99e8af981ecdfc80a0296104ee610cab48a5ae4ffd0b668650eb1")
    version("3.2.0", sha256="cf22deb93d4bcf92f345a5c3cd39d3d41d6340adc60c78bbbd6588c384fda6a1")
    version("3.1.0", sha256="c8e8f552ffcc6194f4e18dd4f68d9aef0c0d58ae7e7be8c82bee3c5e9edfa513")
    version("3.0.0", sha256="04b093b14ddf9fd4d17c53ebfd55582d27b76ed30050193c14e560770c5360eb")
    version("2.0.1", sha256="edb387943b665bf9c434f717bf630fa78aecd53d5900d2e05da6ad6048553144")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@3.0.0:")
    depends_on("python@3.6.1:", type=("build", "run"), when="@3.1.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
