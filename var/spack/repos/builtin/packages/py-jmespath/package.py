# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJmespath(PythonPackage):
    """JSON Matching Expressions."""

    homepage = "https://github.com/jmespath/jmespath.py"
    pypi = "jmespath/jmespath-0.9.4.tar.gz"

    license("MIT")

    version(
        "1.0.1",
        sha256="02e2e4cc71b5bcab88332eebf907519190dd9e6e82107fa7f83b1003a6252980",
        url="https://pypi.org/packages/31/b4/b9b800c45527aadd64d5b442f9b932b00648617eb5d63d2c7a6587b7cafc/jmespath-1.0.1-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="cdf6525904cc597730141d61b36f2e4b8ecc257c420fa2f4549bac2c2d0cb72f",
        url="https://pypi.org/packages/07/cb/5f001272b6faeb23c1c9e0acc04d48eaaf5c862c17709d20e3469c6e0139/jmespath-0.10.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.4",
        sha256="3720a4b1bd659dd2eecad0666459b9788813e032b83e7ba58578e48254e0a0e6",
        url="https://pypi.org/packages/83/94/7179c3832a6d45b266ddb2aac329e101367fbdb11f425f13771d27f225bb/jmespath-0.9.4-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1:")
