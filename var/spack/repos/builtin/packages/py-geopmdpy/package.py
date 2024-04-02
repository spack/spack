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

    version(
        "3.0.1",
        sha256="ebdfa9b77fa92d3f411bfb1c94938039738d453b2441029b8ce44852115a8f73",
        url="https://pypi.org/packages/6f/80/aaef19f83ff6aa4fb80e418b131a77161d988e63983db73ab920f9ef8710/geopmdpy-3.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cffi@1.14.5:", when="@3:")
        depends_on("py-dasbus@1.6:")
        depends_on("py-jsonschema@3.2:")
        depends_on("py-psutil@5.8:", when="@3:")
        depends_on("py-setuptools@53:", when="@3:")

    build_directory = "service"
