# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonGitlab(PythonPackage):
    """Python wrapper for the GitLab API"""

    homepage = "https://github.com/gpocentek/python-gitlab"
    url      = "https://pypi.io/packages/source/p/python-gitlab/python-gitlab-0.19.tar.gz"

    version('0.19', '6564d7204c2b7e65c54b3fa89ec91df6')
    version('0.18', 'c31dae1d0bab3966cb830f2308a96308')
    version('0.17', '8a69c602e07dd4731856531d79bb58eb')
    version('0.16', 'e0421d930718021e7d796d74d2ad7194')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-requests@1.0:', type=('build', 'run'))
