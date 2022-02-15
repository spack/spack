# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDistlib(PythonPackage):
    """Distribution utilities"""

    homepage = "https://bitbucket.org/pypa/distlib"
    pypi     = "distlib/distlib-0.3.3.zip"

    version('0.3.3', sha256='d982d0751ff6eaaab5e2ec8e691d949ee80eddf01a62eaa96ddb11531fe16b05')

    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
