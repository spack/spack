# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySharedMemory38(PythonPackage):
    """Backport of multiprocessing.shared_memory for Python 3.6 and
    3.7. Simply import all things from shared_memory to make your code
    work. Note that multiprocessing.managers.SharedMemoryManager is also
    included under shared_memory package."""

    homepage = "https://github.com/mars-project/shared_memory38"
    pypi = "shared_memory38/shared_memory38-0.1.2.tar.gz"

    version("0.1.2", sha256="9d4f11fcb08cce059cc31fc8c70292b786a4cf9e411555b37077b7020f5d97e5")

    depends_on("python@3.6:3.7", type=("build", "run"))
    depends_on("py-setuptools", type="build")
