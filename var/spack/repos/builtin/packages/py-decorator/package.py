# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDecorator(PythonPackage):
    """The aim of the decorator module it to simplify the usage of decorators
       for the average programmer, and to popularize decorators by showing
       various non-trivial examples."""
    homepage = "https://github.com/micheles/decorator"
    url      = "https://pypi.io/packages/source/d/decorator/decorator-4.0.9.tar.gz"

    version('4.3.0', sha256='c39efa13fbdeb4506c476c9b3babf6a718da943dab7811c206005a4a956c080c')
    version('4.0.9', 'f12c5651ccd707e12a0abaa4f76cd69a')

    depends_on('py-setuptools', type='build')
