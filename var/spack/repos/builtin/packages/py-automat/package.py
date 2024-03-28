# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutomat(PythonPackage):
    """Self-service finite-state machines for the programmer on the go."""

    homepage = "https://github.com/glyph/Automat"
    pypi = "Automat/Automat-20.2.0.tar.gz"

    license("MIT")

    version(
        "20.2.0",
        sha256="b6feb6455337df834f6c9962d6ccf771515b7d939bca142b29c20c2376bc6111",
        url="https://pypi.org/packages/dd/83/5f6f3c1a562674d65efc320257bdc0873ec53147835aeef7762fe7585273/Automat-20.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-attrs@19.2:", when="@20:")
        depends_on("py-six")
