# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Uwtools(PythonPackage):
    """UW Tools is a modern, open-source Python package that helps
    automate common tasks needed for many standard numerical weather
    prediction (NWP) workflows. It also provides drivers to automate
    the configuration and execution of Unified Forecast System (UFS)
    components, providing flexibility, interoperability, and
    usability to various UFS Applications."""

    homepage = "https://uwtools.readthedocs.io/en/stable/"
    url = "https://github.com/ufs-community/uwtools/archive/refs/tags/v2.7.1.tar.gz"
    git = "https://github.com/ufs-community/uwtools.git"

    maintainers("NaureenBharwaniNOAA", "christinaholtNOAA", "elcarpenterNOAA", "maddenp-cu")

    license("GPL-2.0-or-later", checked_by="WeirAE")

    version("2.7.1", sha256="2764aa5fa9f4ebb3eb43bf6ee3cf9e37d3889f374bfc536faabdfb3dc46b26c8")
    version("2.7.0", sha256="778c935256c9511d81e32a7548412ace3a1901d8afc22bdb042639156e45bcc5")
    version("2.6.3", sha256="0b9cd205c91202cf20eef64fa462176b37d6fbbceb752097a065d1772855bfc4")
    version("2.6.2", sha256="d0922ddd2b3bdbeb925c2e4694f929f3e966145d2929e74ab9f9c9ecd27b674a")
    version("2.6.1", sha256="cd3fb06b153ddba3b5256c79c3be4d84c6b388b7c2f7737e8b32bcb28081774b")
    version("2.6.0", sha256="25f350a3f69b29a4b685ce9c93edfc11a39b99192040bc44250495c0e6a09b68")
    version("2.5.3", sha256="fec29a1c1b07788d3144fa45a263566bab6cfd286da0cfbefe2b2a02f7bacad1")
    version("2.5.2", sha256="358da7473205456720e2f8231a43ad7ef0b9946dfdad41ea542963f444d258b9")
    version("2.5.1", sha256="f389f63195492196c8009d5843a3861ad350b5fd1cea1fdb8a6bfdc7cbfd660f")
    version("2.5.0", sha256="246f1cb1d3b7c507eae833f5223d3be5efaea16204a71cafba820901edc0e19e")

    depends_on("py-pip", type="build")
    depends_on("python@3.9")
    depends_on("py-setuptools", type="build")
    depends_on("py-f90nml@1.4")
    depends_on("py-jinja2@3.1")
    depends_on("iotaa@0.8:", when="@:2.6.3")
    depends_on("iotaa@1.1:", when="@2.6.3:")
    depends_on("iotaa@1.2:", when="@2.7.1:")
    depends_on("py-jsonschema@4.18:4.24")
    depends_on("py-lxml@5.3")
    depends_on("py-pyyaml@6.0")
    depends_on("py-requests@2.32", when="@2.6.3:")

    build_directory = "src"

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
