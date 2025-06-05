# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyZfit(PythonPackage):
    """
    scalable pythonic model fitting for high energy physics
    """

    homepage = "https://github.com/zfit/zfit"
    pypi = "zfit/zfit-0.18.0.tar.gz"

    maintainers("jonas-eschle")
    license("BSD-3-Clause", checked_by="jonas-eschle")

    tags = ["likelihood", "statistics", "inference", "fitting", "hep"]

    version("0.26.0", sha256="c61e55177055e775fefb6d985b643a7db8e8eb16e872d8dc66434b36f15c0b36")
    version("0.25.0", sha256="ac5a92bc284094eae55dd9afe1fe2c8f3f67a402dfc7a8ad6087a9ea29ff2b41")
    version("0.24.3", sha256="0efe47a5c597f7c730ac25495625f8bb4460f2fa4a0f4c387f503339ac8e91b5")
    version("0.24.2", sha256="6b83315e16e07d8472d92b142b377d8d7314411d27fe8033168037fd4583f5f6")
    version("0.24.1", sha256="9a0423302ac5647e910feadce634b8b0a1806c1866f4f55795db64918cbdd2d8")
    version("0.24.0", sha256="d2d30886c154a6583c615b68cd43bd156cb7f7576c584c48fb72f5ab89c9d94b")
    version("0.23.0", sha256="19ec469e1703bd38f8b8957871851ee22fa2e68f0a57b7867cc40ea77df98cc5")
    version("0.22.0", sha256="b88fe03ab91d1327fd1f23ba27d602fa8a4a82d74bd8ed5d7c08f167a6b223df")
    version("0.21.1", sha256="7636c42c93d299bcc4346afe46df1ba615acedbc2380711e68a3e47a5445d4fa")
    version("0.21.0", sha256="9d57f8210c5177df615de7f27d937cf0fc9237fb83360e291e2361604d7fe947")
    version("0.20.3", sha256="c300ce5d4dd75d351184c4e10c1b1afb7969f99be1f803e8dd50b09ecc951406")
    version("0.20.2", sha256="f822ff857346fe5b244e0a13f6fa2f2216c60d8c93f512405890289e2fbfac97")
    version("0.20.1", sha256="c834953548be6e1a69ce48eb561b63a6ca8c6cee3bad2d33b98fa5c16001fc27")
    version("0.20", sha256="ec39f0118fe8f918a488dacc633279321a06bb88fc0dc09207830516177ca4ff")
    version("0.18.2", sha256="099b111e135937966b4c6342c7738731f112aea33e1b9f4a9785d2eac9e530f1")
    version("0.18.1", sha256="fbc6b3a636d8dc74fb2e69dfec5855f534c4583ec18efac9e9107ad45b18eb43")
    version("0.18.0", sha256="21d9479480f74945c67707b715780693bd4e94062c551bf41fe04a2eddb47fab")
    version("0.17.0", sha256="cd60dfc360c82666af4e8dddd78edb0ab95a095b9dd0868457f0981dc03afa5a")
    version("0.16.0", sha256="b3b170af23b61d7e265d6fb1bab1d052003f3fb41b3c537527cc1e5a1066dc10")
    version("0.15.5", sha256="00a1138429e8a7f830c9e229b9c0bcd6071b95dadd8c87eb81191079fb679225")
    version("0.14.1", sha256="66d1e349403f1d6c6350138d0f2b422046bcbdfb34fd95453dadae29a8b0c98a")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("python@:3.11", type=("build", "run"), when="@:0.18")
    depends_on("python@:3.12", type=("build", "run"), when="@0.20:")

    depends_on("py-hatchling@42:", type="build", when="@0.26:")
    depends_on("py-hatch-vcs", type="build", when="@0.26:")

    depends_on("py-setuptools@42:", type="build", when="@:0.25")
    depends_on("py-setuptools-scm-git-archive", type="build", when="@:0.25")
    depends_on("py-setuptools-scm@3.4:+toml", type="build", when="@:0.25")

    variant("nlopt", default=False, description="Enable nlopt support")
    variant("hs3", default=True, description="Enable serialization support")

    # TODO: remove "build" once fixed in spack that tests need "run", not "build"
    with default_args(type=("build", "run")):
        depends_on("py-tensorflow")
        depends_on("py-tensorflow-probability")

        depends_on("py-tensorflow@2.16.2:2.19", when="@0.25.0:")
        depends_on("py-tensorflow-probability@0.25:0.26", when="@0.25.0:")

        depends_on("py-tensorflow@2.16.2:2.18", when="@0.24.3:0.24")
        depends_on("py-tensorflow@2.18", when="@0.24:0.24.2")
        depends_on("py-tensorflow-probability@0.25", when="@0.24:0.24")

        depends_on("py-tensorflow@2.16", when="@0.20:0.23")
        depends_on("py-tensorflow-probability@0.24", when="@0.20:0.23")

        depends_on("py-tensorflow@2.15", when="@0.18")
        depends_on("py-tensorflow-probability@0.23", when="@0.18")

        depends_on("py-tensorflow@2.13", when="@0.15:0.17")
        depends_on("py-tensorflow-probability@0.21", when="@0.16:0.17")
        depends_on("py-tensorflow-probability@0.20:0.21", when="@0.15:0.16")

        depends_on("py-tensorflow@2.0:2.12", when="@0.14")
        depends_on("py-tensorflow-probability@0.20", when="@0.14")

        with when("+nlopt"):
            depends_on("nlopt@2.7.1: +python")

        with when("+hs3"):
            depends_on("py-asdf@:3")

        depends_on("py-attrs", when="@0.15:")
        depends_on("py-typing-extensions", when="@:0.17 ^python@:3.8")
        depends_on("py-boost-histogram")
        depends_on("py-colorama")
        depends_on("py-colored")
        depends_on("py-colorlog")
        depends_on("py-deprecated")
        depends_on("py-dill")
        depends_on("py-dotmap")
        depends_on("py-frozendict")
        depends_on("py-hist")
        depends_on("py-iminuit@2.3:")
        depends_on("py-jacobi")
        depends_on("py-numdifftools")
        depends_on("py-numpy@1.16:")
        depends_on("py-ordered-set")
        depends_on("py-pandas")
        depends_on("py-pydantic@:1", when="@:0.21")
        depends_on("py-pydantic@2:", when="@0.22:")
        depends_on("py-pyyaml")
        depends_on("py-scipy@1.2:")
        depends_on("py-tabulate")
        depends_on("py-texttable")
        depends_on("py-uhi")
        depends_on("py-uproot@4:")
        depends_on("py-xxhash")
        depends_on("py-zfit-interface")
