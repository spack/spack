# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMerlin(PythonPackage):
    """Merlin Workflow for HPC."""

    homepage = "https://github.com/LLNL/merlin"
    pypi = "merlin/merlin-1.4.1.tar.gz"
    git = "https://github.com/LLNL/merlin.git"
    tags = ["radiuss"]

    license("MIT")

    version(
        "1.10.3",
        sha256="561d4fb0d332e92ec00901eb7b841eb6758b3fd3434733e6982614faecd23373",
        url="https://pypi.org/packages/b1/db/ac3cb3ad6d039398ed72061fe30ed483bfcb503228b94aed09024f1958e4/merlin-1.10.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cached-property")
        depends_on("py-celery@5.0.3:+redis+sqlalchemy")
        depends_on("py-coloredlogs")
        depends_on("py-cryptography")
        depends_on("py-importlib-resources", when="^python@:3.6")
        depends_on("py-maestrowf@1.1.9:", when="@1.9:")
        depends_on("py-numpy")
        depends_on("py-parse")
        depends_on("py-psutil@5.1:")
        depends_on("py-pyyaml@5.1.2:")
        depends_on("py-redis@4.3.4:", when="@1.9:")
        depends_on("py-tabulate")
