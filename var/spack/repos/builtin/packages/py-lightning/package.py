# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightning(PythonPackage):
    """The deep learning framework to pretrain, finetune and deploy AI models."""

    homepage = "https://github.com/Lightning-AI/pytorch-lightning"
    pypi = "lightning/lightning-2.0.0.tar.gz"
    skip_modules = ["lightning.app", "lightning.data", "lightning.store"]

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "2.2.1",
        sha256="fec9b49d29a6019e8fe49e825082bab8d5ea3fde8e4b36dcf5c8896c2bdb86c3",
        url="https://pypi.org/packages/a0/4a/b7d4f62449d940ce43d4657322a14f5718815b648f9d2b0b23a195acb646/lightning-2.2.1-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="28faa168ac8b9ef17eff4dc23b741972b8d60bc8ba02313e29dff5319d4a0ef7",
        url="https://pypi.org/packages/4e/09/862bd67d21826c0b738172de64646413f01cb90dc5d148c3f8fdeafd037d/lightning-2.2.0-py3-none-any.whl",
    )
    version(
        "2.1.4",
        sha256="b6c72d5f4c10e510a9e5b7b0cf2fde0d545b663697eb8dbdefd056ca50d23563",
        url="https://pypi.org/packages/0f/7a/61bd426456959e959643cee844d78ee090f0d6a34fb466a75254cd99586f/lightning-2.1.4-py3-none-any.whl",
    )
    version(
        "2.1.3",
        sha256="a1ab244c3899d6316794d5e8b2f3fd0ce56feddf8fbd4cabfc6ded3dd5e80fa5",
        url="https://pypi.org/packages/8c/a1/b2a6c33675510bc3e1ca6d010b244ac0dd9c81fc1723a37e7491aa586041/lightning-2.1.3-py3-none-any.whl",
    )
    version(
        "2.1.2",
        sha256="f23358dedd8f5f1151475c9d95f33e4529591c992a99cb9ae89c84bca7289525",
        url="https://pypi.org/packages/9e/8a/9642fdbdac8de47d68464ca3be32baca3f70a432aa374705d6b91da732eb/lightning-2.1.2-py3-none-any.whl",
    )
    version(
        "2.1.1",
        sha256="c1ea10fd112600eda5210bf3dc6d01d82cec6d70a6187e44b800cbb50be7346e",
        url="https://pypi.org/packages/08/f0/617fede29ec0684b310bd2a0c880e640c60b9f2d64ed3d77e2bca2c13bf9/lightning-2.1.1-py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="c12bd10bd28b9e29a8e877be039350a585f248c10b76360faa2aa2497f980de6",
        url="https://pypi.org/packages/08/c7/8c33e2660161a99923fa9b46c72c31884efd482b89f7ead970cee5c0072a/lightning-2.1.0-py3-none-any.whl",
    )
    version(
        "2.0.9",
        sha256="5866cc500fbe816046dd1ea3bc12512ed570fdcfab413647c68b515a15def62e",
        url="https://pypi.org/packages/2f/90/2a2bc44409df179e3959209c2b16b4dab438a116fdd0b52470a0e2f1f0be/lightning-2.0.9-py3-none-any.whl",
    )
    version(
        "2.0.8",
        sha256="42ccc2b622d5ee54322d8f96170da00abc35ace97ec8acaa25e709cf017fd0c8",
        url="https://pypi.org/packages/a6/a3/e3caca2bb110ad5f33b485d48a6b604d104842b922914c973c0231916131/lightning-2.0.8-py3-none-any.whl",
    )
    version(
        "2.0.7",
        sha256="814b371d0715e154b97e3d3108e19d1f96ce1a0f36ef27454f97a3f2f29ac5e7",
        url="https://pypi.org/packages/f6/7d/fdd855f4ecf8525af8026097e433aeb90ebc965fe9f179b1d4900a83cba1/lightning-2.0.7-py3-none-any.whl",
    )
    version(
        "2.0.6",
        sha256="283fb8fd143fa30da1b2cadff4c38509a9b5b88518d0bcc69bab6d76a730865f",
        url="https://pypi.org/packages/53/95/574af29ac656b845f56ce4ff8002119ace2477c90617937f11f1673c841a/lightning-2.0.6-py3-none-any.whl",
    )
    version(
        "2.0.5",
        sha256="965d692597ddf73364c74c99db58e11cf144f0e9a3052ec1b0474b4829c17c85",
        url="https://pypi.org/packages/d2/b2/d5ec3d480c4b9ae08000de90ebfb9962580b379164020686d08eb06e42aa/lightning-2.0.5-py3-none-any.whl",
    )
    version(
        "2.0.4",
        sha256="812b3d59d153f4f47db5e4907310412439c5ff2c5899b8413652627372bc9131",
        url="https://pypi.org/packages/07/db/cc068abd357f290ff2a7249e39540be140b8b29df34b568218ee8a0209c8/lightning-2.0.4-py3-none-any.whl",
    )
    version(
        "2.0.3",
        sha256="8ca7566a5db58e3fca6b120244850a107f00047803119f722fc491a49c5ffa78",
        url="https://pypi.org/packages/6c/cf/b0963d28ae7206c57bd4677714d0fb563a1547324db1fd199dea1b1a3d2f/lightning-2.0.3-py3-none-any.whl",
    )
    version(
        "2.0.2",
        sha256="fcdc2f6fe43543e0d1eb2058c49c7920b89b02184ecead138955e915e2ad3982",
        url="https://pypi.org/packages/43/29/2d024e913ae92f7992592148503b69cc7b3eb3f47b030ef3234bf4b5623c/lightning-2.0.2-py3-none-any.whl",
    )
    version(
        "2.0.1",
        sha256="d43ba45bd0ce7da3e22d31a057dbef47c07403b94dc3ae51d66f97791a92bb6e",
        url="https://pypi.org/packages/a9/62/b8f3a21e82cdf98e02167ab912c9a76ae40c53911ed37849b9944a7ee97b/lightning-2.0.1-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="ef5643acb1aca604a1812ef101ae7c64c9992343818a84d7f1dda272fbb9a7bc",
        url="https://pypi.org/packages/5c/34/b585d91d04b90d7072e884f91d1e93a91a415605411e06f963da1aca3078/lightning-2.0.0-py3-none-any.whl",
    )
    version(
        "1.9.5",
        sha256="a438d08e42de5a602378481c45e64f737ced1b8b13039368869a210402b69f35",
        url="https://pypi.org/packages/ae/81/bfbe03c8b910b526fd0be67ea73e61f67b93e9eab3a5633614982db5422e/lightning-1.9.5-py3-none-any.whl",
    )

    variant("pytorch-extra", default=False)

    with default_args(type="run"):
        depends_on("py-arrow@1.2:", when="@1.9:2.1.0-rc0")
        depends_on("py-backoff@2.2.1:", when="@2.0.5:2.1.0-rc0")
        depends_on("py-beautifulsoup4@4.8:", when="@1.9:2.1.0-rc0")
        depends_on("py-bitsandbytes@0.41:0.41.0", when="@2.2+pytorch-extra")
        depends_on("py-bitsandbytes", when="@2.1.1:2.1+pytorch-extra")
        depends_on("py-click", when="@1.9:2.1.0-rc0")
        depends_on("py-croniter@1.3:1", when="@2.0.5:2.1.0-rc0")
        depends_on("py-croniter@1.3", when="@:2.0.4")
        depends_on("py-dateutils", when="@1.9.0:2.1.0-rc0")
        depends_on("py-deepdiff@5.7:", when="@1.9:2.1.0-rc0")
        depends_on("py-fastapi@0.92:", when="@2.0.4:2.1.0-rc0")
        depends_on("py-fastapi@0.69:0.88", when="@2.0.2:2.0.3")
        depends_on("py-fastapi@:0.88", when="@1.9.0:2.0.1")
        depends_on("py-fsspec@2022.5:+http", when="@2.1.3:2.2")
        depends_on("py-fsspec@2022.5:", when="@2.0.5:2.1.0-rc0")
        depends_on("py-fsspec@2021.6.1:+http", when="@1.9.1:2.1.2")
        depends_on("py-fsspec@2022.5:2023", when="@1.9.0:2.0.4")
        depends_on("py-fsspec@2021.6.1:2023+http", when="@1.9.0")
        depends_on("py-hydra-core@1.0.5:", when="@1.9:2.2+pytorch-extra")
        depends_on("py-inquirer@2.10:", when="@1.9.0:2.1.0-rc0")
        depends_on("py-jinja2", when="@1.9.0:2.1.0-rc0")
        depends_on("py-jsonargparse@4.26.1:+signatures", when="@2.1.3:2.2+pytorch-extra")
        depends_on("py-jsonargparse@4.18:4.24+signatures", when="@2.0.9:2.0+pytorch-extra")
        depends_on("py-jsonargparse@4.18:4.22+signatures", when="@2.0.7:2.0.8+pytorch-extra")
        depends_on(
            "py-jsonargparse@4.18:+signatures", when="@1.9:2.0.6,2.1.0-rc1:2.1.2+pytorch-extra"
        )
        depends_on("py-lightning-cloud@0.5.38:", when="@2.0.9:2.0")
        depends_on("py-lightning-cloud@0.5.37:", when="@2.0.5:2.0.8,2.1:2.1.0-rc0")
        depends_on("py-lightning-cloud@0.5.34:", when="@2.0.2:2.0.4")
        depends_on("py-lightning-cloud@0.5.31:", when="@2.0.0:2.0.1")
        depends_on("py-lightning-cloud@0.5.27:", when="@1.9.4:2.0.0-rc0")
        depends_on("py-lightning-utilities@0.8:", when="@2.1:2.2")
        depends_on("py-lightning-utilities@0.7:", when="@2.0.0:2.0")
        depends_on("py-lightning-utilities@0.6.0.post:", when="@1.9.1:2.0.0-rc0")
        depends_on("py-matplotlib@3.1.1:", when="@1.9:2.2+pytorch-extra")
        depends_on("py-numpy@1.17.2:", when="@1.9.0:2.2")
        depends_on("py-omegaconf@2.0.5:", when="@1.9:2.2+pytorch-extra")
        depends_on("py-packaging@20:", when="@2.1:2.2")
        depends_on("py-packaging@17.1:", when="@1.9.1:2.0")
        depends_on("py-packaging", when="@:2.1.0-rc0,2022:2022.6")
        depends_on("py-psutil", when="@:2.1.0-rc0")
        depends_on("py-pydantic@1.7.4:2.1", when="@2.0.7:2.1.0-rc0")
        depends_on("py-pydantic@1.7.4:2.0", when="@2.0.6")
        depends_on("py-pydantic@1.7.4:1", when="@2.0.5")
        depends_on("py-pydantic@1.7.4:", when="@2.0.2:2.0.4")
        depends_on("py-pydantic", when="@1.9.0:2.0.1")
        depends_on("py-python-multipart@0.0.5:", when="@2.0.3:2.1.0-rc0")
        depends_on("py-pytorch-lightning", when="@2.0.0:2")
        depends_on("py-pyyaml@5.4:", when="@1.9.0:2.2")
        depends_on("py-pyyaml", when="@1.9.0:2.1.0-rc0")
        depends_on("py-requests", when="@1.9.0:2.1.0-rc0")
        depends_on("py-rich@12.3:", when="@2.0.0:2.2+pytorch-extra")
        depends_on("py-rich@12.3:", when="@2.0.0:2.1.0-rc0")
        depends_on("py-rich", when="@1.9.0:2.0.0-rc0")
        depends_on("py-rich@10.14,10.15.0-alpha2:", when="@1.9:2.0.0-rc0+pytorch-extra")
        depends_on("py-starlette", when="@1.9.0:2.1.0-rc0")
        depends_on("py-starsessions@1.2:1", when="@:2.1.0-rc0")
        depends_on("py-tensorboardx@2.2:", when="@1.9.0:2.2+pytorch-extra")
        depends_on("py-tensorboardx@2.2:", when="@1.9:1.9.0-rc0")
        depends_on("py-torch@1.13:", when="@2.2")
        depends_on("py-torch@1.12:", when="@2.1.0-rc1:2.1")
        depends_on("py-torch@1.11:", when="@2:2.1.0-rc0")
        depends_on("py-torch@1.10:", when="@1.9.5:1")
        depends_on("py-torchmetrics@0.7.0:", when="@1.9.0:2.2")
        depends_on("py-tqdm@4.57:", when="@1.9.0:2.2")
        depends_on("py-traitlets@5.3:5.3.0.0,5.4:", when="@1.9:2.1.0-rc0")
        depends_on("py-typing-extensions@4.4:", when="@2.2")
        depends_on("py-typing-extensions@4:", when="@1.9:2.1")
        depends_on("py-urllib3", when="@1.9.0:2.1.0-rc0")
        depends_on("py-uvicorn", when="@1.9.0:2.1.0-rc0")
        depends_on("py-websocket-client", when="@1.9.0:2.1.0-rc0")
        depends_on("py-websockets", when="@2.0.5:2.1.0-rc0")
        depends_on("py-websockets@:11", when="@1.9.0:2.0.4")

    # https://github.com/Lightning-AI/lightning/issues/18858
    conflicts("^py-torch~distributed", when="@2.1.0")
