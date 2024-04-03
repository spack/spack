# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPalettable(PythonPackage):
    """Color palettes for Python."""

    homepage = "https://jiffyclub.github.io/palettable/"
    pypi = "palettable/palettable-3.0.0.tar.gz"

    license("MIT")

    version(
        "3.3.3",
        sha256="74e9e7d7fe5a9be065e02397558ed1777b2df0b793a6f4ce1a5ee74f74fb0caa",
        url="https://pypi.org/packages/cf/f7/3367feadd4ab56783b0971c9b7edfbdd68e0c70ce877949a5dd2117ed4a0/palettable-3.3.3-py2.py3-none-any.whl",
    )
    version(
        "3.3.0",
        sha256="c3bf3f548fc228e86bd3d16928bbf8d621c1d1098791ceab446d0e3a5e1298d1",
        url="https://pypi.org/packages/ca/46/5198aa24e61bb7eef28d06cb69e56bfa1942f4b6807d95a0b5ce361fe09b/palettable-3.3.0-py2.py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="78f050b711f841941360ac6d129ff4489ad15af169e77f0ea2bde8fcafde7a3f",
        url="https://pypi.org/packages/13/6c/99929b2e733125f8005e4f7e4b73851c54d5b099ca87fa5777948feb7417/palettable-3.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3.3.3:")
