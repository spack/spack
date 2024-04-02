# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJedi(PythonPackage):
    """An autocompletion tool for Python that can be used for text editors."""

    homepage = "https://github.com/davidhalter/jedi"
    pypi = "jedi/jedi-0.9.0.tar.gz"

    license("MIT")

    version(
        "0.18.2",
        sha256="203c1fd9d969ab8f2119ec0a3342e0b49910045abe6af0a3ae83a5764d54639e",
        url="https://pypi.org/packages/6d/60/4acda63286ef6023515eb914543ba36496b8929cb7af49ecce63afde09c6/jedi-0.18.2-py2.py3-none-any.whl",
    )
    version(
        "0.18.1",
        sha256="637c9635fcf47945ceb91cd7f320234a7be540ded6f3e99a50cb6febdfd1ba8d",
        url="https://pypi.org/packages/b3/0e/836f12ec50075161e365131f13f5758451645af75c2becf61c6351ecec39/jedi-0.18.1-py2.py3-none-any.whl",
    )
    version(
        "0.18.0",
        sha256="18456d83f65f400ab0c2d3319e48520420ef43b23a086fdc05dff34132f0fb93",
        url="https://pypi.org/packages/f9/36/7aa67ae2663025b49e8426ead0bad983fee1b73f472536e9790655da0277/jedi-0.18.0-py2.py3-none-any.whl",
    )
    version(
        "0.17.2",
        sha256="98cc583fa0f2f8304968199b01b6b4b94f469a1f4a74c1560506ca2a211378b5",
        url="https://pypi.org/packages/c3/d4/36136b18daae06ad798966735f6c3fb96869c1be9f8245d2a8f556e40c36/jedi-0.17.2-py2.py3-none-any.whl",
    )
    version(
        "0.17.1",
        sha256="1ddb0ec78059e8e27ec9eb5098360b4ea0a3dd840bedf21415ea820c21b40a22",
        url="https://pypi.org/packages/07/83/7e711550fcb2722f1ca9c8564d5bb23f625ae67d99f4a360b428c0f3e932/jedi-0.17.1-py2.py3-none-any.whl",
    )
    version(
        "0.15.1",
        sha256="786b6c3d80e2f06fd77162a07fed81b8baa22dde5d62896a790a331d6ac21a27",
        url="https://pypi.org/packages/55/54/da994f359e4e7da4776a200e76dbc85ba5fc319eefc22e33d55296d95a1d/jedi-0.15.1-py2.py3-none-any.whl",
    )
    version(
        "0.15.0",
        sha256="0e4ba6cb008377b5a3c015a99ca007711f22fd69b8d5ff9c1f07673aed512adb",
        url="https://pypi.org/packages/26/1a/010f06da107e3e81eba8a45f7a9bc95ef11953fb8a84f1e3d965b7c02c21/jedi-0.15.0-py2.py3-none-any.whl",
    )
    version(
        "0.14.1",
        sha256="e07457174ef7cb2342ff94fa56484fe41cec7ef69b0059f01d3f812379cb6f7c",
        url="https://pypi.org/packages/4e/06/e906725a5b3ad7996bbdbfe9958aab75db64ef84bbaabefe47574de58865/jedi-0.14.1-py2.py3-none-any.whl",
    )
    version(
        "0.14.0",
        sha256="79d0f6595f3846dffcbe667cc6dc821b96e5baa8add125176c31a3917eb19d58",
        url="https://pypi.org/packages/68/42/6309f3871b2f8361764ac5b2fe6719f9c6e6561d9307d8cecda319cf5843/jedi-0.14.0-py2.py3-none-any.whl",
    )
    version(
        "0.13.3",
        sha256="2c6bcd9545c7d6440951b12b44d373479bf18123a401a52025cf98563fbd826c",
        url="https://pypi.org/packages/25/2b/1f188901be099d52d7b06f4d3b7cb9f8f09692c50697b139eaf6fa2928d8/jedi-0.13.3-py2.py3-none-any.whl",
    )
    version(
        "0.13.2",
        sha256="c8481b5e59d34a5c7c42e98f6625e633f6ef59353abea6437472c7ec2093f191",
        url="https://pypi.org/packages/c2/bc/54d53f5bc4658380d0eca9055d72be4df45e5bfd91a4bac97da224a92553/jedi-0.13.2-py2.py3-none-any.whl",
    )
    version(
        "0.13.1",
        sha256="0191c447165f798e6a730285f2eee783fff81b0d3df261945ecb80983b5c3ca7",
        url="https://pypi.org/packages/7a/1a/9bd24a185873b998611c2d8d4fb15cd5e8a879ead36355df7ee53e9111bf/jedi-0.13.1-py2.py3-none-any.whl",
    )
    version(
        "0.13.0",
        sha256="0ad328f5d9d0a6c8b22a0ca429c7b0cea1974e2b2d5a00e0bc45074dcd44d255",
        url="https://pypi.org/packages/50/a2/b01263ac7192cda0207e5353176091e563183691f399b0b5d30f5b4e0549/jedi-0.13.0-py2.py3-none-any.whl",
    )
    version(
        "0.12.1",
        sha256="c254b135fb39ad76e78d4d8f92765ebc9bf92cbc76f49e97ade1d5f5121e1f6f",
        url="https://pypi.org/packages/3d/68/8bbf0ef969095a13ba0d4c77c1945bd86e9811960d052510551d29a2f23b/jedi-0.12.1-py2.py3-none-any.whl",
    )
    version(
        "0.12.0",
        sha256="5861f6dc0c16e024cbb0044999f9cf8013b292c05f287df06d3d991a87a4eb89",
        url="https://pypi.org/packages/e7/42/074192a165622e645ed4aeade63e76e56b3496a044569b3c6cae3a918352/jedi-0.12.0-py2.py3-none-any.whl",
    )
    version(
        "0.10.2",
        sha256="96678411f2ffa444da3a5e7fdd4adc513b728a4a4617b30308be5c950722424b",
        url="https://pypi.org/packages/bd/04/789d25c1786e6d17f4a19847fd6536a1a491d48e8116db0b5c9c1fe5e821/jedi-0.10.2-py2.py3-none-any.whl",
    )
    version(
        "0.10.1",
        sha256="b18896833027d42556d44571260801cca1a08cca80dd95af500ca728b8082e4b",
        url="https://pypi.org/packages/7e/1e/ea5d5723ef19fb0b76895c4415e1cbf26bc24ee794094e077951e37779be/jedi-0.10.1-py2.py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="c40b58119be456a8fb6a61a981c3bcaaccfc13c350cae59a96337d54b59cc5ae",
        url="https://pypi.org/packages/06/f0/1d2a8462b322a200323f6c1fbd18a3d4047d2ed89a39b2f7f9a2b994a271/jedi-0.10.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="51f2521a257bbc5ef036fddeaf29168e1312782fc580c5e889e53dba41ea730d",
        url="https://pypi.org/packages/c4/59/e48a369168a84c8aef9127c227fc3b9f53bc9c528b24c2cda20487bc2deb/jedi-0.9.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-parso@0.8:", when="@0.18")
        depends_on("py-parso@0.7", when="@0.17.1:0.17")
        depends_on("py-parso@0.5:", when="@0.14.1:0.15.1")
        depends_on("py-parso@0.3:", when="@0.12.1:0.14.0")
        depends_on("py-parso@0.2:", when="@0.12:0.12.0")

    # unfortunately pypi.io only offers a .whl for 0.10.0
