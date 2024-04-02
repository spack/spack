# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygithub(PythonPackage):
    """Typed interactions with the GitHub API v3"""

    homepage = "https://pygithub.readthedocs.io/"
    pypi = "PyGithub/PyGithub-1.54.1.tar.gz"

    license("LGPL-3.0-only")

    version(
        "2.1.1",
        sha256="4b528d5d6f35e991ea5fd3f942f58748f24938805cb7fcf24486546637917337",
        url="https://pypi.org/packages/be/04/810d131be173cba445d3658a45512b2b2b3d0960d52c4a300d6ec5e00f52/PyGithub-2.1.1-py3-none-any.whl",
    )
    version(
        "1.59.1",
        sha256="3d87a822e6c868142f0c2c4bf16cce4696b5a7a4d142a7bd160e1bdf75bc54a9",
        url="https://pypi.org/packages/2c/71/aff5465d9e3d448a5d4beab1dc7c8dec72037e3ae7e0d856ee08538dc934/PyGithub-1.59.1-py3-none-any.whl",
    )
    version(
        "1.55",
        sha256="2caf0054ea079b71e539741ae56c5a95e073b81fa472ce222e81667381b9601b",
        url="https://pypi.org/packages/c1/1f/9dc4ba315eeea222473cf4c15d3e665f32d52f859d9d6e73219d0a408969/PyGithub-1.55-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.57:")
        depends_on("py-deprecated", when="@1.46:")
        depends_on("py-pyjwt@2.4:+crypto", when="@1.58.1:")
        depends_on("py-pyjwt@2.0.0:", when="@1.55:1.56")
        depends_on("py-pynacl@1.4:", when="@1.55:")
        depends_on("py-python-dateutil", when="@2:2.1")
        depends_on("py-requests@2.14:", when="@1.46:1.53,1.54.1:")
        depends_on("py-typing-extensions@4:", when="@2.1:")
        depends_on("py-urllib3@1.26:", when="@2.1.1:")
