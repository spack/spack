# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenapiSchemaPydantic(PythonPackage):
    """OpenAPI (v3) specification schema as pydantic class"""

    homepage = "https://github.com/kuimono/openapi-schema-pydantic"
    pypi = "openapi-schema-pydantic/openapi-schema-pydantic-1.2.4.tar.gz"

    license("MIT")

    version(
        "1.2.4",
        sha256="a932ecc5dcbb308950282088956e94dea069c9823c84e507d64f6b622222098c",
        url="https://pypi.org/packages/a8/e7/22abb5a10733bf8142984201aedf27d4a58f5810ebdfe9679f9876c7bf4d/openapi_schema_pydantic-1.2.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pydantic@1.8.2:", when="@1.2.1:")
