# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyZopeEvent(PythonPackage):
    """Very basic event publishing system."""

    homepage = "https://github.com/zopefoundation/zope.event"
    pypi = "zope.event/zope.event-4.3.0.tar.gz"

    version('4.5.0', sha256='5e76517f5b9b119acf37ca8819781db6c16ea433f7e2062c4afc2b6fbedb1330')
    version('4.3.0', sha256='e0ecea24247a837c71c106b0341a7a997e3653da820d21ef6c08b32548f733e7')

    depends_on('py-setuptools', type=('build', 'run'))
