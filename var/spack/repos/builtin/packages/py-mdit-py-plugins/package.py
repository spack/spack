# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMditPyPlugins(PythonPackage):
    """Collection of core plugins for markdown-it-py"""

    homepage = "https://github.com/executablebooks/mdit-py-plugins/"
    git = "https://github.com/executablebooks/mdit-py-plugins/"
    pypi = "mdit-py-plugins/mdit-py-plugins-0.3.1.tar.gz"

    license("MIT")

    version(
        "0.3.1",
        sha256="606a7f29cf56dbdfaf914acb21709b8f8ee29d857e8f29dcc33d8cb84c57bfa1",
        url="https://pypi.org/packages/de/d9/20870f611989b8dcfd2395eddefdd4b1983d6c36513cce7fbbe9eb345768/mdit_py_plugins-0.3.1-py3-none-any.whl",
    )
    version(
        "0.2.8",
        sha256="1833bf738e038e35d89cb3a07eb0d227ed647ce7dd357579b65343740c6d249c",
        url="https://pypi.org/packages/c0/cb/782222da2cc3d543aee662c33cbaf611ec010146ca21c91d5743e8d99603/mdit_py_plugins-0.2.8-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3.1:0.3")
        depends_on("python@:3", when="@:0.3.0")
        depends_on("py-markdown-it-py@1.0.0:2", when="@0.3")
        depends_on("py-markdown-it-py@1.0.0:1", when="@0.2.7:0.2")
