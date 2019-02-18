# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Flit(MakefilePackage):
    """Floating-point Litmus Tests (FLiT) is a C++ test infrastructure for
    detecting variability in floating-point code caused by variations in
    compiler code generation, hardware and execution environments."""

    homepage = "https://pruners.github.io/flit"
    url      = "https://github.com/PRUNERS/FLiT"
    url      = "https://github.com/PRUNERS/FLiT/archive/v2.0-alpha.1.tar.gz"

    version('2.0-alpha.1', '62cf7784bcdc15b962c813b11e478159')
    # FIXME: fix install and build to handle the old version, which is not
    #        installable
    # version('1.0.0',       '27763c89b044c5e3cfe62dd319a36a2b')
    conflicts("@:1.999", msg="Only can build version 2.0 and up")

    # Add dependencies
    depends_on('python@3:', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib tk=False', type='run')
    depends_on('py-toml', type='run')

    @property
    def install_targets(self):
        return ['install', 'PREFIX=%s' % self.prefix]
