# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUrllib3(PythonPackage):
    """HTTP library with thread-safe connection pooling, file post, and
    more."""

    homepage = "https://urllib3.readthedocs.io/"
    url = "https://pypi.io/packages/source/u/urllib3/urllib3-1.20.tar.gz"

    version('1.20', '34691d4e7e20a8e9cdb452ea24fc38e7')
    version('1.14', '5e1407428ac33b521c71a7ac273b3847')

    depends_on('py-setuptools', type='build')
