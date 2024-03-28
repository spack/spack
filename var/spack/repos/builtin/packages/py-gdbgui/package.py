# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGdbgui(PythonPackage):
    """gdbgui is a modern, free, browser-based frontend to gdb"""

    homepage = "https://gdbgui.com"
    pypi = "gdbgui/gdbgui-0.11.2.1.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "0.13.2.0",
        sha256="458bc73eb4b08c8471e5500f1bf0d354fa6d51e80413e2e2c202b194be7e49fc",
        url="https://pypi.org/packages/1d/67/e9d645374d536aaa0557e26e594f0b254b1dc176f2694295135c8dd3a400/gdbgui-0.13.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-flask@0.12.2:0", when="@0.11.3.1:0.13.2.1,0.14")
        depends_on("py-flask-compress@1.4:", when="@0.12:0.13.2.1,0.14")
        depends_on("py-flask-socketio@2.9:2", when="@0.12:0.13.2.1,0.14")
        depends_on("py-gevent@1.2.2:1", when="@0.12:0.13.2.1,0.14")
        depends_on("py-pygdbmi@0.9:", when="@0.13.1:0.13.2.1")
        depends_on("py-pygments@2.2:", when="@0.12:0.13.2.1,0.14:0.15.0")
