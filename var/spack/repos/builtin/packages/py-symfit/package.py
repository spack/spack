# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySymfit(PythonPackage):
    """Symbolic Fitting; fitting as it should be."""

    homepage = "https://symfit.readthedocs.org"
    pypi = "symfit/symfit-0.3.5.tar.gz"

    license("MIT")

    version(
        "0.3.5",
        sha256="33bde64b1092b57550c3c136d4d2d608896f29a3d41e940d24e0ff8696e5fa00",
        url="https://pypi.org/packages/ea/71/e653cce934d1711198b29f336d31e7bdeff1c5f07bf053948203f8809cb1/symfit-0.3.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@0.3:0.4.1")
        depends_on("py-scipy", when="@0.3:0.4.0")
        depends_on("py-sympy", when="@0.3:0.4.2")
