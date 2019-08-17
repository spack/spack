# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEtXmlfile(PythonPackage):
    """An implementation of lxml.xmlfile for the standard library."""

    homepage = "https://bitbucket.org/openpyxl/et_xmlfile"
    url      = "https://pypi.io/packages/source/e/et_xmlfile/et_xmlfile-1.0.1.tar.gz"

    version('1.0.1', 'f47940fd9d556375420b2e276476cfaf')

    depends_on('py-setuptools', type='build')
