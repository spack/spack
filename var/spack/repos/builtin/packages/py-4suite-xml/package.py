# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Py4suiteXml(PythonPackage):
    """XML tools and libraries for Python: Domlette, XPath, XSLT, XPointer,
    XLink, XUpdate"""

    homepage = "http://4suite.org/"
    url      = "https://pypi.io/packages/source/4/4Suite-XML/4Suite-XML-1.0.2.tar.gz"

    version('1.0.2', '3ca3db95cb0263ad80beba034d1ff6ea')

    depends_on('python@2.2.1:')
