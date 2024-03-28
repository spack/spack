# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBleach(PythonPackage):
    """An easy whitelist-based HTML-sanitizing tool."""

    homepage = "https://github.com/mozilla/bleach"
    pypi = "bleach/bleach-3.1.0.tar.gz"

    license("Apache-2.0")

    version(
        "6.0.0",
        sha256="33c16e3353dbd13028ab4799a0f89a83f113405c766e9c122df8a06f5b85b3f4",
        url="https://pypi.org/packages/ac/e2/dfcab68c9b2e7800c8f06b85c76e5f978d05b195a958daa9b1dda54a1db6/bleach-6.0.0-py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="085f7f33c15bd408dd9b17a4ad77c577db66d76203e5984b1bd59baeee948b2a",
        url="https://pypi.org/packages/d4/87/508104336a2bc0c4cfdbdceedc0f44dc72da3abc0460c57e323ddd1b3257/bleach-5.0.1-py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="4d2651ab93271d1129ac9cbc679f524565cc8a1b791909c4a51eac4446a15994",
        url="https://pypi.org/packages/64/cc/74d634e1e5659742973a23bb441404c53a7bedb6cd3962109ca5efb703e8/bleach-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="c1685a132e6a9a38bf93752e5faab33a9517a6c0bb2f37b785e47bf253bdb51d",
        url="https://pypi.org/packages/b6/23/d06c0bddcef0df58dd2c9ac02f8639533a6671bed0ef3e236888bb3b0a3c/bleach-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.1",
        sha256="ae976d7174bba988c0b632def82fdc94235756edfb14e6558a9c5be555c9fb78",
        url="https://pypi.org/packages/c3/ae/9b9f28245f4570bbdd977dc73e024fbb19f781036734fa0502039bfc41b6/bleach-3.3.1-py2.py3-none-any.whl",
    )
    version(
        "3.1.0",
        sha256="213336e49e102af26d9cde77dd2d0397afabc5a6bf2fed985dc35b5d1e285a16",
        url="https://pypi.org/packages/ab/05/27e1466475e816d3001efb6e0a85a819be17411420494a1e602c36f8299d/bleach-3.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="e67f46adcec78dbc3c04462f3aba3213a673d5652eba2609ed1ef15492a44b8d",
        url="https://pypi.org/packages/33/70/86c5fec937ea4964184d4d6c4f0b9551564f821e1c3575907639036d9b90/bleach-1.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-html5lib@0.999,0.999999:0.9999999", when="@1.5:1")
        depends_on("py-packaging", when="@3.1.5:4")
        depends_on("py-six@1.9:", when="@3.1:3.1.0,3.1.2:")
        depends_on("py-six", when="@1.4.3:3.0")
        depends_on("py-webencodings", when="@3:3.1.0,3.1.2:")
