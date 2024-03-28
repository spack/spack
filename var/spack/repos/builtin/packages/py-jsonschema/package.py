# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonschema(PythonPackage):
    """Jsonschema: An(other) implementation of JSON Schema for Python."""

    homepage = "https://github.com/Julian/jsonschema"
    pypi = "jsonschema/jsonschema-3.2.0.tar.gz"

    license("MIT")

    version(
        "4.17.3",
        sha256="a870ad254da1a8ca84b6a2905cac29d265f805acc57af304784962a2aa6508f6",
        url="https://pypi.org/packages/c1/97/c698bd9350f307daad79dd740806e1a59becd693bd11443a0f531e3229b3/jsonschema-4.17.3-py3-none-any.whl",
    )
    version(
        "4.16.0",
        sha256="9e74b8f9738d6a946d70705dc692b74b5429cd0960d58e79ffecfc43b2221eb9",
        url="https://pypi.org/packages/d8/ad/b96e267a185d0050ac0f128827da6f16a7fd0fd5e045294771b3c265f2e9/jsonschema-4.16.0-py3-none-any.whl",
    )
    version(
        "4.10.0",
        sha256="92128509e5b700bf0f1fd08a7d018252b16a1454465dfa6b899558eeae584241",
        url="https://pypi.org/packages/60/17/8c0f01efcde8920ab6e4e5ec01e19056dc7fa00aebeeae8b6423b736696f/jsonschema-4.10.0-py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="77281a1f71684953ee8b3d488371b162419767973789272434bbc3f29d9c8823",
        url="https://pypi.org/packages/55/b2/2c4af6a97c3f12c6d5a72b41d328c3996e14e1e46701df3fac1ed65119c9/jsonschema-4.4.0-py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="4e5b3cf8216f577bee9ce139cbe72eca3ea4f292ec60928ff24758ce626cd163",
        url="https://pypi.org/packages/c5/8f/51e89ce52a085483359217bc72cdbf6e75ee595d5b1d4b5ade40c7e018b8/jsonschema-3.2.0-py2.py3-none-any.whl",
    )
    version(
        "3.1.1",
        sha256="94c0a13b4a0616458b42529091624e66700a17f847453e52279e35509a5b7631",
        url="https://pypi.org/packages/ce/6c/888d7c3c1fce3974c88a01a6bc553528c99d3586e098eee23e8383dd11c3/jsonschema-3.1.1-py2.py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="5f9c0a719ca2ce14c5de2fd350a64fd2d13e8539db29836a86adc990bb1a068f",
        url="https://pypi.org/packages/54/48/f5f11003ceddcd4ad292d4d9b5677588e9169eef41f88e38b2888e7ec6c4/jsonschema-3.0.2-py2.py3-none-any.whl",
    )
    version(
        "3.0.1",
        sha256="a5f6559964a3851f59040d3b961de5e68e70971afb88ba519d27e6a039efff1a",
        url="https://pypi.org/packages/aa/69/df679dfbdd051568b53c38ec8152a3ab6bc533434fc7ed11ab034bf5e82f/jsonschema-3.0.1-py2.py3-none-any.whl",
    )
    version(
        "2.6.0",
        sha256="000e68abd33c972a5248544925a0cae7d1125f9bf6c58280d37546b946769a08",
        url="https://pypi.org/packages/77/de/47e35a97b2b05c2fadbec67d44cfcdcd09b8086951b331d82de90d2912da/jsonschema-2.6.0-py2.py3-none-any.whl",
    )
    version(
        "2.5.1",
        sha256="71e7b3bcf9fca408bcb65bb60892f375d3abdd2e4f296eeeb8fe0bbbfcde598e",
        url="https://pypi.org/packages/bd/cc/5388547ea3504bd8cbf99ba2ae7a3231598f54038e9b228cbd174f8ec6a1/jsonschema-2.5.1-py2.py3-none-any.whl",
    )

    variant("format", default=False)
    variant("format-nongpl", default=False)

    with default_args(type="run"):
        depends_on("py-attrs@17.4:", when="@3.0.0-alpha4:4.17")
        depends_on("py-fqdn", when="@4:+format-nongpl")
        depends_on("py-fqdn", when="@4:+format")
        depends_on("py-idna", when="@3.2:+format-nongpl")
        depends_on("py-idna", when="@3.0.0-alpha4:+format")
        depends_on("py-importlib-metadata", when="@3.1")
        depends_on("py-importlib-resources@1.4:", when="@4.2.1: ^python@:3.8")
        depends_on("py-isoduration", when="@4.0.0-alpha3:+format-nongpl")
        depends_on("py-isoduration", when="@4.0.0-alpha3:+format")
        depends_on("py-jsonpointer@1.14:", when="@3.2:+format-nongpl")
        depends_on("py-jsonpointer@1.14:", when="@3.0.0-alpha4:+format")
        depends_on("py-pkgutil-resolve-name@1.3:", when="@4.9: ^python@:3.8")
        depends_on("py-pyrsistent@0.14:0.16,0.17.3:", when="@4.0.0-alpha3:4.17")
        depends_on("py-pyrsistent@0.14:", when="@3.0.0-alpha4:4.0.0-alpha2")
        depends_on("py-rfc3339-validator", when="@4.0.0-alpha6:+format")
        depends_on("py-rfc3339-validator", when="@3.2:+format-nongpl")
        depends_on("py-rfc3986-validator@0.1.1:", when="@3.2:+format-nongpl")
        depends_on("py-rfc3987", when="@2.5,3.0.0-alpha4:+format")
        depends_on("py-setuptools", when="@3.0.0-alpha4:3")
        depends_on("py-six@1.11:", when="@3.0.0-alpha4:3")
        depends_on("py-strict-rfc3339", when="@2.5,3.0.0-alpha4:4.0.0-alpha5+format")
        depends_on("py-uri-template", when="@4.0.0-alpha2:+format-nongpl")
        depends_on("py-uri-template", when="@4.0.0-alpha2:+format")
        depends_on("py-webcolors@1.11:", when="@4.0.0-alpha6:+format-nongpl")
        depends_on("py-webcolors@1.11:", when="@4.0.0-alpha6:+format")
        depends_on("py-webcolors", when="@3.2:4.0.0-alpha5+format-nongpl")
        depends_on("py-webcolors", when="@2.5,3.0.0-alpha4:4.0.0-alpha5+format")

    conflicts("^py-pyrsistent@0.17.0:0.17.2")
