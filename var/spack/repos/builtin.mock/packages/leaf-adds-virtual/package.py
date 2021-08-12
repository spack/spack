# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class LeafAddsVirtual(Package):
    version('2.0', sha256='abcde')
    version('1.0', sha256='abcde')

    depends_on('blas', when='@2.0')
