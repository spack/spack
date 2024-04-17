# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocs(PythonPackage):
    """MkDocs is a fast, simple and downright gorgeous static site generator
    that's geared towards building project documentation."""

    homepage = "https://www.mkdocs.org/"
    pypi = "mkdocs/mkdocs-1.3.1.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.3.1",
        sha256="fda92466393127d2da830bc6edc3a625a14b436316d1caf347690648e774c4f0",
        url="https://pypi.org/packages/e4/96/6b9d87ee8a11e6d2483e3767999d4aeb8d5478d2059cfb3e21404beae470/mkdocs-1.3.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-click@3.3:", when="@:1.3")
        depends_on("py-ghp-import@1:", when="@1.2:")
        depends_on("py-importlib-metadata@4.3:", when="@1.3")
        depends_on("py-jinja2@2.10.2:", when="@1.3")
        depends_on("py-markdown@3.2.1:3.3", when="@1.3.1:1.4")
        depends_on("py-mergedeep@1.3.4:", when="@1.2:")
        depends_on("py-packaging@20.5:", when="@1.2:")
        depends_on("py-pyyaml", when="@:1.3")
        depends_on("py-pyyaml-env-tag", when="@1.2:")
        depends_on("py-watchdog@2:", when="@1.2:")
