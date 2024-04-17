# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFasteners(PythonPackage):
    """A python package that provides useful locks."""

    homepage = "https://github.com/harlowja/fasteners"
    pypi = "fasteners/fasteners-0.14.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.18",
        sha256="1d4caf5f8db57b0e4107d94fd5a1d02510a450dced6ca77d1839064c1bacf20c",
        url="https://pypi.org/packages/bc/a2/7d35ba2c8d9963398fcec49cd814e50a6b920d213928f06fdbbf8aa3289b/fasteners-0.18-py3-none-any.whl",
    )
    version(
        "0.17.3",
        sha256="cae0772df265923e71435cc5057840138f4e8b6302f888a567d06ed8e1cbca03",
        url="https://pypi.org/packages/f6/01/274da83334c20dc1ae7a48b1ea4ae50d3571d4e6aea65bb0368f841701ad/fasteners-0.17.3-py3-none-any.whl",
    )
    version(
        "0.16.3",
        sha256="8408e52656455977053871990bd25824d85803b9417aa348f10ba29ef0c751f7",
        url="https://pypi.org/packages/31/91/6630ebd169ca170634ca8a10dfcc5f5c11b0621672d4c2c9e40381c6d81a/fasteners-0.16.3-py2.py3-none-any.whl",
    )
    version(
        "0.15",
        sha256="007e4d2b2d4a10093f67e932e5166722d2eab83b77724156e92ad013c6226574",
        url="https://pypi.org/packages/18/bd/55eb2d6397b9c0e263af9d091ebdb756b15756029b3cededf6461481bc63/fasteners-0.15-py2.py3-none-any.whl",
    )
    version(
        "0.14.1",
        sha256="564a115ff9698767df401efca29620cbb1a1c2146b7095ebd304b79cc5807a7c",
        url="https://pypi.org/packages/14/3a/096c7ad18e102d4f219f5dd15951f9728ca5092a3385d2e8f79a7c1e1017/fasteners-0.14.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-monotonic", when="@0.11:0.15")
        depends_on("py-six", when="@:0.16.0,0.16.2:0.16")
