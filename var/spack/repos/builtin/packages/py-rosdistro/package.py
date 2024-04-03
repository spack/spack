# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosdistro(PythonPackage):
    """A tool to work with rosdistro files."""

    homepage = "https://wiki.ros.org/rosdistro"
    pypi = "rosdistro/rosdistro-0.8.3.tar.gz"

    version(
        "0.8.3",
        sha256="4d61b3d5a3c0661767ecb947c75fa3fd4be06d7f5788ec7d75d0fb734049c921",
        url="https://pypi.org/packages/8e/d2/9edf2b1ee6d9e762ca136eff03c9f4883d5d00d330946cbb2897adb3395f/rosdistro-0.8.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-catkin-pkg")
        depends_on("py-pyyaml")
        depends_on("py-rospkg")
        depends_on("py-setuptools")
