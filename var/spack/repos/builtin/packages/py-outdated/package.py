# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOutdated(PythonPackage):
    """This is a mini-library which, given a package name and a version, checks if
    it's the latest version available on PyPI."""

    homepage = "http://github.com/alexmojaki/outdated"
    pypi = "outdated/outdated-0.2.2.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "0.2.2",
        sha256="3e9c2ee6d17e86ae8cc7bb71d70c4172690121cda367155a30994742172678c8",
        url="https://pypi.org/packages/d3/04/7d2b9a0d1b81e30f39e6f358bac01f4f18b585f35b0ffc5c83fc274f146b/outdated-0.2.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-littleutils", when="@0.2.1:")
        depends_on("py-requests", when="@0.2.1:")
        depends_on("py-setuptools@44:", when="@0.2.2:")
