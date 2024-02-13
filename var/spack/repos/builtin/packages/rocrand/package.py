# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re

from spack.package import *


class Rocrand(CMakePackage):
    """The rocRAND project provides functions that generate
    pseudo-random and quasi-random numbers."""

    homepage = "https://github.com/ROCm/rocRAND"
    git = "https://github.com/ROCm/rocRAND.git"
    url = "https://github.com/ROCm/rocRAND/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["librocrand"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.0.2", sha256="51d66c645987cbfb593aaa6be94109e87fe4cb7e9c70309eb3c159af0de292d7")
    version("6.0.0", sha256="cee93231c088be524bb2cb0e6093ec47e62e61a55153486bebbc2ca5b3d49360")
    version("5.7.1", sha256="885cd905bbd23d02ba8f3f87d5c0b79bc44bd020ea9af190f3959cf5aa33d07d")
    version("5.7.0", sha256="d6053d986821e5cbc6cfec0778476efb1411ef943f11e7a8b973b1814a259dcf")
    version("5.6.1", sha256="6bf71e687ffa0fcc1b00e3567dd43da4147a82390f1b2db5e6f1f594dee6066d")
    version("5.6.0", sha256="cc894d2f1af55e16b62c179062063946609c656043556189c656a115fd7d6f5f")
    version("5.5.1", sha256="e8bed3741b19e296bd698fc55b43686206f42f4deea6ace71513e0c48258cc6e")
    version("5.5.0", sha256="0481e7ef74c181026487a532d1c17e62dd468e508106edde0279ca1adeee6f9a")
    version("5.4.3", sha256="463aa760e9f74e45b326765040bb8a8a4fa27aaeaa5e5df16f8289125f88a619")
    version("5.4.0", sha256="0f6a0279b8b5a6dfbe32b45e1598218fe804fee36170d5c1f7b161c600544ef2")
    version("5.3.3", sha256="b0aae79dce7f6f9ef76ad2594745fe1f589a7b675b22f35b4d2369e7d5e1985a")
    version("5.3.0", sha256="be4c9f9433415bdfea50d9f47b8afb43ac315f205ed39674f863955a6c256dca")
    version("5.2.3", sha256="01eda8022fab7bafb2c457fe26a9e9c99950ed1b772ae7bf8710b23a90b56e32")
    version("5.2.1", sha256="4b2a7780f0112c12b5f307e1130e6b2c02ab984a0c1b94e9190dae38f0067600")
    version("5.2.0", sha256="ab3057e7c17a9fbe584f89ef98ec92a74d638a98d333e7d0f64daf7bc9051e38")
    version("5.1.3", sha256="4a19e1bcb60955a02a73ad64594c23886d6749afe06b0104e2b877dbe02c8d1c")
    version("5.1.0", sha256="0c6f114a775d0b38be71f3f621a10bde2104a1f655d5d68c5fecb79b8b51a815")
    version(
        "5.0.2",
        sha256="2dbce2a7fb273c2f9456c002adf3a510b9ec79f2ff32dfccdd59948f3ddb1505",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="356a03a74d6d5df3ae2d38da07929f23d90bb4dee71f88792c25c25069e673bc",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="1523997a21437c3b74d47a319d81f8cc44b8e96ec5174004944f2fb4629900db",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="fd391f81b9ea0b57808d93e8b72d86eec1b4c3529180dfb99ed6d3e2aa1285c2",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="b3d6ae0cdbbdfb56a73035690f8cb9e173fec1ccaaf9a4c5fdbe5e562e50c901",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="a85ced6c155befb7df8d58365518f4d9afc4407ee4e01d4640b5fd94604ca3e0",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="15725c89e9cc9cc76bd30415fd2c0c5b354078831394ab8b23fe6633497b92c8",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="94327e38739030ab6719a257f5a928a35842694750c7f46d9e11ff2164c2baed",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="1cafdbfa15cde635bd424d2a858dc5cc94d668f9a211ff39606ee01ed1715f41",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="f55e2b49b4dfd887e46eea049f3359ae03c60bae366ffc979667d364205bc99c",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="a500a3a83be36b6c91aa062dc6eef1f9fc1d9ee62422d541cc279513d98efa91",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="79eb84d41363a46ed9bb18d9757cf6a419d2f48bb6a71b8e4db616a5007a6560",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="5e43fe07afe2c7327a692b3b580875bae6e6ee790e044c053fffafbfcbc14860",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="592865a45e7ef55ad9d7eddc8082df69eacfd2c1f3e9c57810eb336b15cd5732",
        deprecated=True,
    )

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant("hiprand", default=True, when="@5.1.0:", description="Build the hiprand library")

    depends_on("cmake@3.10.2:", type="build", when="@4.5.0:")
    depends_on("cmake@3.5.1:", type="build")

    depends_on("googletest@1.10.0:", type="test")

    # This patch ensures that libhiprand.so searches for librocrand.so in its
    # own directory first thanks to the $ORIGIN RPATH setting. Otherwise,
    # libhiprand.so cannot find dependency librocrand.so despite being in the
    # same directory.
    patch(
        "hiprand_prefer_samedir_rocrand.patch", working_dir="hiprand", when="@5.2.0:5.4 +hiprand"
    )

    # Add hiprand sources thru the below
    for d_version, d_commit in [
        ("5.4.3", "125d691d3bcc6de5f5d63cf5f5a993c636251208"),
        ("5.4.0", "125d691d3bcc6de5f5d63cf5f5a993c636251208"),
        ("5.3.3", "12e2f070337945318295c330bf69c6c060928b9e"),
        ("5.3.0", "12e2f070337945318295c330bf69c6c060928b9e"),
        ("5.2.3", "12e2f070337945318295c330bf69c6c060928b9e"),
        ("5.2.1", "12e2f070337945318295c330bf69c6c060928b9e"),
        ("5.2.0", "12e2f070337945318295c330bf69c6c060928b9e"),
        ("5.1.3", "20ac3db9d7462c15a3e96a6f0507cd5f2ee089c4"),
        ("5.1.0", "20ac3db9d7462c15a3e96a6f0507cd5f2ee089c4"),
    ]:
        resource(
            name="hipRAND",
            git="https://github.com/ROCm/hipRAND.git",
            commit=d_commit,
            destination="",
            placement="hiprand",
            when="@{0} +hiprand".format(d_version),
        )
    resource(
        name="hipRAND",
        git="https://github.com/ROCm/hipRAND.git",
        branch="master",
        destination="",
        placement="hiprand",
        when="@master +hiprand",
    )
    resource(
        name="hipRAND",
        git="https://github.com/ROCm/hipRAND.git",
        branch="develop",
        destination="",
        placement="hiprand",
        when="@develop +hiprand",
    )

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
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    def patch(self):
        if self.spec.satisfies("@5.1.0:5.4 +hiprand"):
            os.rmdir("hipRAND")
            os.rename("hiprand", "hipRAND")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    @run_after("install")
    def fix_library_locations(self):
        if self.spec.satisfies("~hiprand"):
            return
        """Fix the rocRAND and hipRAND libraries location"""
        # rocRAND installs librocrand.so* and libhiprand.so* to rocrand/lib and
        # hiprand/lib, respectively. This confuses spack's RPATH management. We
        # fix it by adding a symlink to the libraries.
        if self.spec.satisfies("@:5.0.2"):
            hiprand_lib_path = join_path(self.prefix, "hiprand", "lib")
            rocrand_lib_path = join_path(self.prefix, "rocrand", "lib")
            mkdirp(self.prefix.lib)
            with working_dir(hiprand_lib_path):
                hiprand_libs = glob.glob("*.so*")
                for lib in hiprand_libs:
                    os.symlink(join_path(hiprand_lib_path, lib), join_path(self.prefix.lib, lib))
            with working_dir(rocrand_lib_path):
                rocrand_libs = glob.glob("*.so*")
                for lib in rocrand_libs:
                    os.symlink(join_path(rocrand_lib_path, lib), join_path(self.prefix.lib, lib))
            """Fix the rocRAND and hipRAND include path"""
            # rocRAND installs rocrand*.h* and hiprand*.h* rocrand/include and
            # hiprand/include, respectively. This confuses spack's RPATH management. We
            # fix it by adding a symlink to the header files.
            hiprand_include_path = join_path(self.prefix, "hiprand", "include")
            rocrand_include_path = join_path(self.prefix, "rocrand", "include")

            with working_dir(hiprand_include_path):
                hiprand_includes = glob.glob("*.h*")
            hiprand_path = join_path(self.prefix, "hiprand")
            with working_dir(hiprand_path):
                for header_file in hiprand_includes:
                    os.symlink(join_path("include", header_file), header_file)
            with working_dir(rocrand_include_path):
                rocrand_includes = glob.glob("*.h*")
            rocrand_path = join_path(self.prefix, "rocrand")
            with working_dir(rocrand_path):
                for header_file in rocrand_includes:
                    os.symlink(join_path("include", header_file), header_file)
        elif self.spec.satisfies("@5.1.0:5.1.3"):
            if not os.path.isdir(os.path.join(self.prefix, "hiprand")):
                os.mkdir(os.path.join(self.prefix, "hiprand"))
            os.mkdir(os.path.join(self.prefix, "hiprand", "include"))
            hiprand_include_path = join_path(self.prefix, "include", "hiprand")
            with working_dir(hiprand_include_path):
                hiprand_includes = glob.glob("*.h*")
            hiprand_path = join_path(self.prefix, "hiprand", "include")
            with working_dir(hiprand_path):
                for header_file in hiprand_includes:
                    os.symlink(join_path("../../include/hiprand", header_file), header_file)

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = [self.define("BUILD_BENCHMARK", "OFF"), self.define("BUILD_TEST", self.run_tests)]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.1.0:5.4"):
            args.append(self.define_from_variant("BUILD_HIPRAND", "hiprand"))
        else:
            args.append(self.define("BUILD_HIPRAND", "OFF"))

        return args
