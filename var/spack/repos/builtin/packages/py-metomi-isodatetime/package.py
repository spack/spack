# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
#     spack install py-metomi-isodatetime
#
# You can edit this file again by typing:
#
#     spack edit py-metomi-isodatetime
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyMetomiIsodatetime(PythonPackage):
    """Python ISO 8601 date time parser and data model/manipulation utilities."""

    homepage = "https://github.com/metomi/isodatetime"
    pypi="metomi-isodatetime/metomi-isodatetime-1!3.0.0.tar.gz"
    
    maintainers("LydDeb")

    version("3.0.0", sha256="2141e8aaa526ea7f7f1cb883e6c8ed83ffdab73269658d84d0624f63a6e1357e")

    depends_on("python@3.6:3.9", type=("build", "run"))
    depends_on("py-setuptools", type="build")
