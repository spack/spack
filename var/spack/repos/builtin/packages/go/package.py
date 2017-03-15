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
    url = 'https://storage.googleapis.com/golang/go1.7.4.src.tar.gz'

    extendable = True

    version('1.8',   '7743960c968760437b6e39093cfe6f67')
    version('1.7.5', '506de2d870409e9003e1440bcfeb3a65')
    version('1.7.4', '49c1076428a5d3b5ad7ac65233fcca2f')
    version('1.6.4', 'b023240be707b34059d2c114d3465c92')

    variant('test', default=True, description='Build and run tests as part of the build.')

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

    @when('@1.5.0:')
    def patch(self):
        pass

    def url_for_version(self, version):
        return "https://storage.googleapis.com/golang/go{0}.src.tar.gz".format(version)

    def install(self, spec, prefix):
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

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GOROOT_FINAL', self.spec.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to set GOPATH and use go::

        env = os.environ
        env['GOPATH'] = self.source_path + ':' + env['GOPATH']
        go('get', '<package>', env=env)
        shutil.copytree('bin', os.path.join(prefix, '/bin'))
        """
        #  Add a go command/compiler for extensions
        module.go = Executable(join_path(self.spec.prefix.bin, 'go'))

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
