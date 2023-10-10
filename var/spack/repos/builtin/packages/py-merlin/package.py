# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    version("1.10.3", sha256="6edaf17b502db090cef0bc53ae0118c55f77d7a16f43c7a235e0dd1770decadb")
    version("1.7.5", sha256="1994c1770ec7fc9da216f9d0ca8214684dcc0daa5fd55337b96e308b2e68daaa")
    version("1.7.4", sha256="9a6f8a84a1b52d0bfb0dc7bdbd7e15677e4a1041bd25a49a2d965efe503a6c20")
    version("1.4.1", sha256="9d515cfdbcde2443892afd92b78dbc5bf2aed2060ed3a336e683188e015bca7c")
    version("master", branch="master")
    version("develop", branch="develop")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-cached-property", type=("build", "run"))
    depends_on("py-celery@5.0.3:+redis+sqlalchemy", when="@1.7.6:", type=("build", "run"))
    depends_on("py-celery@5.0.0:+redis+sqlalchemy", when="@1.7.5", type=("build", "run"))
    depends_on("py-celery@4.4.5:+redis+sqlalchemy", when="@1.6.2:1.7.4", type=("build", "run"))
    depends_on("py-celery@4.3.0:+redis+sqlalchemy", when="@:1.5.2", type=("build", "run"))
    depends_on("py-celery@4.3.0:+redis", when="@1.4.1:1.5.1", type=("build", "run"))
    # The upperbound on py-celery is not in requirements.txt because there was no 5.x release
    # then. See commit 61b4fc708a3d6fd22709b35836065c778bf6304e for why it's needed.
    depends_on("py-celery@:4", when="@:1.7.4", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-cryptography", type=("build", "run"))
    depends_on("py-importlib-metadata@:4", when="@1.10: ^python@3.7", type=("build", "run"))
    depends_on("py-maestrowf@1.1.9:", when="@1.9.0:", type=("build", "run"))
    depends_on("py-maestrowf@1.1.7dev0", when="@1.2.0:1.8", type=("build", "run"))
    depends_on("py-maestrowf@1.1.6:", when="@:1.1", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-parse", type=("build", "run"))
    depends_on("py-psutil@5.1.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.1.2:", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-redis@4.3.4:", when="@1.9.0:", type=("build", "run"))
