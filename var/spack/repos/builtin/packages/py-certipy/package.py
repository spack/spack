# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCertipy(PythonPackage):
    """A simple python tool for creating certificate authorities
    and certificates on the fly."""

    pypi = "certipy/certipy-0.1.3.tar.gz"

    version(
        "0.1.3",
        sha256="f272c13bfa9af6b2f3f746329d08adb66af7dd0bbb08fc81175597f25a7284b5",
        url="https://pypi.org/packages/4e/c4/02194a623c03547306c5edfb6b1c0fadaa35ad7fdc2a93b2c1e5e86afc51/certipy-0.1.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyopenssl")
