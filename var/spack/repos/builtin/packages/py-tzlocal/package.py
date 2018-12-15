# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTzlocal(PythonPackage):
    """tzinfo object for the local timezone."""

    homepage = "https://github.com/regebro/tzlocal"
    url      = "https://pypi.io/packages/source/t/tzlocal/tzlocal-1.3.tar.gz"

    version('1.3', '3cb544b3975b59f91a793850a072d4a8')

    depends_on('py-setuptools', type='build')

    depends_on('py-pytz', type=('build', 'run'))
