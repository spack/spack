# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E4sCl(PythonPackage):
    """Container Launcher for E4S containers, facilitating MPI library
    translations"""

    maintainers = ["spoutn1k", "FrederickDeny"]
    homepage = "https://e4s-cl.readthedocs.io"
    url = "https://oaciss.uoregon.edu/e4s/e4s-cl/releases"
    git = "https://github.com/E4S-Project/e4s-cl"

    tags = ["e4s"]

    version("master", branch="master")
    version("1.0.1", commit="b2c92993e0c7cb42de07f0f7cc02da3a06816192")
    version("1.0.0", commit="410bb2e6601d9b90243a487ad7f7d2dabd8ba04c")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-texttable@1.6.1", type="run")
    depends_on("py-pyyaml@6.0", type="run")
    depends_on("py-termcolor@1.1.0", type="run")
    depends_on("py-pyelftools@0.26", type="run")
    depends_on("py-python-ptrace@0.9.8", type="run")
    depends_on("py-python-sotools@0.1.0", type="run")
    depends_on("py-requests@2.26.0", type="run")
    depends_on("py-tinydb@4.7.0", type="run")
