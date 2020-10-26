# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Date(CMakePackage):
    """A date and time library based on the C++11/14/17 <chrono> header"""

    homepage = "https://github.com/HowardHinnant/date"
    url = "https://github.com/HowardHinnant/date/archive/v3.0.0.zip"

    version('3.0.0', sha256='ddbec664607bb6ec7dd4c7be1f9eefc3d8ce88293ffc9391486ce6ce887ec9b2')

    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            description='Use the specified C++ standard when building')
    variant('shared',
            default=False,
            description='Build shared instead of static libraries')
    variant('tz', default=False, description='Build/install of TZ library')
    variant('tzdb',
            default='download',
            values=('download', 'system', 'manual'),
            description="Timezone database source (automatic download, use "
                        "operating system's database, or manually specify)")

    depends_on('cmake@3.7.0:', type='build')
    depends_on('curl', when='+tz tzdb=download')

    def cmake_args(self):
        spec = self.spec
        args = []

        args.append('-DCMAKE_CXX_STANDARD={0}'.format(
            spec.variants['cxxstd'].value))
        # Require standard at configure time to guarantee the
        # compiler supports the selected standard.
        args.append('-DCMAKE_CXX_STANDARD_REQUIRED=ON')

        args.append('-DBUILD_SHARED_LIBS={0}'.format(
            'ON' if spec.variants['shared'].value else 'OFF'))

        args.append('-DBUILD_TZ_LIB={0}'.format(
            'ON' if spec.variants['tz'].value else 'OFF'))

        tzdb = spec.variants['tzdb'].value
        if tzdb == 'system':
            args.append('-DUSE_SYSTEM_TZ_DB=ON')
        elif tzdb == 'manual':
            args.append('-DMANUAL_TZ_DB=ON')
        else:
            args.extend(['-DUSE_SYSTEM_TZ_DB=OFF', '-DMANUAL_TZ_DB=OFF'])

        return args
