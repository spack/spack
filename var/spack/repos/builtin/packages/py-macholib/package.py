# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMacholib(PythonPackage):
    """Python package for Mach-O header analysis and editing"""

    pypi = "macholib/macholib-1.11.tar.gz"

    license("MIT")

    version(
        "1.16",
        sha256="5a0742b587e6e57bfade1ab90651d4877185bf66fd4a176a488116de36878229",
        url="https://pypi.org/packages/dc/02/0d0f2010c17918055a253ba00653b88b4c3af2ec960004fe35c2aaf36f8e/macholib-1.16-py2.py3-none-any.whl",
    )
    version(
        "1.11",
        sha256="ac02d29898cf66f27510d8f39e9112ae00590adb4a48ec57b25028d6962b1ae1",
        url="https://pypi.org/packages/41/f1/6d23e1c79d68e41eb592338d90a33af813f98f2b04458aaf0b86908da2d8/macholib-1.11-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-altgraph@0.15:", when="@1.9:1.16.0")
