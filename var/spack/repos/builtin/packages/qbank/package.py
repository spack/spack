##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Qbank(Package):
    """QBank is a unique dynamic reservation-based allocation management system
    that manages the utilization of computational resources in a multi-project
    environment. It is used in conjunction with a resource management system
    allowing an organization to guarantee greater fairness and enforce mission
    priorities by associating a charge with the use of computational resources
    and allocating resource credits which limit how much of the resources may
    be used at what time and by whom. It tracks resource utilization and allows
    for insightful planning."""

    # QBank is so old that it no longer has (never had?) a homepage
    # but it was developed at Pacific Northwest National Laboratory
    # by Scott Jackson <Scott.Jackson@pnl.gov>
    homepage = "http://www.pnnl.gov/"
    url      = "file://{0}/qbank-2.10.4.tar.gz".format(os.getcwd())

    version('2.10.4', '0820587353e63d32ddb49689dd4289e7')

    variant('doc', default=False, description='Build documentation')

    depends_on('openssl')

    depends_on('perl@5.6:5.16',  type=('build', 'run'))
    depends_on('perl-dbi@1.00:', type=('build', 'run'))

    phases = ['configure', 'build', 'install']

    def configure_args(self):
        prefix = self.prefix

        config_args = [
            '--prefix', prefix,
            '--logdir', join_path(prefix, 'var', 'log', 'qbank')
        ]

        return config_args

    def configure(self, spec, prefix):
        perl = which('perl')
        perl('configure', *self.configure_args())

    def build(self, spec, prefix):
        make()

        if '+doc' in spec:
            make('docs')

    def install(self, spec, prefix):
        make('install')

        if '+doc' in spec:
            install_tree('doc', join_path(prefix, 'doc'))

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        prefix = self.prefix

        if '+doc' in spec:
            run_env.prepend_path('MANPATH', join_path(prefix, 'doc'))
