# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3986(PythonPackage):
    """A Python implementation of RFC 3986 including
    validation and authority parsing."""

    homepage = "https://rfc3986.readthedocs.io/"
    pypi = "rfc3986/rfc3986-1.4.0.tar.gz"
    git = "https://github.com/python-hyper/rfc3986.git"

    license("Apache-2.0")

    version(
        "2.0.0",
        sha256="50b1502b60e289cb37883f3dfd34532b8873c7de9f49bb546641ce9cbd256ebd",
        url="https://pypi.org/packages/ff/9a/9afaade874b2fa6c752c36f1548f718b5b83af81ed9b76628329dab81c1b/rfc3986-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="af9147e9aceda37c91a05f4deb128d4b4b49d6b199775fd2d2927768abdc8f50",
        url="https://pypi.org/packages/78/be/7b8b99fd74ff5684225f50dd0e865393d2265656ef3b4ba9eaaaffe622b8/rfc3986-1.4.0-py2.py3-none-any.whl",
    )

    variant("idna2008", default=False, description="Enable idna2008 Functionality")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2:")
        depends_on("py-idna", when="@1.3:+idna2008")
