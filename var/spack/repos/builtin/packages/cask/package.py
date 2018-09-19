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

    version('0.8.1', '25196468a7ce634cfff14733678be6ba')
    # version 0.8.0 is broken
    version('0.7.4', 'c973a7db43bc980dd83759a5864a1260')

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
