# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParameterized(PythonPackage):
    """Parameterized testing with any Python test framework."""

    homepage = "https://github.com/wolever/parameterized"
    pypi = "parameterized/parameterized-0.7.1.tar.gz"

    version(
        "0.7.1",
        sha256="ea0326ba5bbbe7c427329a27b75003410df07d1173ca254976f8f5a64922c322",
        url="https://pypi.org/packages/a3/bf/6ef8239028beae8298e0806b4f79c2466b1b16ca5b85dc13d631c5ea92c4/parameterized-0.7.1-py2.py3-none-any.whl",
    )
