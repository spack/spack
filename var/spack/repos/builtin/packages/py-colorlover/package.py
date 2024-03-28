# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorlover(PythonPackage):
    """Color scales in Python for humans."""

    homepage = "https://github.com/plotly/colorlover"
    pypi = "colorlover/colorlover-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.3.0",
        sha256="58705cdd1f1c3903b5cbc15ac5ad816779363400a74e5f407563b0b3627902e5",
        url="https://pypi.org/packages/9a/53/f696e4480b1d1de3b1523991dea71cf417c8b19fe70c704da164f3f90972/colorlover-0.3.0-py3-none-any.whl",
    )
