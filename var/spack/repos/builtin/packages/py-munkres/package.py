# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMunkres(PythonPackage):
    """Python library for Munkres algorithm"""

    homepage = "https://github.com/bmc/munkres"
    url = "https://pypi.io/packages/source/m/munkres/munkres-1.0.11.tar.gz"

    version('1.0.11', sha256='7188f2ed6e8d3eb6c5ec4919200faa6194732b99707b058f7e9f068c588f7eca', preferred=True)

    depends_on('py-setuptools', type='build')
