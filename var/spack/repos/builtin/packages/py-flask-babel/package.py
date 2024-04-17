# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskBabel(PythonPackage):
    """Implements i18n and l10n support for Flask."""

    homepage = "https://pythonhosted.org/Flask-Babel/"
    pypi = "Flask-Babel/Flask-Babel-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.0.0",
        sha256="e6820a052a8d344e178cdd36dd4bb8aea09b4bda3d5f9fa9f008df2c7f2f5468",
        url="https://pypi.org/packages/ab/3e/02331179ffab8b79e0383606a028b6a60fb1b4419b84935edd43223406a0/Flask_Babel-2.0.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-babel@2.3:", when="@1:2")
        depends_on("py-flask", when="@1:2")
        depends_on("py-jinja2@2.5:", when="@1:2")
        depends_on("py-pytz", when="@1:2")
