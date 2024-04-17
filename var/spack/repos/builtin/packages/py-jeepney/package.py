# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJeepney(PythonPackage):
    """Low-level, pure Python DBus protocol wrapper."""

    homepage = "https://gitlab.com/takluyver/jeepney"
    pypi = "jeepney/jeepney-0.4.3.tar.gz"

    license("MIT")

    version(
        "0.8.0",
        sha256="c0a454ad016ca575060802ee4d590dd912e35c122fa04e70306de3d076cce755",
        url="https://pypi.org/packages/ae/72/2a1e2290f1ab1e06f71f3d0f1646c9e4634e70e1d37491535e19266e8dc9/jeepney-0.8.0-py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="1b5a0ea5c0e7b166b2f5895b91a08c14de8915afda4407fb5022a195224958ac",
        url="https://pypi.org/packages/14/b8/bb3e34d71472140f9bfdf5d77cd063e2cc964b72b1bb0b70fe3c1e7db932/jeepney-0.7.1-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="aec56c0eb1691a841795111e184e13cad504f7703b9a64f63020816afa79a8ae",
        url="https://pypi.org/packages/51/b0/a6ea72741aaac3f37fb96d195e4ee576a103c4c04e279bc6b446a70960e1/jeepney-0.6.0-py3-none-any.whl",
    )
    version(
        "0.4.3",
        sha256="d6c6b49683446d2407d2fe3acb7a368a77ff063f9182fe427da15d622adc24cf",
        url="https://pypi.org/packages/79/31/2e8d42727595faf224c6dbb748c32b192e212f25495fe841fb7ce8e168b8/jeepney-0.4.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.8:")
