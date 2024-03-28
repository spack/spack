# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWandb(PythonPackage):
    """A tool for visualizing and tracking your machine
    learning experiments."""

    homepage = "https://github.com/wandb/wandb"
    pypi = "wandb/wandb-0.13.9.tar.gz"

    maintainers("thomas-bouvier")

    license("MIT")

    version(
        "0.13.9",
        sha256="b8752e5287aca9f8192eca7be352882975973cd3cd0c88815930498fd357569d",
        url="https://pypi.org/packages/a3/b4/279ec12c6c481d0f672e9cf89fbdf7e57f5aacaf23493c699e1c00671ce0/wandb-0.13.9-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-appdirs@1.4.3:", when="@0.13.8:")
        depends_on("py-click@7:8.0.0-rc1,8.0.1:", when="@0.10.32:0.15.4")
        depends_on("py-docker-pycreds@0.4:", when="@0.7:")
        depends_on("py-gitpython@1:", when="@0.6:0.13.10")
        depends_on("py-numpy", when="@0.10:0.10.0-rc1")
        depends_on("py-pathtools", when="@0.10.16:0.16.0-beta1")
        depends_on("py-protobuf@3.19.0:4.21.0-rc2,4.21.1:4", when="@0.13.6: platform=windows")
        depends_on(
            "py-protobuf@3.15.0:4.21.0-rc2,4.21.1:4",
            when="@0.13.6: platform=linux ^python@3.9:3.9.0",
        )
        depends_on(
            "py-protobuf@3.19.0:4.21.0-rc2,4.21.1:4", when="@0.13.6: platform=linux ^python@3.9.1:"
        )
        depends_on(
            "py-protobuf@3.12.0:4.21.0-rc2,4.21.1:4", when="@0.13.6: platform=linux ^python@:3.8"
        )
        depends_on("py-protobuf@3.19.0:4.21.0-rc2,4.21.1:4", when="@0.13.6: platform=freebsd")
        depends_on("py-protobuf@3.19.0:4.21.0-rc2,4.21.1:4", when="@0.13.6: platform=darwin")
        depends_on("py-protobuf@3.19.0:4.21.0-rc2,4.21.1:4", when="@0.13.6: platform=cray")
        depends_on("py-psutil@5:", when="@0.6.29:")
        depends_on("py-pyyaml", when="@0.10:")
        depends_on("py-requests@2:", when="@0.10.0-rc7:")
        depends_on("py-sentry-sdk@1:", when="@0.11.1:")
        depends_on("py-setproctitle", when="@0.12.11:")
        depends_on("py-setuptools", when="@0.12.16:")
        depends_on("py-typing-extensions", when="@0.13.8: ^python@:3.9")

    conflicts("^py-protobuf@4.21.0")

    conflicts("^py-click@8.0.0")
