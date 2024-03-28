# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModulesGui(PythonPackage):
    """MoGui is a Graphical User Interface (GUI) for Environment Modules.
    It helps users selecting modules to load and save module collections."""

    homepage = "https://github.com/cea-hpc/mogui"
    pypi = "modules-gui/modules-gui-0.2.tar.gz"

    maintainers("adrien-cotte")

    license("GPL-2.0")

    version(
        "0.2",
        sha256="d23cc11ef77668adbde3e4c9d47d464bbc03845960d24cf97b2e7d53af4390a8",
        url="https://pypi.org/packages/f1/93/943d7b8337c7f8c376ca977c2f4e5d560af565f12876d9ef73aa7cba0b48/modules_gui-0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyqt5")
