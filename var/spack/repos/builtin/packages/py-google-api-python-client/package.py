# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApiPythonClient(PythonPackage):
    """The Google API Client for Python is a client library for accessing the
    Plus, Moderator, and many other Google APIs."""

    homepage = "https://github.com/google/google-api-python-client/"
    pypi = "google-api-python-client/google-api-python-client-1.7.10.tar.gz"

    license("Apache-2.0")

    version(
        "2.80.0",
        sha256="b9cd2550c2cdfeb78c3150d8c52208841082dabe597063a116476937170907ab",
        url="https://pypi.org/packages/f8/63/fea1330ab4966d37a64bfd23378f8c32722ed7b91178cab4ab3601f4fd5e/google_api_python_client-2.80.0-py2.py3-none-any.whl",
    )
    version(
        "1.7.10",
        sha256="60f2ac2f27997d9af10ae126d9937b7d8c1fd061d12668ccaf94b4347ee85021",
        url="https://pypi.org/packages/ab/4b/66b7591b83864caef0d960aefd05a110bcf9cb18cc6dd957414e34861530/google_api_python_client-1.7.10-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.53:")
        depends_on("py-google-api-core@1.31.5:1,2.3.1:", when="@2.40:")
        depends_on("py-google-auth@1.19:", when="@2.52:")
        depends_on("py-google-auth@1.4.1:", when="@:1.8")
        depends_on("py-google-auth-httplib2@0.1:", when="@2.1:")
        depends_on("py-google-auth-httplib2@0.0.3:", when="@:2.0")
        depends_on("py-httplib2@0.15:", when="@1.12.3:")
        depends_on("py-httplib2@0.9.2:", when="@:1.7.11,1.8:1.12.2")
        depends_on("py-six@1.6.1:", when="@:1.12.0")
        depends_on("py-uritemplate@3.0.1:", when="@2.34:")
        depends_on("py-uritemplate@3", when="@:2.25")
