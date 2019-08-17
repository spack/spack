# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycurl(PythonPackage):
    """PycURL is a Python interface to libcurl. PycURL can be used to fetch
    objects identified by a URL from a Python program."""

    homepage = "http://pycurl.io/"
    url      = "https://pypi.io/packages/source/p/pycurl/pycurl-7.43.0.tar.gz"

    version('7.43.0', 'c94bdba01da6004fa38325e9bd6b9760')

    depends_on('python@2.6:')
    depends_on('curl@7.19.0:')
