# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMunkres(PythonPackage):
    """Python library for Munkres algorithm"""

    homepage = "https://github.com/bmc/munkres"
    pypi = "munkres/munkres-1.1.2.tar.gz"

    license("Apache-2.0")

    version(
        "1.1.4",
        sha256="6b01867d4a8480d865aea2326e4b8f7c46431e9e55b4a2e32d989307d7bced2a",
        url="https://pypi.org/packages/90/ab/0301c945a704218bc9435f0e3c88884f6b19ef234d8899fb47ce1ccfd0c9/munkres-1.1.4-py2.py3-none-any.whl",
    )
    version(
        "1.1.2",
        sha256="c5276abb54aab946fc5eaac24405c53f145c5d51d779fa86c73fae68f9895d9c",
        url="https://pypi.org/packages/64/97/61ddc63578870e04db6eb1d3bee58ad4e727f682068a7c7405edb8b2cdeb/munkres-1.1.2-py2.py3-none-any.whl",
    )
