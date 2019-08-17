# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMako(PythonPackage):
    """A super-fast templating language that borrows the best
       ideas from the existing templating languages."""

    homepage = "https://pypi.python.org/pypi/mako"
    url = "https://pypi.io/packages/source/M/Mako/Mako-1.0.1.tar.gz"

    version('1.0.4', 'c5fc31a323dd4990683d2f2da02d4e20')
    version('1.0.1', '9f0aafd177b039ef67b90ea350497a54')

    depends_on('py-setuptools', type='build')
    depends_on('py-mock',   type='test')
    depends_on('py-pytest', type='test')
    depends_on('py-markupsafe@0.9.2:', type=('build', 'run'))
