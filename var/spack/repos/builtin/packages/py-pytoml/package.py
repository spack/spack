# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytoml(PythonPackage):
    """A parser for TOML-0.4.0.

    Deprecated: use py-toml instead."""

    homepage = "https://github.com/avakar/pytoml"
    pypi = "pytoml/pytoml-0.1.21.tar.gz"

    license("MIT")

    version(
        "0.1.21",
        sha256="57a21e6347049f73bfb62011ff34cd72774c031b9828cb628a752225136dfc33",
        url="https://pypi.org/packages/a5/47/c7f8a0f210ad18576840922e0b504f0b7f5f73aea4a52ab14c5b58517edf/pytoml-0.1.21-py2.py3-none-any.whl",
    )
