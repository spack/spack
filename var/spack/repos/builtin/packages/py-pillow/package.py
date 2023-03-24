# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPillowBase(PythonPackage):
    """Base class for Pillow and its fork Pillow-SIMD."""

    maintainers("adamjstewart")

    provides("pil")

    # These defaults correspond to Pillow defaults
    # https://pillow.readthedocs.io/en/stable/installation.html#external-libraries
    VARIANTS_IN_SETUP_CFG = (
        "zlib",
        "jpeg",
        "tiff",
        "freetype",
        "lcms",
        "webp",
        "webpmux",
        "jpeg2000",
        "imagequant",
        "xcb",
    )
    variant("zlib", default=True, description="Compressed PNG functionality")
    variant("jpeg", default=True, description="JPEG functionality")
    variant("tiff", default=False, description="Compressed TIFF functionality")
    variant("freetype", default=False, description="Type related services")
    variant("lcms", default=False, description="Color management")
    variant("webp", default=False, description="WebP format")
    variant("webpmux", when="+webp", default=False, description="WebP metadata")
    variant("jpeg2000", default=False, description="JPEG 2000 functionality")
    variant("imagequant", when="@3.3:", default=False, description="Improved color quantization")
    variant("xcb", when="@7.1:", default=False, description="X11 screengrab support")
    variant("raqm", when="@8.2:", default=False, description="RAQM support")

    # Required dependencies
    # https://pillow.readthedocs.io/en/latest/installation.html#notes
    depends_on("python@3.7:3.10", when="@9:", type=("build", "run"))
    depends_on("python@3.6:3.10", when="@8.3.2:8.4", type=("build", "run"))
    depends_on("python@3.6:3.9", when="@8:8.3.1", type=("build", "run"))
    depends_on("python@3.5:3.8", when="@7.0:7.2", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:3.8", when="@6.2.1:6.2.2", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:3.7", when="@6.0:6.2.0", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:3.7", when="@5.2:5.4", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Optional dependencies
    depends_on("zlib", when="+zlib")
    depends_on("jpeg", when="+jpeg")
    depends_on("libtiff", when="+tiff")
    depends_on("freetype", when="+freetype")
    depends_on("lcms@2:", when="+lcms")
    depends_on("libwebp", when="+webp")
    depends_on("libwebp+libwebpmux+libwebpdemux", when="+webpmux")
    depends_on("openjpeg", when="+jpeg2000")
    depends_on("libimagequant", when="+imagequant")
    depends_on("libxcb", when="+xcb")
    depends_on("libraqm", when="+raqm")

    # Conflicting options
    conflicts("+raqm", when="~freetype")

    def patch(self):
        """Patch setup.py to provide library and include directories
        for dependencies."""

        library_dirs = []
        include_dirs = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)
            include_dirs.extend(query.headers.directories)

        setup = FileFilter("setup.py")
        setup.filter("library_dirs = []", "library_dirs = {0}".format(library_dirs), string=True)
        setup.filter("include_dirs = []", "include_dirs = {0}".format(include_dirs), string=True)

        def variant_to_cfg(variant):
            able = "enable" if "+" + variant in self.spec else "disable"
            return "{0}_{1}=1\n".format(able, variant)

        with open("setup.cfg", "a") as setup:
            setup.write("[build_ext]\n")
            for variant in self.VARIANTS_IN_SETUP_CFG:
                setup.write(variant_to_cfg(variant))

            setup.write("rpath={0}\n".format(":".join(self.rpath)))
            setup.write("[install]\n")

    def setup_build_environment(self, env):
        env.set("MAX_CONCURRENCY", str(make_jobs))


class PyPillow(PyPillowBase):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    pypi = "Pillow/Pillow-7.2.0.tar.gz"

    version("9.2.0", sha256="75e636fd3e0fb872693f23ccb8a5ff2cd578801251f3a4f6854c6a5d437d3c04")
    version("9.1.1", sha256="7502539939b53d7565f3d11d87c78e7ec900d3c72945d4ee0e2f250d598309a0")
    version("9.1.0", sha256="f401ed2bbb155e1ade150ccc63db1a4f6c1909d3d378f7d1235a44e90d75fb97")
    version("9.0.1", sha256="6c8bc8238a7dfdaf7a75f5ec5a663f4173f8c367e5a39f87e720495e1eed75fa")
    version("9.0.0", sha256="ee6e2963e92762923956fe5d3479b1fdc3b76c83f290aad131a2f98c3df0593e")
    version("8.4.0", sha256="b8e2f83c56e141920c39464b852de3719dfbfb6e3c99a2d8da0edf4fb33176ed")
    version("8.0.0", sha256="59304c67d12394815331eda95ec892bf54ad95e0aa7bc1ccd8e0a4a5a25d4bf3")
    version("7.2.0", sha256="97f9e7953a77d5a70f49b9a48da7776dc51e9b738151b22dacf101641594a626")
    version("7.0.0", sha256="4d9ed9a64095e031435af120d3c910148067087541131e82b3e8db302f4c8946")
    version("6.2.2", sha256="db9ff0c251ed066d367f53b64827cc9e18ccea001b986d08c265e53625dab950")
    version("6.2.1", sha256="bf4e972a88f8841d8fdc6db1a75e0f8d763e66e3754b03006cbc3854d89f1cb1")
    version("6.2.0", sha256="4548236844327a718ce3bb182ab32a16fa2050c61e334e959f554cac052fb0df")
    version("6.0.0", sha256="809c0a2ce9032cbcd7b5313f71af4bdc5c8c771cb86eb7559afd954cab82ebb5")
    version("5.4.1", sha256="5233664eadfa342c639b9b9977190d64ad7aca4edc51a966394d7e08e7f38a9f")

    for ver in [
        "9.2.0",
        "9.1.1",
        "9.1.0",
        "9.0.1",
        "9.0.0",
        "8.4.0",
        "8.0.0",
        "7.2.0",
        "7.0.0",
        "6.2.2",
        "6.2.1",
        "6.2.0",
        "6.0.0",
        "5.4.1",
    ]:
        provides("pil@" + ver, when="@" + ver)
