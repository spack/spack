# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchvision(PythonPackage):
    """Image and video datasets and models for torch deep learning."""

    homepage = "https://github.com/pytorch/vision"
    url = "https://github.com/pytorch/vision/archive/v0.8.2.tar.gz"
    git = "https://github.com/pytorch/vision.git"

    maintainers("adamjstewart")

    version("main", branch="main")
    version("0.16.1", sha256="d31fe52e4540750c8d372b0f38f1bfa81d8261193f2c2c06577332831d203c50")
    version("0.16.0", sha256="79b30b082237e3ead21e74587cedf4a4d832f977cf7dfeccfb65f67988b12ceb")
    version("0.15.2", sha256="1efcb80e0a6e42c54f07ee16167839b4d302aeeecc12839cc47c74b06a2c20d4")
    version("0.15.1", sha256="689d23d4ebb0c7e54e8651c89b17155b64341c14ae4444a04ca7dc6f2b6a0a43")
    version("0.14.1", sha256="ced67e1cf1f97e168cdf271851a4d0b6d382ab7936e7bcbb39aaa87239c324b6")
    version("0.14.0", sha256="be1621c85c56eb40537cb74e6ec5d8e58ed8b69f8374a58bcb6ec413cb540c8b")
    version("0.13.1", sha256="c32fab734e62c7744dadeb82f7510ff58cc3bca1189d17b16aa99b08afc42249")
    version("0.13.0", sha256="2fe9139150800820d02c867a0b64b7c7fbc964d48d76fae235d6ef9215eabcf4")
    version("0.12.0", sha256="99e6d3d304184895ff4f6152e2d2ec1cbec89b3e057d9c940ae0125546b04e91")
    version("0.11.3", sha256="b4c51d27589783e6e6941ecaa67b55f6f41633874ec37f80b64a0c92c3196e0c")
    version("0.11.2", sha256="55689c57c29f82438a133d0af3315991037be59c8e02471bdcaa31731154a714")
    version("0.11.1", sha256="32a06ccf755e4d75006ce03701f207652747a63dbfdf65f0f20a1b6f93a2e834")
    version("0.11.0", sha256="8e85acf8f5d39f27e92e610ccb506dac0bf4412bb366a318d2aa5f384cbd4d2c")
    version("0.10.1", sha256="4d595cf0214c8adc817f8e3cd0043a027b52b481e05d67b04f4947fcb43d4277")
    version("0.10.0", sha256="82bb2c2b03d8a65f4ea74bb0ee5566b0876a1992aceefb1e11475c7b5d2e857b")
    version("0.9.2", sha256="b41fc99bbf18450750bcd1804393e7c09dc8d4873c6b7e544b11c70fda59cbc8")
    version("0.9.1", sha256="79964773729880e0eee0e6af13f336041121d4cc8491a3e2c0e5f184cac8a718")
    version("0.9.0", sha256="9351ed92aded632f8c7f59dfadac13c191a834babe682f5785ea47e6fcf6b472")
    version("0.8.2", sha256="9a866c3c8feb23b3221ce261e6153fc65a98ce9ceaa71ccad017016945c178bf")
    version("0.8.1", sha256="c46734c679c99f93e5c06654f4295a05a6afe6c00a35ebd26a2cce507ae1ccbd")
    version("0.8.0", sha256="b5f040faffbfc7bac8d4687d8665bd1196937334589b3fb5fcf15bb69ca25391")
    version("0.7.0", sha256="fa0a6f44a50451115d1499b3f2aa597e0092a07afce1068750260fa7dd2c85cb")
    version("0.6.1", sha256="8173680a976c833640ecbd0d7e6f0a11047bf8833433e2147180efc905e48656")
    version("0.6.0", sha256="02de11b3abe6882de4032ce86dab9c7794cbc84369b44d04e667486580f0f1f7")
    version("0.5.0", sha256="eb9afc93df3d174d975ee0914057a9522f5272310b4d56c150b955c287a4d74d")
    version("0.4.2", sha256="1184a27eab85c9e784bacc6f9d6fec99e168ab4eda6047ef9f709e7fdb22d8f9")
    version("0.4.1", sha256="053689351272b3bd2ac3e6ba51efd284de0e4ca4a301f54674b949f1e62b7176")
    version("0.4.0", sha256="c270d74e568bad4559fed4544f6dd1e22e2eb1c60b088e04a5bd5787c4150589")
    version("0.3.0", sha256="c205f0618c268c6ed2f8abb869ef6eb83e5339c1336c243ad321a2f2a85195f0")

    desc = "Enable support for native encoding/decoding of {} formats in torchvision.io"
    variant("png", default=False, description=desc.format("PNG"))
    variant("jpeg", default=False, description=desc.format("JPEG"))
    variant("nvjpeg", default=False, description=desc.format("JPEG"))
    variant("ffmpeg", default=False, description=desc.format("FFMPEG"))
    variant("video_codec", default=False, description=desc.format("video_codec"))

    # https://github.com/pytorch/vision#installation
    depends_on("python@3.8:3.11", when="@0.15:", type=("build", "link", "run"))
    depends_on("python@:3.10", when="@0.12:0.14", type=("build", "link", "run"))
    depends_on("python@:3.9", when="@0.8.2:0.11", type=("build", "link", "run"))
    depends_on("python@:3.8", when="@0.5:0.8.1", type=("build", "link", "run"))
    depends_on("python@:3.7", when="@:0.4", type=("build", "link", "run"))

    # https://github.com/pytorch/vision#installation
    depends_on("py-torch@main", when="@main", type=("build", "link", "run"))
    depends_on("py-torch@2.1.1", when="@0.16.1", type=("build", "link", "run"))
    depends_on("py-torch@2.1.0", when="@0.16.0", type=("build", "link", "run"))
    depends_on("py-torch@2.0.1", when="@0.15.2", type=("build", "link", "run"))
    depends_on("py-torch@2.0.0", when="@0.15.1", type=("build", "link", "run"))
    depends_on("py-torch@1.13.1", when="@0.14.1", type=("build", "link", "run"))
    depends_on("py-torch@1.13.0", when="@0.14.0", type=("build", "link", "run"))
    depends_on("py-torch@1.12.1", when="@0.13.1", type=("build", "link", "run"))
    depends_on("py-torch@1.12.0", when="@0.13.0", type=("build", "link", "run"))
    depends_on("py-torch@1.11.0", when="@0.12.0", type=("build", "link", "run"))
    depends_on("py-torch@1.10.2", when="@0.11.3", type=("build", "link", "run"))
    depends_on("py-torch@1.10.1", when="@0.11.2", type=("build", "link", "run"))
    depends_on("py-torch@1.10.0", when="@0.11.1", type=("build", "link", "run"))
    depends_on("py-torch@1.10.0", when="@0.11.0", type=("build", "link", "run"))
    depends_on("py-torch@1.9.1", when="@0.10.1", type=("build", "link", "run"))
    depends_on("py-torch@1.9.0", when="@0.10.0", type=("build", "link", "run"))
    depends_on("py-torch@1.8.2", when="@0.9.2", type=("build", "link", "run"))
    depends_on("py-torch@1.8.1", when="@0.9.1", type=("build", "link", "run"))
    depends_on("py-torch@1.8.0", when="@0.9.0", type=("build", "link", "run"))
    depends_on("py-torch@1.7.1", when="@0.8.2", type=("build", "link", "run"))
    depends_on("py-torch@1.7.0", when="@0.8.1", type=("build", "link", "run"))
    depends_on("py-torch@1.7.0", when="@0.8.0", type=("build", "link", "run"))
    depends_on("py-torch@1.6.0", when="@0.7.0", type=("build", "link", "run"))
    depends_on("py-torch@1.5.1", when="@0.6.1", type=("build", "link", "run"))
    depends_on("py-torch@1.5.0", when="@0.6.0", type=("build", "link", "run"))
    depends_on("py-torch@1.4.1", when="@0.5.0", type=("build", "link", "run"))
    depends_on("py-torch@1.3.1", when="@0.4.2", type=("build", "link", "run"))
    depends_on("py-torch@1.3.0", when="@0.4.1", type=("build", "link", "run"))
    depends_on("py-torch@1.2.0", when="@0.4.0", type=("build", "link", "run"))
    depends_on("py-torch@1.1.0", when="@0.3.0", type=("build", "link", "run"))
    depends_on("py-torch@:1.0.1", when="@0.2.2", type=("build", "link", "run"))

    depends_on("ninja", type="build")

    # setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-requests", when="@0.12:", type=("build", "run"))
    depends_on("pil@5.3:", when="@0.10:", type=("build", "run"))
    depends_on("pil@4.1.1:", type=("build", "run"))

    # Extensions
    depends_on("libpng@1.6:", when="+png")
    depends_on("jpeg", when="+jpeg")
    depends_on("cuda", when="+nvjpeg")
    depends_on("ffmpeg@3.1:", when="+ffmpeg")
    depends_on("cuda", when="+video_codec")

    # Historical dependencies
    depends_on("py-typing-extensions", when="@0.12:0.14", type=("build", "run"))
    depends_on("py-six", when="@:0.5", type=("build", "run"))

    # https://github.com/pytorch/vision/pull/5898
    conflicts("^pil@10:", when="@:0.12")
    # https://github.com/pytorch/vision/issues/1712
    conflicts("^pil@7:", when="@:0.4")
    # https://github.com/pytorch/vision/issues/4146
    # https://github.com/pytorch/vision/issues/4934
    conflicts("^pil@8.3")
    # https://github.com/pytorch/pytorch/issues/65000
    conflicts("+ffmpeg", when="platform=darwin")
    # https://github.com/pytorch/vision/issues/3367
    conflicts("+ffmpeg", when="^python@3.9")
    # https://github.com/pytorch/vision/pull/7378
    conflicts("^ffmpeg@6:")
    # https://github.com/pytorch/vision/issues/5616
    # https://github.com/pytorch/vision/pull/5644
    conflicts("^ffmpeg@5:", when="@:0.12")

    # Many of the datasets require additional dependencies to use.
    # These can be installed after the fact.

    def setup_build_environment(self, env):
        # The only documentation on building is what is found in setup.py and:
        # https://github.com/pytorch/vision/blob/main/CONTRIBUTING.md#development-installation

        # By default, version is read from `version.txt`, but this includes an `a0`
        # suffix used for alpha builds. Override the version for stable releases.
        if not self.spec.satisfies("@main"):
            env.set("BUILD_VERSION", self.version)

        # Used by ninja
        env.set("MAX_JOBS", make_jobs)

        if "^cuda" in self.spec:
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
            torch_cuda_arch_list = ";".join(
                "{0:.1f}".format(float(i) / 10.0)
                for i in self.spec["py-torch"].variants["cuda_arch"].value
            )
            env.set("TORCH_CUDA_ARCH_LIST", torch_cuda_arch_list)

        for gpu in ["cuda", "mps"]:
            env.set(f"FORCE_{gpu.upper()}", int(f"+{gpu}" in self.spec["py-torch"]))

        for extension in ["png", "jpeg", "nvjpeg", "ffmpeg", "video_codec"]:
            env.set(f"TORCHVISION_USE_{extension.upper()}", int(f"+{extension}" in self.spec))

        include = []
        library = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            include.extend(query.headers.directories)
            library.extend(query.libs.directories)

        # CONTRIBUTING.md says to use TORCHVISION_INCLUDE and TORCHVISION_LIBRARY, but
        # these do not work for older releases. Build uses a mix of Spack's compiler wrapper
        # and the actual compiler, so this is needed to get parts of the build working.
        # See https://github.com/pytorch/vision/issues/2591
        env.set("TORCHVISION_INCLUDE", ":".join(include))
        env.set("TORCHVISION_LIBRARY", ":".join(library))
        env.set("CPATH", ":".join(include))
        env.set("LIBRARY_PATH", ":".join(library))
