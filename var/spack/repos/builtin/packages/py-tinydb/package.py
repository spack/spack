# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTinydb(PythonPackage):
    """TinyDB is a tiny, document oriented database optimized for your happiness."""

    homepage = "https://tinydb.readthedocs.io"
    pypi = "tinydb/tinydb-4.7.0.tar.gz"

    version("4.7.0", sha256="357eb7383dee6915f17b00596ec6dd2a890f3117bf52be28a4c516aeee581100")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
    depends_on("py-typing-extensions@3.10.0:4", type=("build", "run"), when="^python@:3.7")
