# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLxml(PythonPackage):
    """lxml is the most feature-rich and easy-to-use library for processing
    XML and HTML in the Python language."""

    homepage = "http://lxml.de/"
    url      = "https://pypi.io/packages/source/l/lxml/lxml-2.3.tar.gz"

    version('3.7.3', '075692ce442e69bbd604d44e21c02753')
    version('2.3', 'a245a015fd59b63e220005f263e1682a')

    depends_on('py-setuptools@0.6c5:', type='build')
    depends_on('py-cython@0.20:', type='build')
    depends_on('libxml2', type=('build', 'run'))
    depends_on('libxslt', type=('build', 'run'))
