# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinkifyItPy(PythonPackage):
    """Links recognition library with FULL unicode support."""

    homepage = "https://github.com/tsutsu3/linkify-it-py"
    pypi = "linkify-it-py/linkify-it-py-2.0.2.tar.gz"

    license("MIT")

    version(
        "2.0.2",
        sha256="a3a24428f6c96f27370d7fe61d2ac0be09017be5190d68d8658233171f1b6541",
        url="https://pypi.org/packages/1f/1a/16b0d2f66601ba3081f1d4177087c79fd1f11d17706ee01d373e4ba8e00d/linkify_it_py-2.0.2-py3-none-any.whl",
    )
    version(
        "1.0.3",
        sha256="11e29f00150cddaa8f434153f103c14716e7e097a8fd372d9eb1ed06ed91524d",
        url="https://pypi.org/packages/ff/f1/74e54ab5ae6aa1d3b6dc5de56fecf57fe4873d8f6b2a72a1269dbedd111b/linkify_it_py-1.0.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.0.1:")
        depends_on("py-uc-micro-py")
