# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibatomicOps(AutotoolsPackage):
    """This package provides semi-portable access to hardware-provided
    atomic memory update operations on a number architectures."""

    homepage = "https://github.com/ivmai/libatomic_ops"
    url      = "http://www.hboehm.info/gc/gc_source/libatomic_ops-7.4.4.tar.gz"

    version('7.4.4', '426d804baae12c372967a6d183e25af2')

    def configure_args(self):
        return ['--enable-shared']
