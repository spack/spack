# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThop(PythonPackage):
    """A tool to count the FLOPs of PyTorch model."""


    homepage = "https://github.com/Lyken17/pytorch-OpCounter/"
    url = "https://files.pythonhosted.org/packages/bb/0f/72beeab4ff5221dc47127c80f8834b4bcd0cb36f6ba91c0b1d04a1233403/thop-0.1.1.post2209072238-py3-none-any.whl"


    version("0.1.1.post2209072238", sha256="01473c225231927d2ad718351f78ebf7cffe6af3bed464c4f1ba1ef0f7cdda27", expand=False)


    depends_on("py-setuptools", type=("build","run"))

