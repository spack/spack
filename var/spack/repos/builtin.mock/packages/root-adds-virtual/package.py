# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class RootAddsVirtual(Package):
    version('1.0', sha256='abcde')

    depends_on('middle-adds-virtual')
