# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeopmdpy(PythonPackage):
    """The Global Extensible Open Power Manager (GEOPM) Service provides a
    user interface for accessing hardware telemetry and settings securely."""

    homepage = "https://geopm.github.io"
    git = "https://github.com/geopm/geopm.git"
    url = "https://github.com/geopm/geopm/tarball/v3.0.1"

    maintainers("bgeltz", "cmcantalupo")
    license("BSD-3-Clause")
    tags = ["e4s"]

    version("develop", branch="dev")
    version("3.0.1", sha256="32ba1948de58815ee055470dcdea64593d1113a6cad70ce00ab0286c127f8234")

    depends_on("py-dasbus@1.6.0:", type=("build", "run"))
    depends_on("py-cffi@1.14.5:", type="run")
    depends_on("py-psutil@5.8.0:", type="run")
    depends_on("py-jsonschema@3.2.0:", type="run")
    depends_on("py-pyyaml@6.0:", type="run")
    depends_on("py-setuptools@53.0.0:", type="build")

    build_directory = "service"

    @run_before("install")
    def populate_version(self):
        # @develop builds will have a version of 0.0.0
        if not self.spec.version.isdevelop():
            with working_dir(join_path("service", "geopmdpy")):
                with open("version.py", "w") as fd:
                    fd.write(f"__version__ = '{self.spec.version}'")
