# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXlsxwriter(PythonPackage):
    """XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX
       file format."""

    homepage = "https://pypi.python.org/pypi/XlsxWriter"
    url      = "https://pypi.io/packages/source/X/XlsxWriter/XlsxWriter-1.0.2.tar.gz"

    version('1.0.2', '586f97beeb458c5707794882125330d2')
