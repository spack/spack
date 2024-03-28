# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeeadd(PythonPackage):
    """Google Earth Engine Batch Assets Manager with Addons."""

    homepage = "https://github.com/samapriya/gee_asset_manager_addon"
    pypi = "geeadd/geeadd-0.3.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.3.0",
        sha256="77a6d7761fe70273f38c646553c62f962ba16a65a08e718c2c829c82393a4ec5",
        url="https://pypi.org/packages/98/54/3081518063971a339adc171068cab3211f70ebf215c12eede3a3d1421481/geeadd-0.3.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-beautifulsoup4@4.5.1:", when="@0.3:0.3.2")
        depends_on("py-clipboard@0.0.4:", when="@0.3")
        depends_on("py-earthengine-api@0.1.87:", when="@0.3:0.3.0")
        depends_on("py-future@0.16:", when="@0.3")
        depends_on("py-google-cloud-storage@1.1.1:", when="@0.3")
        depends_on("py-oauth2client@4.1.3:", when="@0.3")
        depends_on("py-poster@0.8.1:", when="@0.3:0.3.0")
        depends_on("py-pytest@3:", when="@0.3")
        depends_on("py-requests@2.10:", when="@0.3")
        depends_on("py-requests-toolbelt@0.7:", when="@0.3")
        depends_on("py-retrying@1.3.3:", when="@0.3")
