# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vmatch(Package):
    """Vmatch is a versatile software tool for efficiently solving large scale
       sequence matching tasks"""

    homepage = "http://www.vmatch.de/"
    url      = "http://www.vmatch.de/distributions/vmatch-2.3.0-Linux_x86_64-64bit.tar.gz"

    version('2.3.0', '592a4f941239494d892f3c6ff21a1423')

    def url_for_version(self, version):
        url = 'http://www.vmatch.de/distributions/vmatch-{0}-Linux_x86_64-64bit.tar.gz'
        return url.format(version)

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
