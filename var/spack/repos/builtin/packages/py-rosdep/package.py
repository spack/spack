# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosdep(PythonPackage):
    """rosdep package manager abstraction tool for ROS."""

    homepage = "https://wiki.ros.org/rosdep"
    pypi = "rosdep/rosdep-0.20.0.tar.gz"

    version(
        "0.20.0",
        sha256="e0af90f313c14bdbc92ff94ea2d56057047e515c98677423b1f9535d94fcf085",
        url="https://pypi.org/packages/b9/6a/67afeb7640d66f92446bf5fa2920f1fb86a11d784f0d7063dd8da31d39a3/rosdep-0.20.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-catkin-pkg@0.4:")
        depends_on("py-pyyaml")
        depends_on("py-rosdistro@0.7.5:", when="@0.16.2:")
        depends_on("py-rospkg@1.2.7:", when="@0.20:0.20.0")
