# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBlessed(PythonPackage):
    """Blessed is a thin, practical wrapper around terminal capabilities in
    Python."""

    homepage = "https://github.com/jquast/blessed"
    pypi = "blessed/blessed-1.15.0.tar.gz"

    license("MIT")

    version(
        "1.19.0",
        sha256="1f2d462631b2b6d2d4c3c65b54ef79ad87a6ca2dd55255df2f8d739fcc8a1ddb",
        url="https://pypi.org/packages/d4/f3/73c8e1b77396663e2a5121c78f1278d64d7806cade710abe28b65979aced/blessed-1.19.0-py2.py3-none-any.whl",
    )
    version(
        "1.18.1",
        sha256="dd7c0d33db9a2e7f597b446996484d0ed46e1586239db064fb5025008937dcae",
        url="https://pypi.org/packages/af/7b/5ae28215407a11f8f935cc8d4e5e67cb473e8a5154c6275f153e3a480357/blessed-1.18.1-py2.py3-none-any.whl",
    )
    version(
        "1.18.0",
        sha256="5b5e2f0563d5a668c282f3f5946f7b1abb70c85829461900e607e74d7725106e",
        url="https://pypi.org/packages/26/35/a781470488a304f66843d328052b6cb22df7163246fb47a27bfb21fba4e6/blessed-1.18.0-py2.py3-none-any.whl",
    )
    version(
        "1.17.12",
        sha256="0a74a8d3f0366db600d061273df77d44f0db07daade7bb7a4d49c8bc22ed9f74",
        url="https://pypi.org/packages/88/34/61e670039aefca011b5e6fb1a73de18165ef6d016ac16df423b20d719e64/blessed-1.17.12-py2.py3-none-any.whl",
    )
    version(
        "1.17.11",
        sha256="81125aa5b84cb9dfc09ff451886f64b4b923b75c5eaf51fde9d1c48a135eb797",
        url="https://pypi.org/packages/1b/37/241fec1c8fa767b445c5afb5cfa7eb78cef07f85489b51c2cf292b530265/blessed-1.17.11-py2.py3-none-any.whl",
    )
    version(
        "1.17.10",
        sha256="c8532e648cf102b9800b7f2d2b12c87604bf207db3ca268e00554c9dac4cf980",
        url="https://pypi.org/packages/7d/16/9109bec05f7927f796e498bafa4a250515afc3f6cdc668e94f4f5cbb46f1/blessed-1.17.10-py2.py3-none-any.whl",
    )
    version(
        "1.17.9",
        sha256="a9f059d5b2c32ade04eaafddac486db48c5e9a68fb7e181048aad391d33cef1a",
        url="https://pypi.org/packages/70/13/3d632951633923432f8240da2d1458e54c63b93d0412d517f332e008a1f3/blessed-1.17.9-py2.py3-none-any.whl",
    )
    version(
        "1.17.8",
        sha256="219d422995a0938a0b5c89c711878ce76262091a8e97def7d2028a1721cf06ab",
        url="https://pypi.org/packages/97/68/db2c1fedc40efc428128a21de4be3111584fd82844053428b40e41514fcb/blessed-1.17.8-py2.py3-none-any.whl",
    )
    version(
        "1.17.7",
        sha256="71a36228eeaab313db1402599631bbc20754a11c992d08a5891610ba6cd446f4",
        url="https://pypi.org/packages/bb/78/4373e9948162ade660ed5dba5cd002786a23e05a4f4e01c5f23c4fc5da53/blessed-1.17.7-py2.py3-none-any.whl",
    )
    version(
        "1.17.6",
        sha256="8371d69ac55558e4b1591964873d6721136e9ea17a730aeb3add7d27761b134b",
        url="https://pypi.org/packages/19/de/930a8ab1ccb9779d34305c8ae2a496ed35769b6bc8a1639975ed6f415992/blessed-1.17.6-py2.py3-none-any.whl",
    )
    version(
        "1.17.5",
        sha256="af119076d8b6b7e027999d3ced80290b906d7cdc9e36264842e14e6cf0d4a9ef",
        url="https://pypi.org/packages/f5/ca/85ba2c6da522a5769676b7e43d2fad775f8eeabb2e28cc6d28234912e21c/blessed-1.17.5-py2.py3-none-any.whl",
    )
    version(
        "1.17.4",
        sha256="2e1f368ed67da152fcaea4ce8cd54655972fd4f6808a0e11a1242642196b5130",
        url="https://pypi.org/packages/b7/0e/9c05458dc50f3a71e47cd74da40ed2a09061be5bb67a5425223296ae948c/blessed-1.17.4-py2.py3-none-any.whl",
    )
    version(
        "1.17.3",
        sha256="4fc4b4b41dd58afc41a88e6776e244f3fafe26fd62078e163d2c12eee6f0d662",
        url="https://pypi.org/packages/44/05/fe2ab4f3d1f39cd0f72093e403552f52dec7805fb1fed1d9df2ec591dbc9/blessed-1.17.3-py2.py3-none-any.whl",
    )
    version(
        "1.17.0",
        sha256="ec5eec320a5604721116531f5e665fe4d50e4aa944dfa4bea9b4664e1cf63d18",
        url="https://pypi.org/packages/1b/4c/0bc6f7a224d9a00d771598278bbbf86d217e208251e4b27d85c793362059/blessed-1.17.0-py2.py3-none-any.whl",
    )
    version(
        "1.16.1",
        sha256="01f3305a2f3c89a11020f2e167fe67b275697b3aead72dd869446aad47dd4707",
        url="https://pypi.org/packages/fe/31/ab33f900a948491470bbd7f204a1887dcd4d7f4dbba6160eab5d55a84875/blessed-1.16.1-py2.py3-none-any.whl",
    )
    version(
        "1.16.0",
        sha256="b3ffcc7e840b116fa611ec59bb4ec29a092caca84dfde6d8a6c7d3ff247b2cad",
        url="https://pypi.org/packages/05/53/b924461ba18644cb3183b9635147cfeb3d38ccc9fee2a31a5585a26ca8c0/blessed-1.16.0-py2.py3-none-any.whl",
    )
    version(
        "1.15.0",
        sha256="9a0a98c7070b016341ae0300415deeda930a340ef7961d9b920a5cb200a601e2",
        url="https://pypi.org/packages/3f/96/1915827a8e411613d364dd3a56ef1fbfab84ee878070a69c21b10b5ad1bb/blessed-1.15.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jinxed@1.1:", when="@1.19: platform=windows")
        depends_on("py-jinxed", when="@1.16:1.18 platform=windows")
        depends_on("py-six@1.9:", when="@1.15:")
        depends_on("py-wcwidth@0.1.4:", when="@1.15:")
