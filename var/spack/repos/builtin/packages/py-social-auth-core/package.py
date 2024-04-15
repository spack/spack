# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySocialAuthCore(PythonPackage):
    """Python social authentication made simple."""

    homepage = "https://github.com/python-social-auth/social-core"
    pypi = "social-auth-core/social-auth-core-4.3.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "4.3.0",
        sha256="1e3440d104f743b02dfe258c9d4dba5b4065abf24b2f7eb362b47054d21797df",
        url="https://pypi.org/packages/60/f9/5387e450842d785f4e100e3766bf0d2a8aa44acad619459cf7abff72a9c5/social_auth_core-4.3.0-py3-none-any.whl",
    )
    version(
        "4.0.3",
        sha256="567b1f1bb1912e2c3153df888b48ba883dabdfe72f031e8cae4d404f61745c21",
        url="https://pypi.org/packages/79/be/d7b3c82897a328f42e264965ef4b8194625b4251882e0378a480b188fbac/social_auth_core-4.0.3-py3-none-any.whl",
    )

    variant("openidconnect", default=False, description="Install requirements for openidconnect")

    with default_args(type=("build", "run")):
        depends_on("py-cryptography@1.4:", when="@3.3.2:")
        depends_on("py-defusedxml@0.5:", when="@3.3.2:")
        depends_on("py-oauthlib@1.0.3:", when="@3.3.2:")
        depends_on("py-pyjwt@2.0.0:", when="@4.0.3:4.4")
        depends_on("py-pyjwt@1.7.1:", when="@3.3.2:4.0+openidconnect")
        depends_on("py-python-jose@3:", when="@3.3.2:4.4+openidconnect")
        depends_on("py-python3-openid@3.0.10:", when="@3.3.2:")
        depends_on("py-requests@2.9.1:", when="@3.3.2:")
        depends_on("py-requests-oauthlib@0.6.1:", when="@3.3.2:")
