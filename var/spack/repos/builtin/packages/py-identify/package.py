# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIdentify(PythonPackage):
    """File identification library for Python"""

    homepage = "https://github.com/chriskuehl/identify"
    url      = "https://files.pythonhosted.org/packages/6d/10/888a9535d6dd93d8ade00ca52edc682ed16131b3db69efbb7aa4a7bf4f8e/identify-1.2.2.tar.gz"

    version('1.2.2', sha256='d3ddec4436e043c3398392b4ba8936b4ab52fa262284e767eb6c351d9b3ab5b7')

    depends_on('py-setuptools', type='build')
