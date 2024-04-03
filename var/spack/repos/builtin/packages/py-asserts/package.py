# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsserts(PythonPackage):
    """Stand-alone Assertions."""

    homepage = "https://github.com/srittau/python-asserts"
    url = "https://github.com/srittau/python-asserts/archive/v0.10.0.tar.gz"

    license("MIT")

    version(
        "0.10.0",
        sha256="d42de39290badeb1816f09bec2996912718e9b3a379a3415e6731bb0d2b271b2",
        url="https://pypi.org/packages/e2/07/cbb15d287cd9424b55da504124aea3cf59fec6de870dad1f75b7c0f717aa/asserts-0.10.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.1",
        sha256="a33eed1fbddc053a929011025d6e8589c9e1ba0e13de6ae26d1f76c4f807f8d4",
        url="https://pypi.org/packages/00/bf/6b059c76d427ee802c9372467e344245aaedfef1024333dee76c8748c486/asserts-0.9.1-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="aa0685b6652b15f6b42c2be260e0f315eb6a42cf5f08e4b37ab90fb6d429bfb9",
        url="https://pypi.org/packages/6d/bd/9357ffd43a07dffe5bb980eb776ae4276ac5c02ae5c77ceae3dc369d3b09/asserts-0.9.0-py2.py3-none-any.whl",
    )
    version(
        "0.8.6",
        sha256="609078daa69b619a733e812acd4d6d1d559028bed711c8712942fe718d50db57",
        url="https://pypi.org/packages/90/be/d2b1249330b07afcbbfdbe5387d44e8bdeb728fba80e6e0f2bae2c4c657d/asserts-0.8.6-py2.py3-none-any.whl",
    )
