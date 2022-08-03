# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Podman(Package):
    """An optionally rootless and daemonless container engine: alias docker=podman"""

    homepage    = 'https://podman.io'
    url         = 'https://github.com/containers/podman/archive/v3.4.2.tar.gz'
    maintainers = ['bernhardkaindl']

    version('3.4.2', sha256='b0c4f9a11eb500b1d440d5e51a6c0c632aa4ac458e2dc0362f50f999eb7fbf31')

    depends_on('go',          type='build')
    depends_on('go-md2man',   type='build')
    depends_on('pkgconfig',   type='build')
    depends_on('cni-plugins', type='run')
    depends_on('conmon',      type='run')
    depends_on('runc',        type='run')
    depends_on('slirp4netns', type='run')
    depends_on('gpgme')
    depends_on('libassuan')
    depends_on('libgpg-error')
    depends_on('libseccomp')

    def patch(self):
        defs = FileFilter('vendor/github.com/containers/common/pkg/config/default.go')

        # Prepend the provided runc executable to podman's built-in runc search path
        defs.filter(
            '"runc": {',
            '"runc": {' + '"{0}",'.format(self.spec['runc'].prefix.sbin.runc)
        )
        # Prepend the provided conmon executable to podman's built-in conmon search path
        defs.filter(
            r'ConmonPath = \[\]string{',
            'ConmonPath = []string{' +
            '\n        "{0}",'.format(self.spec['conmon'].prefix.bin.conmon)
        )
        # Prepend the provided cni-plugins directory to the cni-plugin search path
        defs.filter(
            r'DefaultCNIPluginDirs = \[\]string{',
            'DefaultCNIPluginDirs = []string{' +
            '\n        "{0}",'.format(self.spec['cni-plugins'].prefix.bin)
        )
        # Set the default path for slirp4netns to the provided slirp4netns executable
        defs.filter(
            'cniConfig := _cniConfigDir',
            'cniConfig := _cniConfigDir' +
            '\n        defaultEngineConfig.NetworkCmdPath = "{0}"'.format(
                self.spec['slirp4netns'].prefix.bin.slirp4netns
            )
        )
        # Use the podman install prefix as fallback path for finding container.conf
        filter_file(
            r'/usr',
            self.prefix,
            'vendor/github.com/containers/common/pkg/config/config.go',
        )

    def install(self, spec, prefix):
        # Set default policy.json to be located in the install prefix (documented)
        env['EXTRA_LDFLAGS'] = (
            '-X github.com/containers/image/v5/signature.systemDefaultPolicyPath=' +
            prefix + '/etc/containers/policy.json'
        )
        # Build and installation needs to be in two separate make calls
        # The devicemapper and btrfs drivers are (so far) not enabled in this recipe
        tags = 'seccomp exclude_graphdriver_devicemapper exclude_graphdriver_btrfs'
        make('-e', 'BUILDTAGS=' + tags)
        make('install', 'PREFIX=' + prefix)
        # Install an initial etc/containers/policy.json (configured in prefix above)
        mkdirp(prefix.etc.containers)
        install('test/policy.json', prefix.etc.containers)
        # Cleanup directory trees which are created as part of the go build process
        remove_linked_tree(prefix.src)
        remove_linked_tree(prefix.pkg)
