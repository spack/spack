# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMutagen(PythonPackage):
    """Read and write audio tags for many formats."""

    homepage = "https://github.com/quodlibet/mutagen"
    pypi = "mutagen/mutagen-1.45.1.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "1.45.1",
        sha256="9c9f243fcec7f410f138cb12c21c84c64fde4195481a30c9bfb05b5f003adfed",
        url="https://pypi.org/packages/16/b3/f7aa8edf2ff4495116f95fd442b2a346aa55d1d46313143c8814886dbcdb/mutagen-1.45.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@1.43:1.45")
