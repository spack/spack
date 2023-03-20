# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApiCore(PythonPackage):
    """Google API client core library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    pypi = "google-api-core/google-api-core-1.14.2.tar.gz"

    # 'google.api_core.operations_v1' and 'google.api_core.gapic_v1' require 'grpc'.
    # Leave them out of 'import_modules' to avoid optional dependency.
    import_modules = ["google.api_core", "google.api_core.future"]

    version("2.11.0", sha256="4b9bb5d5a380a0befa0573b302651b8a9a89262c1730e37bf423cec511804c22")
    version("1.14.2", sha256="2c23fbc81c76b941ffb71301bb975ed66a610e9b03f918feacd1ed59cf43a6ec")

    with when("@2:"):
        depends_on("py-setuptools", type=("build", "run"))
        depends_on("py-googleapis-common-protos@1.56.2:1", type=("build", "run"))
        depends_on("py-protobuf@3.19.5:3.19,3.20.2:4.20,4.21.6:4", type=("build", "run"))
        depends_on("py-google-auth@2.14.1:2", type=("build", "run"))
        depends_on("py-requests@2.18:2", type=("build", "run"))

    with when("@:1"):
        depends_on("py-googleapis-common-protos@1.6:1", type=("build", "run"))
        depends_on("py-protobuf@3.4.0:", type=("build", "run"))
        depends_on("py-google-auth@0.4:1", type=("build", "run"))
        depends_on("py-requests@2.18:2", type=("build", "run"))
        depends_on("py-setuptools@34.0.0:", type=("build", "run"))
        depends_on("py-six@1.10.0:", type=("build", "run"))
        depends_on("py-pytz", type=("build", "run"))
