# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyConfigobj(PythonPackage):
    """Config file reading, writing and validation.
    """

    homepage = "https://github.com/DiffSK/configobj"
    url      = "https://pypi.io/packages/source/c/configobj/configobj-5.0.6.tar.gz"

    version('5.0.6', sha256='a2f5650770e1c87fb335af19a9b7eb73fc05ccf22144eb68db7d00cd2bcb0902')
    version('4.7.2', sha256='515ff923462592e8321df8b48c47e3428f8d406ee22b8de77bef969d1af11171')

    # The version on PyPi seems to be outdated (2014) although confusingly
    # enough version number is the same as the latest release on github.
    depends_on('py-six', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    def url_for_version(self, version):
        if version <= Version('5.0.0'):
            url = "https://pypi.io/packages/source/c/configobj/configobj-{0}.tar.gz"
        else:
            url = "https://github.com/DiffSK/configobj/archive/v{0}.tar.gz"

        return url.format(version)
