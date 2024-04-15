# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPymdownExtensions(PythonPackage):
    """Extensions for Python Markdown."""

    homepage = "https://github.com/facelessuser/pymdown-extensions"
    pypi = "pymdown_extensions/pymdown_extensions-9.5.tar.gz"

    license("MIT")

    version(
        "9.5",
        sha256="ec141c0f4983755349f0c8710416348d1a13753976c028186ed14f190c8061c4",
        url="https://pypi.org/packages/f1/e0/1ed09f66cd1648f8e009120debf9b7d67596fb688e53e71522da1daa02a0/pymdown_extensions-9.5-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@9.2:10.2")
        depends_on("py-markdown@3.2:", when="@:10.4")
