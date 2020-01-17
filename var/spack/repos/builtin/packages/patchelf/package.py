# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import shutil
import tempfile

import llnl.util.tty as tty


class Patchelf(AutotoolsPackage):
    """PatchELF is a small utility to modify the dynamic linker and RPATH of
       ELF executables."""

    homepage = "https://nixos.org/patchelf.html"
    url      = "https://nixos.org/releases/patchelf/patchelf-0.10/patchelf-0.10.tar.gz"
    list_url = "https://nixos.org/releases/patchelf/"
    list_depth = 1

    version('0.10', sha256='b2deabce05c34ce98558c0efb965f209de592197b2c88e930298d740ead09019')
    version('0.9',  sha256='f2aa40a6148cb3b0ca807a1bf836b081793e55ec9e5540a5356d800132be7e0a')
    version('0.8',  sha256='14af06a2da688d577d64ff8dac065bb8903bbffbe01d30c62df7af9bf4ce72fe')

    def _setup_hello(self):
        src = os.path.join(os.path.dirname(__file__), 'test', 'hello')
        testdir = tempfile.mkdtemp()
        dest = os.path.join(testdir, 'hello')
        shutil.copy(src, dest)
        return dest

    def test(self):
        patchelf = which('patchelf')
        assert patchelf is not None

        tty.msg('\nChecking version')
        output = patchelf('--version', output=str.split, error=str.split)
        assert output.strip() == 'patchelf {0}'.format(self.spec.version)

        tty.msg('\nEnsuring an rpath is changed')
        hello = self._setup_hello()
        new_rpath = os.getcwd()
        patchelf('--set-rpath', new_rpath, hello)
        output = patchelf('--print-rpath', hello,
                          output=str.split, error=str.split)
        assert output.strip() == new_rpath

        # Now cleanup
        shutil.rmtree(os.path.dirname(hello))
