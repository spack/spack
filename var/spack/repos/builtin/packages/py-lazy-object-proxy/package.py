# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazyObjectProxy(PythonPackage):
    """A fast and thorough lazy object proxy."""

    homepage = "https://github.com/ionelmc/python-lazy-object-proxy"
    url      = "https://pypi.io/packages/source/l/lazy-object-proxy/lazy-object-proxy-1.3.1.tar.gz"

    version('1.3.1', 'e128152b76eb5b9ba759504936139fd0')

    conflicts('^python@3.0:3.2.99')

    depends_on('py-setuptools', type='build')
