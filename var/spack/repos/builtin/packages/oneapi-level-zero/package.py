# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OneapiLevelZero(CMakePackage):
    """oneAPI Level Zero Loader.

    Applications that need low-level control of a oneAPI level zero
    device link against the loader. The loader depends on a separately
    installed level zero driver. See
    https://dgpu-docs.intel.com/technologies/level-zero.html for
    information on how to install the driver.
    """

    homepage = "https://dgpu-docs.intel.com/technologies/level-zero.html"
    url      = "https://github.com/oneapi-src/level-zero/archive/refs/tags/v1.7.15.tar.gz"

    maintainers = ['rscohn2']

    version('1.7.15', sha256='c39bb05a8e5898aa6c444e1704105b93d3f1888b9c333f8e7e73825ffbfb2617')
    version('1.7.9',  sha256='b430a7f833a689c899b32172a31c3bca1d16adcad8ff866f240a3a8968433de7')
    version('1.7.4',  sha256='23a3f393f6e8f7ed694e0d3248d1ac1b92f2b6964cdb4d747abc23328050513b')
    version('1.6.2',  sha256='ef124adc7a011b672e661fbe38873d7db6546c068a4a03610fdc5118b6b6cbf7')
    version('1.5.4',  sha256='0332215bd00f49e3cc75cf0cfb0111b5e8b7f41046f0b85e29725f00c26bf750')
    version('1.5',    sha256='f93523b412522713bb28d54e2326cac0c342a0cd2662f524c17a65887cf868e8')
    version('1.4.1',  sha256='2878fa29cbf5cea677a00f6dde6eb42d147c98c8d2a99fefece284d85cd1476b')
    version('1.3.7',  sha256='e84c7f36316257eb46f74b41aef5c37fb593a8821497e45dfeda81aceba0abbc')
    version('1.3.6',  sha256='c2b3bd6e4ee3cc874bdcc32bc8705bd217ffc46b194c77e27b23b8391c0c9704')
    version('1.2.3',  sha256='69689429fcdaef74fa8395785aca65f5652e410bd6c56f47b2b64692c098892b')
