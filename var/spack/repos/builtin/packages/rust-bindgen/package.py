# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class RustBindgen(Package):
    """The rust programming language toolchain"""
    homepage = "http://www.rust-lang.org"
    url = "https://github.com/servo/rust-bindgen/archive/v0.20.5.tar.gz"

    version('0.20.5', '3e4d70a5bec540324fdd95bc9e82bebc')

    extends("rust")
    depends_on("llvm")

    def install(self, spec, prefix):
        env = dict(os.environ)
        env['LIBCLANG_PATH'] = os.path.join(spec['llvm'].prefix, 'lib')
        cargo('install', '--root', prefix, env=env)
