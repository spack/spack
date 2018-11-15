# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    url      = "https://mirrors.sonic.net/pub/OpenBSD/OpenSSH/portable/openssh-7.6p1.tar.gz"

    version('7.9p1',   '6b4b3ba2253d84ed3771c8050728d597c91cfce898713beb7b64a305b6f11aad')
    version('7.6p1',   '06a88699018e5fef13d4655abfed1f63')
    version('7.5p1',   '652fdc7d8392f112bef11cacf7e69e23')
    version('7.4p1',   'b2db2a83caf66a208bb78d6d287cdaa3')
    version('7.3p1',   'dfadd9f035d38ce5d58a3bf130b86d08')
    version('7.2p2',   '13009a9156510d8f27e752659075cced')
    version('7.1p2',   '4d8547670e2a220d5ef805ad9e47acf2')
    version('7.0p1',   '831883f251ac34f0ab9c812acc24ee69')
    version('6.9p1',   '0b161c44fc31fbc6b76a6f8ae639f16f')
    version('6.8p1',   '08f72de6751acfbd0892b5f003922701')
    version('6.7p1',   '3246aa79317b1d23cae783a3bf8275d6')
    version('6.6p1',   '3e9800e6bca1fbac0eea4d41baa7f239')

    depends_on('openssl@:1.0', when='@:7.7p1')
    depends_on('openssl')
    depends_on('libedit')
    depends_on('ncurses')
    depends_on('zlib')

    def configure_args(self):
        # OpenSSH's privilege separation path defaults to /var/empty. At
        # least newer versions want to create the directory during the
        # install step and fail if they cannot do so.
        args = ['--with-privsep-path={0}'.format(self.prefix.var.empty)]
        return args
