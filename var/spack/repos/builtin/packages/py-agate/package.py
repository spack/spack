# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAgate(PythonPackage):
    """agate is a Python data analysis library that is optimized for humans
    instead of machines. It is an alternative to numpy and pandas that solves
    real-world problems with readable code."""

    homepage = "https://agate.readthedocs.io/en/latest/"
    pypi = "agate/agate-1.6.1.tar.gz"

    license("MIT")

    version(
        "1.6.1",
        sha256="48d6f80b35611c1ba25a642cbc5b90fcbdeeb2a54711c4a8d062ee2809334d1c",
        url="https://pypi.org/packages/92/77/ef675f16486884ff7f77f3cb87aafa3429c6bb869d4d73ee23bf4675e384/agate-1.6.1-py2.py3-none-any.whl",
    )
