# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoogleCommon(PythonPackage):
    """Google namespace package"""

    homepage = "http://pypi.python.org/pypi/google-common"
    pypi     = "google-common/google-common-0.0.1.tar.gz"

    version('0.0.1', sha256='add3cf494034fa11080e77cef2cc1f55a436a3353f5f5f95cc4f2b9788a678d1')

    depends_on('py-setuptools', type='build')
