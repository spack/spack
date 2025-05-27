# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyId(PythonPackage):
    """id is a Python tool for generating OIDC identities."""

    homepage = "https://pypi.org/project/id/"
    pypi = "id/id-1.5.0.tar.gz"

    license("Apache-2.0", checked_by="RobertMaaskant")

    version("1.5.0", sha256="292cb8a49eacbbdbce97244f47a97b4c62540169c976552e497fd57df0734c1d")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
