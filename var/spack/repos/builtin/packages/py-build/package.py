# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBuild(PythonPackage):
    """A simple, correct PEP517 package builder."""

    homepage = "https://github.com/pypa/build"
    pypi = "build/build-0.7.0.tar.gz"

    license("MIT")

    version(
        "1.0.3",
        sha256="589bf99a67df7c9cf07ec0ac0e5e2ea5d4b37ac63301c4986d1acb126aa83f8f",
        url="https://pypi.org/packages/93/dd/b464b728b866aaa62785a609e0dd8c72201d62c5f7c53e7c20f4dceb085f/build-1.0.3-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="f4c7b45e70e2c345e673902253d435a9a7729ff09ab574924420cf120c60bcc9",
        url="https://pypi.org/packages/75/59/2b0c77e78f754e4443126349e15a9f12716a34e9dcce8e8d61b1b6d553e7/build-1.0.0-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="af266720050a66c893a6096a2f410989eeac74ff9a68ba194b3f6473e8e26171",
        url="https://pypi.org/packages/58/91/17b00d5fac63d3dca605f1b8269ba3c65e98059e1fd99d00283e42a454f0/build-0.10.0-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="38a7a2b7a0bdc61a42a0a67509d88c71ecfc37b393baba770fae34e20929ff69",
        url="https://pypi.org/packages/03/97/f58c723ff036a8d8b4d3115377c0a37ed05c1f68dd9a0d66dab5e82c5c1c/build-0.9.0-py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="19b0ed489f92ace6947698c3ca8436cb0556a66e2aa2d34cd70e2a5d27cd0437",
        url="https://pypi.org/packages/7a/24/ee8271da317b692fcb9d026ff7f344ac6c4ec661a97f0e2a11fa7992544a/build-0.8.0-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="21b7ebbd1b22499c4dac536abc7606696ea4d909fd755e00f09f3c0f2c05e3c8",
        url="https://pypi.org/packages/46/28/70768d6585162eb29df181aed4c1adb3081307ad46a892c390dab549dc13/build-0.7.0-py3-none-any.whl",
    )

    variant("virtualenv", default=False, description="Install optional virtualenv dependency")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.10:1.1")
        depends_on("py-importlib-metadata@4.6:", when="@1: ^python@:3.9")
        depends_on("py-importlib-metadata@0.22:", when="@0.4:0 ^python@:3.7")
        depends_on("py-packaging@19:", when="@0.4:1.1")
        depends_on("py-pep517@0.9:", when="@0.4:0.9")
        depends_on("py-pyproject-hooks", when="@0.10:")
        depends_on("py-tomli@1.1:", when="@0.10: ^python@:3.10")
        depends_on("py-tomli@1:", when="@0.8:0.9 ^python@:3.10")
        depends_on("py-tomli@1:", when="@0.6:0.7")
        depends_on("py-virtualenv@20.0.35:", when="+virtualenv")

    # Historical dependencies

    # https://github.com/pypa/build/issues/266
    # https://github.com/pypa/build/issues/406
