# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytest(PythonPackage):
    """pytest: simple powerful testing with Python."""

    homepage = "https://pytest.org/"
    pypi = "pytest/pytest-5.2.1.tar.gz"
    git = "https://github.com/pytest-dev/pytest"

    license("MIT")

    version(
        "8.0.0",
        sha256="50fb9cbe836c3f20f0dfa99c565201fb75dc54c8d76373cd1bde06b06657bdb6",
        url="https://pypi.org/packages/c7/10/727155d44c5e04bb08e880668e53079547282e4f950535234e5a80690564/pytest-8.0.0-py3-none-any.whl",
    )
    version(
        "7.4.4",
        sha256="b090cdf5ed60bf4c45261be03239c2c1c22df034fbffe691abe93cd80cea01d8",
        url="https://pypi.org/packages/51/ff/f6e8b8f39e08547faece4bd80f89d5a8de68a38b2d179cc1c4490ffa3286/pytest-7.4.4-py3-none-any.whl",
    )
    version(
        "7.3.2",
        sha256="cdcbd012c9312258922f8cd3f1b62a6580fdced17db6014896053d47cddf9295",
        url="https://pypi.org/packages/7a/d0/de969198293cdea22b3a6fb99a99aeeddb7b3827f0823b33c5dc0734bbe5/pytest-7.3.2-py3-none-any.whl",
    )
    version(
        "7.2.1",
        sha256="c7c6ca206e93355074ae32f7403e8ea12163b1163c976fee7d4d84027c162be5",
        url="https://pypi.org/packages/cc/02/8f59bf194c9a1ceac6330850715e9ec11e21e2408a30a596c65d54cf4d2a/pytest-7.2.1-py3-none-any.whl",
    )
    version(
        "7.1.3",
        sha256="1377bda3466d70b55e3f5cecfa55bb7cfcf219c7964629b967c37cf0bda818b7",
        url="https://pypi.org/packages/e3/b9/3541bbcb412a9fd56593005ff32183825634ef795a1c01ceb6dee86e7259/pytest-7.1.3-py3-none-any.whl",
    )
    version(
        "6.2.5",
        sha256="7310f8d27bc79ced999e760ca304d69f6ba6c6649c0b60fb0e04a4a77cacc134",
        url="https://pypi.org/packages/40/76/86f886e750b81a4357b6ed606b2bcf0ce6d6c27ad3c09ebf63ed674fc86e/pytest-6.2.5-py3-none-any.whl",
    )
    version(
        "6.2.4",
        sha256="91ef2131a9bd6be8f76f1f08eac5c5317221d6ad1e143ae03894b862e8976890",
        url="https://pypi.org/packages/a1/59/6821e900592fbe261f19d67e4def0cb27e52ef8ed16d9922c144961cc1ee/pytest-6.2.4-py3-none-any.whl",
    )
    version(
        "6.2.2",
        sha256="b574b57423e818210672e07ca1fa90aaf194a4f63f3ab909a2c67ebb22913839",
        url="https://pypi.org/packages/a1/cf/7f67585bd2fc0359ec482cf3c430bce3ef6d3f40bc468137225a733e3069/pytest-6.2.2-py3-none-any.whl",
    )
    version(
        "6.2.1",
        sha256="1969f797a1a0dbd8ccf0fecc80262312729afea9c17f1d70ebf85c5e76c6f7c8",
        url="https://pypi.org/packages/d7/15/5ef931cbd22585865aad0ea025162545b53af9319cf38542e0b7981d5b34/pytest-6.2.1-py3-none-any.whl",
    )
    version(
        "6.1.1",
        sha256="7a8190790c17d79a11f847fba0b004ee9a8122582ebff4729a082c109e81a4c9",
        url="https://pypi.org/packages/d6/36/9e022b76a3ac440e1d750c64fa6152469f988efe0c568b945e396e2693b5/pytest-6.1.1-py3-none-any.whl",
    )
    version(
        "5.3.4",
        sha256="c13d1943c63e599b98cf118fcb9703e4d7bde7caa9a432567bcdcae4bf512d20",
        url="https://pypi.org/packages/0b/2d/75def2ed660903839bab38a1cadf819726637a0c3c78951de7e67a97a7c3/pytest-5.3.4-py3-none-any.whl",
    )
    version(
        "5.2.1",
        sha256="7e4800063ccfc306a53c461442526c5571e1462f61583506ce97e4da6a1d88c8",
        url="https://pypi.org/packages/0c/91/d68f68ce54cd3e8afa1ef73ea1ad44df2438521b64c0820e5fd9b9f13b7d/pytest-5.2.1-py3-none-any.whl",
    )
    version(
        "5.1.1",
        sha256="95b1f6db806e5b1b5b443efeb58984c24945508f93a866c1719e1a507a957d7c",
        url="https://pypi.org/packages/ef/3b/5652e27e048ae086f79ce9c4ce8a2da6bad1e9590788e5768aafc6f375ef/pytest-5.1.1-py3-none-any.whl",
    )
    version(
        "4.6.9",
        sha256="c77a5f30a90e0ce24db9eaa14ddfd38d4afb5ea159309bdd2dae55b931bc9324",
        url="https://pypi.org/packages/e3/05/26e00e583640d02c6b38ac53a92d8c9fecacde0842c4f2d7c02bbbd0d57f/pytest-4.6.9-py2.py3-none-any.whl",
    )
    version(
        "4.6.5",
        sha256="d100a02770f665f5dcf7e3f08202db29857fee6d15f34c942be0a511f39814f0",
        url="https://pypi.org/packages/97/72/d4d6d22ad216f149685f2e93ce9280df9f36cbbc87fa546641ac92f22766/pytest-4.6.5-py2.py3-none-any.whl",
    )
    version(
        "4.6.2",
        sha256="6032845e68a17a96e8da3088037f899b56357769a724122056265ca2ea1890ee",
        url="https://pypi.org/packages/cd/eb/04a30246424f5664a8fb72d982a57f60399642a63d24c7fdfaf70d673c27/pytest-4.6.2-py2.py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="13c5e9fb5ec5179995e9357111ab089af350d788cbc944c628f3cde72285809b",
        url="https://pypi.org/packages/7e/16/83b2a35c427b838df9836c9e7e4ae6dfbcbdea643db44652f693b1c57d70/pytest-4.4.0-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="9687049d53695ad45cf5fdc7bbd51f0c49f1ea3ecfc4b7f3fde7501b541f17f4",
        url="https://pypi.org/packages/51/b2/2fa8e8b179c792c457c2f7800f1313bfbd34f515e3a833e6083121844c14/pytest-4.3.0-py2.py3-none-any.whl",
    )
    version(
        "3.7.2",
        sha256="96bfd45dbe863b447a3054145cd78a9d7f31475d2bce6111b133c0cc4f305118",
        url="https://pypi.org/packages/98/37/4b988e339251ec5359824f2529930e793d75b7039f2fa88736743f0ed415/pytest-3.7.2-py2.py3-none-any.whl",
    )
    version(
        "3.7.1",
        sha256="e74466e97ac14582a8188ff4c53e6cc3810315f342f6096899332ae864c1d432",
        url="https://pypi.org/packages/d2/86/7b9513da923b94e48c2cf013ae4eae8184a36ebeb7fe27d386bc3db4f56f/pytest-3.7.1-py2.py3-none-any.whl",
    )
    version(
        "3.5.1",
        sha256="829230122facf05a5f81a6d4dfe6454a04978ea3746853b2b84567ecf8e5c526",
        url="https://pypi.org/packages/76/52/fc48d02492d9e6070cb672d9133382e83084f567f88eff1c27bd2c6c27a8/pytest-3.5.1-py2.py3-none-any.whl",
    )
    version(
        "3.0.7",
        sha256="66f332ae62593b874a648b10a8cb106bfdacd2c6288ed7dec3713c3a808a6017",
        url="https://pypi.org/packages/8e/81/40a4b62b1d15441c282db485f8f08c7c38edab9ffe750a31d77805cd5f6a/pytest-3.0.7-py2.py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="4b0872d00159dd8d7a27c4a45a2be77aac8a6e70c3af9a7c76c040c3e3715b9d",
        url="https://pypi.org/packages/c4/bf/80d1cd053b1c86f6ecb23300fba3a7c572419b5edc155da0f3f104d42775/pytest-3.0.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@8:")
        depends_on("python@3.7:", when="@7.1:7")
        depends_on("py-atomicwrites@1:", when="@5.3:7.1.2 platform=windows")
        depends_on("py-atomicwrites@1:", when="@3.6:5.2")
        depends_on("py-attrs@19.2:", when="@6.2:7.2")
        depends_on("py-attrs@17.4:", when="@3.5:6.1")
        depends_on(
            "py-colorama", when="@:2.8.3,3.0.6,3.1.1:3.1.2,3.2:3.2.2,3.3.2: platform=windows"
        )
        depends_on("py-exceptiongroup@1.0.0-rc8:", when="@7.2: ^python@:3.10")
        depends_on("py-importlib-metadata@0.12:", when="@4.6.6:4,5.1:7 ^python@:3.7")
        depends_on("py-importlib-metadata@0.12:", when="@4.6:4.6.5,5:5.0")
        depends_on("py-iniconfig", when="@6:")
        depends_on("py-more-itertools@4:", when="@3.5:6.0")
        depends_on("py-packaging", when="@4.6:")
        depends_on("py-pluggy@1.3:", when="@8:8.0")
        depends_on("py-pluggy@0.12:", when="@6.2.5:7")
        depends_on("py-pluggy@0.12:0,1.0.0.dev:1.0", when="@6.2:6.2.4")
        depends_on("py-pluggy@0.12:0", when="@4.6:6.1")
        depends_on("py-pluggy@0.9:", when="@4.4:4.4.1")
        depends_on("py-pluggy@0.7:", when="@3.7:4.3")
        depends_on("py-pluggy@0.5:0.6", when="@3.3.2:3.6.3")
        depends_on("py-py@1.8.2:", when="@6:7.1")
        depends_on("py-py@1.5:", when="@3.3.2:5")
        depends_on("py-setuptools", when="@3.0.6,3.1.1:3.1.2,3.2:3.2.2,3.3.2:4.5")
        depends_on("py-six@1.10:", when="@3.3.2:4")
        depends_on("py-toml", when="@6")
        depends_on("py-tomli@1:", when="@7.2: ^python@:3.10")
        depends_on("py-tomli@1:", when="@7:7.1")
        depends_on("py-wcwidth", when="@4.5:5")

    # python_requires
    # see https://github.com/pytest-dev/pytest/releases/tag/7.3.2

    # setup_requires

    # install_requires

    # Historic dependencies
