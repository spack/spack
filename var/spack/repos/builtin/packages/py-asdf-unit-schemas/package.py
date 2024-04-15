# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfUnitSchemas(PythonPackage):
    """ASDF schemas for units"""

    homepage = "https://asdf-unit-schemas.readthedocs.io"
    pypi = "asdf_unit_schemas/asdf_unit_schemas-0.1.0.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version(
        "0.1.0",
        sha256="0e104b53c23a9e15541cfa5d101613d2724a9124fc56301324512659afb470d5",
        url="https://pypi.org/packages/3e/55/78e900affcb8306cb669e52ee2eac670badef4c8d5938e8dae824ef21932/asdf_unit_schemas-0.1.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:")
        depends_on("py-asdf-standard@1.0.1:", when="@:0.1")
        depends_on("py-importlib-resources@3:", when="@:0.1 ^python@:3.8")
