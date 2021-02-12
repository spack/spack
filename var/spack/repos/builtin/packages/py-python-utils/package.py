# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPythonUtils(PythonPackage):
    """Python Utils is a collection of small Python functions and classes
    which make common patterns shorter and easier."""

    homepage = "https://github.com/WoLpH/python-utils"
    pypi = "python-utils/python-utils-2.4.0.tar.gz"

    version('2.5.6', sha256='352d5b1febeebf9b3cdb9f3c87a3b26ef22d3c9e274a8ec1e7048ecd2fac4349')
    version('2.5.5', sha256='47fa0de95dd1ae90b03eb257053d426ce8cf5711b2eb60a0872469fdcf062759')
    version('2.5.3', sha256='5453db694f92aafc3f3285b1526541dee6de0b9344d6fd65b6bac8b68ef120bf')
    version('2.5.2', sha256='10e155d88b706b25ede773354ea782eee6d494294651228469c916eb20f7ee1c')
    version('2.5.1', sha256='579f409ba0dc3d427970d1b31a4074c8e5d17805a4596b16ccceed357e4d78a4')
    version('2.5.0', sha256='c43705696ced0d0e36124a5df2098500fc2f3527f4f2c4f1583f3c50af36671e')
    version('2.4.0', sha256='f21fc09ff58ea5ebd1fd2e8ef7f63e39d456336900f26bdc9334a03a3f7d8089')
    version('2.3.0', sha256='34aaf26b39b0b86628008f2ae0ac001b30e7986a8d303b61e1357dfcdad4f6d3')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
