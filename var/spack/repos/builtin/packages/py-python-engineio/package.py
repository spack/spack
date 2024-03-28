# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonEngineio(PythonPackage):
    """Engine.IO is the implementation of transport-based
    cross-browser/cross-device bi-directional communication
    layer for Socket.IO."""

    homepage = "https://python-engineio.readthedocs.io/en/latest/"
    url = "https://github.com/miguelgrinberg/python-engineio/archive/v2.0.2.tar.gz"

    version(
        "2.0.2",
        sha256="ab79f81a193ca1d9d4df213080fd818bb7ff8cd342f3a405e7302bf7fcfe3eae",
        url="https://pypi.org/packages/c3/5a/316c1d956e229a9d5a80db842261922ea95a073d91d1402951c66bad7963/python_engineio-2.0.2-py2.py3-none-any.whl",
    )
