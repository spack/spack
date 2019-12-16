# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonLogstash(PythonPackage):
    """Python logging handler for Logstash."""

    homepage = "https://github.com/vklochan/python-logstash"
    url      = "https://pypi.io/packages/source/p/python-logstash/python-logstash-0.4.6.tar.gz"

    version('0.4.6', '26fafa0ea306025fb7644d70cb38982a')
