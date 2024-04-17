# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeyringsAlt(PythonPackage):
    """Alternate keyring implementations"""

    homepage = "https://github.com/jaraco/keyrings.alt"
    pypi = "keyrings.alt/keyrings.alt-4.0.2.tar.gz"

    license("MIT")

    version(
        "4.2.0",
        sha256="3d25912ed71d6deec85d7e6e867963e1357cd56186a41c9295b86939a5ebf85c",
        url="https://pypi.org/packages/71/0c/32cf193861389487e062dc91683146f696d11ce0d4bc3fb6539f68aa0ada/keyrings.alt-4.2.0-py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="7b051f13ffeb216ea9940995f91ea3eece7795d199631ea25a625fbf614d74b4",
        url="https://pypi.org/packages/e2/74/5f312f4713aa1836f1b8595318cac4ab770fc2278d12ac66fdabeafb2b67/keyrings.alt-4.1.0-py3-none-any.whl",
    )
    version(
        "4.0.2",
        sha256="49ab586d0610e5f73e874fb3dcfc6b94f222d30a8457ef324f4124c34b3ea2f5",
        url="https://pypi.org/packages/55/bd/36afd53fe86dc28c2f7280d4e1f5e1e58dc26c0272609af069818f575698/keyrings.alt-4.0.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@4.1.1:4")
        depends_on("py-jaraco-classes", when="@4.1.2:")
