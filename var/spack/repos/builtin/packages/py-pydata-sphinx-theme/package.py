# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydataSphinxTheme(PythonPackage):
    """A clean, three-column, Bootstrap-based Sphinx theme by and for the PyData community."""

    homepage = "https://pypi.org/project/pydata-sphinx-theme/"
    pypi = "pydata_sphinx_theme/pydata_sphinx_theme-0.9.0.tar.gz"

    maintainers("chissg", "gartung", "marcmengel", "vitodb")

    version("0.9.0", sha256="03598a86915b596f4bf80bef79a4d33276a83e670bf360def699dbb9f99dc57a")
