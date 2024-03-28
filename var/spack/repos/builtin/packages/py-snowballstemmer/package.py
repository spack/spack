# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnowballstemmer(PythonPackage):
    """This package provides 29 stemmers for 28 languages generated from
    Snowball algorithms."""

    homepage = "https://github.com/snowballstem/snowball"
    pypi = "snowballstemmer/snowballstemmer-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.2.0",
        sha256="c8e1716e83cc398ae16824e5572ae04e0d9fc2c6b985fb0f900f5f0c96ecba1a",
        url="https://pypi.org/packages/ed/dc/c02e01294f7265e63a7315fe086dd1df7dacb9f840a804da846b96d01b96/snowballstemmer-2.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="209f257d7533fdb3cb73bdbd24f436239ca3b2fa67d56f6ff88e86be08cc5ef0",
        url="https://pypi.org/packages/7d/4b/cdf1113a0e88b641893b814e9c36f69a6fda28cd88b62c7f0d858cde3166/snowballstemmer-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="9f3bcd3c401c3e862ec0ebe6d2c069ebc012ce142cce209c098ccb5b09136e89",
        url="https://pypi.org/packages/d4/6c/8a935e2c7b54a37714656d753e4187ee0631988184ed50c0cf6476858566/snowballstemmer-1.2.1-py2.py3-none-any.whl",
    )
