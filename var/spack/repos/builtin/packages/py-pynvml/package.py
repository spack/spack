# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPynvml(PythonPackage):
    """Provides a Python interface to GPU management and monitoring
    functions. This is a wrapper around the NVML library. For
    information about the NVML library, see the NVML developer page
    https://developer.nvidia.com/nvidia-management-library-nvml"""

    homepage = "https://www.nvidia.com/"
    pypi = "pynvml/pynvml-8.0.4.tar.gz"

    license("Unlicense")

    version(
        "8.0.4",
        sha256="00c1a54fd3462a0774ec08add0d9fbb5f051214a85f782ca7d55b85eb8d54e53",
        url="https://pypi.org/packages/1b/1a/a25c143e1d2f873d67edf534b269d028dd3c20be69737cca56bf28911d02/pynvml-8.0.4-py3-none-any.whl",
    )
