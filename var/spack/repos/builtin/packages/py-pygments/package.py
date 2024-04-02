# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygments(PythonPackage):
    """Pygments is a syntax highlighting package written in Python."""

    homepage = "https://pygments.org/"
    pypi = "Pygments/Pygments-2.4.2.tar.gz"
    git = "https://github.com/pygments/pygments.git"

    license("BSD-2-Clause")

    version(
        "2.16.1",
        sha256="13fc09fa63bc8d8671a6d247e1eb303c4b343eaee81d861f3404db2935653692",
        url="https://pypi.org/packages/43/88/29adf0b44ba6ac85045e63734ae0997d3c58d8b1a91c914d240828d0d73d/Pygments-2.16.1-py3-none-any.whl",
    )
    version(
        "2.16.0",
        sha256="90e046f72a58b65edd7e6bd99926ffa1b9d19e23db166905046bea0069c0894d",
        url="https://pypi.org/packages/ec/9a/40aa8248006cbe35b8bffc83cfca0ffdf68306d4354bca334a25b4b275a0/Pygments-2.16.0-py3-none-any.whl",
    )
    version(
        "2.15.1",
        sha256="db2db3deb4b4179f399a09054b023b6a586b76499d36965813c71aa8ed7b5fd1",
        url="https://pypi.org/packages/34/a7/37c8d68532ba71549db4212cb036dbd6161b40e463aba336770e80c72f84/Pygments-2.15.1-py3-none-any.whl",
    )
    version(
        "2.13.0",
        sha256="f643f331ab57ba3c9d89212ee4a2dabc6e94f117cf4eefde99a0574720d14c42",
        url="https://pypi.org/packages/4f/82/672cd382e5b39ab1cd422a672382f08a1fb3d08d9e0c0f3707f33a52063b/Pygments-2.13.0-py3-none-any.whl",
    )
    version(
        "2.12.0",
        sha256="dc9c10fb40944260f6ed4c688ece0cd2048414940f1cea51b8b226318411c519",
        url="https://pypi.org/packages/5c/8e/1d9017950034297fffa336c72e693a5b51bbf85141b24a763882cf1977b5/Pygments-2.12.0-py3-none-any.whl",
    )
    version(
        "2.10.0",
        sha256="b8e67fe6af78f492b3c4b3e2970c0624cbf08beb1e493b2c99b9fa1b67a20380",
        url="https://pypi.org/packages/78/c8/8d9be2f72d8f465461f22b5f199c04f7ada933add4dae6e2468133c17471/Pygments-2.10.0-py3-none-any.whl",
    )
    version(
        "2.6.1",
        sha256="ff7a40b4860b727ab48fad6360eb351cc1b33cbf9b15a0f689ca5353e9463324",
        url="https://pypi.org/packages/2d/68/106af3ae51daf807e9cdcba6a90e518954eb8b70341cee52995540a53ead/Pygments-2.6.1-py3-none-any.whl",
    )
    version(
        "2.4.2",
        sha256="71e430bc85c88a430f000ac1d9b331d2407f681d6f6aec95e8bcfbc3df5b0127",
        url="https://pypi.org/packages/5c/73/1dfa428150e3ccb0fa3e68db406e5be48698f2a979ccbcec795f28f44048/Pygments-2.4.2-py2.py3-none-any.whl",
    )
    version(
        "2.3.1",
        sha256="e8218dd399a61674745138520d0d4cf2621d7e032439341bc3f647bff125818d",
        url="https://pypi.org/packages/13/e5/6d710c9cf96c31ac82657bcfb441df328b22df8564d58d0c4cd62612674c/Pygments-2.3.1-py2.py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="78f3f434bcc5d6ee09020f92ba487f95ba50f1e3ef83ae96b9d5ffa1bab25c5d",
        url="https://pypi.org/packages/02/ee/b6e02dc6529e82b75bb06823ff7d005b141037cb1416b10c6f00fc419dca/Pygments-2.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.1.3",
        sha256="485602129949b14247e8b124d28af4654dffbd076537c4a9c44a538a2c1755b7",
        url="https://pypi.org/packages/9e/d0/d692085518c6a2dc875fe421c866fb6a08e0d9796ca507803c1e545fa116/Pygments-2.1.3-py2.py3-none-any.whl",
    )
    version(
        "2.0.2",
        sha256="5ded2fa9094fd7dfeb3da92636409fd702a0d07d606283504d7ee04401cee5cb",
        url="https://pypi.org/packages/87/e3/cadb43a197476ec0adef73292ea7ea188f2b0531188eebc150905d3ed78c/Pygments-2.0.2-py3-none-any.whl",
    )
    version(
        "2.0.1",
        sha256="668c8e665b935f623859c13213e1bc9b33fd19feec4db7c2f8e855c1c8c559d7",
        url="https://pypi.org/packages/19/2f/a5ff1b61ee66ebf0cffc69137b1c9dc021fc85c338f7da56fc43b21479d7/Pygments-2.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.15:")
