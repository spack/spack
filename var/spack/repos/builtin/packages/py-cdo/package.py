# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCdo(PythonPackage):
    """The cdo package provides an interface to the Climate Data
    Operators from Python."""

    pypi = "cdo/cdo-1.3.2.tar.gz"

    version('1.5.4', sha256='997c5d31c964edbae4835eed7055734e8ec67533a5aaa2a9f69f86a0c23173ac')
    version('1.5.3', sha256='b35b872046c3bd98e9d325882197df6f4c4b92c0602bb2ce4bb3af645b0cdb4f')
    version('1.5.2', sha256='eb4a6dbae6656f7a6f7822f0429aedd410e799df9a0ec37e9c55256d5808be56')
    version('1.5.1', sha256='cf1feacf21cafa7af3373e40c75a83c412cc3c8d57b67a138484bcbbb0d98f6c')
    version('1.4.0', sha256='dae7cdba3c52d36a4cdcd9e91183416f05f1478a02960048777b1860c2601d27')
    version('1.3.6', sha256='b167efbbac7d0a6cbf74f5d211255705c73245f7c2590b6d9eb634347d8b2c1f')
    version('1.3.5', sha256='b1225773f29c0e52354c66cf0d1026ce78cb6fa9872fdb2748c0f209218df316')
    version('1.3.4', sha256='2f086a4141f8448947ebcd11532faad42a5836d57b63edf3e1f054ea6feab289')
    version('1.3.3', sha256='33653e582a8e62df2da9c8be2832618a85e20dc59ef92db53540a1740f0b387e')
    version('1.3.2', sha256='9f78879d90d14134f2320565016d0d371b7dfe7ec71110fd313868ec1db34aee')

    depends_on('cdo')

    depends_on('py-setuptools', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
