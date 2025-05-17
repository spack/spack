# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack_repo.builtin.build_systems.python import PythonPackage, PythonPipBuilder

from spack.package import *


class PyTensorboardDataServer(PythonPackage):
    """Fast data loading for TensorBoard"""

    homepage = "https://github.com/tensorflow/tensorboard/tree/master/tensorboard/data/server"
    git = "https://github.com/tensorflow/tensorboard"

    license("Apache-2.0")

    version("0.7.0", commit="f1cb31c86d871e0258250248ab9488575410e784")
    version("0.6.1", commit="6acf0be88b5727e546dd64a8b9b12d790601d561")

    depends_on("py-setuptools", type="build")
    depends_on("rust+dev", type="build")

    # https://github.com/tensorflow/tensorboard/issues/5713
    patch(
        "https://github.com/tensorflow/tensorboard/commit/b085eab93a689230f24d3bba6a8caf75b387f1b9.patch?full_index=1",
        sha256="ce5d221a3302cba1ee7948d6c9e7d4ce053c392b3849a1290a5210905d8e8cbd",
        when="@0.6.1",
    )
    patch(
        "https://github.com/tensorflow/tensorboard/commit/1675de9a2c905ef6cc8ecaa59394cb2fb52489db.patch?full_index=1",
        sha256="8cbd5feb7235d3944fd05ba1f3e16ed3fa0e2212680d6e060c19489be372d6c5",
        when="@0.6.1",
    )

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("CARGO_HOME", self.stage.source_path)

    def install(self, spec, prefix):
        with working_dir(join_path("tensorboard", "data", "server")):
            cargo = which("cargo")
            cargo("build", "--release")

        with working_dir(join_path("tensorboard", "data", "server", "pip_package")):
            python(
                "build.py",
                "--out-dir={0}".format(self.stage.source_path),
                "--server-binary={0}".format(
                    join_path(
                        self.stage.source_path,
                        "tensorboard",
                        "data",
                        "server",
                        "target",
                        "release",
                        "rustboard",
                    )
                ),
            )

        wheel = glob.glob("*.whl")[0]
        pip(*PythonPipBuilder.std_args(self), f"--prefix={prefix}", wheel)
