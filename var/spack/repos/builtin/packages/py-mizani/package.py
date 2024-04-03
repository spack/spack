# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMizani(PythonPackage):
    """Mizani is a scales package for graphics. It is based on Hadley Wickham's
    Scales package."""

    homepage = "https://mizani.readthedocs.io/en/latest"
    pypi = "mizani/mizani-0.7.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.8.1",
        sha256="a45f16d1bb420bd92361284252fd29c5e52a20662ad96dfe7a15141a4ca4c287",
        url="https://pypi.org/packages/a5/6a/738cec3b98020b9cf27bdbfe7c1f385a102300a3d06b2a8ad95f31923dfe/mizani-0.8.1-py3-none-any.whl",
    )
    version(
        "0.7.4",
        sha256="f8cd18a4e761846d948ee87429cc84730277d128a46861c719eb6997e6c538a1",
        url="https://pypi.org/packages/6a/10/999db77b9ce38adc22eb51a869b8c29b6b6fbd9c3b71a627bfee15b8f4d5/mizani-0.7.4-py3-none-any.whl",
    )
    version(
        "0.7.3",
        sha256="7f95d713e2bd28d51919e065d3453d470a654a0a219a7f777f8e9b6ed6e6ed35",
        url="https://pypi.org/packages/28/ed/d66698fff045087a220561f2bed1ec4cc9cfc58611a914c1f17bbbc27d05/mizani-0.7.3-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="da896b6c0e8868d411be0e46c72766596714869912359de44df269496ba9e29b",
        url="https://pypi.org/packages/e3/76/7a2c9094547ee592f9f43f651ab824aa6599af5e1456250c3f4cc162aece/mizani-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.7.4:0.9")
        depends_on("py-backports-zoneinfo", when="@0.8:0.9 ^python@:3.8")
        depends_on("py-matplotlib@3.5.0:", when="@0.7.4:0.9")
        depends_on("py-matplotlib@3.1.1:", when="@0.6:0.7.3")
        depends_on("py-numpy@1.19.0:", when="@0.7.4:0.10")
        depends_on("py-numpy", when="@:0.7.3")
        depends_on("py-palettable", when="@:0.8")
        depends_on("py-pandas@1.3.5:", when="@0.7.4:0.10")
        depends_on("py-pandas@1.1.0:", when="@0.7.2:0.7.3")
        depends_on("py-pandas@0.25.0:", when="@0.6")
        depends_on("py-scipy@1.5.0:", when="@0.7.4:0.10")
        depends_on("py-tzdata", when="@0.8: platform=windows")

    # common requirements

    # variable requirements
