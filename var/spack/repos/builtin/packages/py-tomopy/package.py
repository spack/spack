# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTomopy(PythonPackage):
    """TomoPy is an open-source Python package for tomographic data
    processing and image reconstruction."""

    homepage = "https://tomopy.readthedocs.io/en/latest/index.html"
    url = "https://github.com/tomopy/tomopy/archive/1.0.0.tar.gz"
    git = "https://github.com/tomopy/tomopy.git"

    version("master", branch="master")
    version("1.11.0", sha256="4e5691c2b083753692ba4376ce301578037071c83fc61a6ae9e5bc9e6fcd3d1f")
    # Never was an official 1.10.4 release, checksum doesn't match for some reason
    version(
        "1.10.4",
        sha256="2f15edda11b4337a1a5560684fcf8f28a35c5035932b22b842ce728bd13fba01",
        deprecated=True,
    )
    version("1.0.0", sha256="ee45f7a062e5a66d6f18a904d2e204e48d85a1ce1464156f9e2f6353057dfe4c")

    # GPU accel needs PTL which is a git submodule. Thus, we can only build it on master
    depends_on("cuda", when="@master")
    # The shared opencv is not found by during runtest. Not using GOT/PLT is faster too
    depends_on("opencv+imgproc~shared@3.4:", when="@master")
    # During the runtest, the shared MKL libs aren't found yet:
    # depends_on('intel-mkl~shared')
    depends_on("cmake@3.17:", type=("build"))
    depends_on("ninja", type=("build"))
    depends_on("py-setuptools-scm", type=("build"))
    depends_on("py-setuptools-scm-git-archive", type=("build"))
    # Note: The module name of py-scikit-build is skbuild:
    depends_on("py-scikit-build", type=("build"))
    depends_on("py-scikit-image@0.17:", type=("build", "run"))
    depends_on("py-numpy+blas", type=("build", "run"))
    depends_on("py-pyfftw", type=("build", "run"), when="@1.0:1.9")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pywavelets", type=("build", "run"))
    depends_on("py-dxchange", type=("build", "run"))
    depends_on("py-numexpr", when="@1.11:", type=("build", "run"))

    @when("@1.10:")
    def install_options(self, spec, prefix):
        args = ["--enable-arch"]
        if "avx512" in self.spec.target:
            args.append("--enable-avx512")

        # PTL is a git submodule, we only fetch it's source by git-submodule on master:
        if self.version != Version("master"):
            args.append("--disable-tasking")

        return args
