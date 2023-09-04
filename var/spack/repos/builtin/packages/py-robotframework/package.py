# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRobotframework(PythonPackage):
    """Robot Framework is a generic open source automation framework for acceptance testing, acceptance test driven development (ATDD), and robotic process automation (RPA). 
    It has simple plain text syntax and it can be extended easily with generic and custom libraries.

    You can learn more about EPICS here: https://robotframework.org/
    """

    homepage = "https://pypi.org/project/robotframework/"
    url = "https://files.pythonhosted.org/packages/c6/37/fc94979077241a09f31f347cbae401c9f62705eadd441a392285537e603c/robotframework-6.1.1.zip"

    version("6.1.1", sha256="3fa18f2596a4df2418c4b59abf43248327c15ed38ad8665f6a9a9c75c95d7789")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))