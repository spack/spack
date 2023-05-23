# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudStorage(PythonPackage):
    """Google Cloud Storage API client library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    pypi = "google-cloud-storage/google-cloud-storage-1.18.0.tar.gz"

    version("2.7.0", sha256="1ac2d58d2d693cb1341ebc48659a3527be778d9e2d8989697a2746025928ff17")
    version("1.18.0", sha256="9fb3dc68948f4c893c2b16f5a3db3daea2d2f3b8e9d5c2d505fe1523758009b6")

    depends_on("py-setuptools", type="build")

    with when("@2:"):
        depends_on("py-google-auth@1.25:2", type=("build", "run"))
        depends_on("py-google-api-core@1.31.5:1,2.3.1:2", type=("build", "run"))
        depends_on("py-google-cloud-core@2.3:2", type=("build", "run"))
        depends_on("py-google-resumable-media@2.3.2:", type=("build", "run"))
        depends_on("py-requests@2.18:2", type=("build", "run"))

    with when("@:1"):
        depends_on("py-google-auth@1.2.0:", type=("build", "run"))
        depends_on("py-google-cloud-core@1.0:1", type=("build", "run"))
        depends_on("py-google-resumable-media@0.3.1:", type=("build", "run"))
