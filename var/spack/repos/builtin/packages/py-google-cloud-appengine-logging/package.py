# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudAppengineLogging(PythonPackage):
    """Google Cloud Appengine Logging API client library."""

    homepage = "https://googleapis.github.io/google-cloud-python"
    pypi = "google_cloud_appengine_logging/google-cloud-appengine-logging-1.4.1.tar.gz"

    license("Apache-2.0")

    version(
        "1.4.1",
        sha256="851dad2c4dd85dcf5b9e32879acda998a250e82c4d4f2bd5ef67b904840c7b17",
        url="https://pypi.org/packages/ea/4c/cc55e3ebaeca3cbb87441cd296051d5aafce3c9f5ff8b7f5b69549fc66a5/google_cloud_appengine_logging-1.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-google-api-core@1.34:1,2.11:+grpc", when="@1.2:1.4.1")
        depends_on("py-google-auth@2.14.1:", when="@1.4.1:1.4.2")
        depends_on("py-proto-plus@1.22.3:", when="@1.4:")
        depends_on(
            "py-protobuf@3.19.5:3.20.0-rc2,3.20.1-rc1,3.20.2:4.21.0-rc2,4.21.6:4", when="@1.1.6:"
        )

    # https://github.com/googleapis/google-cloud-python/blob/google-cloud-appengine-logging-v1.4.1/packages/google-cloud-appengine-logging/setup.py

    conflicts("py-google-api-core@2.0:2.10")

    conflicts("py-protobuf@3.20.0,3.20.1,4.21.0:4.21.5")
