# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWw(PythonPackage):
    """Wrappers for Python builtins with higher-level APIs."""

    homepage = "https://github.com/tygs/ww/"
    pypi = "ww/ww-0.2.1.tar.gz"

    license("MIT")

    version(
        "0.2.1",
        sha256="02d2b9ea134317901c889fc844958630f478b5d1a98d5938ce787cf92d02b8ed",
        url="https://pypi.org/packages/54/f2/5a43036cb61ce29a49b99a53c7d0fb68a4274467064ff77c5feafca03177/ww-0.2.1-py3-none-any.whl",
    )
