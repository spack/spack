# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInstaller(Package, PythonExtension):
    """A library for installing Python wheels."""

    homepage = "https://github.com/pypa/installer"
    url = (
        "https://files.pythonhosted.org/packages/py3/i/installer/installer-0.6.0-py3-none-any.whl"
    )
    list_url = "https://pypi.org/simple/installer/"

    version(
        "0.7.0",
        sha256="05d1933f0a5ba7d8d6296bb6d5018e7c94fa473ceb10cf198a92ccea19c27b53",
        url="https://pypi.org/packages/e5/ca/1172b6638d52f2d6caa2dd262ec4c811ba59eee96d54a7701930726bce18/installer-0.7.0-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="ae7c62d1d6158b5c096419102ad0d01fdccebf857e784cee57f94165635fe038",
        url="https://pypi.org/packages/bf/42/fe5f10fd0d58d5d8231a0bc39e664de09992f960597e9fbd3753f84423a3/installer-0.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.5:")

    extends("python")

    def setup_dependent_package(self, module, dependent_spec):
        installer = dependent_spec["python"].command
        installer.add_default_arg("-m", "installer")
        setattr(module, "installer", installer)
