# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyS3transfer(PythonPackage):
    """S3transfer is a Python library for managing Amazon S3 transfers."""

    homepage = "https://github.com/boto/s3transfer"
    pypi = "s3transfer/s3transfer-0.2.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.10.0",
        sha256="3cdb40f5cfa6966e812209d0994f2a4709b561c88e90cf00c2696d2df4e56b2e",
        url="https://pypi.org/packages/12/bb/7e7912e18cd558e7880d9b58ffc57300b2c28ffba9882b3a54ba5ce3ebc4/s3transfer-0.10.0-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="01d4d2c35a016db8cb14f9a4d5e84c1f8c96e7ffc211422555eed45c11fa7eb1",
        url="https://pypi.org/packages/fd/fb/46eda754e80fa2efd82981e37cd75cabbecef71df63843e6e94e12fae9db/s3transfer-0.9.0-py3-none-any.whl",
    )
    version(
        "0.8.2",
        sha256="c9e56cbe88b28d8e197cf841f1f0c130f246595e77ae5b5a05b69fe7cb83de76",
        url="https://pypi.org/packages/75/ca/5399536cbd5889ca4532d4b8bbcd17efa0fe0be0da04e143667a4ff5644e/s3transfer-0.8.2-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="10d6923c6359175f264811ef4bf6161a3156ce8e350e705396a7557d6293c33a",
        url="https://pypi.org/packages/5a/4b/fec9ce18f8874a96c5061422625ba86c3ee1e6587ccd92ff9f5bf7bd91b2/s3transfer-0.7.0-py3-none-any.whl",
    )
    version(
        "0.6.2",
        sha256="b014be3a8a2aab98cfe1abc7229cc5a9a0cf05eb9c1f2b86b230fd8df3f78084",
        url="https://pypi.org/packages/d9/17/a3b666f5ef9543cfd3c661d39d1e193abb9649d0cfbbfee3cf3b51d5af02/s3transfer-0.6.2-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="06176b74f3a15f61f1b4f25a1fc29a4429040b7647133a463da8fa5bd28d5ecd",
        url="https://pypi.org/packages/5e/c6/af903b5fab3f9b5b1e883f49a770066314c6dcceb589cf938d48c89556c1/s3transfer-0.6.0-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="9c1dc369814391a6bda20ebbf4b70a0f34630592c9aa520856bf384916af2803",
        url="https://pypi.org/packages/ab/84/fc3717a7b7f0f6bb08af593127171f08e3e0087c197922da09c01bfe7c3a/s3transfer-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.2",
        sha256="9b3752887a2880690ce628bc263d6d13a3864083aeacff4890c1c9839a5eb0bc",
        url="https://pypi.org/packages/63/d0/693477c688348654ddc21dcdce0817653a294aa43f41771084c25e7ff9c7/s3transfer-0.4.2-py2.py3-none-any.whl",
    )
    version(
        "0.3.4",
        sha256="1e28620e5b444652ed752cf87c7e0cb15b0e578972568c6609f0f18212f259ed",
        url="https://pypi.org/packages/ea/43/4b4a1b26eb03a429a4c37ca7fdf369d938bd60018fc194e94b8379b0c77c/s3transfer-0.3.4-py2.py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="b780f2411b824cb541dbcd2c713d0cb61c7d1bcadae204cdddda2b35cef493ba",
        url="https://pypi.org/packages/16/8a/1fc3dba0c4923c2a76e1ff0d52b305c44606da63f718d14d3231e21c51b0/s3transfer-0.2.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.9:")
        depends_on("python@3.7:", when="@0.6:0.8")
        depends_on("py-botocore@1.33.2:", when="@0.8.1:")
        depends_on("py-botocore@1.12.36:", when="@0.3.4:0.7")
