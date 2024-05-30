# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HipifyClang(CMakePackage):
    """hipify-clang is a clang-based tool for translation CUDA
    sources into HIP sources"""

    homepage = "https://github.com/ROCm/HIPIFY"
    git = "https://github.com/ROCm/HIPIFY.git"
    url = "https://github.com/ROCm/HIPIFY/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    license("MIT")

    version("master", branch="master")
    version("6.1.1", sha256="240b83ccbe1b6514a6af6c2261e306948ce6c2b1c4d1056e830bbaebddeabd82")
    version("6.1.0", sha256="dc61b476081750130c62c7540fce49ee3a45a2b74e185d20049382574c1842d1")
    version("6.0.2", sha256="21e46276677ec8c00e61c0cbf5fa42185517f6af0d4845ea877fd40eb35198c4")
    version("6.0.0", sha256="91bed2b72a6684a04e078e50b12b36b93f64ff96523283f4e5d9a33c11e6b967")
    version("5.7.1", sha256="43121e62233dab010ab686d6805bc2d3163f0dc5e89cc503d50c4bcd59eeb394")
    version("5.7.0", sha256="10e4386727e102fba166f012147120a6ec776e8d95fbcac3af93e243205d80a6")
    version("5.6.1", sha256="ec3a4f276556f9fd924ea3c89be11b6c6ddf999cdd4387f669e38e41ee0042e8")
    version("5.6.0", sha256="a2572037a7d3bd0813bd6819a5e6c0e911678db5fd3ab15a65370601df91891b")
    version("5.5.1", sha256="35b9c07a7afaf9cf6f3bbe9dd147fa81b1b297af3e5e26e60c55629e83feaa48")
    version("5.5.0", sha256="1b75c702799ac93027337f8fb61d7c27ba960e8ece60d907fc8c5ab3f15c3fe9")
    version("5.4.3", sha256="79e27bd6c0a28e6a62b02dccc0b5d88a81f69fe58487e83f3b7ab47d6b64341b")
    version("5.4.0", sha256="9f51eb280671ae7f7e14eb593ee3ef099899221c4bdccfbdb7a78681ad17f37f")
    version("5.3.3", sha256="9d08e2896e52c10a0a189a5407567043f2510adc7bf618591c97a22a23699691")
    version("5.3.0", sha256="7674900d2b9319d91fa8f469252c5acb5bedf339142417cdcb64f33ee8482e00")
    with default_args(deprecated=True):
        version("5.2.3", sha256="1314a37ab544b68fd51858b77d2d4b30ecff82ef3f90de6e80891a95f6749849")
        version("5.2.1", sha256="4d658d00b219f7ef40e832da3680852aeb4c258c0a114f1779fa4cda99ee23b1")
        version("5.2.0", sha256="dcd5f44daceb984bb654a209e78debf81e1cdeaf9202444a1e110b45ad6c3f4f")
        version("5.1.3", sha256="6354b08b8ab2f4c481398fb768652bae00bb78c4cec7a11d5f6c7e4cb831ddf1")
        version("5.1.0", sha256="ba792294cbdcc880e0f02e38ee352dff8d4a2c183430e13d1c5ed176bd46cfc5")

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    # the patch was added to install the targets in the correct directory structure
    # this will fix the issue https://github.com/spack/spack/issues/30711

    patch("0001-install-hipify-clang-in-bin-dir-and-llvm-clangs-head.patch", when="@5.1.0:5.5")
    patch("0002-install-hipify-clang-in-bin-dir-and-llvm-clangs-head.patch", when="@5.6:6.0")
    patch("0003-install-hipify-clang-in-bin-dir-and-llvm-clangs-head.patch", when="@6.1:")

    depends_on("cmake@3.5:", type="build")
    for ver in [
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "master",
    ]:
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

    for ver in [
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    def setup_run_environment(self, env):
        # The installer puts the binaries directly into the prefix
        # instead of prefix/bin, so add prefix to the PATH
        env.prepend_path("PATH", self.spec.prefix)

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@5.5"):
            args.append(self.define("SWDEV_375013", "ON"))
        if self.spec.satisfies("@5.7.0:"):
            args.append(self.define_from_variant("ADDRESS_SANITIZER", "asan"))
        return args
