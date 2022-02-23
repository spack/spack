# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class PyDocutils(PythonPackage):
    """Docutils is an open-source text processing system for processing
    plaintext documentation into useful formats, such as HTML, LaTeX,
    man-pages, open-document or XML. It includes reStructuredText, the
    easy to read, easy to use, what-you-see-is-what-you-get plaintext
    markup language."""

    homepage = "http://docutils.sourceforge.net/"
    pypi = "docutils/docutils-0.15.2.tar.gz"

    version('0.18.1', sha256='679987caf361a7539d76e584cbeddc311e3aee937877c87346f31debc63e9d06')
    version('0.18',   sha256='c1d5dab2b11d16397406a282e53953fe495a46d69ae329f55aa98a5c4e3c5fbb')
    version('0.17.1', sha256='686577d2e4c32380bb50cbb22f575ed742d58168cee37e99117a854bcd88f125')
    version('0.17',   sha256='e2ffeea817964356ba4470efba7c2f42b6b0de0b04e66378507e3e2504bbff4c')
    version('0.15.2', sha256='a2aeea129088da402665e92e0b25b04b073c04b2dce4ab65caaa38b7ce2e1a99')
    version('0.14',   sha256='51e64ef2ebfb29cae1faa133b3710143496eca21c530f3f71424d77687764274')
    version('0.13.1', sha256='718c0f5fb677be0f34b781e04241c4067cbd9327b66bdd8e763201130f5175be')
    version('0.12',   sha256='c7db717810ab6965f66c8cf0398a98c9d8df982da39b4cd7f162911eb89596fa')

    depends_on('py-setuptools',       when='@0.15:',         type='build')
    depends_on('python@2.7:2.8,3.5:', when='@0.16:',         type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', when='@0.14:0.15',     type=('build', 'run'))
    depends_on('python@2.4:',         when='@:0.13',     type=('build', 'run'))

    # NOTE: This creates symbolic links to be able to run docutils scripts
    # without .py file extension similarly to various linux distributions to
    # increase compatibility with other packages
    @run_after('install')
    def post_install(self):
        bin_path = self.prefix.bin
        for file in os.listdir(bin_path):
            if file.endswith(".py"):
                os.symlink(os.path.join(bin_path, file),
                           os.path.join(bin_path, file[:-3]))
