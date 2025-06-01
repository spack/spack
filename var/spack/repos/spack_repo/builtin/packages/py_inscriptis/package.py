# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyInscriptis(PythonPackage):
    """A python based HTML to text conversion library, command line client and Web service."""

    homepage = "https://github.com/weblyzard/inscriptis"
    pypi = "inscriptis/inscriptis-2.6.0.tar.gz"

    maintainers("thomas-bouvier")

    version("2.6.0", sha256="6f164bf45ea6972d61fd048a8e074d5125d215eaa837f8e70c158c97c31c3181")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-poetry-core", type="build")
    depends_on("py-requests@2.32.2:", type=("build", "run"))
    depends_on("py-lxml@4.9.3:", type=("build", "run"))
    depends_on("py-fastapi@0.115.11:", type=("build", "run"))
    depends_on("py-uvicorn@0.34.0:", type=("build", "run"))

    # Development dependencies
    depends_on("py-pytest@8.3.5:", type="test")
