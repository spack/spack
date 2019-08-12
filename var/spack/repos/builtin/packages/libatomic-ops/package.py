# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibatomicOps(AutotoolsPackage):
    """This package provides semi-portable access to hardware-provided
    atomic memory update operations on a number architectures."""

    homepage = "https://www.hboehm.info/gc/"
    url      = "https://www.hboehm.info/gc/gc_source/libatomic_ops-7.6.6.tar.gz"

    version('7.6.6', sha256='99feabc5f54877f314db4fadeb109f0b3e1d1a54afb6b4b3dfba1e707e38e074')
    version('7.4.4', '426d804baae12c372967a6d183e25af2')

    def configure_args(self):
        return ['--enable-shared']
