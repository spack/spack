# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-parsel
#
# You can edit this file again by typing:
#
#     spack edit py-parsel
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyParsel(PythonPackage):
    """Parsel is a BSD-licensed Python library to extract and remove data from
    HTML and XML using XPath and CSS selectors and regular expressions.
    """

    homepage = "https://parsel.readthedocs.io"
    url = "https://github.com/scrapy/parsel/archive/refs/tags/v1.6.0.tar.gz"

    maintainers = ["frerappa"]

    version("1.6.0", sha256="15546bb637074725e4b2c0d7c579356636251389d9b296520543d835d615e83d")

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    # depends_on("python@2.X:2.Y,3.Z:", type=("build", "run"))
    # depends_on("py-pip@X.Y:", type="build")
    # depends_on("py-wheel@X.Y:", type="build")

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    # depends_on("py-setuptools", type="build")
    # depends_on("py-flit-core", type="build")
    # depends_on("py-poetry-core", type="build")

    # FIXME: Add additional dependencies if required.
    # depends_on("py-foo", type=("build", "run"))

    # def global_options(self, spec, prefix):
    #     # FIXME: Add options to pass to setup.py
    #     # FIXME: If not needed, delete this function
    #     options = []
    #     return options

    # def install_options(self, spec, prefix):
    #     # FIXME: Add options to pass to setup.py install
    #     # FIXME: If not needed, delete this function
    #     options = []
    #     return options
