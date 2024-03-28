# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpbin(PythonPackage):
    """HTTP Request and Response Service"""

    homepage = "https://github.com/Runscope/httpbin"
    pypi = "httpbin/httpbin-0.7.0.tar.gz"

    license("0BSD")

    version(
        "0.7.0",
        sha256="7a04b5904c80b7aa04dd0a6af6520d68ce17a5db175e66a64b971f8e93d73a26",
        url="https://pypi.org/packages/ff/dd/c988f90445763b0a09668209756fa89bbdc8590a8ade902f7dc69c36b26f/httpbin-0.7.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="710069973216d4bbf9ab6757f1e9a1f3be05832ce77da023adce0a98dfeecfee",
        url="https://pypi.org/packages/55/0a/387c7e8dca03cd40a0048cd20c096c1204cb4c63eafb6e21bf00dbfbe8a6/httpbin-0.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-brotlipy", when="@0.6:0.6.0,0.6.2:0.7")
        depends_on("py-decorator", when="@0.4.1:0.6.0,0.6.2:")
        depends_on("py-flask", when="@0.4.1:0.6.0,0.6.2:0.10.1")
        depends_on("py-itsdangerous", when="@0.4.1:0.6.0,0.6.2:0.10.0")
        depends_on("py-markupsafe", when="@0.4.1:0.6.0,0.6.2:0.10.0")
        depends_on("py-raven+flask", when="@0.6:0.6.0,0.6.2:0.7")
        depends_on("py-six", when="@0.4.1:0.6.0,0.6.2:0.7,0.10.1:")
        depends_on("py-werkzeug@0.14.1:", when="@0.7,0.10.1")
