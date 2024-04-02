# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHuggingfaceHub(PythonPackage):
    """This library allows anyone to work with the Hub
    repositories: you can clone them, create them and upload
    your models to them."""

    homepage = "https://github.com/huggingface/huggingface_hub"
    pypi = "huggingface_hub/huggingface_hub-0.0.10.tar.gz"

    license("Apache-2.0")

    version(
        "0.19.4",
        sha256="dba013f779da16f14b606492828f3760600a1e1801432d09fe1c33e50b825bb5",
        url="https://pypi.org/packages/05/09/1945ca6ba3ad8ad6e2872ba682ce8d68c5e63c8e55458ed8ab4885709f1d/huggingface_hub-0.19.4-py3-none-any.whl",
    )
    version(
        "0.14.1",
        sha256="9fc619170d800ff3793ad37c9757c255c8783051e1b5b00501205eb43ccc4f27",
        url="https://pypi.org/packages/58/34/c57b951aecd0248845932c1cfc15721237c50e463f26b0536673bcb76f4f/huggingface_hub-0.14.1-py3-none-any.whl",
    )
    version(
        "0.10.1",
        sha256="dc3b0e9a663fe6cad6a8522055c02a9d8673dbd527223288e2442bc028c253db",
        url="https://pypi.org/packages/b2/2b/715a1924d470691a27b2dcdf472a9ef87f04718a897de25e68bf86ac0184/huggingface_hub-0.10.1-py3-none-any.whl",
    )
    version(
        "0.0.10",
        sha256="447cb5ac83da68dba8b5c42069165da81c4d9450b3d6a78ce027a9e5cce9461f",
        url="https://pypi.org/packages/3c/e3/fb7b6aefaf0fc7b792cebbbd590b1895c022ab0ff27f389e1019c6f2e68a/huggingface_hub-0.0.10-py3-none-any.whl",
    )
    version(
        "0.0.8",
        sha256="feec10c3cff31bab75fa90ed801a1979301d4ebcbdf681312cb0371f77f53dff",
        url="https://pypi.org/packages/a1/88/7b1e45720ecf59c6c6737ff332f41c955963090a18e72acbcbeac6b25e86/huggingface_hub-0.0.8-py3-none-any.whl",
    )

    variant(
        "cli",
        default=False,
        when="@0.10:",
        description="Install dependencies for CLI-specific features",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.17:")
        depends_on("python@3.7:", when="@0.5:0.16")
        depends_on("py-filelock")
        depends_on("py-fsspec@2023.5:", when="@0.18:")
        depends_on("py-fsspec", when="@0.14:0.17")
        depends_on("py-importlib-metadata", when="@0.0.2:0.16 ^python@:3.7")
        depends_on("py-inquirerpy@0.3.4:", when="@0.10:+cli")
        depends_on("py-packaging@20.9:", when="@0.0.11:")
        depends_on("py-pyyaml@5.1:", when="@0.7:")
        depends_on("py-requests")
        depends_on("py-tqdm@4.42.1:", when="@0.12:")
        depends_on("py-tqdm", when="@:0.11")
        depends_on("py-typing-extensions@3.7.4.3:", when="@0.1.1:")
        depends_on("py-typing-extensions", when="@0.0.9:0.1.0")
