# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfTransformSchemas(PythonPackage):
    """ASDF schemas for transforms"""

    homepage = "asdf-transform-schemas.readthedocs.io"
    pypi = "asdf_transform_schemas/asdf_transform_schemas-0.3.0.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version(
        "0.3.0",
        sha256="b0dbcae1bd15afea52d67209d8a75533c0ad3713e7e0eb55d968ff70393cc7fc",
        url="https://pypi.org/packages/2a/f2/b184f660552be16a3bd00b5c70eeb3abff9d154ccfbb1c868482a9559de0/asdf_transform_schemas-0.3.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.3:0.4")
        depends_on("py-asdf-standard@1.0.1:", when="@0.2.1:0.4")
        depends_on("py-importlib-resources@3:", when="@0.2.1:0.4 ^python@:3.8")
