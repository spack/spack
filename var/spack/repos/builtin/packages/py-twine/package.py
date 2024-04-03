# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTwine(PythonPackage):
    """Twine is a utility for publishing Python packages on PyPI."""

    homepage = "https://twine.readthedocs.io/"
    pypi = "twine/twine-2.0.0.tar.gz"
    git = "https://github.com/pypa/twine.git"

    version(
        "4.0.2",
        sha256="929bc3c280033347a00f847236564d1c52a3e61b1ac2516c97c48f3ceab756d8",
        url="https://pypi.org/packages/3a/38/a3f27a9e8ce45523d7d1e28c09e9085b61a98dab15d35ec086f36a44b37c/twine-4.0.2-py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="42026c18e394eac3e06693ee52010baa5313e4811d5a11050e7d48436cf41b9e",
        url="https://pypi.org/packages/38/ab/5adc82687fea5cc0414a2bb6a871ef269f8c80e808d279ee5be6fa9ad911/twine-4.0.1-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="5319dd3e02ac73fcddcd94f035b9631589ab5d23e1f4699d57365199d85261e1",
        url="https://pypi.org/packages/c4/43/b9c56d378f5d0b9bee7be564b5c5fb65c65e5da6e82a97b6f50c2769249a/twine-2.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4")
        depends_on("py-importlib-metadata@3.6:", when="@3.4:")
        depends_on("py-keyring@15.1:", when="@3:")
        depends_on("py-pkginfo@1.8.1:", when="@3.7:")
        depends_on("py-pkginfo@1.4.2:", when="@1.11:3.6")
        depends_on("py-readme-renderer@35:", when="@4.0.1:")
        depends_on("py-readme-renderer@21:", when="@1.12:4.0.0")
        depends_on("py-requests@2.20:", when="@2:")
        depends_on("py-requests-toolbelt@0.8,0.9.1:", when="@1.13:")
        depends_on("py-rfc3986@1.4:", when="@3.2:")
        depends_on("py-rich@12.0.0:", when="@4:")
        depends_on("py-setuptools@0.7:", when="@:3.3")
        depends_on("py-tqdm@4.14:", when="@1.10:3")
        depends_on("py-urllib3@1.26:", when="@3.8:")

    # Historical Dependencies
