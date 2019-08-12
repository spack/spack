# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyReportlab(PythonPackage):
    """The ReportLab Toolkit. An Open Source Python library for generating
    PDFs and graphics."""

    homepage = "https://pypi.python.org/pypi/reportlab"
    url      = "https://pypi.io/packages/source/r/reportlab/reportlab-3.4.0.tar.gz"

    version('3.4.0', '3f2522cf3b69cd84426c216619bbff53')

    # py-reportlab provides binaries that duplicate those of other packages,
    # thus interfering with activation.
    # - easy_install, provided by py-setuptools
    # - pip, provided by py-pip
    extends('python', ignore=r'bin/.*')
