# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloConfig(PythonPackage):
    """
    The Oslo configuration API supports parsing command line arguments and .ini
    style configuration files.
    """

    homepage = "https://docs.openstack.org/oslo.config/"
    pypi = "oslo.config/oslo.config-8.7.1.tar.gz"

    maintainers("haampie")

    version(
        "8.7.1",
        sha256="3c5cc681ef106a4573d677510f907ab48f40004dc3aac2298d9a517559491efb",
        url="https://pypi.org/packages/35/3a/62f4f3e724151d78b97608b8c72a285decdaa91ac2073946381ef042ebb1/oslo.config-8.7.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-debtcollector@1.2:")
        depends_on("py-importlib-metadata@1.7:", when="@:9.2 ^python@:3.7")
        depends_on("py-netaddr@0.7.18:")
        depends_on("py-oslo-i18n@3.15.3:")
        depends_on("py-pyyaml@5.1:", when="@8.5:")
        depends_on("py-requests@2.18:")
        depends_on("py-rfc3986@1.2:")
        depends_on("py-stevedore@1.20:")
