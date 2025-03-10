# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class FrugallyDeep(CMakePackage):
    """A lightweight header-only library for using Keras (TensorFlow) models in C++."""

    homepage = "https://github.com/Dobiasd/frugally-deep"
    url = "https://github.com/Dobiasd/frugally-deep/archive/refs/tags/v0.16.3.tar.gz"

    license("MIT")

    version("0.16.3", sha256="2e3f6c77219465ba3960111fab0b0c80ec5a487df5c95e9c73173e946e990bc8")
    version("0.16.2", sha256="b16af09606dcf02359de53b7c47323baaeda9a174e1c87e126c3127c55571971")
    version("0.16.1", sha256="4dac01b779fded96b252b58b76fd29d93bb61257cfff9d2d96ccdab4f0e362ee")
    version("0.16.0", sha256="5ffe8dddb43a645094b2ca1d48e4ee78e685fbef3c89f08cea8425a39dad9865")

    depends_on("cxx", type="build")
    depends_on("functionalplus")
    depends_on("eigen")
    depends_on("nlohmann-json")
