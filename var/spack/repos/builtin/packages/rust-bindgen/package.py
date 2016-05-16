from spack import *
import os


class RustBindgen(Package):
    """The rust programming language toolchain"""
    homepage = "http://www.rust-lang.org"
    url = "https://github.com/crabtw/rust-bindgen"

    extends("rust")

    def install(self, spec, prefix):
        cargo('install', '--root', prefix)
