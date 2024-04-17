# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRospkg(PythonPackage):
    """Library for retrieving information about ROS packages and stacks."""

    homepage = "https://wiki.ros.org/rospkg"
    pypi = "rospkg/rospkg-1.2.9.tar.gz"

    version(
        "1.2.9",
        sha256="7494c6c7c268c99c51e9d98b0a9eee82900cfd97408e485c6a4294898d834ad6",
        url="https://pypi.org/packages/66/78/5395e9e4d3767f27ae63d74777e3fd735a2aaf9d764de8fc9f042d899dfc/rospkg-1.2.9-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-catkin-pkg")
        depends_on("py-distro", when="@1.2.1:1.2.4,1.2.6:1.3")
        depends_on("py-pyyaml")
