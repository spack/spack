# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEarthengineApi(PythonPackage):
    """This package allows developers to interact with Google Earth Engine
    using the Python programming language."""

    homepage = "https://github.com/google/earthengine-api"
    pypi = "earthengine-api/earthengine-api-0.1.186.tar.gz"

    version("0.1.344", sha256="bc5a270b8296aaae8574e68dfd93fe878bc5fbe77d1c41f90bcb5e5b830ca5c8")
    version("0.1.186", sha256="ced86dc969f5db13eea91944e29c39146bacbb7026a46f4b4ac349b365979627")

    depends_on("py-setuptools", type="build")
    depends_on("py-google-cloud-storage", when="@0.1.344:", type=("build", "run"))
    depends_on("py-google-api-python-client@1.12.1:", when="@0.1.344:", type=("build", "run"))
    depends_on("py-google-api-python-client", type=("build", "run"))
    depends_on("py-google-auth@1.4.1:", type=("build", "run"))
    depends_on("py-google-auth-httplib2@0.0.3:", type=("build", "run"))
    depends_on("py-httplib2@0.9.2:0", type=("build", "run"))
    depends_on("py-requests", when="@0.1.344:", type=("build", "run"))
    depends_on("py-six", when="@:0.1.186", type=("build", "run"))
