# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Munge(AutotoolsPackage):
    """ MUNGE Uid 'N' Gid Emporium """
    homepage = "https://code.google.com/p/munge/"
    url      = "https://github.com/dun/munge/releases/download/munge-0.5.13/munge-0.5.13.tar.xz"
    version('0.5.13', '9204f34aac7f0cc50880196f4a8f5f33')
    version('0.5.12', '84ffef069af93caea4b4c06f183b99c0')
    version('0.5.11', 'bd8fca8d5f4c1fcbef1816482d49ee01',
            url='https://github.com/dun/munge/releases/download/munge-0.5.11/munge-0.5.11.tar.bz2')

    depends_on('openssl')
    depends_on('libgcrypt')

    def install(self, spec, prefix):
        os.makedirs(os.path.join(prefix, "lib/systemd/system"))
        super(Munge, self).install(spec, prefix)
