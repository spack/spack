# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloUtils(PythonPackage):
    """
    The oslo.utils library provides support for common utility type functions,
    such as encoding, exception handling, string manipulation, and time
    handling.
    """

    homepage = "https://docs.openstack.org/oslo.utils/"
    pypi = "oslo.utils/oslo.utils-4.9.2.tar.gz"

    maintainers("haampie")

    version(
        "4.9.2",
        sha256="ff38bc69bbed11103ceb5d06ac47454fe439ee9351ed2640d47c1b2cc71b2ea5",
        url="https://pypi.org/packages/0e/28/2acc0e9726c8eff4c9539d3dbf3cb4845e9eb5bc99f26002510e13d7f6f8/oslo.utils-4.9.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-debtcollector@1.2:", when="@3.5:")
        depends_on("py-iso8601@0.1.11:", when="@3.10:")
        depends_on("py-netaddr@0.7.18:", when="@3.30:")
        depends_on("py-netifaces@0.10.4:", when="@1.1.1:1.4.0,1.4.2:3.0,3.2:")
        depends_on("py-oslo-i18n@3.15.3:", when="@3.30:")
        depends_on("py-packaging@20.4:", when="@4.3:")
        depends_on("py-pbr@2:2.0,3:", when="@3.25.1:5")
        depends_on("py-pyparsing@2.1:", when="@3.22.1:")
        depends_on("py-pytz@2013.6:", when="@7.1: ^python@:3.8")
        depends_on("py-pytz@2013.6:", when="@1.6:7.0")
