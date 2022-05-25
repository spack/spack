# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ActsDd4hep(CMakePackage):
    """Glue library to connect Acts to DD4hep"""

    homepage = "https://github.com/acts-project/acts-dd4hep"
    url      = "https://github.com/acts-project/acts-dd4hep/archive/refs/tags/v1.tar.gz"

    maintainers = ['HadrianG2', 'wdconinc']

    version('1', sha256='a220d74933b8887ed8cc9be40c7645d5cb9e5eb4a4ac70d0170d8e2403f29a52')

    depends_on('dd4hep@1.11: +dddetectors')
