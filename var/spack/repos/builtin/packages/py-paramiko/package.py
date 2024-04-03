# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParamiko(PythonPackage):
    """SSH2 protocol library"""

    homepage = "https://www.paramiko.org/"
    pypi = "paramiko/paramiko-2.7.1.tar.gz"

    license("LGPL-2.1-or-later")

    version(
        "2.12.0",
        sha256="b2df1a6325f6996ef55a8789d0462f5b502ea83b3c990cbb5bbe57345c6812c4",
        url="https://pypi.org/packages/71/6d/95777fd66507106d2f8f81d005255c237187951644f85a5bd0baeec8a88f/paramiko-2.12.0-py2.py3-none-any.whl",
    )
    version(
        "2.9.2",
        sha256="04097dbd96871691cdb34c13db1883066b8a13a0df2afd4cb0a92221f51c2603",
        url="https://pypi.org/packages/60/3e/84c52fb09db84548c5d366bac8863125c6db099b87495e04c8af5527e6f1/paramiko-2.9.2-py2.py3-none-any.whl",
    )
    version(
        "2.7.1",
        sha256="9c980875fa4d2cb751604664e9a2d0f69096643f5be4db1b99599fe114a97b2f",
        url="https://pypi.org/packages/06/1e/1e08baaaf6c3d3df1459fd85f0e7d2d6aa916f33958f151ee1ecc9800971/paramiko-2.7.1-py2.py3-none-any.whl",
    )
    version(
        "2.1.2",
        sha256="bdf239647e18b9b9ddbc2894fd1de9786b7a9144b1d19e32a5be3bb4bb63ae5d",
        url="https://pypi.org/packages/14/1e/2988f842e3194daf4d6e14e6e38e8d7085b2b45c669c3b635708c4a7618c/paramiko-2.1.2-py2.py3-none-any.whl",
    )

    variant("invoke", default=False, description="Enable invoke support")

    with default_args(type="run"):
        depends_on("py-bcrypt@3.1.3:", when="@2.2.1:2")
        depends_on("py-cryptography@2.5:", when="@2.5:2")
        depends_on("py-cryptography@1.1:", when="@:2.2")
        depends_on("py-invoke@1.3:", when="@2.7:2+invoke")
        depends_on("py-pyasn1@0.1.7:", when="@:2.4")
        depends_on("py-pynacl@1.0.1:", when="@2.2:2")
        depends_on("py-six", when="@2.9.3:2")

    conflicts("+invoke", when="@2.1.2")
