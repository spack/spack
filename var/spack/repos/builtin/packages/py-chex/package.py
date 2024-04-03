# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyChex(PythonPackage):
    """Chex is a library of utilities for helping to write reliable JAX code."""

    homepage = "https://github.com/deepmind/chex"
    pypi = "chex/chex-0.1.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.1.85",
        sha256="32c96719aa94045339174138a6aec14aed2630a8a17fb2633ad3eb868890551d",
        url="https://pypi.org/packages/9a/82/257141baabfaf8b0187521ddb83e996f2a71cdd4f7796d9599ca3e3ea4a9/chex-0.1.85-py3-none-any.whl",
    )
    version(
        "0.1.5",
        sha256="b3321184850d5fc29b2eca63087cdbdd83a1b3e4f33c1314ff8b3b8bd67abbca",
        url="https://pypi.org/packages/38/ee/bce278eceda025e8f7d1939b5a5fd8ebfe4f3307fe33dab7c243b2bc3668/chex-0.1.5-py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="7fd187a68285aae9a35e314817ba037b6e0996da782a40689cfafae1fe7d0536",
        url="https://pypi.org/packages/09/dc/c10c71ec92a4a0e31b4bb0b930389ad4f2c7ad82e7c74aca9bd5bcfc7842/chex-0.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@0.1.8:")
        depends_on("python@3.7:", when="@0.1:0.1.5")
        depends_on("py-absl-py@0.9:")
        depends_on("py-dataclasses@0.7:", when="@0.0.3:0.1.5 ^python@:3.6")
        depends_on("py-dm-tree@0.1.5:", when="@0.0.3:0.1.81")
        depends_on("py-jax@0.4.16:", when="@0.1.83:")
        depends_on("py-jax@0.1.55:", when="@:0.1.6")
        depends_on("py-jaxlib@0.1.37:")
        depends_on("py-numpy@1.24.1:", when="@0.1.83:")
        depends_on("py-numpy@1.18.0:", when="@:0.1.8")
        depends_on("py-setuptools", when="@0.1.85: ^python@3.12:")
        depends_on("py-toolz@0.9:")
        depends_on("py-typing-extensions@4.2:", when="@0.1.8:")

    # Historical dependencies

    # AttributeError: module 'jax.interpreters.pxla' has no attribute 'ShardedDeviceArray'
    conflicts("^py-jax@0.4.14:", when="@:0.1.5")
