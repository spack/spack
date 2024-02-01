# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyScikitLearn(PythonPackage):
    """A set of python modules for machine learning and data mining."""

    homepage = "https://scikit-learn.org/"
    pypi = "scikit-learn/scikit-learn-0.24.0.tar.gz"
    git = "https://github.com/scikit-learn/scikit-learn.git"

    maintainers("adamjstewart")

    version("master", branch="master")
    version("1.3.2", sha256="a2f54c76accc15a34bfb9066e6c7a56c1e7235dda5762b990792330b52ccfb05")
    version("1.3.1", sha256="1a231cced3ee3fa04756b4a7ab532dc9417acd581a330adff5f2c01ac2831fcf")
    version("1.3.0", sha256="8be549886f5eda46436b6e555b0e4873b4f10aa21c07df45c4bc1735afbccd7a")
    version("1.2.2", sha256="8429aea30ec24e7a8c7ed8a3fa6213adf3814a6efbea09e16e0a0c71e1a1a3d7")
    version("1.2.1", sha256="fbf8a5c893c9b4b99bcc7ed8fb3e8500957a113f4101860386d06635520f7cfb")
    version("1.2.0", sha256="680b65b3caee469541385d2ca5b03ff70408f6c618c583948312f0d2125df680")
    version("1.1.3", sha256="bef51978a51ec19977700fe7b86aecea49c825884f3811756b74a3b152bb4e35")
    version("1.1.2", sha256="7c22d1305b16f08d57751a4ea36071e2215efb4c09cb79183faa4e8e82a3dbf8")
    version("1.1.1", sha256="3e77b71e8e644f86c8b5be7f1c285ef597de4c384961389ee3e9ca36c445b256")
    version("1.1.0", sha256="80f9904f5b1356adfc32406725dd94c8cc9c8d265047d98390033a6c238cbb29")
    version("1.0.2", sha256="b5870959a5484b614f26d31ca4c17524b1b0317522199dc985c3b4256e030767")
    version("1.0.1", sha256="ac2ca9dbb754d61cfe1c83ba8483498ef951d29b93ec09d6f002847f210a99da")
    version("1.0", sha256="776800194e757cd212b47cd05907e0eb67a554ad333fe76776060dbb729e3427")
    version("0.24.2", sha256="d14701a12417930392cd3898e9646cf5670c190b933625ebe7511b1f7d7b8736")
    version("0.24.1", sha256="a0334a1802e64d656022c3bfab56a73fbd6bf4b1298343f3688af2151810bbdf")
    version("0.24.0", sha256="076369634ee72b5a5941440661e2f306ff4ac30903802dc52031c7e9199ac640")
    version("0.23.2", sha256="20766f515e6cd6f954554387dfae705d93c7b544ec0e6c6a5d8e006f6f7ef480")
    version("0.23.1", sha256="e3fec1c8831f8f93ad85581ca29ca1bb88e2da377fb097cf8322aa89c21bc9b8")
    version("0.23.0", sha256="639a53df6273acc6a7510fb0c658b94e0c70bb13dafff9d14932c981ff9baff4")
    version(
        "0.22.2.post1", sha256="57538d138ba54407d21e27c306735cbd42a6aae0df6a5a30c7a6edde46b0017d"
    )
    version("0.22.1", sha256="51ee25330fc244107588545c70e2f3570cfc4017cff09eed69d6e1d82a212b7d")
    version("0.22", sha256="314abf60c073c48a1e95feaae9f3ca47a2139bd77cebb5b877c23a45c9e03012")
    version("0.21.3", sha256="eb9b8ebf59eddd8b96366428238ab27d05a19e89c5516ce294abc35cea75d003")
    version("0.21.2", sha256="0aafc312a55ebf58073151b9308761a5fcfa45b7f7730cea4b1f066f824c72db")
    version("0.21.1", sha256="228d0611e69e5250946f8cd7bbefec75347950f0ca426d0c518db8f06583f660")
    version("0.20.3", sha256="c503802a81de18b8b4d40d069f5e363795ee44b1605f38bc104160ca3bfe2c41")
    version("0.20.2", sha256="bc5bc7c7ee2572a1edcb51698a6caf11fae554194aaab9a38105d9ec419f29e6")
    version("0.20.0", sha256="97d1d971f8ec257011e64b7d655df68081dd3097322690afa1a71a1d755f8c18")
    version("0.19.2", sha256="b276739a5f863ccacb61999a3067d0895ee291c95502929b2ae56ea1f882e888")

    variant("openmp", default=True, description="Build with OpenMP support")

    # Based on PyPI wheel availability
    depends_on("python@3.8:3.12", when="@1.3.1:", type=("build", "run"))
    depends_on("python@3.8:3.11", when="@1.1.3:1.3.0", type=("build", "run"))
    depends_on("python@3.8:3.10", when="@1.1.0:1.1.2", type=("build", "run"))
    depends_on("python@:3.10", when="@1.0.2", type=("build", "run"))
    depends_on("python@:3.9", when="@0.24:1.0.1", type=("build", "run"))
    depends_on("python@:3.8", when="@0.22:0.23", type=("build", "run"))
    depends_on("python@:3.7", when="@:0.21", type=("build", "run"))

    # pyproject.toml
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@:59", when="@:1.2.1", type="build")
    depends_on("py-cython@0.29.33:2", when="@1.3:", type="build")
    depends_on("py-cython@0.29.24:2", when="@1.0.2:", type="build")
    depends_on("py-cython@0.28.5:2", when="@0.21:", type="build")
    depends_on("py-cython@0.23:2", type="build")

    # sklearn/_min_dependencies.py
    depends_on("py-numpy@1.17.3:", when="@1.1:", type=("build", "run"))
    depends_on("py-numpy@1.14.6:", when="@1.0:", type=("build", "run"))
    depends_on("py-numpy@1.13.3:", when="@0.23:", type=("build", "run"))
    depends_on("py-numpy@1.11.0:", when="@0.21:", type=("build", "run"))
    depends_on("py-numpy@1.8.2:", when="@0.20", type=("build", "run"))
    depends_on("py-numpy@1.6.1:", when="@:0.19", type=("build", "run"))
    depends_on("py-scipy@1.5:", when="@1.3:", type=("build", "run"))
    depends_on("py-scipy@1.3.2:", when="@1.1:", type=("build", "run"))
    depends_on("py-scipy@1.1.0:", when="@1.0:", type=("build", "run"))
    depends_on("py-scipy@0.19.1:", when="@0.23:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", when="@0.21:", type=("build", "run"))
    depends_on("py-scipy@0.13.3:", when="@0.20", type=("build", "run"))
    depends_on("py-scipy@0.9:", when="@:0.19", type=("build", "run"))
    depends_on("py-joblib@1.1.1:", when="@1.2:", type=("build", "run"))
    depends_on("py-joblib@1:", when="@1.1:", type=("build", "run"))
    depends_on("py-joblib@0.11:", type=("build", "run"))
    depends_on("py-threadpoolctl@2.0.0:", when="@0.23:", type=("build", "run"))
    depends_on("llvm-openmp", when="@0.21: %apple-clang +openmp")

    # Test dependencies
    depends_on("py-matplotlib@3.1.3:", type="test")
    depends_on("py-scikit-image@0.16.2:", type="test")
    depends_on("py-pandas@1.0.5:", type="test")
    depends_on("py-pytest@7.1.2:", type="test")
    depends_on("py-pyamg@4:", type="test")
    depends_on("py-pooch@1.6:", type="test")

    # Release tarballs are already cythonized. If you wanted to build a release
    # version without OpenMP support, you would need to delete all .c files
    # that include omp.h, as well as PKG-INFO.
    # See https://github.com/scikit-learn/scikit-learn/issues/14332
    conflicts("~openmp", when="@:999", msg="Only master supports ~openmp")

    def setup_build_environment(self, env):
        # enable parallel builds of the sklearn backend
        env.append_flags("SKLEARN_BUILD_PARALLEL", str(make_jobs))

        # https://scikit-learn.org/stable/developers/advanced_installation.html#building-from-source
        if self.spec.satisfies("~openmp"):
            env.set("SKLEARN_NO_OPENMP", "True")
        # https://scikit-learn.org/stable/developers/advanced_installation.html#mac-osx
        elif self.spec.satisfies("@0.21: %apple-clang +openmp"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        # https://scikit-learn.org/stable/developers/advanced_installation.html#testing
        with working_dir("spack-test", create=True):
            pytest = which("pytest")
            pytest(join_path(self.prefix, python_purelib, "sklearn"))
