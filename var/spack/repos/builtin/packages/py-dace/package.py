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
    pypi = "dace/dace-0.15.1.tar.gz"
    git = "https://github.com/spcl/dace.git"

    maintainers("tbennun")

    version("master", branch="master", submodules=True)
    version("0.15.1", sha256="69bfdbbd5c7177f2926a874f5fa82fcdef61fc532c022b4bc12e1e9218724093")

    variant(
        "counters",
        description="Optional requirements that enable performance counter collection.",
        default=False,
    )

    depends_on("python@3.6:3.12", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Dependencies from setup.py
    depends_on("cmake@3.15.0:", type=("build", "run"))
    depends_on("py-networkx@2.5:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-ply", type=("build", "run"))
    depends_on("py-websockets", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-aenum@3.1:", type=("build", "run"))
    depends_on("py-dill", type=("build", "run"))
    depends_on("py-fparser@0.1.3:", type=("build", "run"))

    depends_on("py-pyreadline", when="platform=win32", type=("build", "run"))
    depends_on("py-dataclasses", when="^python@:3.6", type=("build", "run"))
    depends_on("py-typing-compat", when="^python@:3.7", type=("build", "run"))

    # A typo in the 0.15.1 setup.py specifies sympy <= 1.9 instead of >= 1.9
    depends_on("py-sympy@1.9:", type=("build", "run"))

    # Dependencies in setup.py with specific constraints in requirements.txt
    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-astunparse@1.6.3:", type=("build", "run"))

    # From performance counters requirements
    depends_on("likwid@5.2.2:", when="+counters", type=("build", "run"))
