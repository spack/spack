# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
 
from spack import *
 
 
class Streamstat(CMakePackage):
    """streamstat"""
    homepage = "https://github.com/LLNL/STREAMSTAT"
    git      = "https://github.com/xuanhuang1/STREAMSTAT.git"
    version('main', branch='main')
    
    def cmake_args(self):
           args = []
           # force to shared
           args.append('-DBUILD_SHARED_LIBS=ON')
           return args
