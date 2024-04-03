# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySuperqt(PythonPackage):
    """Missing widgets and components for PyQt/PySide"""

    homepage = "https://pyapp-kit.github.io/superqt/"
    pypi = "superqt/superqt-0.6.1.tar.gz"

    license("BSD-3-Clause", checked_by="A-N-Other")

    version(
        "0.6.1",
        sha256="93c063b77581f9b0883b6198a6365d5cdacb5e4953fb2f7b0466d741c3bbfd30",
        url="https://pypi.org/packages/9e/25/f24abb44959276070c737bd45d2a2948b814360629a83a93d291dc42baf3/superqt-0.6.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.5.1:")
        depends_on("py-packaging", when="@0.5:0.6.1")
        depends_on("py-pygments@2.4:", when="@0.5:")
        depends_on("py-qtpy@1.1:", when="@0.5:")
        depends_on("py-typing-extensions@3.7.4.3:3.7,3.10.0.1:", when="@0.5.1:")

    conflicts("^py-typing-extensions@3.10.0.0")
