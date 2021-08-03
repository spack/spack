# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import llnl.util.tty as tty

from spack import *


class PerlTk(PerlPackage):
    """Interface to Tk Graphics Library"""

    homepage = "https://metacpan.org/pod/distribution/Tk/Tk.pod"
    url      = "https://cpan.metacpan.org/authors/id/S/SR/SREZIC/Tk-804.035.tar.gz"
    git      = "https://github.com/eserte/perl-tk.git"

    maintainers = ['cessenat']

    version('master', branch='master')
    version('804.036', sha256='32aa7271a6bdfedc3330119b3825daddd0aa4b5c936f84ad74eabb932a200a5e')
    version('804.035', sha256='4d2b80291ba6de34d8ec886a085a6dbd2b790b926035a087e99025614c5ffdd4')
    version('804.033', sha256='84756e9b07a2555c8eecf88e63d5cbbba9b1aa97b1e71a3d4aa524a7995a88ad')

    depends_on('perl-extutils-makemaker', type='build')

    @run_before('install')
    def filter_nonutf8(self):
        path = 'ptked'
        with open(path, 'rb') as original_file:
            original = original_file.read()
            if sys.version_info >= (2, 7):
                try:
                    original = original.decode(encoding='UTF-8')
                except Exception:
                    try:
                        original = original.decode(encoding='latin-1')
                        with open(path, 'wb') as new_file:
                            new_file.write(original.encode(encoding='UTF-8'))
                    except Exception:
                        tty.warn('Encoding not detected file={0}'.format(path))
