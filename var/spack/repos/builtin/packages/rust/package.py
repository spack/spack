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
from spack import *
import os


def get_submodules():
    git = which('git')
    git('submodule', 'update', '--init', '--recursive')


class Rust(Package):
    """The rust programming language toolchain"""
    homepage = "http://www.rust-lang.org"
    url = "https://github.com/rust-lang/rust"

    version('1.8.0', tag='1.8.0', git="https://github.com/rust-lang/rust")

    resource(name='cargo',
             git="https://github.com/rust-lang/cargo.git",
             tag='0.10.0',
             destination='cargo')

    extendable = True

    # Rust
    depends_on("llvm")
    depends_on("curl")
    depends_on("git")
    depends_on("cmake")
    depends_on("python@:2.8")

    # Cargo
    depends_on("openssl")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--llvm-root=' + spec['llvm'].prefix)

        make()
        make("install")

        # Install cargo, rust package manager
        with working_dir(os.path.join('cargo', 'cargo')):
            get_submodules()
            configure('--prefix=' + prefix,
                      '--local-rust-root=' + prefix)

            make()
            make("install")

    def setup_dependent_package(self, module, dependent_spec):
        """
        Called before python modules' install() methods.

        In most cases, extensions will only need to have one or two lines::

            cargo('build')
            cargo('install', '--root', prefix)

        or

            cargo('install', '--root', prefix)
        """
        # Rust extension builds can have a global cargo executable function
        module.cargo = Executable(join_path(self.spec.prefix.bin, 'cargo'))
