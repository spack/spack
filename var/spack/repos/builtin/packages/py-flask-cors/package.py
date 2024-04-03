# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskCors(PythonPackage):
    """A Flask extension for handling Cross Origin Resource Sharing (CORS),
    making cross-origin AJAX possible.
    """

    homepage = "https://flask-cors.corydolphin.com/en/latest/index.html"
    pypi = "Flask-Cors/Flask-Cors-3.0.10.tar.gz"

    license("MIT")

    version(
        "3.0.10",
        sha256="74efc975af1194fc7891ff5cd85b0f7478be4f7f59fe158102e91abb72bb4438",
        url="https://pypi.org/packages/db/84/901e700de86604b1c4ef4b57110d4e947c218b9997adf5d38fa7da493bce/Flask_Cors-3.0.10-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-flask@0.9:", when="@3:")
        depends_on("py-six", when="@3")
