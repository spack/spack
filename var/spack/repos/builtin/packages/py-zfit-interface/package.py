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
        url="https://pypi.org/packages/61/ce/07d8fa63a501dc3af9639595e486be0a18de00726b54a7dc88a5ada235d8/zfit_interface-0.0.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.0.3:")
        depends_on("py-numpy", when="@0.0.3:")
        depends_on("py-typing-extensions", when="@0.0.3:")
        depends_on("py-uhi", when="@0.0.3:")
