# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySagaPython(PythonPackage):
    """A light-weight access layer for distributed computing infrastructure.
    DEPRECATED (Please use `py-radical-saga`)"""

    homepage = "https://radical-cybertools.github.io"
    pypi = "saga-python/saga-python-0.41.3.tar.gz"

    maintainers("andre-merzky")

    version(
        "0.41.3",
        sha256="b30961e634f32f6008e292aa1fe40560f257d5294b0cda95baac1cf5391feb5d",
        deprecated=True,
    )

    depends_on("py-radical-utils@:0.45", type=("build", "run"))

    depends_on("py-apache-libcloud", type=("build", "run"))
    depends_on("py-setuptools", type="build")
