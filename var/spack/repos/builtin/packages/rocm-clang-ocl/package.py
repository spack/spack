# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RocmClangOcl(CMakePackage):
    """OpenCL compilation with clang compiler"""

    homepage = "https://github.com/RadeonOpenCompute/clang-ocl"
    git = "https://github.com/RadeonOpenCompute/clang-ocl.git"
    url = "https://github.com/RadeonOpenCompute/clang-ocl/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    version("master", branch="master")

    version("5.4.3", sha256="689e0354ea685bd488116de8eb902b902492e9ace184c3109b97b9a43f8b2d59")
    version("5.4.0", sha256="602f8fb1f36587543cc0ee95fd1938f8eeb03de79119101e128150332cc8d89c")
    version("5.3.3", sha256="549d5bf37507f67c5277abdeed4ec40b5d0edbfbb72907c685444c26b9ce6f8a")
    version("5.3.0", sha256="66b80ba050848ad921496bd894e740e66afad0ba1923b385f01f2eeae97999ad")
    version("5.2.3", sha256="9cdb387168975207314c08ba63ae7cd11f70542117a5390eddbec77ebb84bed0")
    version("5.2.1", sha256="693a9a360cb2f7e6910a6714df236df6a9d984f94b01712103a520d8e506c03f")
    version("5.2.0", sha256="a2059f6aeccc119abbd444cb37128e00e4854e22a88a47f120f8f8b947d862c5")
    version("5.1.3", sha256="e19ee15f26fc03309398ac73cc738508c0e1617deccfd667d369a3948b5d3552")
    version("5.1.0", sha256="38d9e2e98cff1a262fdd45c3239fd76a9f6ad5eff38a31aa19c3bb0faea53375")
    version(
        "5.0.2",
        sha256="5e8f39200227388817024ee7ce46a996e43e433ed308f8d5e8e4c03629d8a5e7",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="0dff230754b790a417eb3d6be6f50c3727f944e0157686100354eba1e47d30f3",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="8cc7b8658e81ef378c16bbb00fc6b29140c850da70adc4e520ecec9b4517beb8",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="b9ab42629c8697f8ffdae99ffd25f939161fa8a7a1c49a9ce19d8b207bedbbae",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="12461d4fd4f3f40710d2c041cfee37da83ccda9d2761d7708335349e7ec5ad87",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="bc5650f2f105b10a1e22d8e5cc9464b0f960252a08e5e1fdee222af1fc5c022c",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="702796f4e31f6119173d915db9bee13c060a75d9eb5b1f8e3d20779d6702dfdc",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="c6e65da5541df9ee940caeeffe1b87c92547edc1770538fd2010c9c998a593b5",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="c8f9091396ee0096f6d7c1cd13d80532c424e838bec1e4cebf903ebaf649e82e",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="17fc8fb8c38b18f9f0cac339dda6cea3e9e66805f7a92ec2456072fc1e72fa85",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="3d63c7ac259ba8b0bfd5e4a94df1490c2b6cbac4d43dc7bbc210a536251268fe",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="a829aa2efb6e3bc00d8a08a96404f937f3c8adf3b4922b5ac35050d6e08b912d",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="9c00c7e7dd3ac8326ae6772a43866b44ae049d5960ea6993d14a2370db74d326",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="38c95fbd0ac3d11d9bd224ad333b68b9620dde502b8a8a9f3d96ba642901e8bb",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.5:", type="build")

    for ver in [
        "3.5.0",
        "3.7.0",
        "3.8.0",
        "3.9.0",
        "3.10.0",
        "4.0.0",
        "4.1.0",
        "4.2.0",
        "4.3.0",
        "4.3.1",
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "master",
    ]:
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)

        # support both builtin and standalone device libs
        depends_on(
            "rocm-device-libs@" + ver, when="@{0} ^llvm-amdgpu ~rocm-device-libs".format(ver)
        )
