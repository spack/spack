# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.paths
import spack.store
from spack import *


class OldSbang(Package):
    """Toy package for testing the old sbang replacement problem"""

    homepage = "https://www.example.com"
    url      = "https://www.example.com/old-sbang.tar.gz"

    version('1.0.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        sbang_style_1 = '''#!/bin/bash {0}/bin/sbang
#!/usr/bin/env python

{1}
'''.format(spack.paths.prefix, prefix.bin)
        sbang_style_2 = '''#!/bin/sh {0}/bin/sbang
#!/usr/bin/env python

{1}
'''.format(spack.store.unpadded_root, prefix.bin)
        style_1 = '%s/sbang-style-1.sh' % self.prefix.bin
        style_2 = '%s/sbang-style-2.sh' % self.prefix.bin
        with open(style_1, 'w') as f:
            f.write(sbang_style_1)
        with open(style_2, 'w') as f:
            f.write(sbang_style_2)
        os.chmod(style_1, 0o775)
        os.chmod(style_2, 0o775)
