from spack import *
import os


class RustBindgen(Package):
    """The rust programming language toolchain"""
    homepage = "http://www.rust-lang.org"
    url = "https://github.com/crabtw/rust-bindgen"

    version('0.16', tag='0.16', git='https://github.com/crabtw/rust-bindgen')

    extends("rust")
    depends_on("llvm")

    def install(self, spec, prefix):
        env = dict(os.environ)
        env['LIBCLANG_PATH'] = os.path.join(spec['llvm'].prefix, 'lib')
        cargo('install', '--root', prefix, env=env)
