# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCatkinPkg(PythonPackage):
    """Library for retrieving information about catkin packages."""

    homepage = "https://wiki.ros.org/catkin_pkg"
    pypi = "catkin-pkg/catkin_pkg-0.4.23.tar.gz"

    version(
        "0.4.23",
        sha256="fbfb107e7e7f3167175b6a68bd51eee7d5a85b2e18c4dbee96d715178f029d8c",
        url="https://pypi.org/packages/32/36/4e418a15c6b0334503f57ff59ccb11a7a3f99c5937d725846110ae1c752d/catkin_pkg-0.4.23-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-docutils")
        depends_on("py-pyparsing", when="@:0.4.16,0.4.19:")
        depends_on("py-python-dateutil")
