# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyHumanfriendly(PythonPackage):
    """Human friendly output for text interfaces using Python"""

    homepage = "https://humanfriendly.readthedocs.io/"
    pypi = "humanfriendly/humanfriendly-8.1.tar.gz"
    git = "https://github.com/xolox/python-humanfriendly.git"

    license("MIT")

    version(
        "10.0",
        sha256="1697e1a8a8f550fd43c2865cd84542fc175a61dcb779b6fee18cf6b6ccba1477",
        url="https://pypi.org/packages/f0/0f/310fb31e39e2d734ccaa2c0fb981ee41f7bd5056ce9bc29b2248bd569169/humanfriendly-10.0-py2.py3-none-any.whl",
    )
    version(
        "8.2",
        sha256="e78960b31198511f45fd455534ae7645a6207d33e512d2e842c766d15d9c8080",
        url="https://pypi.org/packages/8e/2d/2f1b0a780b8c948c06c74c8c80e68ac354da52397ba432a1c5ac1923c3af/humanfriendly-8.2-py2.py3-none-any.whl",
    )
    version(
        "8.1",
        sha256="3a831920e40e55ad49adb64c9179ed50c604cabca72cd300e7bd5b51310e4ebb",
        url="https://pypi.org/packages/9d/25/417cfcd511782bc678c1285a365271bdbe9ec895fa69a4c7a294ae9586f5/humanfriendly-8.1-py2.py3-none-any.whl",
    )
    version(
        "4.18",
        sha256="23057b10ad6f782e7bc3a20e3cb6768ab919f619bbdc0dd75691121bbde5591d",
        url="https://pypi.org/packages/90/df/88bff450f333114680698dc4aac7506ff7cab164b794461906de31998665/humanfriendly-4.18-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyreadline", when="@4.4.2:9 platform=windows")
        depends_on("py-pyreadline3", when="@10: platform=windows")
