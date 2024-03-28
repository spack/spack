# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeeup(PythonPackage):
    """Simple Client for Earth Engine Uploads with Selenium Support."""

    homepage = "https://github.com/samapriya/geeup"
    pypi = "geeup/geeup-0.2.4.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.4",
        sha256="ab6ac8a10cd56d67bd7c1b1e12327fba1766f7f434d09a83a4aae95249b69c29",
        url="https://pypi.org/packages/b0/47/3295bd655286c4dcf9df98c1ca85afe9ca93404522becf354b484d7f7587/geeup-0.2.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-beautifulsoup4@4.5.1:", when="@0.1.7:0.3")
        depends_on("py-earthengine-api@0.1.87:", when="@0.1.7:0.2.1,0.2.3:0.2.4")
        depends_on("py-future@0.16:", when="@0.1.7:0.2")
        depends_on("py-google-cloud-storage@1.1.1:", when="@0.1.7:0")
        depends_on("py-lxml@4.1.1:", when="@0.1.7:")
        depends_on("py-oauth2client@4.1.3:", when="@0.1.7:")
        depends_on("py-pandas@0.23.0:", when="@0.1.7:0")
        depends_on("py-pathlib@1.0.1:", when="@0.1.7:")
        depends_on("py-psutil@5.4.5:", when="@0.1.7:")
        depends_on("py-pysmartdl@1.3:", when="@0.1.9:0.5.7")
        depends_on("py-pytest@3:", when="@0.1.7:")
        depends_on("py-requests@2.10:", when="@0.1.7:")
        depends_on("py-requests-toolbelt@0.7:", when="@0.1.7:")
        depends_on("py-retrying@1.3.3:", when="@0.1.7:")
        depends_on("py-selenium@3.13:", when="@0.1.7:0.5.2")
