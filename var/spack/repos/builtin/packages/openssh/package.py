# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import socket

from spack import *


class Openssh(AutotoolsPackage):
    """OpenSSH is the premier connectivity tool for remote login with the
       SSH protocol. It encrypts all traffic to eliminate
       eavesdropping, connection hijacking, and other attacks. In
       addition, OpenSSH provides a large suite of secure tunneling
       capabilities, several authentication methods, and sophisticated
       configuration options.
    """

    homepage = "https://www.openssh.com/"
    url      = "https://mirrors.sonic.net/pub/OpenBSD/OpenSSH/portable/openssh-8.7p1.tar.gz"

    tags = ['core-packages']

    version('8.9p1', sha256='fd497654b7ab1686dac672fb83dfb4ba4096e8b5ffcdaccd262380ae58bec5e7')
    version('8.8p1', sha256='4590890ea9bb9ace4f71ae331785a3a5823232435161960ed5fc86588f331fe9')
    version('8.7p1', sha256='7ca34b8bb24ae9e50f33792b7091b3841d7e1b440ff57bc9fabddf01e2ed1e24')
    version('8.6p1', sha256='c3e6e4da1621762c850d03b47eed1e48dff4cc9608ddeb547202a234df8ed7ae')
    version('8.5p1', sha256='f52f3f41d429aa9918e38cf200af225ccdd8e66f052da572870c89737646ec25')
    version('8.4p1', sha256='5a01d22e407eb1c05ba8a8f7c654d388a13e9f226e4ed33bd38748dafa1d2b24')
    version('8.3p1', sha256='f2befbe0472fe7eb75d23340eb17531cb6b3aac24075e2066b41f814e12387b2')
    version('8.1p1', sha256='02f5dbef3835d0753556f973cd57b4c19b6b1f6cd24c03445e23ac77ca1b93ff')
    version('7.9p1', sha256='6b4b3ba2253d84ed3771c8050728d597c91cfce898713beb7b64a305b6f11aad')
    version('7.6p1', sha256='a323caeeddfe145baaa0db16e98d784b1fbc7dd436a6bf1f479dfd5cd1d21723')
    version('7.5p1', sha256='9846e3c5fab9f0547400b4d2c017992f914222b3fd1f8eee6c7dc6bc5e59f9f0')
    version('7.4p1', sha256='1b1fc4a14e2024293181924ed24872e6f2e06293f3e8926a376b8aec481f19d1')
    version('7.3p1', sha256='3ffb989a6dcaa69594c3b550d4855a5a2e1718ccdde7f5e36387b424220fbecc')
    version('7.2p2', sha256='a72781d1a043876a224ff1b0032daa4094d87565a68528759c1c2cab5482548c')
    version('7.1p2', sha256='dd75f024dcf21e06a0d6421d582690bf987a1f6323e32ad6619392f3bfde6bbd')
    version('7.0p1', sha256='fd5932493a19f4c81153d812ee4e042b49bbd3b759ab3d9344abecc2bc1485e5')
    version('6.9p1', sha256='6e074df538f357d440be6cf93dc581a21f22d39e236f217fcd8eacbb6c896cfe')
    version('6.8p1', sha256='3ff64ce73ee124480b5bf767b9830d7d3c03bbcb6abe716b78f0192c37ce160e')
    version('6.7p1', sha256='b2f8394eae858dabbdef7dac10b99aec00c95462753e80342e530bbb6f725507')
    version('6.6p1', sha256='48c1f0664b4534875038004cc4f3555b8329c2a81c1df48db5c517800de203bb')

    depends_on('openssl@:1.0', when='@:7.7p1')
    depends_on('openssl')
    depends_on('libedit')
    depends_on('ncurses')
    depends_on('zlib')
    depends_on('py-twisted', type='test')

    maintainers = ['bernhardkaindl']
    executables = ['^ssh$', '^scp$', '^sftp$', '^ssh-add$', '^ssh-agent$',
                   '^ssh-keygen$', '^ssh-keyscan$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('-V', output=str, error=str).rstrip()
        match = re.search(r'OpenSSH_([^, ]+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        # OpenSSH's privilege separation path defaults to /var/empty. At
        # least newer versions want to create the directory during the
        # install step and fail if they cannot do so.
        args = ['--with-privsep-path={0}'.format(self.prefix.var.empty)]

        # Somehow creating pie executables fails with nvhpc, not with gcc.
        if '%nvhpc' in self.spec:
            args.append('--without-pie')
        return args

    def install(self, spec, prefix):
        """Install generates etc/sshd_config, but it fails in parallel mode"""
        make('install', parallel=False)

    def setup_build_environment(self, env):
        """Until spack supports a real implementation of setup_test_environment()"""
        if self.run_tests:
            self.setup_test_environment(env)

    def setup_test_environment(self, env):
        """Configure the regression test suite like Debian's openssh-tests package"""
        p = self.prefix
        j = join_path
        env.set('TEST_SSH_SSH', p.bin.ssh)
        env.set('TEST_SSH_SCP', p.bin.scp)
        env.set('TEST_SSH_SFTP', p.bin.sftp)
        env.set('TEST_SSH_SK_HELPER', j(p.libexec, 'ssh-sk-helper'))
        env.set('TEST_SSH_SFTPSERVER', j(p.libexec, 'sftp-server'))
        env.set('TEST_SSH_PKCS11_HELPER', j(p.libexec, 'ssh-pkcs11-helper'))
        env.set('TEST_SSH_SSHD', p.sbin.sshd)
        env.set('TEST_SSH_SSHADD', j(p.bin, 'ssh-add'))
        env.set('TEST_SSH_SSHAGENT', j(p.bin, 'ssh-agent'))
        env.set('TEST_SSH_SSHKEYGEN', j(p.bin, 'ssh-keygen'))
        env.set('TEST_SSH_SSHKEYSCAN', j(p.bin, 'ssh-keyscan'))
        env.set('TEST_SSH_UNSAFE_PERMISSIONS', '1')
        # Get a free port for the simple tests and skip the complex tests:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        host, port = tcp.getsockname()
        tcp.close()
        env.set('TEST_SSH_PORT', port)
        env.set('SKIP_LTESTS', 'key-options forward-control forwarding '
                'multiplex addrmatch cfgmatch cfgmatchlisten percent')

    def installcheck(self):
        make('-e', 'tests', parallel=False)
