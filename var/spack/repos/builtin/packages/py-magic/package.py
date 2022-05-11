# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyMagic(PythonPackage):
    """A python wrapper for libmagic.

    .. warning::
        DO NOT USE: this is a duplicate of py-python-magic and will be deleted.
    """

    homepage = "https://github.com/ahupp/python-magic"
    url      = "https://github.com/ahupp/python-magic/archive/0.4.15.tar.gz"

    version('0.4.15', sha256='6d730389249ab1e34ffb0a3c5beaa44e116687ffa081e0176dab6c59ff271593', deprecated=True)

    depends_on('python@2.7.0:2.7,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('file', type='run')
