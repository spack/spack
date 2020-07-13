# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zsh(AutotoolsPackage):
    """Zsh is a shell designed for interactive use, although it is also a
    powerful scripting language. Many of the useful features of bash, ksh, and
    tcsh were incorporated into zsh; many original features were added.
    """

    homepage = "http://www.zsh.org"
    url = "http://downloads.sourceforge.net/project/zsh/zsh/5.4.2/zsh-5.4.2.tar.xz"

    version('5.8', sha256='dcc4b54cc5565670a65581760261c163d720991f0d06486da61f8d839b52de27')
    version('5.7.1', sha256='7260292c2c1d483b2d50febfa5055176bd512b32a8833b116177bf5f01e77ee8')
    version('5.6.2', sha256='a50bd66c0557e8eca3b8fa24e85d0de533e775d7a22df042da90488623752e9e')
    version('5.4.2', sha256='957bcdb2c57f64c02f673693ea5a7518ef24b6557aeb3a4ce222cefa6d74acc9')
    version('5.3.1', sha256='3d94a590ff3c562ecf387da78ac356d6bea79b050a9ef81e3ecb9f8ee513040e')
    version('5.1.1', sha256='94ed5b412023761bc8d2f03c173f13d625e06e5d6f0dff2c7a6e140c3fa55087')

    # Testing for terminal related things causes failures in e.g. Jenkins.
    # See e.g. https://www.zsh.org/mla/users/2003/msg00845.html,
    # although the name of the option has evolved since then.
    variant('skip-tcsetpgrp-test', default=True,
            description="Skip configure's tcsetpgrp test")

    depends_on("pcre")
    depends_on("ncurses")

    def configure_args(self):
        if '+skip-tcsetpgrp-test' in self.spec:
            # assert that we have a functional tcsetpgrp
            args = ['--with-tcsetpgrp']
        else:
            # let configure run it's test and see what's what
            args = []

        return args
