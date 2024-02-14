# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZfitInterface(PythonPackage):
    """
    zfit model fitting interface for HEP
    """

    homepage = "https://github.com/zfit/zfit-interface"
    pypi = "zfit_interface/zfit_interface-0.0.3.tar.gz"

    maintainers("jonas-eschle")
    license("BSD-3-Clause", checked_by="jonas-eschle")

    version(
        "0.0.3",
        sha256="c41cf79f1da4150b9a60bb1e8cab15df895b6ff4b753e2306494a7abda4150d0",
        expand=False,
    )

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="run")
    depends_on("py-uhi", type="run")
