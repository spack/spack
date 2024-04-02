# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudLogging(PythonPackage):
    """Stackdriver Logging API client library."""

    homepage = "https://github.com/googleapis/python-logging"
    pypi = "google-cloud-logging/google-cloud-logging-3.9.0.tar.gz"

    license("Apache-2.0")

    version(
        "3.9.0",
        sha256="094a2db068ff7f38c9e0c1017673fa49c0768fbae02769e03e06baa30f138b87",
        url="https://pypi.org/packages/a9/94/24603046ca57f88a0602dd682fce99282c62be1b4e90e1316974f7cb1691/google_cloud_logging-3.9.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-google-api-core@1.33.2:1,2.8:+grpc", when="@3.4:3.9")
        depends_on("py-google-cloud-appengine-logging")
        depends_on("py-google-cloud-audit-log")
        depends_on("py-google-cloud-core@2.0.0:")
        depends_on("py-grpc-google-iam-v1@0.12.4:")
        depends_on("py-proto-plus@1.22.2:", when="@3.5: ^python@3.11:")
        depends_on("py-proto-plus@1.22:")
        depends_on(
            "py-protobuf@3.19.5:3.20.0-rc2,3.20.1-rc1,3.20.2:4.21.0-rc2,4.21.6:4", when="@3.4:"
        )

    conflicts("py-google-api-core@2.0:2.7")

    conflicts("py-protobuf@3.20.0:3.20.1,4.21.0:4.21.5")
