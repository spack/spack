# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Infernal(AutotoolsPackage):
    """Infernal (INFERence of RNA ALignment) is for searching DNA sequence
       databases for RNA structure and sequence similarities. It is an
       implementation of a special case of profile stochastic context-free
       grammars called covariance models (CMs)."""

    homepage = "http://eddylab.org/infernal/"
    url      = "http://eddylab.org/infernal/infernal-1.1.2.tar.gz"

    version('1.1.2', 'a73e6bbab0c4b79af2cc4c0aabb8accc')

    variant('mpi', default=False, description='Enable MPI parallel support')

    depends_on('mpi', when='+mpi')

    def configure_args(self):
        args = []
        if '+mpi' in self.spec:
            args.append('--enable-mpi')
        else:
            args.append('--disable-mpi')
        return args
