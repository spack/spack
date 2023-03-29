# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestJsonReport(PythonPackage):
    """A pytest plugin to create test reports as JSON"""

    homepage = "https://github.com/numirias/pytest-json-report"
    pypi = "pytest-json-report/pytest-json-report-1.5.0.tar.gz"

    maintainers("angus-g")

    version("1.5.0", sha256="2dde3c647851a19b5f3700729e8310a6e66efb2077d674f27ddea3d34dc615de")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@3.8:", type=("build", "run"))
    depends_on("py-pytest-metadata", type=("build", "run"))
