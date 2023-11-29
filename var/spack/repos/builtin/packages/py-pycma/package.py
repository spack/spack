# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycma(PythonPackage):
    """
    Python implementation of CMA-ES Covariance Matrix Adaptation Evolution Str
    ategy for non-linear numerical optimization in Python
    """

    homepage = "https://github.com/CMA-ES/pycma"

    url = "https://github.com/CMA-ES/pycma/archive/refs/tags/r3.3.0.tar.gz"

    maintainers("LydDeb")

    version("3.3.0", sha256="2a061296bfca4eb979ed471e0c5acf40fc69345c13d4522ac6ed62a50d864bcf")

    variant("plotting", default=True, description="Build with matplotlib support.")
    variant(
        "constrained_solution_tracking",
        default=True,
        description="Build with moarchiving support.",
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"), when="+plotting")
    depends_on("py-moarchiving", type=("build", "run"), when="+constrained_solution_tracking")
