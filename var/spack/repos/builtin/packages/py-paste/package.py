# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPaste(PythonPackage):
    """Tools for using a Web Server Gateway Interface stack"""

    homepage = "https://pythonpaste.readthedocs.io"
    pypi = "Paste/Paste-3.5.2.tar.gz"

    license("MIT")

    version(
        "3.5.2",
        sha256="fa0385cd07a50e6c679e735e44afef1e24ab1a0578eea501e45b8c2d38669b77",
        url="https://pypi.org/packages/0c/f7/e965ace528fca3319fc6656f6ed6f6ba7c8f17fa32e588da1af291b95fd1/Paste-3.5.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-setuptools", when="@3.4.6:")
        depends_on("py-six@1.4:")
