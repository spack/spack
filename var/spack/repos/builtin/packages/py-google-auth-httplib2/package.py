# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleAuthHttplib2(PythonPackage):
    """Google Authentication Library: httplib2 transport."""

    homepage = "https://github.com/GoogleCloudPlatform/google-auth-library-python-httplib2"
    pypi = "google-auth-httplib2/google-auth-httplib2-0.0.3.tar.gz"

    license("Apache-2.0")

    version(
        "0.1.0",
        sha256="31e49c36c6b5643b57e82617cb3e021e3e1d2df9da63af67252c02fa9c1f4a10",
        url="https://pypi.org/packages/ba/db/721e2f3f32339080153995d16e46edc3a7657251f167ddcb9327e632783b/google_auth_httplib2-0.1.0-py2.py3-none-any.whl",
    )
    version(
        "0.0.3",
        sha256="f1c437842155680cf9918df9bc51c1182fda41feef88c34004bd1978c8157e08",
        url="https://pypi.org/packages/33/49/c814d6d438b823441552198f096fcd0377fd6c88714dbed34f1d3c8c4389/google_auth_httplib2-0.0.3-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-google-auth")
        depends_on("py-httplib2@0.15:", when="@0.1:0.1.0")
        depends_on("py-httplib2@0.9.1:", when="@0.0.3:0.0")
        depends_on("py-six", when="@0.0.4:0.1.0")
