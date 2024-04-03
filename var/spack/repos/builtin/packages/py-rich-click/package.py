# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRichClick(PythonPackage):
    """The intention of rich-click is to provide attractive help output
    from click, formatted with rich, with minimal customisation required."""

    homepage = "https://github.com/ewels/rich-click"
    pypi = "rich-click/rich-click-1.5.2.tar.gz"

    license("MIT")

    version(
        "1.5.2",
        sha256="131a94bed597eab9f1eda7eb41fb7275b6b60ae9e6defc3769277b70b104285d",
        url="https://pypi.org/packages/6b/7f/b60be5d08e0dd119a05884e55ab26a2b14c2a0bb696e4bbb05c2bb1436d1/rich_click-1.5.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.3:")
        depends_on("py-click@7:")
        depends_on("py-importlib-metadata", when="@1.2: ^python@:3.7")
        depends_on("py-rich@10.7:", when="@1.3.1:")
