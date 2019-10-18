# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


def makefile_onoff(option):
    if option:
        return "ON"
    return "OFF"


class Pciutils(MakefilePackage):
    """The PCI Utilities package contains a library for portable access to PCI bus
    configuration registers and several utilities based on this library."""

    homepage = "https://mj.ucw.cz/sw/pciutils/"
    url      = "https://www.kernel.org/pub/software/utils/pciutils/pciutils-3.6.2.tar.xz"

    version('3.6.2', sha256='db452ec986edefd88af0d222d22f6102f8030a8633fdfe846c3ae4bde9bb93f3')

    variant('zlib', default=False, description="Enable zlib support.")
    variant('shared', default=True, description="Build as a shared library.")

    depends_on('zlib', when='+zlib')
    depends_on('curl', type="run")  # when updating database

    def make_options(self):
        spec = self.spec
        return ['PREFIX={}'.format(self.prefix),
                'ZLIB={}'.format(makefile_onoff("+zlib" in spec)),
                'SHARED={}'.format(makefile_onoff("+shared" in spec))]

    @property
    def build_targets(self):
        return self.make_options()

    @property
    def install_targets(self):
        args = self.make_options()
        args.append('install')
        return args
