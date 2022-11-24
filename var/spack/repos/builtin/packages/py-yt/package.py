# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYt(PythonPackage):
    """Volumetric Data Analysis

    yt is a python package for analyzing and visualizing
    volumetric, multi-resolution data from astrophysical
    simulations, radio telescopes, and a burgeoning
    interdisciplinary community.
    """

    homepage = "https://yt-project.org"
    git = "https://github.com/yt-project/yt.git"
    pypi = "yt/yt-4.1.2.tar.gz"

    maintainers = ["charmoniumq"]

    version("4.1.2", sha256="0ae03288b067721baad14c016f253dc791cd444a1f2dd5d804cf91da622a0c76")
    version("3.6.1", sha256="a1be3ea7e18729d3cd86e9234dc4731bf23200dff3344fa756fe173ea36cc747")
    version("3.6.0", sha256="4e3bab11766d5950477ba4d6c528a495e12cda1155227361b4579ac4ac0bf975")
    version("3.5.1", sha256="cdc0ecb153e737d74820581f311d1be7b6f1a7ee065ad69706470939db88b041")
    version("3.5.0", sha256="548598912adba72b782b7422d40d1d12a8c1a6cd064281a9a537fdb2a5af89fc")
    version("3.4.1", sha256="b9a73ade3726a8163fc992999c8c1010ca89473131901fe4d48b820ab2ced486")
    version("3.4.0", sha256="2120793a76864cf3165b2b7290ef719e358fa57501ee8721941e7cfc434cfb2b")
    version("3.3.5", sha256="2ebe4bbefd9f5367563ce4d7eb87d3f6ef0de1f97ed1c03106d9541e71b7e1ca")
    version("3.3.4", sha256="2842bab891cfbf3269a3c4bd8f22fef23c9a15a790ba48c6490730cb51ce9b0e")
    version("3.3.3", sha256="7b9244089e92b1d32cef791cd72760bb8c80b391eaec29672a5377c33f932d88")
    version("3.3.2", sha256="d323419ad3919e86d2af1738c846021fd7f5b5dc5c06059cdf3a2bc63226466a")
    version("3.3.1", sha256="7ac68d5e05e2b57fb3635f1027f3201094f3547d584e72ab55fedbfd3bc09a36")
    version("3.3.0", sha256="e6be799c0d9a83a06649f0d77a61ad9c23b94b34f94e16724e2b18f5c7513c33")
    version("3.2.3", sha256="96476d17e9ce35f0d4380b2ddb398fe729e39f1f3894602ff07e49844541e5ca")
    version("3.2.2", sha256="498ed77b3dae8c54929602d4931f3c3e0a3420a9b500cbd870f50b1e0efea8c3")

    variant("astropy", default=True, description="enable astropy support")
    variant("h5py", default=True, description="enable h5py support")
    variant("scipy", default=True, description="enable scipy support")
    variant("rockstar", default=False, description="enable rockstar support")

    # Main dependencies:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/setup.cfg#L40
    depends_on("py-cmyt@0.2.2:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-ipywidgets@8:", type=("build", "run"), when="@4.1.2")
    depends_on("py-matplotlib@1.5.3:", type=("build", "run"))
    depends_on("py-matplotlib@:3.2.2", type=("build", "run"), when="@:3.6.0")
    depends_on("py-matplotlib@3.1:", type=("build", "run"), when="@4.1.2:")
    conflicts("^py-matplotlib@3.4.2", when="@4.1.2:")
    depends_on("py-more-itertools@8.4:", when="@4.1.2:")
    depends_on("py-numpy@1.10.4:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-setuptools@19.6:", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"), when="@4.1.2:")
    # PIL/pillow and pyparsing dependency is handled by matplotlib
    depends_on("py-tomli-w@0.4:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-tqdm@3.4.0:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-unyt@2.8:2", type=("build", "run"), when="@4.1.2:")
    depends_on("py-importlib-metadata@1.4:", type=("build", "run"), when="@4.1.2: ^python@:3.7")
    depends_on("py-tomli@1.2.3:", type=("build", "run"), when="@4.1.2: ^python@:3.10")
    depends_on("py-typing-extensions@4.2:", type=("build", "run"), when="@4.1.2: ^python@:3.7")
    # See https://github.com/spack/spack/pull/30418#discussion_r863962805
    depends_on("py-ipython@1.0:", type=("build", "run"), when="@:3")
    depends_on("python@2.7.0:2.7,3.5:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@4.1.2:")

    # Extras:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/setup.cfg#L80
    depends_on("py-h5py@3.1:3", type=("build", "run"), when="+h5py")
    depends_on("py-scipy@1.5.0:", type=("build", "run"), when="+scipy")
    depends_on("rockstar@yt", type=("build", "run"), when="+rockstar")
    depends_on("py-astropy@4.0.1:5", type=("build", "run"), when="+astropy")

    # Build dependencies:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/pyproject.toml#L2
    depends_on("py-cython@0.24:", type="build")
    depends_on("py-cython@0.29.21:2", type="build", when="@4.1.2:")
    depends_on("py-wheel@0.36.2", type="build", when="@4.1.2:")
    depends_on("py-setuptools@59.0.1:", type="build", when="@4.1.2:")

    @run_before("install")
    def prep_yt(self):
        if "+rockstar" in self.spec:
            with open("rockstar.cfg", "w") as rockstar_cfg:
                rockstar_cfg.write(self.spec["rockstar"].prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # The Python interpreter path can be too long for this
        # yt = Executable(join_path(prefix.bin, "yt"))
        # yt("--help")
        python(join_path(self.prefix.bin, "yt"), "--help")
