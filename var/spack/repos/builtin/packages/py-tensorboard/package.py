# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorboard(PythonPackage):
    """TensorBoard is a suite of web applications for
    inspecting and understanding your TensorFlow runs and
    graphs."""

    homepage = "https://github.com/tensorflow/tensorboard"
    url = "https://files.pythonhosted.org/packages/py3/t/tensorboard/tensorboard-2.9.1-py3-none-any.whl"
    list_url = "https://pypi.org/simple/tensorboard/"

    maintainers("aweits")

    version(
        "2.10.0",
        sha256="76c91a5e8959cd2208cc32cb17a0cb002badabb66a06ac2af02a7810f49a59e3",
        expand=False,
    )
    version(
        "2.9.1",
        sha256="baa727f791776f9e5841d347127720ceed4bbd59c36b40604b95fb2ae6029276",
        expand=False,
    )
    version(
        "2.9.0",
        sha256="bd78211076dca5efa27260afacfaa96cd05c7db12a6c09cc76a1d6b2987ca621",
        expand=False,
    )
    version(
        "2.8.0",
        sha256="65a338e4424e9079f2604923bdbe301792adce2ace1be68da6b3ddf005170def",
        expand=False,
    )
    version(
        "2.7.0",
        sha256="239f78a4a8dff200ce585a030c787773a8c1184d5c159252f5f85bac4e3c3b38",
        expand=False,
    )
    version(
        "2.6.0",
        sha256="f7dac4cdfb52d14c9e3f74585ce2aaf8e6203620a864e51faf84988b09f7bbdb",
        expand=False,
    )
    version(
        "2.5.0",
        sha256="e167460085b6528956b33bab1c970c989cdce47a6616273880733f5e7bde452e",
        expand=False,
    )
    version(
        "2.4.1",
        sha256="7b8c53c396069b618f6f276ec94fc45d17e3282d668979216e5d30be472115e4",
        expand=False,
    )
    version(
        "2.4.0",
        sha256="cde0c663a85609441cb4d624e7255fd8e2b6b1d679645095aac8a234a2812738",
        expand=False,
    )
    version(
        "2.3.0",
        sha256="d34609ed83ff01dd5b49ef81031cfc9c166bba0dabd60197024f14df5e8eae5e",
        expand=False,
    )
    version(
        "2.2.0",
        sha256="bb6bbc75ad2d8511ba6cbd49e4417276979f49866e11841e83da8298727dbaed",
        expand=False,
    )

    depends_on("python@2.7:2.8,3.2:", type=("build", "run"), when="@:2.5")
    depends_on("python@3.6:", type=("build", "run"), when="@2.6:")
    depends_on("py-absl-py@0.4:", type=("build", "run"))
    depends_on("py-grpcio@1.24.3:", type=("build", "run"), when="@2.3:")
    depends_on("py-grpcio@1.23.3:", type=("build", "run"), when="@2.2")
    depends_on("py-google-auth@1.6.3:1", type=("build", "run"), when="@:2.6")
    depends_on("py-google-auth@1.6.3:2", type=("build", "run"), when="@2.7:")
    depends_on("py-google-auth-oauthlib@0.4.1:0.4", type=("build", "run"))
    depends_on("py-markdown@2.6.8:", type=("build", "run"))
    depends_on("py-numpy@1.12.0:", type=("build", "run"))
    depends_on("py-protobuf@3.6.0:3.19", type=("build", "run"), when="@:2.8")
    depends_on("py-protobuf@3.9.2:3.19", type=("build", "run"), when="@2.9:")
    depends_on("py-requests@2.21.0:2", type=("build", "run"))
    depends_on("py-setuptools@41.0.0:", type=("build", "run"))
    depends_on("py-tensorboard-data-server@0.6", type=("build", "run"), when="@2.5:")
    depends_on("py-tensorboard-plugin-wit@1.6.0:", type=("build", "run"))
    depends_on("py-werkzeug@0.11.15:", type=("build", "run"))
    depends_on("py-werkzeug@1.0.1:", type=("build", "run"), when="@2.9:")
    depends_on("py-wheel@0.26:", type="build")
    depends_on("py-six@1.10.0:", type=("build", "run"), when="@:2.4")
