# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParam(PythonPackage):
    """Param is a library providing Parameters: Python attributes extended to have
    features such as type and range checking, dynamically generated values,
    documentation strings, default values, etc., each of which is inherited from
    parent classes if not specified in a subclass."""

    homepage = "https://param.holoviz.org/"
    pypi = "param/param-1.12.0.tar.gz"

    maintainers("haralmha")

    license("BSD-3-Clause")

    version(
        "1.12.0",
        sha256="401929e5b9252c00001d91745c0af1e48d9ca6cda07d2d7b2de9c8fbf2c8e5e7",
        url="https://pypi.org/packages/e4/1b/a65e2e882f264ee7aac3c37a72003950a7d16ac7df40356017a798aebb60/param-1.12.0-py2.py3-none-any.whl",
    )
