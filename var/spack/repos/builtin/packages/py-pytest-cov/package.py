# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestCov(PythonPackage):
    """Pytest plugin for measuring coverage."""

    homepage = "https://github.com/pytest-dev/pytest-cov"
    pypi = "pytest-cov/pytest-cov-2.8.1.tar.gz"

    license("MIT")

    version(
        "4.0.0",
        sha256="2feb1b751d66a8bd934e5edfa2e961d11309dc37b73b0eabe73b5945fee20f6b",
        url="https://pypi.org/packages/fe/1f/9ec0ddd33bd2b37d6ec50bb39155bca4fe7085fa78b3b434c05459a860e3/pytest_cov-4.0.0-py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="578d5d15ac4a25e5f961c938b85a05b09fdaae9deef3bb6de9a6e766622ca7a6",
        url="https://pypi.org/packages/20/49/b3e0edec68d81846f519c602ac38af9db86e1e71275528b3e814ae236063/pytest_cov-3.0.0-py3-none-any.whl",
    )
    version(
        "2.8.1",
        sha256="cdbdef4f870408ebdbfeb44e63e07eb18bb4619fae852f6e760645fa36172626",
        url="https://pypi.org/packages/b9/54/3673ee8be482f81527678ac894276223b9814bb7262e4f730469bb7bf70e/pytest_cov-2.8.1-py2.py3-none-any.whl",
    )
    version(
        "2.3.1",
        sha256="09f34ed04d5ea1a6dc7e5bc08435eaca9a2b55086c50f5cc0a3229b4001bc5f0",
        url="https://pypi.org/packages/67/94/93dd3288f9a6accfc25e4c636aa912824a2e66d08a464d6f62421da8742f/pytest_cov-2.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-coverage@5.2.1:+toml", when="@2.12:2.12.0,3:")
        depends_on("py-coverage@4.4:", when="@2.6:2.10")
        depends_on("py-coverage@3.7.1:", when="@2.1:2.5")
        depends_on("py-pytest@4.6:", when="@2.10:")
        depends_on("py-pytest@3.6:", when="@2.6.1:2.9")
        depends_on("py-pytest@2.6:", when="@2.1:2.5")
