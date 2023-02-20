# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HipifyClang(CMakePackage):
    """hipify-clang is a clang-based tool for translation CUDA
    sources into HIP sources"""

    homepage = "https://github.com/ROCm-Developer-Tools/HIPIFY"
    git = "https://github.com/ROCm-Developer-Tools/HIPIFY.git"
    url = "https://github.com/ROCm-Developer-Tools/HIPIFY/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    version("master", branch="master")

    version("5.4.3", sha256="79e27bd6c0a28e6a62b02dccc0b5d88a81f69fe58487e83f3b7ab47d6b64341b")
    version("5.4.0", sha256="9f51eb280671ae7f7e14eb593ee3ef099899221c4bdccfbdb7a78681ad17f37f")
    version("5.3.3", sha256="9d08e2896e52c10a0a189a5407567043f2510adc7bf618591c97a22a23699691")
    version("5.3.0", sha256="7674900d2b9319d91fa8f469252c5acb5bedf339142417cdcb64f33ee8482e00")
    version("5.2.3", sha256="1314a37ab544b68fd51858b77d2d4b30ecff82ef3f90de6e80891a95f6749849")
    version("5.2.1", sha256="4d658d00b219f7ef40e832da3680852aeb4c258c0a114f1779fa4cda99ee23b1")
    version("5.2.0", sha256="dcd5f44daceb984bb654a209e78debf81e1cdeaf9202444a1e110b45ad6c3f4f")
    version("5.1.3", sha256="6354b08b8ab2f4c481398fb768652bae00bb78c4cec7a11d5f6c7e4cb831ddf1")
    version("5.1.0", sha256="ba792294cbdcc880e0f02e38ee352dff8d4a2c183430e13d1c5ed176bd46cfc5")
    version(
        "5.0.2",
        sha256="812bccfeb044483a1c7df89f45843afcb28d8146f348c792f082b693cbff3984",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="06fbb3259b6d014bc24fb3c05f71026bc39ae564559d40f2ca37236044c7ba17",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="f0d401e634642a1d6659b9163a38661ee38da1e1aceabb1f16f78f8fce048a4e",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="1f6e1bd4b9d64eed67f519c453fa65b362a20583df1f35fd09d08de831f3c8de",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="c5754f7c2c68ea4f65cc0ffc1e8ccc30634181525b25c10817e07eaa75ca8157",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="182b336a994e3de0dfbce935dc35091388d18a29e3cfdadb2ab7da8a2dc121a2",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="afdc82ae00e14e8e742be6cd47d8fb120d18fc52fe96cba8d8ac4c56176a432e",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="ec9cc410167b6ab31706742f3d7a77dbd29eb548e7371134b3aace8597665475",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="9d3906d606fca2bcb58f5f2a70cc4b9e298ca0e12a84ee5f18e42b7df97b38a4",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="7ebba22ed70100150bedddffa08a84f91b546347662862487b6703a1edce2623",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="07adb98e91ddd7420d873806866d53eaf77527fac57799e846823522191ba89a",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="095b876a750a0dc1ae669102ba53d668f65062b823f8be745411db86a2db7916",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="dd58c8b88d4b7877f2521b02954de79d570fa36fc751a17d33e56436ee02571e",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="31e7c11d3e221e15a2721456c4f8bceea9c28fd37345464c86ea74cf05ddf2c9",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    # the patch was added to install the targets in the correct directory structure
    # this will fix the issue https://github.com/spack/spack/issues/30711

    patch("0001-install-hipify-clang-in-bin-dir-and-llvm-clangs-head.patch", when="@5.1.0:")

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
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)

    def setup_run_environment(self, env):
        # The installer puts the binaries directly into the prefix
        # instead of prefix/bin, so add prefix to the PATH
        env.prepend_path("PATH", self.spec.prefix)
