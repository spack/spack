# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTimm(PythonPackage):
    """(Unofficial) PyTorch Image Models."""

    homepage = "https://github.com/rwightman/pytorch-image-models"
    pypi = "timm/timm-0.4.12.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "0.9.5",
        sha256="6e70af3a347bddb4167db46c3252a83c59165332ecf6b3df480d49c22866fa46",
        url="https://pypi.org/packages/14/38/05b37b7692e521bbada22593ac3b6d7ba3f378d56b5d1ccb322a541bbb6e/timm-0.9.5-py3-none-any.whl",
    )
    version(
        "0.9.2",
        sha256="8da40cc58ed32b0622bf87d8714f9b7023398ba4cfa8fa678578d2aefde4a909",
        url="https://pypi.org/packages/29/90/94f5deb8d76e24a89813aef95e8809ca8fd7414490428480eda19b133d4a/timm-0.9.2-py3-none-any.whl",
    )
    version(
        "0.9.1",
        sha256="af5fff9a3f33abf7224bdc1b33dd21ba129207c84ec1e035f20aec03b71832d8",
        url="https://pypi.org/packages/ca/68/92012b248227134be8f5babdca3f684129175c902ef4f9cbd5fb3dd3945f/timm-0.9.1-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="1aeb4e3bbb1bfaa775b3f49e80bfaebfe45efb0b4733d0c57653a121a15d48a8",
        url="https://pypi.org/packages/38/b5/068b486caa27fa2d883dfc499dadd38e0065a33695182eda552f4d3c53b2/timm-0.9.0-py3-none-any.whl",
    )
    version(
        "0.6.13",
        sha256="ea5aed42f94062a80da414e6f1791cb82012fdb54f7db72c607637914a521345",
        url="https://pypi.org/packages/f6/c6/806d9b2fa95f418ad700dd206a935d5e8d7355505589dd13a70eb3a45048/timm-0.6.13-py3-none-any.whl",
    )
    version(
        "0.6.12",
        sha256="3dfa19b82afa707acc0c2392a84c0e549dd9ea626c285fb2e8d9e4073b58dbd1",
        url="https://pypi.org/packages/89/4e/97622efc48a6e0c11781ed8a3472c679f2c8a5cf6ebd58a57b050e758bfe/timm-0.6.12-py3-none-any.whl",
    )
    version(
        "0.5.4",
        sha256="0592c8fd2d46d0769c0b7e954b3dacea93769eee40dabb4bd7f2acb85243b588",
        url="https://pypi.org/packages/49/65/a83208746dc9c0d70feff7874b49780ff110810feb528df4b0ecadcbee60/timm-0.5.4-py3-none-any.whl",
    )
    version(
        "0.4.12",
        sha256="dba6b1702b7d24bf9f0f1c2fc394b4ee28f93cde5404f1dc732d63ccd00533b6",
        url="https://pypi.org/packages/90/fc/606bc5cf46acac3aa9bd179b3954433c026aaf88ea98d6b19f5d14c336da/timm-0.4.12-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.6.13:0.6,0.8.13:0.9.12")
        depends_on("py-huggingface-hub", when="@0.6.11:")
        depends_on("py-pyyaml", when="@0.6.11:")
        depends_on("py-safetensors", when="@0.8.13:")
        depends_on("py-torch@1.7:", when="@0.6.11:0.9.12")
        depends_on("py-torch@1.4:", when="@0.2,0.3.4:0.6.7")
        depends_on("py-torchvision")

    # https://github.com/huggingface/pytorch-image-models/commit/f744bda994ec305a823483bf52a20c1440205032
    # https://github.com/huggingface/pytorch-image-models/issues/1530
    # https://github.com/huggingface/pytorch-image-models/pull/1649

    # https://github.com/rwightman/pytorch-image-models/pull/1256
