# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPynvml(PythonPackage):
    """Provides a Python interface to GPU management and monitoring
    functions. This is a wrapper around the NVML library. For
    information about the NVML library, see the NVML developer page
    https://developer.nvidia.com/nvidia-management-library-nvml"""

    homepage = "https://www.nvidia.com/"
    pypi = "pynvml/pynvml-8.0.4.tar.gz"

    license("BSD-3-Clause", when="@12:")
    license("Unlicense", when="@:11")

    version("12.0.0", sha256="299ce2451a6a17e6822d6faee750103e25b415f06f59abb8db65d30f794166f5")
    version("11.5.3", sha256="183d223ae487e5f00402d8da06c68c978ef8a9295793ee75559839c6ade7b229")
    version("8.0.4", sha256="c8d4eadc648c7e12a3c9182a9750afd8481b76412f83747bcc01e2aa829cde5d")

    depends_on("py-nvidia-ml-py", when="@12:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("python@3.9:", when="@12:", type=("build", "run"))
    depends_on("python", when="@11:", type=("build", "run"))
    depends_on("python@:3.11", when="@8.0.4", type=("build", "run"))
