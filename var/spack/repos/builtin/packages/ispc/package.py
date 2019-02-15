# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack import *


class Ispc(Package):
    """ispc is a compiler for a variant of the C programming language, with
    extensions for single program, multiple data programming mainly aimed at CPU
    SIMD platforms."""

    homepage = "https://github.com/ispc/ispc/"
    url      = "https://netix.dl.sourceforge.net/project/ispcmirror/v1.10.0/ispc-v1.10.0-linux.tar.gz"

    version('1.10.0', sha256='453211ade91c33826f4facb1336114831adbd35196d016e09d589a6ad8699aa3')

    def url_for_version(self, version):
        url = "https://netix.dl.sourceforge.net/project/ispcmirror/v{0}/ispc-v1.10.0-{1}.tar.gz"

        system = platform.system()
        if system == 'Darwin':
            checksums = {
                Version('1.10.0'): '2b2e2499549ce09a6597b6b645e387953de84544ecb44307e7ee960c9b742a89'
            }
            self.versions[version] = {'checksum': checksums[version]}
            return url.format(version, 'osx')
        else:  # linux
            return url.format(version, 'linux')

    def install(self, spec, prefix):
        for d in ['bin', 'examples']:
            if os.path.isdir(d):
                install_tree(d, join_path(self.prefix, d))
