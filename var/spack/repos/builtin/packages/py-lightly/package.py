# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightly(PythonPackage):
    """A deep learning package for self-supervised learning."""

    homepage = "https://www.lightly.ai/"
    # https://github.com/lightly-ai/lightly/issues/1146
    url = "https://github.com/lightly-ai/lightly/archive/refs/tags/v1.4.1.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version(
        "1.5.0",
        sha256="d17e6b09e2b3b50a02e976dad88bf8d11c7018ffdbe54edd783b7e9911f0892e",
        url="https://pypi.org/packages/82/81/866ee00fe5a112af2d940f37d2642545fa33f3625c551504bd1f5866423f/lightly-1.5.0-py3-none-any.whl",
    )
    version(
        "1.4.26",
        sha256="f1477299003c8076ecad70266dc721fec4dc4a69b1fea247c8fa10a809b94d89",
        url="https://pypi.org/packages/55/3a/d665499e854855390c6c622a47f356a8aa67eb0f88f7b2996861a85558b7/lightly-1.4.26-py3-none-any.whl",
    )
    version(
        "1.4.25",
        sha256="81c65bc53a88feb9f8e8cb8a077baa2edec87d609907fc557bb31ea8068c5289",
        url="https://pypi.org/packages/de/25/8f711c8ecf720e16e99f0cb5ef287ce16795c97aaefd7d8c57b4b000ded8/lightly-1.4.25-py3-none-any.whl",
    )
    version(
        "1.4.18",
        sha256="405805ca145169dfe5994f4ea18fb853a5a6138dc33b7c669f3de4e1e04c5ef0",
        url="https://pypi.org/packages/68/bc/2e373e7bb5b4a5286b4678a3166820e156e46b1a70f650d357587dcbaee6/lightly-1.4.18-py3-none-any.whl",
    )
    version(
        "1.4.17",
        sha256="f8619d9c0d51fc71ba23ac01832a1c8ea433633160f4223ab384a113d36f4722",
        url="https://pypi.org/packages/61/99/afb8740d63280e48792d7d3fa1b07f1e128a4c0bd60702b506e1f6d923a2/lightly-1.4.17-py3-none-any.whl",
    )
    version(
        "1.4.16",
        sha256="1132ac729bf6a0263f1cd9fcdda8b376f55bfa7f3f71dafe0f75a184a2f278eb",
        url="https://pypi.org/packages/b4/ff/9d8efc9e3f1f9a863ad9b8a63c6ac2ab746b61c749a7e8831185a61131eb/lightly-1.4.16-py3-none-any.whl",
    )
    version(
        "1.4.15",
        sha256="2cca4efc060b5499df22cdd0e66a5748b44277275316495465218022352e7f6e",
        url="https://pypi.org/packages/4f/5e/fcbc949527c3ddd1f1d66a70feaef5cf60b31de17a81675beea952eb237c/lightly-1.4.15-py3-none-any.whl",
    )
    version(
        "1.4.14",
        sha256="eab2e5ccb250c31084a5d7645fb2f5713f9e23811369533db276e6a39ac1f5a9",
        url="https://pypi.org/packages/8a/80/982771ee702152aebbad9befc70a78242a6291741acfd55c25825d070c92/lightly-1.4.14-py3-none-any.whl",
    )
    version(
        "1.4.13",
        sha256="71a70dfe975edeef9f12fecd7f8aa613183b22ab8091da821a8cf81d4750fca7",
        url="https://pypi.org/packages/7e/12/d85154c03dd9941a15dc6820ae7ac0b19255257003d32bdf64df72fb1724/lightly-1.4.13-py3-none-any.whl",
    )
    version(
        "1.4.12",
        sha256="96cd571c6e6c0764eb92ba8ef95a79778054a04e111bbfc5c5f040fcb9e3d4a9",
        url="https://pypi.org/packages/9a/2e/bed6f1038a39e3f633406aee79aaf3a98ccf846ace7993f5fcf7078a9fff/lightly-1.4.12-py3-none-any.whl",
    )
    version(
        "1.4.11",
        sha256="b61bf95e0402184f18b7636ece4532433db0722964cca83acca44425a60646dd",
        url="https://pypi.org/packages/a0/eb/502091271bf78c71c7c865911a55d56320bb8a12c6b12feb83fedb575e8e/lightly-1.4.11-py3-none-any.whl",
    )
    version(
        "1.4.10",
        sha256="50b98c5d229c33f43557185b8256cc2986c9b09adada1e78d3147072289146c2",
        url="https://pypi.org/packages/29/05/a548cdadd4bda103089580e32864b83b0e35dacae0ab1f64dedf7c741765/lightly-1.4.10-py3-none-any.whl",
    )
    version(
        "1.4.8",
        sha256="7c0b7186dece1d0f1158a969827052ef79c4043f72e7203f3de9999c11b03784",
        url="https://pypi.org/packages/ac/c2/09929cb5b6f4d902bf3325b7f5923518e9fa6469382afc615716a3017349/lightly-1.4.8-py3-none-any.whl",
    )
    version(
        "1.4.7",
        sha256="3ff2d6c09782ff0751a34248a0a4503411b6a47ad9a93b506bcb190354ef2fa0",
        url="https://pypi.org/packages/c8/84/78e2f25edbd2da75da2b98f0c21ebb59cfae87661a7a61dc6037d443d932/lightly-1.4.7-py3-none-any.whl",
    )
    version(
        "1.4.6",
        sha256="ac0ba388a63434f7bd9f1561705370c0b254e76fe911f297fcbd990058864e7a",
        url="https://pypi.org/packages/2c/5d/eca1e83ed2be260c07cd4fbb6de3857053810f71f68dc7e6c4650e5eb62b/lightly-1.4.6-py3-none-any.whl",
    )
    version(
        "1.4.5",
        sha256="0eea156efa7c13a51f86cf3333158fc0ce8fc779b8720da4d92426399543b468",
        url="https://pypi.org/packages/71/ed/057a233c9938aed792b4c3fb060510e4f55881b7c42492aab4a676c2e140/lightly-1.4.5-py3-none-any.whl",
    )
    version(
        "1.4.4",
        sha256="b73592ebaed770f0284a03eda56f6631829f5940ccdcdf5ff9ae860b0ef15ab6",
        url="https://pypi.org/packages/2f/56/3e9e5123d032b9e942a75d9976151ce5082c0a62c23606644854519d8c74/lightly-1.4.4-py3-none-any.whl",
    )
    version(
        "1.4.3",
        sha256="501e88da56c7426048a6200531f413b6ceaa384fe6120aa27e241d2fb25e3923",
        url="https://pypi.org/packages/a1/2b/1e9e37961d1f1eb85cdfa2409f17943d549b60acb8c7cd31d911b1cb7352/lightly-1.4.3-py3-none-any.whl",
    )
    version(
        "1.4.2",
        sha256="4e931d2aff77a61f5ee4cf4fccdacae6df4945be196eee78ddd678a28d9eb210",
        url="https://pypi.org/packages/fe/12/29a57e70e017d63adad6d60c42cd8b5e13d046dbf53f452bf4cd9e69df9d/lightly-1.4.2-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="5c9890910e2574ab913824daae8c393467fa32fd227e8f976fc7b8509a3066bc",
        url="https://pypi.org/packages/7f/62/a19d0f3555bd031216cbf0e0f72b9b54bb8c7ef8b8a760d031108952304f/lightly-1.4.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-aenum@3.1.11:", when="@1.4.8:")
        depends_on("py-certifi@14:")
        depends_on("py-hydra-core@1.0.0:")
        depends_on("py-lightly-utils")
        depends_on("py-numpy@1.18.1:")
        depends_on("py-pydantic@1.10.5:1", when="@1.4.8:")
        depends_on("py-python-dateutil@2.5.3:")
        depends_on("py-pytorch-lightning@1.0.4:")
        depends_on("py-requests@2.23:")
        depends_on("py-setuptools@21:", when="@1.4.8,1.4.15:1.4.25")
        depends_on("py-setuptools@21:65.5", when="@:1.4.1")
        depends_on("py-six@1.10:")
        depends_on("py-torch", when="@1.4.2:")
        depends_on("py-torchvision")
        depends_on("py-tqdm@4.44:")
        depends_on("py-urllib3@1.25.3:", when="@1.4.8:")
        depends_on("py-urllib3@1.15.1:", when="@:1.4.25")

    # setup.py

    # requirements/base.txt

    # requirements/torch.txt

    # https://github.com/lightly-ai/lightly/issues/1153

    # https://github.com/microsoft/torchgeo/issues/1824
    conflicts("py-timm@:0.9.8", when="@1.4.26")
