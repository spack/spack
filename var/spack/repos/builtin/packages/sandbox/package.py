# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sandbox(AutotoolsPackage):
    """sandbox'd LD_PRELOAD hack by Gentoo Linux"""

    homepage = "https://www.gentoo.org/proj/en/portage/sandbox/"
    url      = "https://dev.gentoo.org/~mgorny/dist/sandbox-2.12.tar.xz"

    version('2.20', sha256='de220bcd15548fce3ca42edc42092d7e3ebadaeb97bc53fe330b0f74188fd081')
    version('2.15', sha256='3ae3202191180aa4c25634e28a1a122bcc72c825053be216eab5a19f8ec30683')
    version('2.14', sha256='62afedfb300d563dacdc00ac93109831494885ef8b3738fe791a54981a79a5f7')
    version('2.13', sha256='257d9f70fa24e5fd30217f9a4ba7f2e81205c498276d2136637d5bfef83f8199')
    version('2.12', sha256='265a490a8c528237c55ad26dfd7f62336fa5727c82358fc9cfbaa2e52c47fc50')
