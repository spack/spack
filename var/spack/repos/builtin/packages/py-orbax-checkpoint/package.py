# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrbaxCheckpoint(PythonPackage):
    """Orbax includes a checkpointing library oriented towards JAX users, supporting a variety
    of different features required by different frameworks, including asynchronous checkpointing
    various types, and various storage formats. We aim to provide a highly customizable and
    composable API which maximizes flexibility for diverse use cases.
    """

    homepage = "http://github.com/google/orbax"
    pypi = "orbax_checkpoint/orbax_checkpoint-0.5.3.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.3",
        sha256="82acdf18acb1e294396dd583634d3b1bd005bbb81f3de650740384c465d735c3",
        url="https://pypi.org/packages/83/a2/0677f2ee06bdbf7b4e6be4ad931ffe58f2ea82d67bb2a277d9d7b3b1e352/orbax_checkpoint-0.5.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-absl-py")
        depends_on("py-etils+epath+epy")
        depends_on("py-jax@0.4.9:")
        depends_on("py-jaxlib")
        depends_on("py-msgpack")
        depends_on("py-nest-asyncio")
        depends_on("py-numpy")
        depends_on("py-protobuf")
        depends_on("py-pyyaml")
        depends_on("py-tensorstore@0.1.51:", when="@0.4.5:")
        depends_on("py-typing-extensions")
