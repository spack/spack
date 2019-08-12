# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKiwisolver(PythonPackage):
    """A fast implementation of the Cassowary constraint solver"""

    homepage = "https://github.com/nucleic/kiwi"
    url      = "https://pypi.io/packages/source/k/kiwisolver/kiwisolver-1.0.1.tar.gz"

    version('1.0.1', 'e2a1718b837e2cd001f7c06934616fcd')

    depends_on('py-setuptools', type='build')
