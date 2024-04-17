# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonJose(PythonPackage):
    """JOSE implementation in Python"""

    homepage = "http://github.com/mpdavis/python-jose"
    pypi = "python-jose/python-jose-3.3.0.tar.gz"

    license("MIT")

    version(
        "3.3.0",
        sha256="9b1376b023f8b298536eedd47ae1089bcdb848f1535ab30555cd92002d78923a",
        url="https://pypi.org/packages/bd/2d/e94b2f7bab6773c70efc70a61d66e312e1febccd9e0db6b9e0adf58cbad1/python_jose-3.3.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-ecdsa@:0.14,0.16:", when="@3.3:")
        depends_on("py-pyasn1", when="@3.2:")
        depends_on("py-rsa", when="@3.2:")
