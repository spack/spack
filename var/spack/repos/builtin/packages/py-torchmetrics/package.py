# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchmetrics(PythonPackage):
    """Machine learning metrics for distributed, scalable PyTorch applications."""

    homepage = "https://github.com/PyTorchLightning/metrics"
    pypi = "torchmetrics/torchmetrics-0.3.1.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "1.3.2",
        sha256="44ca3a9f86dc050cb3f554836ef291698ea797778457195b4f685fce8e2e64a3",
        url="https://pypi.org/packages/f3/0e/cedcb9c8aeb2d1f655f8d05f841b14d84b0a68d9f31afae4af55c7c6d0a9/torchmetrics-1.3.2-py3-none-any.whl",
    )
    version(
        "1.3.1",
        sha256="a44bd1edee629bbf463eb81bfba8300b3785d8b3b8d758bdcafa862b80955b4f",
        url="https://pypi.org/packages/cd/23/4bb4c1b78b57682a1309974a29bfdcbfa6fcf5476e698a4f0f22affa3799/torchmetrics-1.3.1-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="1ba8c0702143f59646dac4f45829ccf15d495c596ee63e63e66b9a2b972b310e",
        url="https://pypi.org/packages/95/f4/07d76def72c02f0d93e5eec953fd3349b653af0e0b792276aeb5b3e6f7bf/torchmetrics-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="fe03a8c53d0ae5800d34ea615f56295fda281282cd83f647d2184e81c1d4efee",
        url="https://pypi.org/packages/62/17/eedb48177a4679b75b82185492f8ad2b4d010e032fd38160e157b0e22028/torchmetrics-1.2.1-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="da2cb18822b285786d082c40efb9e1d861aac425f58230234fe6ce233cf002f8",
        url="https://pypi.org/packages/a3/88/cc27059747ddecff744826e38014822023cbfff4ca079a6ee9a96602dd0b/torchmetrics-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="903b4fc30537acfc5221505c48f7627e58dbf6d9dea85c16ea7b4323f9e13793",
        url="https://pypi.org/packages/e3/86/47091c33ecf05f8826d134fd518485d4c68ca524c053b2fdd4e041c20547/torchmetrics-1.1.1-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="16afba73195495844248f9120d1629e4067c998194458f4a37bf05642223d29d",
        url="https://pypi.org/packages/ec/83/c69e70d559747126f952b6210ebd1f83dcf0f64f8a0591e0f9996f996db3/torchmetrics-1.1.0-py3-none-any.whl",
    )
    version(
        "1.0.3",
        sha256="612a74ab8ebfcd4ebb38e5c370ce29a0e73af074948048f6f2233e25cf60da75",
        url="https://pypi.org/packages/67/90/9ac94af10cd1777859a92be1e8186325490654930e871f8bb219cc342868/torchmetrics-1.0.3-py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="8fe425dd7cf0f636998af83c25cd12eacbe66acb948b79f2f107f8e1bf003ddd",
        url="https://pypi.org/packages/26/0e/12a29ab102e45e1ad1cffb27cf385b3c87ce0c49177419118090e390bf94/torchmetrics-1.0.2-py3-none-any.whl",
    )
    version(
        "0.11.4",
        sha256="45f892f3534e91f3ad9e2488d1b05a93b7cb76b7d037969435a41a1f24750d9a",
        url="https://pypi.org/packages/fb/47/6e9f9b41c48750a45ad07cc6d43a2979bfc09e6989656aece97cc59cbef1/torchmetrics-0.11.4-py3-none-any.whl",
    )
    version(
        "0.11.3",
        sha256="7797c6e86f7474b6e0beb46f979044354a831e012199e96e52d2208a15ebe418",
        url="https://pypi.org/packages/5f/ea/97954b8a14d60e121b91475fae7806c2f3b891708f9fd71b7baccea321df/torchmetrics-0.11.3-py3-none-any.whl",
    )
    version(
        "0.11.2",
        sha256="b200fe96adcb7d6473c4b69a5bcf13f391afa15adcd8ab085140e46714991fc4",
        url="https://pypi.org/packages/e1/df/d62977457ad0005c23cf828461b7809ee079ea6f678a024f1c44997aefd7/torchmetrics-0.11.2-py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="9987d7c21b081cceef246a72be1ce25bf29c842764f59dda54f59e3b4cd1970b",
        url="https://pypi.org/packages/9d/a2/facc6b32b2d959c6e5685f075a6a3884bc5d9dac3e0d96a04665f0ffd09b/torchmetrics-0.11.1-py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="f809c3cb86a0bd3d8743df0888040257e20d371a937ff9114f582a60ce1a1c67",
        url="https://pypi.org/packages/e5/aa/5fdb143def5eb679658dcaa7a649dc8ad2ff150b01ed935174c6a75f7895/torchmetrics-0.11.0-py3-none-any.whl",
    )
    version(
        "0.10.3",
        sha256="b12cf92897545e24a825b0d168888c0f3052700c2901e2d4f7d90b252bc4a343",
        url="https://pypi.org/packages/08/b7/f1e49be0e076c8ec981f1d4cea1f32da2bd754eaeaf6ed74d5add3f840b4/torchmetrics-0.10.3-py3-none-any.whl",
    )
    version(
        "0.10.2",
        sha256="43757d82266969906fc74b6e80766fcb2a0d52d6c3d09e3b7c98cf3b733fd20c",
        url="https://pypi.org/packages/6c/f1/89c4c39ebc53106179e9a636a73046aa35534c16fa4e893b329440f90247/torchmetrics-0.10.2-py3-none-any.whl",
    )
    version(
        "0.10.1",
        sha256="e69fae7c6597ba505753f48e0f4ae1e73abde56c28fdc0c3baae826ec8c1d213",
        url="https://pypi.org/packages/5d/8e/2a962b16131326b3bb27eca3cc28b25c898243d45376f4baff9323f0cbbf/torchmetrics-0.10.1-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="1e99ee7379f8ff7e383383513ae0594bc5424de83b43e36c6ce12d464f1635b9",
        url="https://pypi.org/packages/6c/fe/65b7a40b3153807705b94aed0126547649eadc014300a119bc35b54c1795/torchmetrics-0.10.0-py3-none-any.whl",
    )
    version(
        "0.9.3",
        sha256="3babb9e75d223512621af69a84eabf52b621a4f768b83f86701d66d09abed80b",
        url="https://pypi.org/packages/8f/dc/a1f1282b8502db4c0e9dc670869d43291dc5b28512bf15576cc69a393df3/torchmetrics-0.9.3-py3-none-any.whl",
    )
    version(
        "0.9.2",
        sha256="ced006295c95c4555df0b8dea92960c00e3303de0da878fcf27e394df4757827",
        url="https://pypi.org/packages/38/b2/6dc94b11b56bf92728f50e50fadee6d7e755dae4e9daf4336dfcd74bfd3b/torchmetrics-0.9.2-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="4fec7d3d070dafba9dc024853bd7c654fd3f7d2c2fe72fab9415cafccd719b8e",
        url="https://pypi.org/packages/fc/37/514b7049e2864646330d24d8fcc386b786a7806065739c3635a71ae8a073/torchmetrics-0.9.0-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="908f6c129ba84864176c23217ab548069a59f1db555b08f20d2f20274564f90a",
        url="https://pypi.org/packages/e6/57/8575aca0e9f3b16385b1b4d8247fe56cfbb1a4e56e38b36fc97361ec4e4b/torchmetrics-0.7.0-py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="4e5497bc5c9d19fa520748cda89f6d863868bb5be33ec47d2834c0988bf737c5",
        url="https://pypi.org/packages/2b/9f/79c680deea27c2ce1b0516bf64f547da1de681157b2c6aefcfe26bcc4dfa/torchmetrics-0.5.1-py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="70c83f0fc804a4fe00a9e72dbd2960ff76e39ef62570a19bbdce0c15a1ee0d71",
        url="https://pypi.org/packages/4d/8b/de8df9044ca2ac5dfc6b13b9ad3b3ebe6b3a45807311102b569d680e811f/torchmetrics-0.4.1-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="bf6162b56c9466fdfa8f185e8bbd48c7740c4f46d1335bc4db87ac1efcdad0e2",
        url="https://pypi.org/packages/14/99/dc59248df9a50349d537ffb3403c1bdc1fa69077109d46feaa0843488001/torchmetrics-0.3.1-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="16a8ceac8e579828aa8a5a4f8830fc207a18e0fbc8774257fbb1cbfb95248faf",
        url="https://pypi.org/packages/3a/42/d984612cabf005a265aa99c8d4ab2958e37b753aafb12f31c81df38751c8/torchmetrics-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1:")
        depends_on("python@3.7:", when="@0.9:0")
        depends_on("py-lightning-utilities@0.8:", when="@1.1:")
        depends_on("py-lightning-utilities@0.7:", when="@1:1.0")
        depends_on("py-numpy@1.20.1:", when="@1:")
        depends_on("py-numpy@1.17.2:", when="@0.4:0.4.0.0,0.4.1-rc0:0")
        depends_on("py-numpy", when="@0.3:0.3.1")
        depends_on("py-packaging@18:", when="@1.2.1:")
        depends_on("py-packaging", when="@0.3.0-rc1:1.1.0")
        depends_on("py-pydeprecate@0.3:", when="@0.7:0.8")
        depends_on("py-torch@1.10:", when="@1.3:")
        depends_on("py-torch@1.8.1:", when="@0.11:1.2")
        depends_on("py-torch@1.3.1:", when="@0.2:0.10")
        depends_on("py-typing-extensions", when="@0.10: ^python@:3.8")
        depends_on("py-typing-extensions", when="@0.9 ^python@:3.7")

    # setup.py

    # requirements/base.txt (upper bound is removed during processing)

    # Historical dependencies
