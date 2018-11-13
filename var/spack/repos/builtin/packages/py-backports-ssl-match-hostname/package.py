# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsSslMatchHostname(PythonPackage):
    """The ssl.match_hostname() function from Python 3.5"""

    homepage = "https://pypi.python.org/pypi/backports.ssl_match_hostname"
    url      = "https://pypi.io/packages/source/b/backports.ssl_match_hostname/backports.ssl_match_hostname-3.5.0.1.tar.gz"

    py_namespace = 'backports'

    version('3.5.0.1', 'c03fc5e2c7b3da46b81acf5cbacfe1e6')
