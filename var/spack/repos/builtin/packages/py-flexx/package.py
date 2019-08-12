# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlexx(PythonPackage):
    """Write desktop and web apps in pure Python."""

    homepage = "http://flexx.readthedocs.io"
    url      = "https://pypi.io/packages/source/f/flexx/flexx-0.4.1.zip"

    version('0.4.1', '7138a378aa68d781212c4b2cfb6ddfcb')

    depends_on('py-setuptools', type='build')
    depends_on('py-tornado',    type=('build', 'run'))
