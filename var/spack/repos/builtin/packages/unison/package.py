# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unison(Package):
    """Unison is a file-synchronization tool for OSX, Unix, and
       Windows. It allows two replicas of a collection of files and
       directories to be stored on different hosts (or different disks
       on the same host), modified separately, and then brought up to
       date by propagating the changes in each replica to the
       other."""

    homepage = "https://www.cis.upenn.edu/~bcpierce/unison/"
    url      = "https://www.seas.upenn.edu/~bcpierce/unison//download/releases/stable/unison-2.48.4.tar.gz"

    version('2.48.4', sha256='30aa53cd671d673580104f04be3cf81ac1e20a2e8baaf7274498739d59e99de8')

    depends_on('ocaml', type='build')

    parallel = False

    def install(self, spec, prefix):
        make('./mkProjectInfo')
        make('UISTYLE=text')

        mkdirp(prefix.bin)
        install('unison', prefix.bin)
        set_executable(join_path(prefix.bin, 'unison'))
