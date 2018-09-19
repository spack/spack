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

# THIS PACKAGE SHOULD NOT EXIST
# it exists to make up for the inability to:
# * use an external go compiler
# * have go depend on itself
# * have a sensible way to find gccgo without a dep on gcc


class GoBootstrap(Package):
    """Old C-bootstrapped go to bootstrap real go"""

    homepage = "https://golang.org"

    extendable = True

    # NOTE: Go@1.4.x is the only supported bootstrapping compiler because all
    # later versions require a Go compiler to build.
    # See: https://golang.org/doc/install/source#go14 and
    # https://github.com/golang/go/issues/17545 and
    # https://github.com/golang/go/issues/16352
    version('1.4-bootstrap-20171003', 'dbf727a4b0e365bf88d97cbfde590016',
            url='https://dl.google.com/go/go1.4-bootstrap-20171003.tar.gz')
    version('1.4-bootstrap-20170531', 'd2cc61cb9f829b3510ee39c0c5568014',
            url='https://storage.googleapis.com/golang/go1.4-bootstrap-20170531.tar.gz')
    version('1.4-bootstrap-20161024', '76e42c8152e8560ded880a6d1d1f53cb',
            url='https://storage.googleapis.com/golang/go1.4-bootstrap-20161024.tar.gz')

    provides('golang@:1.4-bootstrap-20171003')

    depends_on('git', type=('build', 'link', 'run'))

    # NOTE: Older versions of Go attempt to download external files that have
    # since been moved while running the test suite.  This patch modifies the
    # test files so that these tests don't cause false failures.
    # See: https://github.com/golang/go/issues/15694
    @when('@:1.4.3')
    def patch(self):
        test_suite_file = FileFilter(join_path('src', 'run.bash'))
        test_suite_file.filter(
            r'^(.*)(\$GOROOT/src/cmd/api/run.go)(.*)$',
            r'# \1\2\3',
        )

    def install(self, spec, prefix):
        env['CGO_ENABLED'] = '0'
        bash = which('bash')
        with working_dir('src'):
            bash('{0}.bash'.format('all' if self.run_tests else 'make'))

        install_tree('.', prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('GOROOT_BOOTSTRAP', self.spec.prefix)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GOROOT_FINAL', self.spec.prefix)
