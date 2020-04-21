# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from copy import deepcopy
import inspect
import json
import spack

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir, join_path, copy
from spack.directives import cargo_manifest, depends_on, variant
from spack.package import PackageBase
from spack.util.executable import Executable


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

    depends_on('rust', type='build')

    cargo_manifest()

    @property
    def cargo(self):
        cargo = Executable(join_path(self.spec['rust'].prefix.bin, 'cargo'))
        cargo.add_default_arg('--locked')
        cargo.add_default_arg('--offline')
        return cargo

    @property
    def cargo_build(self):
        jobs = spack.config.get('config:build_jobs') if self.parallel else 1

        cargo_build = self.cargo
        cargo_build.add_default_arg('build')
        cargo_build.add_default_arg('--jobs')
        cargo_build.add_default_arg(str(jobs))
        cargo_build.add_default_arg('-vv') # Very verbose output
        cargo_build.add_default_arg('--manifest-path')
        cargo_build.add_default_arg(self.manifest_path)
        if 'build_type=release' in self.spec:
            cargo_build.add_default_arg('--release')

        cargo_build.add_default_env(
            'RUSTFLAGS',
            '--codegen rpath \
             --cap-lints warn'
        )
        return cargo_build

    @property
    def manifest_path(self):
        return join_path(self.stage.source_path, self.cargo_manifest)

    @property
    def metadata(self):
        """Returns the metadata description of the crate.
        
        Used to determine the installable targets in the crate"""
        return json.loads(inspect.getmodule(self).cargo(
            'metadata', '--manifest-path', self.manifest_path,
            '--format-version', '1',
            output=str))

    @property
    def target_path(self):
        return join_path(
            self.stage.source_path, 'target', self.spec.variants['build_type'].value)

    def build(self, spec, prefix):
        """cargo build"""
        self.cargo_build()

    def install(self, spec, prefix):
        """Install cargo targets"""
        # This is not implemented using "cargo install" because we want to
        # install libraries, too.
        metadata = self.metadata

        so_ext = 'dylib' if 'platform=darwin' in self.spec else 'so'

        # This loop attempts to install all
        for p in metadata["packages"]:
            for w in metadata["workspace_members"]:
                if p["id"] == w:
                    for t in p["targets"]:
                        if "bin" in t["kind"]:
                            mkdirp(prefix.bin)
                            copy(
                                join_path(self.target_path, t["name"]),
                                prefix.bin
                            )

                        if "staticlib" in t["kind"]:
                            mkdirp(prefix.lib)
                            copy(
                                "lib{0}.a".format(
                                    join_path(self.target_path, t["name"])
                                ),
                                prefix.lib
                            )

                        if "cdylib" in t["kind"]:
                            mkdirp(prefix.lib)
                            copy(
                                "lib{0}.{1}".format(
                                    join_path(self.target_path, t["name"]),
                                    so_ext
                                ),
                                prefix.lib
                            )
