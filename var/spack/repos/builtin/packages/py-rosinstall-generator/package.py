# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosinstallGenerator(PythonPackage):
    """A tool for generating rosinstall files."""

    homepage = "https://wiki.ros.org/rosinstall_generator"
    pypi = "rosinstall-generator/rosinstall_generator-0.1.22.tar.gz"

    version(
        "0.1.22",
        sha256="a175ac6c27224148a8d3b2cc263ac6fda3f7b29bc536eab32619197530729dcc",
        url="https://pypi.org/packages/95/32/12c47a4bfc47dd648f8446cd8bc7e634422092dcd9c7bca07ec250010e61/rosinstall_generator-0.1.22-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-catkin-pkg@0.1.28:", when="@0.1.15:")
        depends_on("py-pyyaml", when="@0.1.15:")
        depends_on("py-rosdistro@0.7.3:", when="@0.1.16:")
        depends_on("py-rospkg", when="@0.1.15:")
        depends_on("py-setuptools", when="@0.1.15:0.1.22")
