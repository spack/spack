# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColoredlogs(PythonPackage):
    """Colored terminal output for Python's logging module"""

    homepage = "https://pypi.org/project/coloredlogs/"
    url      = "https://files.pythonhosted.org/packages/63/09/1da37a51b232eaf9707919123b2413662e95edd50bace5353a548910eb9d/coloredlogs-10.0.tar.gz"

    version('10.0', sha256='b869a2dda3fa88154b9dd850e27828d8755bfab5a838a1c97fbc850c6e377c36')

    depends_on('py-setuptools', type='build')
    depends_on('py-humanfriendly', type='run')
