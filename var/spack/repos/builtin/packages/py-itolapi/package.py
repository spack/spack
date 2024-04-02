# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyItolapi(PythonPackage):
    """API for interacting with itol.embl.de"""

    homepage = "https://github.com/albertyw/itolapi"
    pypi = "itolapi/itolapi-4.1.2.tar.gz"

    maintainers("snehring")

    license("MIT")

    version(
        "4.1.2",
        sha256="5eb44a21ef2db4fdb890a1e2ec6b29b0a5f6b2a253872e5032915ca88823d8c0",
        url="https://pypi.org/packages/b4/ec/e67083cb4c6ac58763ff8eb0f4128de7cf8d6a9d082c4e686e7b8a0595f6/itolapi-4.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests@2:", when="@:3.0.1,3.0.3:")
