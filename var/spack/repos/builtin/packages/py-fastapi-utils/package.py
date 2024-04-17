# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastapiUtils(PythonPackage):
    """Reusable utilities for FastAPI"""

    homepage = "https://fastapi-utils.davidmontague.xyz"
    pypi = "fastapi-utils/fastapi-utils-0.2.1.tar.gz"

    license("MIT")

    version(
        "0.2.1",
        sha256="dd0be7dc7f03fa681b25487a206651d99f2330d5a567fb8ab6cb5f8a06a29360",
        url="https://pypi.org/packages/72/b8/9353a1b6b3adc5e6ede398eea2095968ac334883266dbd5bf55e99958b0a/fastapi_utils-0.2.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3")
        depends_on("py-fastapi")
        depends_on("py-pydantic@1.0:1")
        depends_on("py-sqlalchemy@1.3.12:1")
