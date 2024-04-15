# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAttrs(PythonPackage):
    """Classes Without Boilerplate"""

    homepage = "https://attrs.org/"
    pypi = "attrs/attrs-20.3.0.tar.gz"
    git = "https://github.com/python-attrs/attrs"

    license("MIT")

    version(
        "23.1.0",
        sha256="1f28b4522cdc2fb4256ac1a020c78acf9cba2c6b461ccd2c126f3aa8e8335d04",
        url="https://pypi.org/packages/f0/eb/fcb708c7bf5056045e9e98f62b93bd7467eb718b0202e7698eb11d66416c/attrs-23.1.0-py3-none-any.whl",
    )
    version(
        "22.2.0",
        sha256="29e95c7f6778868dbd49170f98f8818f78f3dc5e0e37c0b1f474e3561b240836",
        url="https://pypi.org/packages/fb/6e/6f83bf616d2becdf333a1640f1d463fef3150e2e926b7010cb0f81c95e88/attrs-22.2.0-py3-none-any.whl",
    )
    version(
        "22.1.0",
        sha256="86efa402f67bf2df34f51a335487cf46b1ec130d02b8d39fd248abfd30da551c",
        url="https://pypi.org/packages/f2/bc/d817287d1aa01878af07c19505fafd1165cd6a119e9d0821ca1d1c20312d/attrs-22.1.0-py2.py3-none-any.whl",
    )
    version(
        "21.4.0",
        sha256="2d27e3784d7a565d36ab851fe94887c5eccd6a463168875832a1be79c82828b4",
        url="https://pypi.org/packages/be/be/7abce643bfdf8ca01c48afa2ddf8308c2308b0c3b239a44e57d020afa0ef/attrs-21.4.0-py2.py3-none-any.whl",
    )
    version(
        "21.2.0",
        sha256="149e90d6d8ac20db7a955ad60cf0e6881a3f20d37096140088356da6c716b0b1",
        url="https://pypi.org/packages/20/a9/ba6f1cd1a1517ff022b35acd6a7e4246371dfab08b8e42b829b6d07913cc/attrs-21.2.0-py2.py3-none-any.whl",
    )
    version(
        "20.3.0",
        sha256="31b2eced602aa8423c2aea9c76a724617ed67cf9513173fd3a4f03e3a929c7e6",
        url="https://pypi.org/packages/c3/aa/cb45262569fcc047bf070b5de61813724d6726db83259222cd7b4c79821a/attrs-20.3.0-py2.py3-none-any.whl",
    )
    version(
        "20.2.0",
        sha256="fce7fc47dfc976152e82d53ff92fa0407700c21acd20886a13777a0d20e655dc",
        url="https://pypi.org/packages/14/df/479736ae1ef59842f512548bacefad1abed705e400212acba43f9b0fa556/attrs-20.2.0-py2.py3-none-any.whl",
    )
    version(
        "20.1.0",
        sha256="2867b7b9f8326499ab5b0e2d12801fa5c98842d2cbd22b35112ae04bf85b4dff",
        url="https://pypi.org/packages/d6/e1/3aa3b03e7643ffd6e499b203fd2a44f79893443e8b0b520d05d3e5c638d5/attrs-20.1.0-py2.py3-none-any.whl",
    )
    version(
        "19.3.0",
        sha256="08a96c641c3a74e44eb59afb61a24f2cb9f4d7188748e76ba4bb5edfa3cb7d1c",
        url="https://pypi.org/packages/a2/db/4313ab3be961f7a763066401fb77f7748373b6094076ae2bda2806988af6/attrs-19.3.0-py2.py3-none-any.whl",
    )
    version(
        "19.2.0",
        sha256="ec20e7a4825331c1b5ebf261d111e16fa9612c1f7a5e1f884f12bd53a664dfd2",
        url="https://pypi.org/packages/6b/e8/2ecaf86b128a34e225807f03b22664302937ab826bd3b7eccab6754d29ea/attrs-19.2.0-py2.py3-none-any.whl",
    )
    version(
        "19.1.0",
        sha256="69c0dbf2ed392de1cb5ec704444b08a5ef81680a61cb899dc08127123af36a79",
        url="https://pypi.org/packages/23/96/d828354fa2dbdf216eaa7b7de0db692f12c234f7ef888cc14980ef40d1d2/attrs-19.1.0-py2.py3-none-any.whl",
    )
    version(
        "18.1.0",
        sha256="4b90b09eeeb9b88c35bc642cbac057e45a5fd85367b985bd2809c62b7b939265",
        url="https://pypi.org/packages/41/59/cedf87e91ed541be7957c501a92102f9cc6363c623a7666d69d51c78ac5b/attrs-18.1.0-py2.py3-none-any.whl",
    )
    version(
        "16.3.0",
        sha256="c59426b15b45e39a7bc408eb6ba7e7188d9532764f873cc691199ddd975c97ef",
        url="https://pypi.org/packages/bb/6c/730710c765ab6d4493f460196ab003671d27b38568412a780fc67532b47c/attrs-16.3.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@23:")
        depends_on("py-importlib-metadata", when="@23: ^python@:3.7")
