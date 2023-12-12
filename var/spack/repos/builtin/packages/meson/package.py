# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Meson(PythonPackage):
    """Meson is a portable open source build system meant to be both
    extremely fast, and as user friendly as possible."""

    homepage = "https://mesonbuild.com/"
    url = "https://github.com/mesonbuild/meson/archive/0.49.0.tar.gz"

    tags = ["build-tools"]

    maintainers("eli-schwartz", "michaelkuhn")

    version("1.3.0", sha256="6c4b4f35b51a260b362535fd32fee6d244871be38a2880f4de3ea9c6e69a0808")
    version("1.2.2", sha256="1caa0ef6082e311bdca9836e7907f548b8c3f041a42ed41f0ff916b83ac7dddd")
    version("1.2.1", sha256="e1f3b32b636cc86496261bd89e63f00f206754697c7069788b62beed5e042713")
    version("1.2.0", sha256="603489f0aaa6305f806c6cc4a4455a965f22290fc74f65871f589b002110c790")
    version("1.1.1", sha256="1c3b9e1a3a36b51adb5de498d582fd5cbf6763fadbcf151de9f2a762e02bd2e6")
    version("1.1.0", sha256="f29a3e14062043d75e82d16f1e41856e6b1ed7a7c016e10c7b13afa7ee6364cc")
    version("1.0.2", sha256="1f1239c3091668643f7d2086663d6afd8cc87fbab84fe7462bc18b9ba6d65de8")
    version("1.0.1", sha256="4ab3a5c0060dc22bdefb04507efc6c38acb910e91bcd467a38e1fa211e5a6cfe")
    version("1.0.0", sha256="a2ada84d43c7e57400daee80a880a1f5003d062b2cb6c9be1747b0db38f2eb8d")
    version("0.64.1", sha256="1d12a4bc1cf3ab18946d12cf0b6452e5254ada1ad50aacc97f87e2cccd7da315")
    version("0.64.0", sha256="6477993d781b6efea93091616a6d6a0766c0e026076dbeb11249bf1c9b49a347")
    version("0.63.3", sha256="7c516c2099b762203e8a0a22412aa465b7396e6f9b1ab728bad6e6db44dc2659")
    version("0.62.2", sha256="97108f4d9bb16bc758c44749bd25ec7d42c6a762961efbed8b7589a2a3551ea6")
    version("0.61.4", sha256="c9cc34bcb15c19cfd5ee0d7b07111152701f602db2b59ef6b63d3628e0bbe719")
    version("0.60.3", sha256="6c191a9b4049e0c9a2a7d1275ab635b91f6ffec1912d75df4c5ec6acf35f74fe")
    version("0.59.2", sha256="e6d5ccd503d41f938f6cfc4dc9e7326ffe28acabe091b1ff0c6535bdf09732dd")
    version("0.58.2", sha256="58115604dea9c1f70811578df3c210f4d67cf795d21a4418f6e9bb35406953f5")
    version("0.57.2", sha256="cd3773625253df4fd1c380faf03ffae3d02198d6301e7c8bc7bba6c66af66096")
    version("0.56.2", sha256="aaae961c3413033789248ffe6762589e80b6cf487c334d0b808e31a32c48f35f")

    depends_on("python@3.7:", when="@0.62.0:", type=("build", "run"))
    depends_on("python@3.6:", when="@0.57.0:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@0.62.0:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("ninja@1.8.2:", when="@0.62.0:", type="run")
    depends_on("ninja", type="run")

    # By default, Meson strips the rpath on installation. This patch disables
    # rpath modification completely to make sure that Spack's rpath changes
    # are not reverted.
    patch("rpath-0.56.patch", when="@0.56:0.57")
    patch("rpath-0.58.patch", when="@0.58:0.63")
    patch("rpath-0.64.patch", when="@0.64:")

    # Intel OneAPI compiler support
    # https://github.com/mesonbuild/meson/pull/10909
    # https://github.com/mesonbuild/meson/pull/9850
    patch("oneapi.patch", when="@0.62:0.63 %oneapi")

    # Python 3.12 detection support
    patch("python-3.12-support.patch", when="@1.1:1.2.2")

    # Broken config.h generation
    # https://github.com/mesonbuild/meson/pull/12532
    patch(
          "https://github.com/mesonbuild/meson/commit/9016e6958bb83feb9a724f20d8badb116bf7c5f2.patch?full_index=1",
          sha256="344a59f5606c233699b9aabbf10ef9c456edf82994d0d902329aa915f9f6ba6d",
          when="@1.3.0",
    )

    executables = ["^meson$"]

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)("--version", output=str, error=str).rstrip()

    def setup_dependent_build_environment(self, env, dependent_spec):
        # https://github.com/pybind/pybind11/issues/595
        if self.spec.satisfies("platform=darwin"):
            env.set("STRIP", "strip -x")

    def setup_dependent_package(self, module, dspec):
        module.meson = Executable(self.spec.prefix.bin.meson)
