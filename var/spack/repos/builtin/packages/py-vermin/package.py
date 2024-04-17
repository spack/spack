# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVermin(PythonPackage):
    """Concurrently detect the minimum Python versions needed to run code."""

    homepage = "https://github.com/netromdk/vermin"
    url = "https://github.com/netromdk/vermin/archive/v1.6.0.tar.gz"

    maintainers("netromdk")

    license("MIT")

    version(
        "1.6.0",
        sha256="f1fa9ee40f59983dc40e0477eb2b1fa8061a3df4c3b2bcf349add462a5610efb",
        url="https://pypi.org/packages/2e/98/1a2ca43e6d646421eea16ec19977e2e6d1ea9079bd9d873bfae513d43f1c/vermin-1.6.0-py2.py3-none-any.whl",
    )
    version(
        "1.5.2",
        sha256="c1566ad4e1c8e1b0e98cf5f7d69b691d44a578e2ce9c5aa1d418736bc4944b32",
        url="https://pypi.org/packages/46/ed/420955392d9c2743c93e0418928927e34aba355c716a70c6bdba209b930f/vermin-1.5.2-py2.py3-none-any.whl",
    )
    version(
        "1.5.1",
        sha256="420995de564ac0c31e2157220259d7ac82556e8fa69c112d8005b78c14b0caf5",
        url="https://pypi.org/packages/d2/9d/7dc49fece1a9c99c87671f11df1355fcfe620407f524235e503f5602e58d/vermin-1.5.1-py2.py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="e3ffdc753d1cff45bd631d74c417193d2b0290c4082810ee298884d7670b5e53",
        url="https://pypi.org/packages/12/79/e7f255bba4d8ea96894f3f7a5806bb67ea43f547060299ffc8c1b25e06f3/vermin-1.5.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.2",
        sha256="0e5e712686d47e6529c365748771ae0db2c8df22835134c10ad4c7f1fa62533c",
        url="https://pypi.org/packages/22/01/7a59f2fb5720565ca48ba0b3c8407e30c4e45ff2c6e47e2831ef6ca06746/vermin-1.4.2-py2.py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="e528e8d7d96bda8cb2df1015afd0b51cc1c97c285695c9d10d9df924c3f6352c",
        url="https://pypi.org/packages/ee/d1/99d437a557d844256d062b0af31072a09a64f342e91be68bd918b5bc461b/vermin-1.4.1-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="0370f562cfa004a234c2ca33cff3c187fe05741c1c36570ef27a514ad9b7e202",
        url="https://pypi.org/packages/cb/d7/ef85a8b5e5e00b32594f4a02574362d2b782feb21451b17c15529a7c460c/vermin-1.4.0-py2.py3-none-any.whl",
    )
    version(
        "1.3.3",
        sha256="c5bd8bf2026d87563332293a0479606954bd973d8cf72ab370e1164a019c0524",
        url="https://pypi.org/packages/8c/90/789eec4298bc14b22aac16d27c4741ca50e22c4a0a7eccfd3e17687825a8/vermin-1.3.3-py2.py3-none-any.whl",
    )
    version(
        "1.3.2",
        sha256="07fd72e7ec9649e255485948995c6f03fd7a0a7bcd3acb982f14faeb83d168c5",
        url="https://pypi.org/packages/4a/67/ec4280afe00af77fa8a0ebf9d57e7b1f75f2526b2c7bbbe1ea5ed5f5d411/vermin-1.3.2-py2.py3-none-any.whl",
    )
    version(
        "1.3.1",
        sha256="ef38dedab8cf7b68f8037f531b82222153ab21d3c54b91dd80776bbf95637ae5",
        url="https://pypi.org/packages/a0/7c/a08694e3993d5eda15432687de32a23922c5cedcd3690b85174651d961b2/vermin-1.3.1-py2.py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="7fe5ab707e06f61d094e7afcaf1ec5f334fbcddb65c2b326c150a9b0b2bad525",
        url="https://pypi.org/packages/a1/56/95a2f0c3cc69ddec48295a81477a8710bf27e21c429e65e5cc1cdc9cbd75/vermin-1.3.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.2",
        sha256="5dfa0a36bdd6a73a925e417a452df5b0c7afcebc01362439409b5cf56ee8a6f2",
        url="https://pypi.org/packages/b9/d1/ab60cf1e3cecd8fcc65ca24fc6755ef30517b477df7d8157fc165a9e4175/vermin-1.2.2-py2.py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="301b2a1f781d1a94e253fd0106560ab187cc869a32db27e0d95d32ae2ab70b3a",
        url="https://pypi.org/packages/b0/a1/799e6e3a1355c518c86520674557d38bc2f91c8b706a78e8cf82bd5dca35/vermin-1.2.1-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="f014273dca89e0a9bb8c6bc79cd616c67fc4f0957232ed1a979dfd66e4ec53f4",
        url="https://pypi.org/packages/a4/f8/c5bd6de611f1d4d45c963f6d9a594aa7062e4b2241e0789d7c764184ea85/vermin-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="2866f2d3ec3a67a9249f6491e66af10be01931a91376f55ef2cb5e2915779e13",
        url="https://pypi.org/packages/a0/56/dd3f0316e0b84f33675274bafa3def4d760b955421d011f286144098e709/vermin-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="ab0c03ec1199c477ea49196355e2320934bfedc64605186c40850df36f5c64a0",
        url="https://pypi.org/packages/f7/98/9bce73e146b4e796ecc46fece22f168e987ad9e4d22c4e09b384169dbbd5/vermin-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.3",
        sha256="1670633084e337e7912c2ea1fbba241efd191d0f88bf1132131d15f827f6b637",
        url="https://pypi.org/packages/9f/82/94b13803bc7ac5d3311ea00033d0e4c8c2c1a3f8817def380c50d76964eb/vermin-1.0.3-py2.py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="153c9c7e8a9c3fa28214fe1eb6b81e2da5bae5bf14c9dd1e99dd6a036676d506",
        url="https://pypi.org/packages/5f/ba/2402ea5d22120fe76e5cf566499dd3f8843c09b06c9d5b505c586bcb3299/vermin-1.0.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="01ac8c033d2884f6b640a2669defea314a3c9929ea1a0a6a1b693adbaf4f25f0",
        url="https://pypi.org/packages/71/0b/cbd0d72498077a38f4e756aed615ee3380e2440b92a292cd684478053dc3/vermin-1.0.1-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="11d2f8c4183f78fb4338af3c23f6d77d1d1c60e4bea6446491bf077fc92954c7",
        url="https://pypi.org/packages/71/e6/a472c8e947038907df721dd9d0118f65ebfbad74e371684e1bf4ab4c3d9a/vermin-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.10.5",
        sha256="c66ae418e4030915de4cdc53f26fe375fea9b51c17fa04bae2cc63efc0b780b3",
        url="https://pypi.org/packages/7a/ce/e96f49f4957cd6cc14f7924f2960f27d947a9ffdebc0b0a2cbaab3f30c1f/vermin-0.10.5-py2.py3-none-any.whl",
    )
    version(
        "0.10.4",
        sha256="32d5ae48d3104e402db4297da23e877c01af793897396930ff9573c27a5cd17f",
        url="https://pypi.org/packages/9b/95/0284010434b7d848f422d1506b1e9b5ff514ca94ed4e4c88e0e6f643ff49/vermin-0.10.4-py2.py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="d5ef8d0861193965d25b59a640eb08e573b24bec207136b931b93ce161d52e7e",
        url="https://pypi.org/packages/1b/39/43794d1a6162cd7bc8a0c3c77b49b65e5a487aac7a160d5380e6fd6dc562/vermin-0.10.0-py2.py3-none-any.whl",
    )
