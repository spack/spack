# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOnnx(PythonPackage):
    """Open Neural Network Exchange (ONNX) is an open ecosystem that
    empowers AI developers to choose the right tools as their
    project evolves. ONNX provides an open source format for AI
    models, both deep learning and traditional ML. It defines an
    extensible computation graph model, as well as definitions of
    built-in operators and standard data types. Currently we focus
    on the capabilities needed for inferencing (scoring)."""

    homepage = "https://github.com/onnx/onnx"
    pypi = "Onnx/onnx-1.6.0.tar.gz"

    version("1.12.0", sha256="13b3e77d27523b9dbf4f30dfc9c959455859d5e34e921c44f712d69b8369eff9")
    version("1.11.0", sha256="eca224c7c2c8ee4072a0743e4898a84a9bdf8297b5e5910a2632e4c4182ffb2a")
    version("1.10.1", sha256="9d941ba76cab55db8913ecad9dc50cefeb368460f6338a91783a5d7643f3a044")
    version("1.8.1", sha256="9d65c52009a90499f8c25fdfe5acda3ac88efe0788eb1d5f2575a989277145fb")
    version("1.6.0", sha256="3b88c3fe521151651a0403c4d131cb2e0311bd28b753ef692020a432a81ce345")
    version("1.5.0", sha256="1a584a4ef62a6db178c257fffb06a9d8e61b41c0a80bfd8bcd8a253d72c4b0b4")

    depends_on("py-setuptools", type="build")
    depends_on("protobuf")
    depends_on("py-protobuf+cpp", type=("build", "run"))
    # Protobuf version limit is due to removal of SetTotalBytesLimit in
    # https://github.com/protocolbuffers/protobuf/pull/8794, fixed in
    # https://github.com/onnx/onnx/pull/3112
    depends_on("protobuf@:3.17", when="@:1.8")
    depends_on("py-protobuf@:3.17", when="@:1.8", type=("build", "run"))
    # https://github.com/protocolbuffers/protobuf/issues/10051
    # https://github.com/onnx/onnx/issues/4222
    depends_on("protobuf@:3", when="@1.10.1")
    depends_on("py-protobuf@:3", type=("build", "run"), when="@1.10.1")
    depends_on("protobuf@3.12.2:", when="@1.11.0")
    depends_on("py-protobuf@3.12.2:", type=("build", "run"), when="@1.11.0")
    depends_on("protobuf@3.12.2:3.20.1", when="@1.12.0:")
    depends_on("py-protobuf@3.12.2:3.20.1", type=("build", "run"), when="@1.12.0:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-numpy@1.16.6:", type=("build", "run"), when="@1.8.1:")
    depends_on("py-six", type=("build", "run"), when="@:1.8.1")
    depends_on("py-typing-extensions@3.6.2.1:", type=("build", "run"))
    depends_on("cmake@3.1:", type="build")
    depends_on("py-pytest-runner", type="build")

    # 'python_out' does not recognize dllexport_decl.
    patch("remove_dllexport_decl.patch", when="@:1.6.0")
