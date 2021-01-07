# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HybridLambda(AutotoolsPackage):
    """Hybrid-Lambda is a software package that can simulate gene trees
       within a rooted species network or a rooted species tree under the
       coalescent process. The main feature of this program is that users can
       choose to use the standard Kingman coalescent process, which produces
       bifurcating genealogies, or two other Lambda coalescent processes,
       which produce multifurcating genealogies. The other feature is that
       hybrid sim uses extended Newick formatted strings to make it easier to
       represent hybridization events between species."""

    homepage = "https://github.com/hybridLambda/hybrid-Lambda"
    #url      = "https://github.com/hybridLambda/hybrid-Lambda/archive/v0.6.3-beta.tar.gz"
    git      = "https://github.com/hybridLambda/hybrid-Lambda.git"

    version('dev', submodules=True)

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('doxygen', type='build')
    depends_on('graphviz', type='build')
    depends_on('boost', type='build')
    depends_on('cppunit', type='build')

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        # args = ['--disable-doxygen-doc', '--disable-doxygen-dot']
        args = []
        return args

    def build(self, spec, prefix):
        with working_dir('src'):
            make

    def install(self, spec, prefix):
        filter_file(r'INSTALL = /bin/install -c',
                    'INSTALL = /bin/install -C', 'Makefile')
        make('install')
