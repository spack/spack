# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySmmap2(PythonPackage):
    """A pure Python implementation of a sliding window memory map manager
    """

    homepage = "https://github.com/gitpython-developers/smmap"
    url      = "https://pypi.io/packages/source/s/smmap2/smmap2-3.11.2.tar.gz"

    version('2.0.5', '29a9ffa0497e7f2be94ca0ed1ca1aa3cd4cf25a1f6b4f5f87f74b46ed91d609a')

    depends_on('py-setuptools', type=('build', 'run'))
