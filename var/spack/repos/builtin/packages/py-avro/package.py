# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAvro(PythonPackage):
    """Avro is a serialization and RPC framework."""

    homepage = "https://avro.apache.org/docs/current/"
    pypi = "avro/avro-1.8.2.tar.gz"

    version("1.11.1", sha256="f123623ecc648d0e20ce14f8ed85162140c13cc4b108865d1b2529fbfa06c008")
    version("1.11.0", sha256="1206365cc30ad561493f735329857dd078533459cee4e928aec2505f341ce445")
    version("1.10.2", sha256="381b990cc4c4444743c3297348ffd46e0c3a5d7a17e15b2f4a9042f6e955c31a")
    version("1.8.2", sha256="8f9ee40830b70b5fb52a419711c9c4ad0336443a6fba7335060805f961b04b59")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@40.8.0:", when="@1.11.1:", type="build")
    depends_on("python@2.7:", type=("build", "run"))
    depends_on("python@3.6:", when="@1.11.1:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
