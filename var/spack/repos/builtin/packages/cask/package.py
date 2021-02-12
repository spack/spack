# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Based on Homebrew's formula:
# https://github.com/Homebrew/homebrew-core/blob/master/Formula/cask.rb
#
from spack import *
from glob import glob


class Cask(Package):
    """Cask is a project management tool for Emacs Lisp to automate the package
       development cycle; development, dependencies, testing, building,
       packaging and more."""
    homepage = "http://cask.readthedocs.io/en/latest/"
    url      = "https://github.com/cask/cask/archive/v0.7.4.tar.gz"

    version('0.8.5', sha256='b7a6bda663d5a83a99036287cd9362d131ae3a0e0525a48b50eb194684e4447d')
    version('0.8.4', sha256='02f8bb20b33b23fb11e7d2a1d282519dfdb8b3090b9672448b8c2c2cacd3e478')
    version('0.8.3', sha256='71bafe94b7ea08b0f9075df2cb3cc2063a00c88e64fb1bf7073ae1b5fa2560cc')
    version('0.8.2', sha256='16b1054af3f58cf95b72f2d10e03450f550311774c7f16b918e3f29ecc7fcd13')
    version('0.8.1', sha256='8739ba608f23c79b3426faa8b068d5d1bc096c7305ce30b1163babd354be821c')
    # version 0.8.0 is broken
    version('0.7.4', sha256='b183ea1c50fc215c9040f402b758ecc335901fbc2c3afd4a7302386c888d437d')

    depends_on('emacs', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bin/cask', prefix.bin)
        install_tree('templates', join_path(prefix, 'templates'))
        for el_file in glob("*.el"):
            install(el_file, prefix)
        for misc_file in ['COPYING', 'cask.png', 'README.md']:
            install(misc_file, prefix)
        # disable cask's automatic upgrading feature
        touch(join_path(prefix, ".no-upgrade"))
