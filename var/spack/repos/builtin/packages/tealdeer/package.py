# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tealdeer(CargoPackage):
    """Fetch and show tldr help pages for many CLI commands. Full featured
    offline client with caching support."""

    homepage  = "https://github.com/dbrgn/tealdeer/"
    crates_io = "tealdeer"
    git       = "https://github.com/dbrgn/tealdeer.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('1.3.0', sha256='39d280123d74716028e5298110568cb7186636793e47350c0505b94703259329')
    version('1.2.0', sha256='d0dd331d47c2d55a127a960a979024c2e430f0d461dd9b840c079df9e1d01f48')
    version('1.1.0', sha256='96d1ac948e1e2befbdf4e4ac0873be4836fbf3f7f8df5428d547a3415466b76b')
    version('1.0.0', sha256='784704f8f69ef22af9d0cd35e248a6df536da3945c54ceafcbf1e2a6bcf153fc')
    version('0.4.0', sha256='356292978f1ac7f8b829caba9900f46b8784d93f722c1390b3a8588c76860693')
    version('0.3.0', sha256='0d875b20603e10187a98d54804f025b70787d61398f51b8701e3941dd2f8cac7')
    version('0.2.0', sha256='9d4189562f79ede17cfe066205bb01c9eec87883c9f783c4f8ad78c13fc8e029')
