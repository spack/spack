# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudCore(PythonPackage):
    """Google Cloud API client core library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    pypi = "google-cloud-core/google-cloud-core-1.0.3.tar.gz"

    license("Apache-2.0")

    version(
        "2.3.2",
        sha256="8417acf6466be2fa85123441696c4badda48db314c607cf1e5d543fa8bdc22fe",
        url="https://pypi.org/packages/ac/4d/bae84e736080ed465a6b02e9f447c89c60c00fcdade2eb6911fecf3f46aa/google_cloud_core-2.3.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.3",
        sha256="0ee17abc74ff02176bee221d4896a00a3c202f3fb07125a7d814ccabd20d7eb5",
        url="https://pypi.org/packages/ee/f0/084f598629db8e6ec3627688723875cdb03637acb6d86999bb105a71df64/google_cloud_core-1.0.3-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2.3.2:")
        depends_on("py-google-api-core@1.31.6:1,2.3.1:", when="@2.3.2:")
        depends_on("py-google-api-core@1.14:1", when="@1.0.3:1.1")
        depends_on("py-google-auth@1.25:", when="@2.2.3:")
