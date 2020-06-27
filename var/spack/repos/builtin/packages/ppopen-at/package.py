# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class PpopenAt(MakefilePackage):
    """ppOpen-AT is a part of the ppOpenHPC"""

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    url = "file://{0}/ppohAT_1.0.0.tar.gz".format(os.getcwd())

    version('1.0.0', sha256='2b5664839762c941e0b2dd7c15416e2dcfd5d909558cf7e4347a79ce535f3887')

    def edit(self, spec, prefix):
        makefile_in = FileFilter('Makefile.in')
        makefile_in.filter('gcc', spack_cxx)
        makefile_in.filter('~/ppohAT_1.0.0', prefix)
        makefile_in.filter('mkdir', 'mkdir -p')

    def install(self, spec, prefix):
        make('install')
        install_tree('examples', prefix.examples)
        install_tree('doc', prefix.doc)
