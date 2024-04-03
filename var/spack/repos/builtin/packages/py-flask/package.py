# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlask(PythonPackage):
    """A simple framework for building complex web applications."""

    homepage = "https://palletsprojects.com/p/flask/"
    pypi = "Flask/Flask-1.1.1.tar.gz"
    git = "https://github.com/pallets/flask.git"

    license("BSD-3-Clause")

    version(
        "2.3.2",
        sha256="77fd4e1249d8c9923de34907236b747ced06e5467ecac1a7bb7115ae0e9670b0",
        url="https://pypi.org/packages/fa/1a/f191d32818e5cd985bdd3f47a6e4f525e2db1ce5e8150045ca0c31813686/Flask-2.3.2-py3-none-any.whl",
    )
    version(
        "2.2.2",
        sha256="b9c46cc36662a7949f34b52d8ec7bb59c0d74ba08ba6cb9ce9adc1d8676d9526",
        url="https://pypi.org/packages/0f/43/15f4f9ab225b0b25352412e8daa3d0e3d135fcf5e127070c74c3632c8b4c/Flask-2.2.2-py3-none-any.whl",
    )
    version(
        "2.0.2",
        sha256="cb90f62f1d8e4dc4621f52106613488b5ba826b2e1e10a33eac92f723093ab6a",
        url="https://pypi.org/packages/8f/b6/b4fdcb6d01ee20f9cfe81dcf9d3cd6c2f874b996f186f1c0b898c4a59c04/Flask-2.0.2-py3-none-any.whl",
    )
    version(
        "1.1.2",
        sha256="8a4fdd8936eba2512e9c85df320a37e694c93945b33ef33c89946a340a238557",
        url="https://pypi.org/packages/f2/28/2a03252dfb9ebf377f40fba6a7841b47083260bf8bd8e737b0c6952df83f/Flask-1.1.2-py2.py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="45eb5a6fd193d6cf7e0cf5d8a5b31f83d5faae0293695626f539a823e93b13f6",
        url="https://pypi.org/packages/9b/93/628509b8d5dc749656a9641f4caf13540e2cdec85276964ff8f43bbb1d3b/Flask-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "0.12.4",
        sha256="6c02dbaa5a9ef790d8219bdced392e2d549c10cd5a5ba4b6aa65126b2271af29",
        url="https://pypi.org/packages/2e/48/f1936dadac2326b3d73f2fe0a964a87d16be16eb9d7fc56f09c1bea3d17c/Flask-0.12.4-py2.py3-none-any.whl",
    )
    version(
        "0.12.2",
        sha256="0749df235e3ff61ac108f69ac178c9770caeaccad2509cb762ce1f65570a8856",
        url="https://pypi.org/packages/77/32/e3597cb19ffffe724ad4bf0beca4153419918e7fa4ba6a34b04ee4da3371/Flask-0.12.2-py2.py3-none-any.whl",
    )
    version(
        "0.12.1",
        sha256="6c3130c8927109a08225993e4e503de4ac4f2678678ae211b33b519c622a7242",
        url="https://pypi.org/packages/f4/43/fb2d5fb1d10e1d0402dd57836cf9a78b7f69c8b5f76a04b6e6113d0d7c5a/Flask-0.12.1-py2.py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="a4f97abd30d289e548434ef42317a793f58087be1989eab96f2c647470e77000",
        url="https://pypi.org/packages/63/2b/01f5ed23a78391f6e3e73075973da0ecb467c831376a0b09c0ec5afd7977/Flask-0.11.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2.3:")
        depends_on("python@3.7:", when="@2.1:2.2")
        depends_on("py-blinker@1.6.2:", when="@2.3:")
        depends_on("py-click@8.1.3:", when="@2.3:")
        depends_on("py-click@8.0.0:", when="@2.1:2.2")
        depends_on("py-click@7.1.2:", when="@2.0.0-rc2:2.0")
        depends_on("py-click@5.1:", when="@1:1.1.2")
        depends_on("py-click@2:", when="@0.12.3:0")
        depends_on("py-importlib-metadata@3.6:", when="@2.1.1: ^python@:3.9")
        depends_on("py-itsdangerous@2.1.2:", when="@2.3:")
        depends_on("py-itsdangerous@2.0.0:", when="@2.0.0:2.2")
        depends_on("py-itsdangerous@0.24:", when="@1:1.1.2")
        depends_on("py-itsdangerous@0.21:", when="@0.12.3:0")
        depends_on("py-jinja2@3.1.2:", when="@2.3:")
        depends_on("py-jinja2@3.0.0:", when="@2.0.0:2.2")
        depends_on("py-jinja2@2.10.1:", when="@1.1:1.1.2")
        depends_on("py-jinja2@2.4:", when="@0.12.3:0")
        depends_on("py-werkzeug@2.3.3:", when="@2.3.2")
        depends_on("py-werkzeug@2.2.2:", when="@2.2.2:2.2")
        depends_on("py-werkzeug@2.0.0:", when="@2.0.0:2.1")
        depends_on("py-werkzeug@0.15:", when="@1.1:1.1.2")
        depends_on("py-werkzeug@0.7:", when="@0.12.3:0.12.4")
