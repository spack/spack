# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHvac(PythonPackage):
    """HashiCorp Vault API client"""

    homepage = "https://github.com/hvac/hvac/"
    url = "https://github.com/hvac/hvac/archive/v0.2.17.tar.gz"

    license("Apache-2.0")

    version(
        "0.9.6",
        sha256="f0b035f41d9fbf49a14e721b65f495f685060e870084323d1e8e0ee0eb024df5",
        url="https://pypi.org/packages/1d/95/489323e0f6ec69b16ea07dd74ad23053392c78fdc6ea981672a33835971f/hvac-0.9.6-py2.py3-none-any.whl",
    )
    version(
        "0.9.5",
        sha256="4fb2ee5060b735e994a3398085b3cf9ef0c57112f28a9e36f174c010b2899aa8",
        url="https://pypi.org/packages/c7/e3/11abb594a7e5df9ecced05b586d4fe6f542aa2cfae5ba93a3b9502eecbfe/hvac-0.9.5-py2.py3-none-any.whl",
    )
    version(
        "0.9.4",
        sha256="101934798b34676ebae1ccb3fdd44e4e2eea389041d52e32f9e3922d0369bfd9",
        url="https://pypi.org/packages/0a/27/61b2087db577001469b0b10d759a3ff6e9e003ae2f314d00f8930e3bf26c/hvac-0.9.4-py2.py3-none-any.whl",
    )
    version(
        "0.9.3",
        sha256="af21faaccfba88ed0e1f1365b9bb7de477e5c9a6ebd6fa3712bab94ea4f12356",
        url="https://pypi.org/packages/17/e4/a50e316e97b263fce604cc8480888936df6f60447a79276fe89b980e8abc/hvac-0.9.3-py2.py3-none-any.whl",
    )
    version(
        "0.2.17",
        sha256="9e277a7864927f53fb1aca4fd33559390da43b21b6dc0c99058cf05ac8d5335f",
        url="https://pypi.org/packages/51/d9/8645102e8a05d1273ada844a2922cae934c37ddbbd047f95bbdb4e4e3003/hvac-0.2.17-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-requests@2.21:", when="@0.7.2:0.11.0,0.11.2:0")
        depends_on("py-requests@2.7:", when="@:0.2,0.6.2:0.7.1")
        depends_on("py-six@1.5:", when="@0.9.6:0.11.0,0.11.2:0")
