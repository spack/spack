# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDmHaiku(PythonPackage):
    """JAX-based neural network library"""

    homepage = "https://github.com/deepmind/dm-haiku"
    pypi = "dm-haiku/dm-haiku-0.0.5.tar.gz"

    version("0.0.7", sha256="86c34af6952a305a4bbfda6b9925998577acc4aa2ad9333da3d6047f4f8ed7c1")
    version("0.0.5", sha256="e986237e1f840aa3bd26217ecad84b611bf1456e2139f0f79ea71f9c6222d231")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.7.1:", type=("build", "run"))
    depends_on("py-jmp@0.0.2:", type=("build", "run"))
    depends_on("py-numpy@1.18.0:", type=("build", "run"))
    depends_on("py-tabulate@0.8.9:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
    # from README.md:
    # Because JAX installation is different depending on your CUDA version, Haiku does
    # not list JAX as a dependency in `requirements.txt`.
    depends_on("py-jax", type=("build", "run"))
