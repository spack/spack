# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect

from llnl.util.filesystem import working_dir
from spack.directives import cargo_manifest, variant
from spack.package import PackageBase


class CargoPackage(PackageBase):
    """
    Specialized class for installing packages that use the Cargo package
    manager.
    
    Cargo is the official build tool and package manager of the Rust
    programming language. It has its own package repository, which this
    class will automatically pull from while ensuring checksums are respected.

    This package can install both executable files and C-style static and
    dynamic libraries from a cargo package. It can not install native Rust-style
    libraries.
    """

    phases = ['build', 'install']

    build_system_class = 'CargoPackage'

    variant('build_type',
            default='release',
            description='Cargo build type',
            values=('debug', 'release'))

    cargo_manifest()

    def build(self, spec, prefix):
        """cargo build"""
        with working_dir(self.stage.source_path):
            if 'build_type=debug' in self.spec:
                inspect.getmodule(self).cargo_build()
            else:
                inspect.getmodule(self).cargo_build('--release')

    def install(self, spec, prefix):
        """Install cargo targets"""
        pass
