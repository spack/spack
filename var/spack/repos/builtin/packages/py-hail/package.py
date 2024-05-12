# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHail(MakefilePackage):
    """Cloud-native genomic dataframes and batch computing (Python API)"""

    homepage = "https://hail.is"
    url = "https://github.com/hail-is/hail/archive/refs/tags/0.2.130.tar.gz"
    git = "https://github.com/hail-is/hail.git"

    maintainers("teaguesterling")
    license("MIT", checked_by="teaguesterling")

    version(
        "0.2.130", 
        commit="bea04d9c79b5ca739364e8c121132845475f617a",
    #    sha256="0a80704e474cac72264db5dad27c876d7b0c8563a0fbfbdd47d465d33515d07f"
    )
    version(
        "0.2.129", 
        commit="41126be2df04e4ef823cefea40fba4cadbe5db8a",
    #    sha256="9c5511cb92d5ec1f839960b78d3be25aedfd1ab97486ccf67ee102d2730a72a4"
    )

    variant("native", default=True)
    variant(
        "query_backend", 
        values=["undefined", "spark", "batch"], 
        default="spark"
    )

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    extends("python")

    # Hail build requirements
    with default_args(type=("build", "run")):
        depends_on("gcc@5:")
        depends_on("blas")
        depends_on("lapack")
        depends_on("lz4")
        depends_on("java@8,11")
        depends_on("scala@2.12")
        depends_on("spark@3.3:")
        depends_on("py-pyspark")

    # HAIL API requirements
    with default_args(type=("build", "run")):
        depends_on("py-avro@1.10:1.11")
        depends_on("py-bokeh@:3.3")
        depends_on("py-decorator@:4.4.2")
        depends_on("py-deprecated@1.2.10:1.2")
        depends_on("py-numpy@:2")
        depends_on("py-pandas@2")
        depends_on("py-parsimonious@:0")
        depends_on("py-plotly@5.18:5.20")
        depends_on("py-protobuf@3.20.2")
        depends_on("py-requests@2.31")
        depends_on("py-scipy@1.3:1.11")

    # HAIL wheels are pinned to a specific version of
    # Spark. If we implement building from source, this
    # will likely not be as much of an issue, but that
    # isn't working yet.
    #with default_args(type=("build", "run")):
    #    depends_on("py-pyspark@3.3", when="@0.2.130")


    # hailtop requirements
    with default_args(type="run"):
        depends_on("py-aiodns@2")
        depends_on("py-aiohttp@3.9")
        depends_on("py-azure-identity@1.6:1")
        depends_on("py-azure-mgmt-storage@20.1.0")
        depends_on("py-azure-storage-blob@12.11:12")
        depends_on("py-boto3@1.17:1")
        depends_on("py-botocore@1.20:1")
        depends_on("py-dill@0.3.6:0.3")
        depends_on("py-frozenlist@1.3.1:1")
        depends_on("py-google-auth@2.14.1:2")
        depends_on("py-google-auth-oauthlib@0.5.2:0")
        depends_on("py-humanize@1.0.0:1")
        depends_on("py-janus@0.6:1.0")
        depends_on("py-nest-asyncio@1.5.8:1")
        depends_on("py-rich@12.6.0:12")
        depends_on("py-orjson@3.9.15:3")
        depends_on("py-typer@0.9.0:0")
        depends_on("py-python-json-logger@2.0.2:2")
        depends_on("py-pyyaml@6.0:7")
        depends_on("py-sortedcontainers@2.4.0:2")
        depends_on("py-tabulate@0.8.9:0")
        depends_on("py-uvloop@0.19.0:0")
        depends_on("py-jproperties@2.1.1:2")

    # Undocumented runtime requirements for hailtop
    # These are also required to use the HAIL API
    # but are not explicitly mentioned anywhere
    with default_args(type="run"):
        depends_on("py-azure-mgmt-core")
        depends_on("py-typing-extensions")

    build_directory = "hail"

    @property
    def hail_pip_version(self):
        # This is the same behavior is as is defined in hail/version.mk
        return f"{self.spec.version.up_to(3)}"

    @property
    def build_wheel_file_path(self):
        build_wheel_file_name = f"hail-{self.hail_pip_version}-py3-none-any.whl"
        build_wheel_file_dir = self.build_directory.build.deploy.dist
        return join_path(build_wheel_file_dir, build_wheel_file_name)

    def patch(self):
        version = self.spec.version
        #filter_file(
        #    "^REVISION :=",
        #    f"REVISION := revision_not_available_from_archive",
        #    "hail/version.mk"
        #)
        #filter_file(
        #    "^SHORT_REVISION :=",
        #    f"SHORT_REVISION := builtbyspack",
        #    "hail/version.mk"
        #)
        #filter_file(
        #    "^BRANCH :=",
        #    f"BRANCH := tags/{version.up_to(3)}",
        #    "hail/version.mk"
        #)


    @property
    def build_targets(self):
        spec = self.spec
        variables = [
            f"SCALA_VERSION={spec['scala'].version}",
            f"SPARK_VERSION={spec['spark'].version}",
        ]
        if spec.satisfies("+native"):
            variables += ["HAIL_COMPILE_NATIVES=1"]

        # We're not using the documented target to 
        # because it depends on pipto install and resolve 
        # dependencies directly and does everythin in one step.
        # The documented target is `install-on-cluster`
        targets = [
            # This may be too specific but it would detect failures
            # and fail to build instead of taking a long time to build
            # and then failing at install time.
            self.build_wheel_file_path,
        ]

        return targets + variables

    def install(self, spec, prefix):
        spec = self.spec
        pip = which("pip")

        # This mimics the install-on-cluster target but avoids anything
        # that utilizes pip to resolve dependencies
        with working_dir(join_path(self.stage.source_path, "hail")):
            pip("install", "--no-deps", self.build_wheel_file_path)

        backend = spec.variants['query_backend'].value
        if backend != "undefined":
            hailctl = which("hailctl")  # Should be installed from above
            hailctl("config", "set", "query/backend", f"{backend}")

    def setup_run_environment(self, env):
        #TODO: Add Spark configuration values to find HAIL Jars
        #This would be needed if one was connecting to a Spark
        #cluster that was started outside of HAIL
        pass
