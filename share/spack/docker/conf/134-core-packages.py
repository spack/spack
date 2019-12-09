# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class SpackBootstrap(BundlePackage):
    version('1.0')
    depends_on('gzip')
    depends_on('patch')
    depends_on('sed')
    depends_on('unzip')
