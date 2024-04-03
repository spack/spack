# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFiletype(PythonPackage):
    """Small and dependency free Python package to infer file type and MIME
    type checking the magic numbers signature of a file or buffer.
    """

    homepage = "https://github.com/h2non/filetype.py"
    pypi = "filetype/filetype-1.2.0.tar.gz"

    license("MIT")

    version(
        "1.2.0",
        sha256="7ce71b6880181241cf7ac8697a2f1eb6a8bd9b429f7ad6d27b8db9ba5f1c2d25",
        url="https://pypi.org/packages/18/79/1b8fa1bb3568781e84c9200f951c735f3f157429f44be0495da55894d620/filetype-1.2.0-py2.py3-none-any.whl",
    )
