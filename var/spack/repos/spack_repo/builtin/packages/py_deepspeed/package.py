# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyDeepspeed(PythonPackage):
    """DeepSpeed library.

    DeepSpeed enables world's most powerful language models like MT-530B and BLOOM. It is an
    easy-to-use deep learning optimization software suite that powers unprecedented scale and
    speed for both training and inference.
    """

    homepage = "http://deepspeed.ai/"
    pypi = "deepspeed/deepspeed-0.10.0.tar.gz"

    license("Apache-2.0")

    version("0.16.4", sha256="495febfb6dd20423f44b1c4a1bb6da2cadbcaf9b07962e17f87d52edfeec9bba")
    version("0.15.4", sha256="60e7c044b7fc386cdad1206212d22b6963ea551f656ed51f7cb34b299459bf2c")
    version("0.13.5", sha256="05404e083b5df36dcfe36884565dcb1d9fd1165e443a82c1c09370293943f6d1")
    version("0.13.0", sha256="e890adca061af36c775b40252306191c3029f0b8bd33cceefa9fa7ecbf350a05")
    version("0.10.0", sha256="afb06a97fde2a33d0cbd60a8357a70087c037b9f647ca48377728330c35eff3e")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-hjson", type=("build", "run"))
    depends_on("ninja", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging@20:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-py-cpuinfo", type=("build", "run"))
    depends_on("py-pydantic@2:", type=("build", "run"), when="@0.15.4:")
    depends_on("py-pydantic@:1", type=("build", "run"), when="@:0.13")
    # https://github.com/microsoft/DeepSpeed/issues/2830
    depends_on("py-torch+distributed", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
