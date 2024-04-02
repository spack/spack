# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestRemotedata(PythonPackage):
    """Pytest plugin for controlling remote data access."""

    homepage = "https://github.com/astropy/pytest-remotedata"
    pypi = "pytest-remotedata/pytest-remotedata-0.4.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.0",
        sha256="48ebd360d24bc670cfeca43fff62c1866251af9cfe53f2662f225f74b3496357",
        url="https://pypi.org/packages/b3/b3/f08170b2a24a108f555ce517aae70628ce152e195b53d5dfac1dd33d94d2/pytest_remotedata-0.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.4:")
        depends_on("py-packaging", when="@0.3.3:")
        depends_on("py-pytest@4.6:", when="@0.3.3:")
