# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Onnx(CMakePackage):
    """Open Neural Network Exchange (ONNX).

    ONNX provides an open source format for AI models, both deep learning and
    traditional ML. It defines an extensible computation graph model, as well
    as definitions of built-in operators and standard data types."""

    homepage = "https://github.com/onnx/onnx"
    url = "https://github.com/onnx/onnx/archive/refs/tags/v1.9.0.tar.gz"
    git = "https://github.com/onnx/onnx.git"

    version("master", branch="master")
    version("1.12.0", sha256="052ad3d5dad358a33606e0fc89483f8150bb0655c99b12a43aa58b5b7f0cc507")
    version(
        "1.11.0", sha256="a20f2d9df805b16ac75ab4da0a230d3d1c304127d719e5c66a4e6df514e7f6c0"
    )  # py-torch@1.12:
    version("1.10.2", sha256="520b3aa34272cc215e2eb41385f58adf01750d88858d4722563edca8410c5dc9")
    version(
        "1.10.1_2021-10-08", commit="85546f8c44e627f8ff1181725d03cc49f675e44f"
    )  # py-torch@1.11
    version(
        "1.10.1", sha256="cb2fe3e0c9bba128a5790a565d81be30f4b5571eaca5418fb19df8d2d0f11ce2"
    )  # py-torch@1.10
    version("1.10.0", sha256="705a27ee076713b8c755911913c9ffa8f96b95fc3a8568ed0b8e1dd954d67147")
    version("1.9.0", sha256="61d459a5f30604cabec352574119a6685dfd43bfa757cfbff52be9471d5b8ea0")
    version(
        "1.8.0_2020-11-03", commit="54c38e6eaf557b844e70cebc00f39ced3321e9ad"
    )  # py-torch@1.8:1.9
    version(
        "1.7.0_2020-05-31", commit="a82c6a7010e2e332d8f74ad5b0c726fd47c85376"
    )  # py-torch@1.6:1.7
    version("1.6.0_2020-02-16", commit="9fdae4c68960a2d44cd1cc871c74a6a9d469fa1f")  # py-torch@1.5
    version("1.6.0_2019-11-06", commit="fea8568cac61a482ed208748fdc0e1a8e47f62f5")  # py-torch@1.4
    version("1.6.0_2019-09-26", commit="034921bd574cc84906b7996c07873454b7dd4135")  # py-torch@1.3
    version("1.5.0_2019-07-25", commit="28ca699b69b5a31892619defca2391044a9a6052")  # py-torch@1.2
    version("1.5.0_2019-04-25", commit="22662bfd4dcc6baebf29e3b823a051676f991001")  # py-torch@1.1
    version("1.3.0_2018-12-04", commit="42804705bdbf179d1a98394008417e1392013547")  # py-torch@1.0
    version(
        "1.2.2_2018-07-16", commit="b2817a682f25f960586f06caa539bbbd7a96b859"
    )  # py-torch@0.4.1
    version(
        "1.1.0_2018-04-19", commit="7e1bed51cc508a25b22130de459830b5d5063c41"
    )  # py-torch@0.4.0

    depends_on("cmake@3.1:", type="build")
    depends_on("ninja", type="build")
    depends_on("python", type="build")
    depends_on("protobuf")

    generator = "Ninja"

    def cmake_args(self):
        # Try to get ONNX to use the same version of python as the spec is using
        args = ["-DPY_VERSION={0}".format(self.spec["python"].version.up_to(2))]
        return args
