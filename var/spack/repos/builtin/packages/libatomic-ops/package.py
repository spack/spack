# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibatomicOps(AutotoolsPackage):
    """This package provides semi-portable access to hardware-provided
    atomic memory update operations on a number architectures."""

    homepage = "https://www.hboehm.info/gc/"
    url      = "https://www.hboehm.info/gc/gc_source/libatomic_ops-7.6.6.tar.gz"

    version('7.6.10', sha256='587edf60817f56daf1e1ab38a4b3c729b8e846ff67b4f62a6157183708f099af')
    version('7.6.8',  sha256='1d6a279edf81767e74d2ad2c9fce09459bc65f12c6525a40b0cb3e53c089f665')
    version('7.6.6', sha256='99feabc5f54877f314db4fadeb109f0b3e1d1a54afb6b4b3dfba1e707e38e074')
    version('7.4.4', sha256='bf210a600dd1becbf7936dd2914cf5f5d3356046904848dcfd27d0c8b12b6f8f')

    def configure_args(self):
        return ['--enable-shared']
