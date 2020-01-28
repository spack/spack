# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFusepy(PythonPackage):
    """Fusepy is a Python module that provides a simple interface to FUSE and
    MacFUSE. It's just one file and is implemented using ctypes."""

    homepage = "https://github.com/fusepy/fusepy"
    url      = "https://github.com/fusepy/fusepy/archive/v2.0.4.tar.gz"

    version('2.0.4', sha256='802610ab25ad04fc9ef34d024a0abe41cdcaff6a2cb8b2fb92cdda0057c09d1f')

    depends_on('py-setuptools', type='build')
