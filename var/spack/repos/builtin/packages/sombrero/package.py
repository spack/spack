# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import join_path

from spack import *


class Sombrero(MakefilePackage):
    "A next-generation conjugate gradient benchmark from computational particle physics"

    homepage = "https://github.com/sa2c/sombrero"
    url = "https://github.com/sa2c/sombrero/archive/refs/tags/1.0.tar.gz"

    version('2021-07-08',
            sha256='816b0f0a684a421fa620f11c21649ac162e85d1febd6a7e10cfd07604760c0d6')

    # Version 1 is incompatible with spack
    # as CFLAGS and the like are hardcoded in the makefile.
    version('1.0',
            sha256='423a631c86f0e5f14dea186228871099ca0374dc07bf1bb24b6be17f79784682',
            deprecated=True)

    depends_on('mpi')

    maintainers = ['mmesiti', 'edbennett']

    def edit(self, spec, prefix):
        # Make the `sombrero.sh` driver relocatable
        sombrero_sh = FileFilter(
            join_path(self.stage.source_path, 'sombrero.sh'))
        sombrero_dir = join_path(prefix.bin, 'sombrero')
        sombrero_sh.filter('sombrero/', '{0}/'.format(sombrero_dir))

    def install(self, spec, prefix):
        sombrero_dir = join_path(prefix.bin, 'sombrero')
        mkdirp(sombrero_dir)
        # Install the shell driver
        install('sombrero.sh', prefix.bin)
        # Install all executables
        for i in range(1, 7):
            install(join_path('sombrero', 'sombrero{0}'.format(i)),
                    sombrero_dir)
