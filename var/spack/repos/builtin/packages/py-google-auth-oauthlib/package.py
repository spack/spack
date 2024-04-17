# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGoogleAuthOauthlib(PythonPackage):
    """This library provides oauthlib integration with google-auth."""

    homepage = "https://github.com/googleapis/google-auth-library-python-oauthlib"
    pypi = "google-auth-oauthlib/google-auth-oauthlib-0.4.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.2",
        sha256="6d6161d0ec0a62e2abf2207c6071c117ec5897b300823c4bb2d963ee86e20e4f",
        url="https://pypi.org/packages/f8/93/aa9e5c46c955758ec9f08779e78838f7e041cbef8338ac9e490465aa4947/google_auth_oauthlib-0.5.2-py2.py3-none-any.whl",
    )
    version(
        "0.4.6",
        sha256="3f2a6e802eebbb6fb736a370fbf3b055edcb6b52878bf2f26330b5e041316c73",
        url="https://pypi.org/packages/b1/0e/0636cc1448a7abc444fb1b3a63655e294e0d2d49092dc3de05241be6d43c/google_auth_oauthlib-0.4.6-py2.py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="a92a0f6f41a0fb6138454fbc02674e64f89d82a244ea32f98471733c8ef0e0e1",
        url="https://pypi.org/packages/7b/b8/88def36e74bee9fce511c9519571f4e485e890093ab7442284f4ffaef60b/google_auth_oauthlib-0.4.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-google-auth@1:", when="@0.4.3:0.6")
        depends_on("py-google-auth", when="@:0.4.2")
        depends_on("py-requests-oauthlib@0.7:")
