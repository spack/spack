# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReadmeRenderer(PythonPackage):
    """readme_renderer is a library for rendering "readme" descriptions
    for Warehouse."""

    homepage = "https://github.com/pypa/readme_renderer"
    pypi = "readme_renderer/readme_renderer-24.0.tar.gz"

    version(
        "37.3",
        sha256="f67a16caedfa71eef48a31b39708637a6f4664c4394801a7b0d6432d13907343",
        url="https://pypi.org/packages/97/52/fd8a77d6f0a9ddeb26ed8fb334e01ac546106bf0c5b8e40dc826c5bd160f/readme_renderer-37.3-py3-none-any.whl",
    )
    version(
        "24.0",
        sha256="c8532b79afc0375a85f10433eca157d6b50f7d6990f337fa498c96cd4bfc203d",
        url="https://pypi.org/packages/c3/7e/d1aae793900f36b097cbfcc5e70eef82b5b56423a6c52a36dce51fedd8f0/readme_renderer-24.0-py2.py3-none-any.whl",
    )
    version(
        "16.0",
        sha256="7f807259fc9b2ababfc1335d106fbc90254cf940f4b4e40d94aebd5a39fcab5d",
        url="https://pypi.org/packages/d2/c0/f16aa42d72aac3ca90aa3b4d0f80e30161b01b2873324a30772c26d43556/readme_renderer-16.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@35:37")
        depends_on("py-bleach@2.1:", when="@17.3:41")
        depends_on("py-bleach", when="@:16")
        depends_on("py-docutils@0.13:", when="@16:")
        depends_on("py-pygments@2.5:", when="@25:")
        depends_on("py-pygments", when="@:24")
        depends_on("py-six", when="@:29")
