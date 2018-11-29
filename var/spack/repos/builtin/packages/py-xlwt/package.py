# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyXlwt(PythonPackage):
    """Library to create spreadsheet files compatible with
    MS Excel 97/2000/XP/2003 XLS files, on any platform,
    with Python 2.6, 2.7, 3.3+."""

    homepage = "https://pypi.org/project/xlwt/"
    url      = "https://pypi.io/packages/source/x/xlwt/xlwt-1.3.0.tar.gz"

    version('1.3.0', '4b1ca8a3cef3261f4b4dc3f138e383a8')

    depends_on('py-setuptools', type='build')
