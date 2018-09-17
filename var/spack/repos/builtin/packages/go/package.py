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
import os
import llnl.util.tty as tty
from spack import *

# - vanilla CentOS 7, and possibly other systems, fail a test:
#   TestCloneNEWUSERAndRemapRootDisableSetgroups
#
#   The Fix, discussed here: https://github.com/golang/go/issues/16283
#   is to enable "user_namespace".
#
#   On a Digital Ocean image, this can be achieved by updating
#   `/etc/default/grub` so that the `GRUB_CMDLINE_LINUX` variable
#   includes `user_namespace.enable=1`, re-cooking the grub
#   configuration with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`,
#   and then rebooting.
#
# - on CentOS 7 systems (and possibly others) you need to have the
#   glibc package installed or various static cgo tests fail.
#
# - When building on a *large* machine (144 cores, 1.5TB RAM) I need
#   to run `ulimit -u 8192` to bump up the max number of user processes.
#   Failure to do so results in an explosion in one of the tests and an
#   epic stack trace....


class Go(Package):
    """The golang compiler and build environment"""
    homepage = "https://golang.org"
    url = 'https://dl.google.com/go/go1.10.1.src.tar.gz'

    extendable = True

    version('1.11',   'afc1e12f5fe49a471e3aae7d906c73e9d5b1fdd36d52d72652dde8f6250152fb')
    version('1.10.3', '567b1cc66c9704d1c019c50bef946272e911ec6baf244310f87f4e678be155f2')
    version('1.10.2', '6264609c6b9cd8ed8e02ca84605d727ce1898d74efa79841660b2e3e985a98bd')
    version('1.10.1', '589449ff6c3ccbff1d391d4e7ab5bb5d5643a5a41a04c99315e55c16bbf73ddc')
    version('1.9.5',  'f1c2bb7f32bbd8fa7a19cc1608e0d06582df32ff5f0340967d83fb0017c49fbc')
    version('1.9.2',  '44105c865a1a810464df79233a05a568')
    version('1.9.1',  '27bce1ffb05f4f6bd90d90081e5d4169')
    version('1.9',    'da2d44ea384076efec43ee1f8b7d45d2')
    version('1.8.3',  '64e9380e07bba907e26a00cf5fcbe77e')
    version('1.8.1',  '409dd21e7347dd1ea9efe64a700073cc')
    version('1.8',    '7743960c968760437b6e39093cfe6f67')
    version('1.7.5',  '506de2d870409e9003e1440bcfeb3a65')
    version('1.7.4',  '49c1076428a5d3b5ad7ac65233fcca2f')
    version('1.6.4',  'b023240be707b34059d2c114d3465c92')

    provides('golang')

    depends_on('git', type=('build', 'link', 'run'))
    # TODO: Make non-c self-hosting compilers feasible without backflips
    # should be a dep on external go compiler
    depends_on('go-bootstrap', type='build')

    # https://github.com/golang/go/issues/17545
    patch('time_test.patch', when='@1.6.4:1.7.4')

    # https://github.com/golang/go/issues/17986
    # The fix for this issue has been merged into the 1.8 tree.
    patch('misc-cgo-testcshared.patch', level=0, when='@1.6.4:1.7.5')

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
        bash = which('bash')
        with working_dir('src'):
            bash('{0}.bash'.format('all' if self.run_tests else 'make'))

        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GOROOT_FINAL', self.spec.prefix)
        # We need to set CC/CXX_FOR_TARGET, otherwise cgo will use the
        # internal Spack wrappers and fail.
        spack_env.set('CC_FOR_TARGET', self.compiler.cc)
        spack_env.set('CXX_FOR_TARGET', self.compiler.cxx)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to set GOPATH and use go::

        env['GOPATH'] = self.source_path + ':' + env['GOPATH']
        go('get', '<package>', env=env)
        install_tree('bin', prefix.bin)
        """
        #  Add a go command/compiler for extensions
        module.go = self.spec['go'].command

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if os.environ.get('GOROOT', False):
            tty.warn('GOROOT is set, this is not recommended')

        path_components = []
        # Set GOPATH to include paths of dependencies
        for d in dependent_spec.traverse():
            if d.package.extends(self.spec):
                path_components.append(d.prefix)

        # This *MUST* be first, this is where new code is installed
        spack_env.set('GOPATH', ':'.join(path_components))

        # Allow packages to find this when using module or dotkit
        run_env.prepend_path('GOPATH', ':'.join(
            [dependent_spec.prefix] + path_components))
