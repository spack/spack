# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpaddress(PythonPackage):
    """Python 3.3's ipaddress for older Python versions"""

    homepage = "https://github.com/phihag/ipaddress"
    pypi = "ipaddress/ipaddress-1.0.23.tar.gz"

    license("PSF-2.0")

    version(
        "1.0.23",
        sha256="6e0f4a39e66cb5bb9a137b00276a2eff74f93b71dcbdad6f10ff7df9d3557fcc",
        url="https://pypi.org/packages/c2/f8/49697181b1651d8347d24c095ce46c7346c37335ddc7d255833e7cde674d/ipaddress-1.0.23-py2.py3-none-any.whl",
    )
    version(
        "1.0.22",
        sha256="64b28eec5e78e7510698f6d4da08800a5c575caa4a286c93d651c5d3ff7b6794",
        url="https://pypi.org/packages/fc/d0/7fc3a811e011d4b388be48a0e381db8d990042df54aa4ef4599a31d39853/ipaddress-1.0.22-py2.py3-none-any.whl",
    )
    version(
        "1.0.18",
        sha256="d34cf15d95ce9a734560f7400a8bd2ac2606f378e2a1d0eadbf1c98707e7c74a",
        url="https://pypi.org/packages/17/93/28f4dd560780dd70fe75ce7e2662869770dfac181f6bbb472179ea8da516/ipaddress-1.0.18-py2-none-any.whl",
    )
