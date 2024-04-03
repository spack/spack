# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytorchLightning(PythonPackage):
    """PyTorch Lightning is the lightweight PyTorch wrapper for ML researchers."""

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "pytorch-lightning/pytorch-lightning-1.2.10.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "2.0.0",
        sha256="eda04e51c3ca030f92f9eb30cbb10583575b4144a155cfd6b7d17e1bb9a08ffe",
        url="https://pypi.org/packages/4c/6e/8a0b395b4058bd7e24a8f6a572255b815723d67ed65a121da25346f3148d/pytorch_lightning-2.0.0-py3-none-any.whl",
    )
    version(
        "1.9.4",
        sha256="a2d2bd7657716087c294b076fe385ed17879764d6daaad0a541394a8f7164f93",
        url="https://pypi.org/packages/ce/ac/09980114432e759e56e8ff35c16d05dd7c8c0f512c9a88a91c5110272a1f/pytorch_lightning-1.9.4-py3-none-any.whl",
    )
    version(
        "1.9.3",
        sha256="cd642fbbe763968269637835efe68833dd5019801359c950c04898e355b74fea",
        url="https://pypi.org/packages/bf/9d/ba77d6d9fd7ca5ff7260ae5033c2355e6f920d3dad764ef107d8c2b54a27/pytorch_lightning-1.9.3-py3-none-any.whl",
    )
    version(
        "1.9.2",
        sha256="a92c4053c4a57cc79778e9317b5aac57b0594b0f1718909730ab8a5b529639dc",
        url="https://pypi.org/packages/5b/37/879011263bb09039463e5e86e2434c5a952613028cf941580ea4d303a21a/pytorch_lightning-1.9.2-py3-none-any.whl",
    )
    version(
        "1.9.1",
        sha256="c143ee0a7e4c5779b54aa1bf1ae5faa19ed3e5546e31dad4a0298db6b115cc21",
        url="https://pypi.org/packages/8b/2d/d556b71fbb6a61e452d75de8dccc6b192e52877a53e7f95da26a8455e2b9/pytorch_lightning-1.9.1-py3-none-any.whl",
    )
    version(
        "1.9.0",
        sha256="fcd19d985db8d1a9656faaed80bb79a3548f2ed0471c05c089e01e0fb7ff92b2",
        url="https://pypi.org/packages/71/a5/e8f046591b09d9e92582cf2ef3c3a40fcca829cae250521ae593c7236bed/pytorch_lightning-1.9.0-py3-none-any.whl",
    )
    version(
        "1.8.6",
        sha256="8b6b4126b85c56a9dd08a03f7096ce749bcb452a9a50f6201a7165dbd92d866d",
        url="https://pypi.org/packages/7a/b8/8f5d44a83f5243163b04cad2985e3d1ccf7db24d9a23c73362c5202d2a33/pytorch_lightning-1.8.6-py3-none-any.whl",
    )
    version(
        "1.8.5",
        sha256="0d690ee2792376472f81d423d24c4dc5f465aaf4fb97a0841e63d880b08df52c",
        url="https://pypi.org/packages/88/f3/2c821db2fb6a353d55b5732288db32751af18e45d1980f5480a7ea8ce052/pytorch_lightning-1.8.5-py3-none-any.whl",
    )
    version(
        "1.8.4",
        sha256="9ef0af4c02f20c46572168f6a64c0b6bc18a7a065a5943d430e1d4aaf9a69e91",
        url="https://pypi.org/packages/bc/e4/3ff865f284e2bf55c70bb38aa9c7dd5a73286f3d3bac395e4904b9d53384/pytorch_lightning-1.8.4-py3-none-any.whl",
    )
    version(
        "1.5.3",
        sha256="e4a9563a2922d023e98c3a660cee5ef9d8b0c43a3c79509b8721837434e37c18",
        url="https://pypi.org/packages/8d/2f/8010a8c5d20ed162abeed75e870eedf7fbf4a9ab30b0f06ab548107b4e1a/pytorch_lightning-1.5.3-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="4a06723a66296a2ac94cdf353335d64e7ae76c37202b2a4c38a845063e3fe386",
        url="https://pypi.org/packages/68/3a/3d1d3985158fa1573164a4cf1aa9e2347a089dd1d5f62fb82dd395dd124a/pytorch_lightning-1.4.1-py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="41fb26e649b830019ecdffb6dc6558266e1317963f7bf2cddb1f1ed862245928",
        url="https://pypi.org/packages/a2/6b/09d5a5ab8ff20aab86516020751323db6cef8df88c310acad0b9a705a80b/pytorch_lightning-1.4.0-py3-none-any.whl",
    )
    version(
        "1.3.8",
        sha256="f3ccd987d6df628e0339925239dcf20a787e2ce01310f3cab49a58218fe0357b",
        url="https://pypi.org/packages/48/5e/19c817ad2670c1d822642ed7bfc4d9d4c30c2f8eaefebcd575a3188d7319/pytorch_lightning-1.3.8-py3-none-any.whl",
    )
    version(
        "1.2.10",
        sha256="52d05dda39e6ddd7ab6775c4ca8943e7881000acd9c9218c7e3c9feae43489b2",
        url="https://pypi.org/packages/07/0c/e2d52147ac12a77ee4e7fd7deb4b5f334cfb335af9133a0f2780c8bb9a2c/pytorch_lightning-1.2.10-py3-none-any.whl",
    )

    variant("extra", default=False, description="extra")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2:")
        depends_on("python@3.7:", when="@1.8:1")
        depends_on("py-fsspec@2021.6.1:+http", when="@1.8:2.1.2")
        depends_on("py-fsspec@2021.5,2021.6.1:+http", when="@1.3.5:1.5")
        depends_on("py-fsspec@0.8.1:+http", when="@:1.3.0-rc1")
        depends_on("py-future@0.17.1:", when="@:1.5")
        depends_on("py-gcsfs@2021.5:", when="@1.4:1.5+extra")
        depends_on("py-horovod@0.21.2:", when="@:1.5+extra")
        depends_on("py-hydra-core@1.0.5:", when="@1.5.0:+extra")
        depends_on("py-hydra-core@1.0.0:", when="@:1.5.0-rc1+extra")
        depends_on("py-jsonargparse@4.18:+signatures", when="@1.9:2.0.6,2.1.0-rc1:2.1.2+extra")
        depends_on("py-jsonargparse@4.15.2:+signatures", when="@1.8+extra")
        depends_on("py-jsonargparse@3.19.3:+signatures", when="@1.5+extra")
        depends_on("py-jsonargparse@3.17:+signatures", when="@1.4.0-rc2:1.4+extra")
        depends_on("py-jsonargparse@3.13.1:+signatures", when="@1.3.5:1.3+extra")
        depends_on("py-lightning-utilities@0.7:", when="@2.0.0:2.0")
        depends_on("py-lightning-utilities@0.6.0.post:", when="@1.9.1:2.0.0-rc0")
        depends_on("py-lightning-utilities@0.4.2:", when="@1.9:1.9.0")
        depends_on("py-lightning-utilities@0.3,0.4.1:", when="@1.8")
        depends_on("py-matplotlib@3.1.1:", when="+extra")
        depends_on("py-numpy@1.17.2:", when="@1.3.0-rc2:")
        depends_on("py-numpy@1.16.6:", when="@:1.3.0-rc1")
        depends_on("py-omegaconf@2.0.5:", when="@1.5.0:+extra")
        depends_on("py-omegaconf@2.0.1:", when="@:1.5.0-rc1+extra")
        depends_on("py-onnx@1.7:", when="@:1.2.3,1.4:1.5.0-rc1+extra")
        depends_on("py-onnxruntime@1.3:", when="@:1.5.0-rc1+extra")
        depends_on("py-packaging@17.1:", when="@1.9.0:2.0")
        depends_on("py-packaging@17:", when="@1.3.8:1.9.0-rc0")
        depends_on("py-packaging", when="@1.2.10:1.2,1.3.0-rc2:1.3.7")
        depends_on("py-pillow@:8.2,8.3.1:", when="@1.3.8:1.3")
        depends_on("py-pydeprecate@0.3.1", when="@1.4:1.5")
        depends_on("py-pydeprecate@0.3:0.3.0", when="@1.3.0-rc2:1.3")
        depends_on("py-pyyaml@5.4:", when="@1.8:")
        depends_on("py-pyyaml@5.1:", when="@1.4:1.5")
        depends_on("py-pyyaml@5.1:5", when="@1.3.0-rc3:1.3")
        depends_on("py-pyyaml@5.1:5.3,6:", when="@:1.3.0-rc2")
        depends_on("py-rich@12.3:", when="@2.0.0:+extra")
        depends_on("py-rich@10.14,10.15.0-alpha2:", when="@1.8:2.0.0-rc0+extra")
        depends_on("py-rich@10.2.2:", when="@1.5+extra")
        depends_on("py-tensorboard@2.2:2.4,2.6:", when="@1.2.9:1.2,1.3.0-rc2:1.4.1")
        depends_on("py-tensorboard@2.2:", when="@:1.2.8,1.3:1.3.0-rc1,1.4.2:1.5")
        depends_on("py-tensorboardx@2.2:", when="@1.9.0:+extra")
        depends_on("py-tensorboardx@2.2:", when="@1.8:1.9.0-rc0")
        depends_on("py-torch@1.11:", when="@2:2.1.0-rc0")
        depends_on("py-torch@1.10:", when="@1.9:1")
        depends_on("py-torch@1.9:", when="@1.8")
        depends_on("py-torch@1.6:", when="@1.4:1.5")
        depends_on("py-torch@1.4:", when="@:1.3")
        depends_on("py-torchmetrics@0.7.0:", when="@1.8:")
        depends_on("py-torchmetrics@0.4.1:", when="@1.5")
        depends_on("py-torchmetrics@0.4.0:0.4.0.0,0.4.1-rc0:", when="@1.4")
        depends_on("py-torchmetrics@0.2.0:0.2", when="@1.2.9:1.2")
        depends_on("py-torchmetrics@0.2.0:", when="@1.2.5:1.2.8,1.3")
        depends_on("py-torchtext@0.7:", when="@1.4:1.5+extra")
        depends_on("py-torchtext@0.5:", when="@1.2.4:1.3+extra")
        depends_on("py-tqdm@4.57:", when="@1.8:")
        depends_on("py-tqdm@4.41:", when="@:1.5")
        depends_on("py-typing-extensions@4:", when="@1.8:2.1")
        depends_on("py-typing-extensions", when="@1.4:1.5")

    # src/pytorch_lightning/__setup__.py

    # requirements/pytorch/base.txt

    # Historical dependencies

    # https://github.com/Lightning-AI/lightning/issues/16637
    conflicts("^py-torch~distributed", when="@1.9.0")
    # https://github.com/Lightning-AI/lightning/issues/15494
    conflicts("^py-torch~distributed", when="@1.8.0")
    # https://github.com/Lightning-AI/lightning/issues/10348
    conflicts("^py-torch~distributed", when="@1.5.0:1.5.2")
