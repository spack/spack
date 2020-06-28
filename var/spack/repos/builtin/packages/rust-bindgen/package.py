# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RustBindgen(CargoPackage):
    """bindgen automatically generates Rust FFI bindings to C (and some C++)
    libraries."""

    homepage = "https://rust-lang.github.io/rust-bindgen/"
    crates_io = "bindgen"
    git = "https://github.com/rust-lang/rust-bindgen.git"

    maintainers = ['AndrewGaspar']

    depends_on('llvm@6.0:', type=('build', 'run'))

    # rust-bindgen has a dependency on libclang - add path
    def setup_build_environment(self, env):
        env.append_flags(
            'LLVM_CONFIG_PATH',
            join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))

    version('master', branch='master')
    version('0.54.0', sha256='66c0bb6167449588ff70803f4127f0684f9063097eca5016f37eb52b92c2cf36')
