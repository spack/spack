# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupytext(PythonPackage):
    """Jupyter Notebooks as Markdown Documents, Julia, Python or R scripts"""

    homepage = "https://github.com/mwouts/jupytext/"
    git = "https://github.com/mwouts/jupytext/"
    pypi = "jupytext/jupytext-1.13.0.tar.gz"

    maintainers("vvolkl")

    license("MIT")

    version(
        "1.16.0",
        sha256="c2b951ac72871f39cd6cd242b56bc43219b7ed8169598bae5359811fb1f54d28",
        url="https://pypi.org/packages/b4/35/1f396e6745cbaa1aec3624fb6656a77f2e001b324cb4a056aa6a4a436e46/jupytext-1.16.0-py3-none-any.whl",
    )
    version(
        "1.14.1",
        sha256="216bddba8bbb9355831ba17fd8d45cfe5d1355e7152bc8980f39175fc2584875",
        url="https://pypi.org/packages/1e/b6/53edfeda6e8ac67a9fd31b510fe8c8e46c1b505805ae958d6fff82f9b2df/jupytext-1.14.1-py3-none-any.whl",
    )
    version(
        "1.13.6",
        sha256="2160774e30587fb427213231f0267ed070ba4ede41cf6121dbb2b14225eb83ba",
        url="https://pypi.org/packages/07/3f/18d7d371bd1d74b9ef8a7d14b91f28a609277d849c036d930436ed243b92/jupytext-1.13.6-py3-none-any.whl",
    )
    version(
        "1.13.0",
        sha256="c31f016c6fc000d88c5aed2cfc58f1acbfb3d9c58898aa0e4bdc3716f3860b09",
        url="https://pypi.org/packages/f9/c9/24d58379d6c6600aec4dc1ed5c893b6c963a73598bfcb9270d494c3c3896/jupytext-1.13.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.16:")
        depends_on("python@:3", when="@:1.15")
        depends_on("py-markdown-it-py@1.0.0:", when="@1.14.7:")
        depends_on("py-markdown-it-py@1.0.0:2", when="@1.13.8:1.14.6")
        depends_on("py-markdown-it-py@1.0.0:1", when="@1.11.4:1.13.7")
        depends_on("py-mdit-py-plugins", when="@1.11.4:")
        depends_on("py-nbformat")
        depends_on("py-packaging", when="@1.16:")
        depends_on("py-pyyaml")
        depends_on("py-toml")

    # todo: in order to use jupytext as a jupyterlab extension,
    # some additional dependencies need to be added (and checked):
