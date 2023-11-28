# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyTensorflowEstimator(Package):
    """TensorFlow Estimator is a high-level TensorFlow API that greatly
    simplifies machine learning programming."""

    homepage = "https://github.com/tensorflow/estimator"
    url = "https://github.com/tensorflow/estimator/archive/v2.2.0.tar.gz"

    maintainers("aweits")

    version("2.10", sha256="60df309377cf4e584ca20198f9639beb685d50616395f50770fc0999092d6d85")
    version("2.9.0", sha256="62d7b5a574d9c995542f6cb485ff1c18ad115afd9ec6d63437b2aab227c35ef6")
    version("2.8.0", sha256="58a2c3562ca6491c257e9a4d9bd8825667883257edcdb452181efa691c586b17")
    version("2.7.0", sha256="e5164e802638d3cf110ecc17912be9d514a9d3354ec48e77200b9403dcc15965")
    version("2.6.0", sha256="947705c60c50da0b4a8ceec1bc058aaf6bf567a7efdcd50d5173ebf6bafcf30f")
    version("2.5.0", sha256="66661f30ea05d57377c45267ca770935fb8c54f85b7901f0a7deb91766fe9f45")
    version("2.4.0", sha256="e6ea12014c3d8c89a81ace95f8f8b7c39ffcd3e4e4626709e4aee0010eefd962")
    version("2.3.0", sha256="75403e7de7e8ec30ec0781ede56ed84cbe5e90daad64a9c242cd489c8fe63a17")
    version("2.2.0", sha256="2d68cb6e6442e7dcbfa2e092aa25bdcb0eda420536a829b85d732854a4c85d46")
    version("2.1", sha256="1d74c8181b981748976fa33ad97d3434c3cf2b7e29a0b00861365fe8329dbc4e")
    version("2.0.0", sha256="6f4bdf1ab219e1f1cba25d2af097dc820f56479f12a839853d97422fe4d8b465")
    version("1.13.0", sha256="a787b150ff436636df723e507019c72a5d6486cfe506886279d380166953f12f")

    extends("python")

    depends_on("python@3.7:", when="@2.9:", type=("build", "run"))

    for ver in ["2.10", "2.9", "2.8", "2.7", "2.6"]:
        depends_on("py-keras@" + ver, when="@" + ver, type=("build", "run"))

    for ver in [
        "2.10",
        "2.9",
        "2.8",
        "2.7",
        "2.6",
        "2.5",
        "2.4",
        "2.3",
        "2.2",
        "2.1",
        "2.0",
        "1.13",
    ]:
        depends_on("py-tensorflow@" + ver, when="@" + ver, type=("build", "run"))

    depends_on("bazel@0.19.0:", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")

    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["TEST_TMPDIR"] = self.tmp_path
        env["HOME"] = self.tmp_path

        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + self.tmp_path,
            "build",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            # Enable verbose output for failures
            "--verbose_failures",
            "--spawn_strategy=local",
            # bazel uses system PYTHONPATH instead of spack paths
            "--action_env",
            "PYTHONPATH={0}".format(env["PYTHONPATH"]),
            "//tensorflow_estimator/tools/pip_package:build_pip_package",
        ]

        bazel(*args)

        build_pip_package = Executable(
            join_path("bazel-bin/tensorflow_estimator/tools", "pip_package/build_pip_package")
        )
        buildpath = join_path(self.stage.source_path, "spack-build")
        build_pip_package("--src", buildpath)
        with working_dir(buildpath):
            args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*args)
        remove_linked_tree(self.tmp_path)
