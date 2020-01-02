# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCoverage(PythonPackage):
    """ Testing coverage checker for python """

    homepage = "http://nedbatchelder.com/code/coverage/"
    url      = "https://pypi.io/packages/source/c/coverage/coverage-4.5.4.tar.gz"

    version('4.5.4', sha256='e07d9f1a23e9e93ab5c62902833bf3e4b1f65502927379148b6622686223125c')
    version('4.3.4', sha256='eaaefe0f6aa33de5a65f48dd0040d7fe08cac9ac6c35a56d0a7db109c3e733df')
    version('4.0a6', sha256='85c7f3efceb3724ab066a3fcccc05b9b89afcaefa5b669a7e2222d31eac4728d')

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
