# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudAuditLog(PythonPackage):
    """Google Cloud Audit Protos."""

    homepage = "https://github.com/googleapis/python-audit-log"
    pypi = "google_cloud_audit_log/google-cloud-audit-log-0.2.5.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.5",
        sha256="18b94d4579002a450b7902cd2e8b8fdcb1ea2dd4df3b41f8f82be6d9f7fcd746",
        url="https://pypi.org/packages/55/9b/2920117f37aff47b5b7d6081e2d5e13441d0952e5bd449babc392e03b621/google_cloud_audit_log-0.2.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2.3:")
        depends_on("py-googleapis-common-protos@1.56.2:", when="@0.2.1:")
        depends_on(
            "py-protobuf@3.19.5:3.20.0-rc2,3.20.1-rc1,3.20.2:4.21.0,4.21.6:4", when="@0.2.5:"
        )

    # https://github.com/googleapis/python-audit-log/blob/v0.2.5/setup.py

    conflicts("py-protobuf@3.20.0,3.20.1,4.21.1:4.21.5")
