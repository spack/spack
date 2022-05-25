# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ActsDd4hep(CMakePackage):
    """Glue library to connect Acts to DD4hep"""

    homepage = "https://github.com/acts-project/acts-dd4hep"
    url      = "https://github.com/acts-project/acts-dd4hep/archive/refs/tags/v1.0.0.tar.gz"

    maintainers = ['HadrianG2', 'wdconinc']

    version('1.0.0', sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    depends_on('dd4hep@1.11: +dddetectors')
