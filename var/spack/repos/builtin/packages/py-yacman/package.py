# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYacman(PythonPackage):
    """A YAML configuration manager."""

    homepage = "https://github.com/databio/yacman"
    pypi = "yacman/yacman-0.8.4.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.8.4",
        sha256="0cc7aed9e400b9757f937eaf95b2257e822822cdf30626cb35ce7974b2446323",
        url="https://pypi.org/packages/7d/a6/ff07474f18e129fa1e034558f84391c665038f940cec89efc59e3b4a2b71/yacman-0.8.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-attmap@0.13:", when="@0.7.1:")
        depends_on("py-jsonschema@3.2:", when="@0.8:")
        depends_on("py-oyaml", when="@0.6.8:")
        depends_on("py-pyyaml@3.13:", when="@0.6.8:")
        depends_on("py-ubiquerg@0.6.1:", when="@0.6.9:0.9.2")
