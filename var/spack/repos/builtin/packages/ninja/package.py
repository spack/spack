from spack import *
import os

class Ninja(Package):
    """ A small, fast Make alternative """
    homepage = "https://martine.github.io/ninja/"
    url      = "https://github.com/martine/ninja/archive/v1.6.0.tar.gz"

    version('1.6.0', '254133059f2da79d8727f654d7198f43')

    extends('python')

    def install(self, spec, prefix):
        sh = which('sh')
        python('configure.py', '--bootstrap')

        cp = which('cp')

        bindir = os.path.join(prefix, 'bin/')
        mkdir(bindir)
        cp('-a', 'ninja', bindir)
        cp('-a', 'misc', prefix)
