# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZipp(PythonPackage):
    """Pathlib-compatible object wrapper for zip files"""

    homepage = "https://github.com/jaraco/zipp"
    url      = "https://files.pythonhosted.org/packages/0f/f4/930f91b0527d9701623d4895a978ec0abd6b8904ef272a2701190fdbf9f8/zipp-0.3.3.tar.gz"

    version('0.3.3', sha256='55ca87266c38af6658b84db8cfb7343cdb0bf275f93c7afaea0d8e7a209c7478')

    depends_on('py-setuptools', type='build')
