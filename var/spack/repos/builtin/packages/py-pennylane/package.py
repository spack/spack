# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""

    homepage = "https://github.com/XanaduAI/pennylane"
    pypi = "pennylane/PennyLane-0.27.0.tar.gz"

    maintainers = ["marcodelapierre"]

    version("0.27.0", sha256="b5d84488e6ce29fec84674f5cb5c1f3eedb8a4895a4e5aa2cf2497c1fcae530b")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-retworkx", type=("build", "run"))
    depends_on("py-autograd", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-semantic-version@2.7:", type=("build", "run"))
    depends_on("py-autoray@0.3.1:", type=("build", "run"))
    depends_on("py-cachetools/", type=("build", "run"))
    #depends_on("py-pennylane-lightning@0.27:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))

    depends_on("", type="run")
