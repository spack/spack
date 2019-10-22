# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    url = 'https://dl.google.com/go/go1.12.6.src.tar.gz'

    extendable = True

    version('1.13.1', sha256='81f154e69544b9fa92b1475ff5f11e64270260d46e7e36c34aafc8bc96209358')
    version('1.13', sha256='3fc0b8b6101d42efd7da1da3029c0a13f22079c0c37ef9730209d8ec665bf122')
    version('1.12.10', sha256='f56e48fce80646d3c94dcf36d3e3f490f6d541a92070ad409b87b6bbb9da3954')
    version('1.12.9', sha256='ab0e56ed9c4732a653ed22e232652709afbf573e710f56a07f7fdeca578d62fc')
    version('1.12.8', sha256='11ad2e2e31ff63fcf8a2bdffbe9bfa2e1845653358daed593c8c2d03453c9898')
    version('1.12.6', sha256='c96c5ccc7455638ae1a8b7498a030fe653731c8391c5f8e79590bce72f92b4ca')
    version('1.12.5', sha256='2aa5f088cbb332e73fc3def546800616b38d3bfe6b8713b8a6404060f22503e8')
    version('1.11.13', sha256='5032095fd3f641cafcce164f551e5ae873785ce7b07ca7c143aecd18f7ba4076')
    version('1.11.11', sha256='1fff7c33ef2522e6dfaf6ab96ec4c2a8b76d018aae6fc88ce2bd40f2202d0f8c')
    version('1.11.10', sha256='df27e96a9d1d362c46ecd975f1faa56b8c300f5c529074e9ea79bdd885493c1b')
    version('1.11.5', sha256='bc1ef02bb1668835db1390a2e478dcbccb5dd16911691af9d75184bbe5aa943e')
    version('1.11.4', sha256='4cfd42720a6b1e79a8024895fa6607b69972e8e32446df76d6ce79801bbadb15')
    version('1.11.2', sha256='042fba357210816160341f1002440550e952eb12678f7c9e7e9d389437942550')
    version('1.11.1', sha256='558f8c169ae215e25b81421596e8de7572bd3ba824b79add22fba6e284db1117')
    version('1.11',   sha256='afc1e12f5fe49a471e3aae7d906c73e9d5b1fdd36d52d72652dde8f6250152fb')
    version('1.10.3', sha256='567b1cc66c9704d1c019c50bef946272e911ec6baf244310f87f4e678be155f2')
    version('1.10.2', sha256='6264609c6b9cd8ed8e02ca84605d727ce1898d74efa79841660b2e3e985a98bd')
    version('1.10.1', sha256='589449ff6c3ccbff1d391d4e7ab5bb5d5643a5a41a04c99315e55c16bbf73ddc')
    version('1.9.5',  sha256='f1c2bb7f32bbd8fa7a19cc1608e0d06582df32ff5f0340967d83fb0017c49fbc')
    version('1.9.2',  sha256='665f184bf8ac89986cfd5a4460736976f60b57df6b320ad71ad4cef53bb143dc')
    version('1.9.1',  sha256='a84afc9dc7d64fe0fa84d4d735e2ece23831a22117b50dafc75c1484f1cb550e')
    version('1.9',    sha256='a4ab229028ed167ba1986825751463605264e44868362ca8e7accc8be057e993')
    version('1.8.3',  sha256='5f5dea2447e7dcfdc50fa6b94c512e58bfba5673c039259fd843f68829d99fa6')
    version('1.8.1',  sha256='33daf4c03f86120fdfdc66bddf6bfff4661c7ca11c5da473e537f4d69b470e57')
    version('1.8',    sha256='406865f587b44be7092f206d73fc1de252600b79b3cacc587b74b5ef5c623596')
    version('1.7.5',  sha256='4e834513a2079f8cbbd357502cccaac9507fd00a1efe672375798858ff291815')
    version('1.7.4',  sha256='4c189111e9ba651a2bb3ee868aa881fab36b2f2da3409e80885ca758a6b614cc')
    version('1.6.4',  sha256='8796cc48217b59595832aa9de6db45f58706dae68c9c7fbbd78c9fdbe3cd9032')

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

        wd = '.'

        # 1.11.5 directory structure is slightly different
        if self.version == Version('1.11.5'):
            wd = 'go'

        with working_dir(join_path(wd, 'src')):
            bash('{0}.bash'.format('all' if self.run_tests else 'make'))

        install_tree(wd, prefix)

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

        # Allow packages to find this when using module files
        run_env.prepend_path('GOPATH', ':'.join(
            [dependent_spec.prefix] + path_components))
