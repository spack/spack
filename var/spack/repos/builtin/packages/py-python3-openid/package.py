# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPython3Openid(PythonPackage):
    """OpenID support for modern servers and consumers."""

    homepage = "https://github.com/necaris/python3-openid"
    pypi = "python3-openid/python3-openid-3.2.0.tar.gz"

    license("Apache-2.0")

    version(
        "3.2.0",
        sha256="6626f771e0417486701e0b4daff762e7212e820ca5b29fcc0d05f6f8736dfa6b",
        url="https://pypi.org/packages/e0/a5/c6ba13860bdf5525f1ab01e01cc667578d6f1efc8a1dba355700fb04c29b/python3_openid-3.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-defusedxml", when="@3.1:")
