# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyprojectMetadata(PythonPackage):
    """PEP 621 metadata parsing."""

    homepage = "https://github.com/FFY00/python-pyproject-metadata"
    pypi = "pyproject-metadata/pyproject-metadata-0.6.1.tar.gz"

    license("MIT")

    version("0.9.1", sha256="b8b2253dd1b7062b78cf949a115f02ba7fa4114aabe63fa10528e9e1a954a816")
    version("0.7.1", sha256="0a94f18b108b9b21f3a26a3d541f056c34edcb17dc872a144a15618fed7aef67")
    version("0.6.1", sha256="b5fb09543a64a91165dfe85796759f9e415edc296beb4db33d1ecf7866a862bd")

    with default_args(type="build"):
        depends_on("py-typing-extensions", when="@0.9: ^python@:3.7")
        depends_on("py-flit-core", when="@0.8:")
        depends_on("py-setuptools@42:", when="@:0.7.1")

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
        depends_on("py-packaging@19:")

    def url_for_version(self, version):
        if version >= Version("0.8.0"):
            return f"https://files.pythonhosted.org/packages/source/p/pyproject_metadata/pyproject_metadata-{version}.tar.gz"
        else:
            return f"https://files.pythonhosted.org/packages/source/p/pyproject-metadata/pyproject-metadata-{version}.tar.gz"
