# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyopengl(PythonPackage):
    """PyOpenGL is the most common cross platform Python binding to OpenGL and related APIs."""

    homepage = "http://pyopengl.sourceforge.net"
    url = "https://files.pythonhosted.org/packages/py3/p/pyopengl/PyOpenGL-3.1.6-py3-none-any.whl"
    list_url = "https://pypi.org/simple/pyopengl/"

    version(
        "3.1.6",
        sha256="a7139bc3e15d656feae1f7e3ef68c799941ed43fadc78177a23db7e946c20738",
        expand=False,
    )

    depends_on("python@3.6:", type=("build", "run"))
