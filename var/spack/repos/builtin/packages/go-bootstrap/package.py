##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os
import shutil
import glob
from spack import *

# THIS PACKAGE SHOULD NOT EXIST
# it exists to make up for the inability to:
# * use an external go compiler
# * have go depend on itself
# * have a sensible way to find gccgo without a dep on gcc


class GoBootstrap(Package):
    """Old C-bootstrapped go to bootstrap real go"""
    homepage = "https://golang.org"
    url = "https://go.googlesource.com/go"

    extendable = True

    # NOTE: Go@1.4.x is the only supported bootstrapping compiler because all
    # later versions require a Go compiler to build.
    # See: https://golang.org/doc/install/source#go14 and
    # https://github.com/golang/go/issues/17545 and
    # https://github.com/golang/go/issues/16352
    version('1.4-bootstrap-20161024', '76e42c8152e8560ded880a6d1d1f53cb',
            url='https://storage.googleapis.com/golang/go1.4-bootstrap-20161024.tar.gz')

    variant('test', default=True, description='Build and run tests as part of the build.')

    provides('golang@:1.4-bootstrap-20161024')

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

    @when('@1.5.0:')
    def patch(self):
        pass

    def install(self, spec, prefix):
        env['CGO_ENABLED'] = '0'
        bash = which('bash')
        with working_dir('src'):
            bash('{0}.bash'.format('all' if '+test' in spec else 'make'))

        try:
            os.makedirs(prefix)
        except OSError:
            pass
        for f in glob.glob('*'):
            if os.path.isdir(f):
                shutil.copytree(f, os.path.join(prefix, f))
            else:
                shutil.copy2(f, os.path.join(prefix, f))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('GOROOT_BOOTSTRAP', self.spec.prefix)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GOROOT_FINAL', self.spec.prefix)
