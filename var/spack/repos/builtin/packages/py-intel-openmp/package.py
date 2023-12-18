# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyIntelOpenmp(PythonPackage):
    """Intel OpenMP* Runtime Library x86_64 dynamic libraries
    for macOS*. Intel OpenMP* Runtime Library provides OpenMP
    API specification support in Intel C Compiler, Intel C++
    Compiler and Intel Fortran Compiler. It helps to improve
    performance by creating multithreaded software using shared
    memory and running on multi-core processor systems."""

    homepage = "https://pypi.org/project/intel-openmp/"

    version(
        "2021.2.0",
        sha256="2c40b766bbcf346d298c54b92733c75a70b5f4f3b63461fa92753e49f14e4ac0",
        expand=False,
    )

    if sys.platform.startswith("linux"):
        version(
            "2021.2.0",
            url="https://pypi.io/packages/py2.py3/i/intel-openmp/intel_openmp-2021.2.0-py2.py3-none-manylinux1_x86_64.whl",
            sha256="2c40b766bbcf346d298c54b92733c75a70b5f4f3b63461fa92753e49f14e4ac0",
            expand=False,
        )
        version(
            "2021.1.2",
            url="https://pypi.io/packages/py2.py3/i/intel-openmp/intel_openmp-2021.1.2-py2.py3-none-manylinux1_x86_64.whl",
            sha256="8796797ecae99f39b27065e4a7f1f435e2ca08afba654ca57a77a2717f864dca",
            expand=False,
        )

    if sys.platform.startswith("darwin"):
        version(
            "2021.2.0",
            url="https://pypi.io/packages/py2.py3/i/intel-openmp/intel_openmp-2021.2.0-py2.py3-none-macosx_10_15_x86_64.whl",
            sha256="39467008e822d6c2a7b183f443acb6521098ebee6bb084f3f97fec338b40fa4c",
            expand=False,
        )
        version(
            "2021.1.2",
            url="https://pypi.io/packages/py2.py3/i/intel-openmp/intel_openmp-2021.1.2-py2.py3-none-macosx_10_15_x86_64.whl",
            sha256="2af893738b4b06cb0183746f2992169111031340b59c84a0fd4dec1ed66b80f2",
            expand=False,
        )
