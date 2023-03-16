# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDace(PythonPackage):
    """DaCe is a fast parallel programming framework that takes code in
    Python/NumPy and other programming languages, and maps it to
    high-performance CPU, GPU, and FPGA programs, which can be
    optimized programmatically or interactively."""

    homepage = "https://github.com/spcl/dace"
    pypi = "dace/dace-0.14.2.tar.gz"
    git = "https://github.com/spcl/dace.git"

    maintainers("tbennun")

    version("master", branch="master", submodules=True)
    version("0.14.2", sha256="13e5c5af31ca7313839dee257305d2020ac79c3cfa77af8ea3feb5260b0582a4")

    variant(
        "counters",
        description="Optional requirements that enable performance counter collection.",
        default=False,
    )

    depends_on("python@3.6:3.10", when="@0.14.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # From setup.py
    depends_on("cmake@3.15.0:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-numpy@1.19:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-networkx@2.5:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-astunparse@1.6.3:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-sympy@1.10:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-ply@3.8:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-websockets@10.3:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-requests@2.24:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-aenum@3.1.11:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-flask@2.2.2:", when="@0.14.2:", type=("build", "run"))
    depends_on("py-dill@0.3.6:", when="@0.14.2:", type=("build", "run"))

    # From performance counters requirements
    depends_on("likwid@5.2.2:", when="@0.14.2:+counters", type=("build", "run"))
