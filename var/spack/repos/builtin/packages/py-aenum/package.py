# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAenum(PythonPackage):
    """Advanced Enumerations (compatible with Python's stdlib Enum),
    NamedTuples, and NamedConstants."""

    homepage = "https://github.com/ethanfurman/aenum"
    pypi = "aenum/aenum-2.1.2.tar.gz"

    version(
        "3.1.12",
        sha256="2d544ef7323c088d68abf9a84b9f3f6db0d516fec685e15678b5f84fdb7b8ba0",
        url="https://pypi.org/packages/57/32/18862210ce170908bc19de5cbb3844b165679123b32fe119d4116e46c2c8/aenum-3.1.12-py3-none-any.whl",
    )
    version(
        "2.1.2",
        sha256="3df9b84cce5dc9ed77c337079f97b66c44c0053eb87d6f4d46b888dc45801e38",
        url="https://pypi.org/packages/0d/46/5b6a6c13fee40f9dfaba84de1394bfe082c0c7d95952ba0ffbd56ce3a3f7/aenum-2.1.2-py3-none-any.whl",
    )
