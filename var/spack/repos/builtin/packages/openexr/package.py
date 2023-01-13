# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openexr(CMakePackage):
    """OpenEXR Graphics Tools (high dynamic-range image file format)"""

    homepage = "https://www.openexr.com/"
    url = "https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v3.1.5.tar.gz"

    # New versions should come from github now
    version("3.1.5", sha256="93925805c1fc4f8162b35f0ae109c4a75344e6decae5a240afdfce25f8a433ec")
    version(
        "2.3.0",
        sha256="fd6cb3a87f8c1a233be17b94c74799e6241d50fc5efd4df75c7a4b9cf4e25ea6",
        url="https://github.com/AcademySoftwareFoundation/openexr/releases/download/v2.3.0/openexr-2.3.0.tar.gz",
    )

    version(
        "2.2.0",
        sha256="36a012f6c43213f840ce29a8b182700f6cf6b214bea0d5735594136b44914231",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.2.0.tar.gz",
    )
    version(
        "2.1.0",
        sha256="54486b454073c1dcb5ae9892cf0f730ffefe62f38176325281505093fd218a14",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.1.0.tar.gz",
    )
    version(
        "2.0.1",
        sha256="b9924d2f9d57376ff99234209231ad97a47f5cfebd18a5d0570db6d1a220685a",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.0.1.tar.gz",
    )
    version(
        "1.7.0",
        sha256="b68a2164d01bd028d15bd96af2704634a344e291dc7cc2019a662045d8c52ca4",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.7.0.tar.gz",
    )
    version(
        "1.6.1",
        sha256="c616906ab958de9c37bb86ca7547cfedbdfbad5e1ca2a4ab98983c9afa6a5950",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.6.1.tar.gz",
    )
    version(
        "1.5.0",
        sha256="5a745eee4b8ab94cd16f85528c2debfebe6aa1ba23f5b8fc7933d4aa5c3c3416",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.5.0.tar.gz",
    )
    version(
        "1.4.0a",
        sha256="5d8a7327bd28eeb5d3064640d8eb32c3cd8c5a15999c70b0afa9f8af851936d1",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.4.0a.tar.gz",
    )
    version(
        "1.3.2",
        sha256="fa08ad904bf89e2968078d25d1d9817f5bc17f372d1bafabf82e8f08ca2adc20",
        url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.3.2.tar.gz",
    )

    variant("debug", default=False, description="Builds a debug version of the libraries")

    depends_on("cmake@3.12:", when="@3:", type="build")
    depends_on("pkgconfig", when="@:2", type="build")
    depends_on("imath", when="@3:")
    depends_on("ilmbase", when="@:2")
    depends_on("zlib")

    @property
    def build_directory(self):
        if self.spec.satisfies("@3:"):
            return super(Openexr, self).build_directory
        else:
            return "."

    def configure_args(self):
        args = ["--prefix=" + self.prefix]

        if "+debug" in self.spec:
            args.append("--enable-debug")
        else:
            args.append("--disable-debug")

        return args

    @when("@:2")
    def cmake(self, spec, prefix):
        configure(*self.configure_args())
