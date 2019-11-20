# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lsof(Package):
    """Lsof displays information about files open to Unix processes."""

    homepage = "https://people.freebsd.org/~abe/"
    url      = "https://www.mirrorservice.org/sites/lsof.itap.purdue.edu/pub/tools/unix/lsof/OLD/lsof_4.89.tar.gz"

    version('4.89', sha256='5d08da7ebe049c9d9a6472d6afb81aa5af54c4733a3f8822cbc22b57867633c9')

    def install(self, spec, prefix):
        tar = which('tar')
        tar('xf', 'lsof_{0}_src.tar'.format(self.version))

        with working_dir('lsof_{0}_src'.format(self.version)):
            configure = Executable('./Configure')
            configure('-n', 'linux')

            make()

            mkdir(prefix.bin)
            install('lsof', prefix.bin)
