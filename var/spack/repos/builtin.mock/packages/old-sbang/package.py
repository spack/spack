# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.paths
import spack.store
from spack.package import *


class OldSbang(Package):
    """Toy package for testing the old sbang replacement problem"""

    homepage = "https://www.example.com"
    url = "https://www.example.com/old-sbang.tar.gz"

    version("1.0.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with open(os.path.join(self.prefix.bin, "sbang-style-2.sh"), "w") as f:
            f.write(
                f"""#!/bin/sh {spack.store.STORE.unpadded_root}/bin/sbang
#!/usr/bin/env python

{prefix.bin}
"""
            )
