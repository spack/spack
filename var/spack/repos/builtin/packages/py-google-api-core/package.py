# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApiCore(PythonPackage):
    """Google API client core library."""

    homepage = "https://github.com/googleapis/python-api-core"
    pypi = "google-api-core/google-api-core-2.17.0.tar.gz"

    # 'google.api_core.operations_v1' and 'google.api_core.gapic_v1' require 'grpc'.
    # Leave them out of 'import_modules' to avoid optional dependency.
    import_modules = ["google.api_core", "google.api_core.future"]

    license("Apache-2.0")

    version(
        "2.17.0",
        sha256="08ed79ed8e93e329de5e3e7452746b734e6bf8438d8d64dd3319d21d3164890c",
        url="https://pypi.org/packages/60/51/2054dfc08dda9a3add0d715cee98d6f8211c99bd6e5bff0ff1bdd3cf3384/google_api_core-2.17.0-py3-none-any.whl",
    )
    version(
        "2.16.2",
        sha256="449ca0e3f14c179b4165b664256066c7861610f70b6ffe54bb01a04e9b466929",
        url="https://pypi.org/packages/29/37/f7d78e23eb97c1c1753163d5c0734ae8a412d829dbe6e1527f486664f483/google_api_core-2.16.2-py3-none-any.whl",
    )
    version(
        "2.15.0",
        sha256="2aa56d2be495551e66bbff7f729b790546f87d5c90e74781aa77233bcb395a8a",
        url="https://pypi.org/packages/d6/c9/0462f037b62796fbda4801be62d0ae3147eaeb99e2939661580c98abe3eb/google_api_core-2.15.0-py3-none-any.whl",
    )
    version(
        "2.14.0",
        sha256="de2fb50ed34d47ddbb2bd2dcf680ee8fead46279f4ed6b16de362aca23a18952",
        url="https://pypi.org/packages/c4/1e/924dcad4725d2e697888e044edf7a433db84bf9a3e40d3efa38ba859d0ce/google_api_core-2.14.0-py3-none-any.whl",
    )
    version(
        "2.13.1",
        sha256="e24c3a20799df3ee08a10d1d44d7df2d2ef2bc986cca80edfd982f3e415edd20",
        url="https://pypi.org/packages/94/a1/ab9fcb5a6a3e6dc36345f21ebebb4a6d4679e9e270661e93c3a6e9eabdfe/google_api_core-2.13.1-py3-none-any.whl",
    )
    version(
        "2.12.0",
        sha256="ec6054f7d64ad13b41e43d96f735acbd763b0f3b695dabaa2d579673f6a6e160",
        url="https://pypi.org/packages/4d/ce/4fd62ea66b3508debc795e475336ce915929765870f0ad52328426ba016e/google_api_core-2.12.0-py3-none-any.whl",
    )
    version(
        "2.11.1",
        sha256="d92a5a92dc36dd4f4b9ee4e55528a90e432b059f93aee6ad857f9de8cc7ae94a",
        url="https://pypi.org/packages/6e/c4/c3cd048b6cbeba8d9ae50dd7643ac065b85237338aa7501b0efae91eb4d9/google_api_core-2.11.1-py3-none-any.whl",
    )
    version(
        "2.11.0",
        sha256="ce222e27b0de0d7bc63eb043b956996d6dccab14cc3b690aaea91c9cc99dc16e",
        url="https://pypi.org/packages/f7/24/a17e75c733609dce285a2dae6f56837d69a9566963c9d1cab96d788546c8/google_api_core-2.11.0-py3-none-any.whl",
    )
    version(
        "1.14.2",
        sha256="b2b91107bcc3b981633c89602b46451f6474973089febab3ee51c49cb7ae6a1f",
        url="https://pypi.org/packages/71/e5/7059475b3013a3c75abe35015c5761735ab224eb1b129fee7c8e376e7805/google_api_core-1.14.2-py2.py3-none-any.whl",
    )

    variant(
        "grpc",
        default=False,
        description="Enable support for gRPC Remote Procedure Call framework.",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1.33:1,2.9:")
        depends_on("py-google-auth@2.14.1:", when="@2.11:")
        depends_on("py-google-auth@0.4:1", when="@:1.16")
        depends_on("py-googleapis-common-protos@1.56.2:", when="@1.33:1,2.8.1:")
        depends_on("py-googleapis-common-protos@1.6.0:", when="@1.14:1.32,2:2.1")
        depends_on("py-grpcio@1.49.1:", when="@2.11:+grpc ^python@3.11:")
        depends_on("py-grpcio@1.33.2:", when="@1.33:1,2.0.0:+grpc")
        depends_on("py-grpcio@1.8.2:", when="@1.11.1:1.19.0+grpc")
        depends_on("py-grpcio-status@1.49.1:", when="@2.11:+grpc ^python@3.11:")
        depends_on("py-grpcio-status@1.33.2:", when="@1.33:1,2.2:+grpc")
        depends_on(
            "py-protobuf@3.19.5:3.20.0-rc2,3.20.1-rc1,3.20.2:4.21.0-rc2,4.21.6:4", when="@2.10.2:"
        )
        depends_on("py-protobuf@3.4:", when="@:1.20.0")
        depends_on("py-pytz", when="@:1.32")
        depends_on("py-requests@2.18:")
        depends_on("py-setuptools@34:", when="@:1.24")
        depends_on("py-six@1.10:", when="@:1.22.2")
