# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class FrugallyDeep(CMakePackage):
    """A lightweight header-only library for using Keras (TensorFlow) models in C++."""

    homepage = "https://github.com/Dobiasd/frugally-deep"
    url = "https://github.com/Dobiasd/frugally-deep/archive/refs/tags/v0.16.3.tar.gz"

    license("MIT")

    version("0.18.2", sha256="e4274735261c89fd312e5a23e16bfa540752d1a61a190037f63f4d2612495c64")
    version("0.18.1", sha256="86e54c8faf47a9c5a217d71b9f7ea902dbaa05baf6e22b0e2e1e48337550cc59")
    version("0.18.0", sha256="0d757f564e8cb6dc418e2f76191d12b8ae6c1eae3cabac5968583b8b53eda20d")
    version("0.17.1", sha256="f3130dc0d01640e12ea7cb88e440ec9ac716b89ce45eae3f1d1eb937194c305f")
    version("0.17.0", sha256="b92a151b9a5a8c69b00e63e9d4cc4da018056d111ca6a976eec14fc59db87d0b")
    version("0.16.3", sha256="2e3f6c77219465ba3960111fab0b0c80ec5a487df5c95e9c73173e946e990bc8")
    version("0.16.2", sha256="b16af09606dcf02359de53b7c47323baaeda9a174e1c87e126c3127c55571971")
    version("0.16.1", sha256="4dac01b779fded96b252b58b76fd29d93bb61257cfff9d2d96ccdab4f0e362ee")
    version("0.16.0", sha256="5ffe8dddb43a645094b2ca1d48e4ee78e685fbef3c89f08cea8425a39dad9865")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("functionalplus")
    depends_on("eigen")
    depends_on("nlohmann-json")
