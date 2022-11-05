# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPystache(Package):
    """Pystache is a Python implementation of Mustache. Mustache is a
    framework-agnostic, logic-free templating system inspired by ctemplate and
    et."""

    homepage = "git@github.com:sarnold/pystache.git"
    git = "git@github.com:sarnold/pystache.git"
    pypi = "https://files.pythonhosted.org/packages/3f/e7/8750ba6c6101d6aa5ceeb20c013adf2c6f3554a12c71d75654b468404bfa/pystache-0.6.0.tar.gz"

    list_url = "https://pypi.org/simple/setuptools/"

    maintainers = ["adamjstewart"]

    version("0.6.0", sha256="880b29367f9d94c8c0f154df5566f03512b4d8c1")

    extends("python")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pip", type="build")
