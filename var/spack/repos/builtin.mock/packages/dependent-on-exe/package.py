# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import stat


class DependentOnExe(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('pkg-with-executable', type=('run',))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        exe_fname = join_path(prefix.bin, 'dependent-exe')

        with open(exe_fname, 'w') as exe_file:
            exe_file.write("""\
#!/bin/bash
echo "Dependent bash script"
dependency-exe
""")

        st = os.stat(exe_fname)
        os.chmod(exe_fname, st.st_mode | stat.S_IEXEC)
