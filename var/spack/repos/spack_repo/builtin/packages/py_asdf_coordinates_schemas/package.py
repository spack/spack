# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfCoordinatesSchemas(PythonPackage):
    """ASDF schemas for coordinates"""

    homepage = "https://www.asdf-format.org/projects/asdf-coordinates-schemas/"
    pypi = "asdf_coordinates_schemas/asdf_coordinates_schemas-0.3.0.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause", checked_by="lgarrison")

    version("0.3.0", sha256="c98b6015dcec87a158fcde7798583f0615d08125fa6e1e9de16c4eb03fcd604e")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-setuptools@60:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    depends_on("py-asdf@2.12.1:", type=("build", "run"))
    depends_on("py-asdf-standard@1.1.0:", type=("build", "run"))
