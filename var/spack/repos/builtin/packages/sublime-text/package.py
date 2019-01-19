# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SublimeText(Package):
    """Sublime Text is a sophisticated text editor for code, markup and
    prose."""

    homepage = "http://www.sublimetext.com/"
    url      = "https://download.sublimetext.com/sublime_text_3_build_3176_x64.tar.bz2"

    version('3_build_3176', '7d4c8c5167224888d901e8cbafb6ec7f')
    version('3_build_3126', 'acc34252b0ea7dff1f581c5db1564dcb')
    version('2.0.2',        '699cd26d7fe0bada29eb1b2cd7b50e4b')

    # Sublime text comes as a pre-compiled binary.
    # Since we can't link to Spack packages, we'll just have to
    # add them as runtime dependencies.

    # depends_on('libgobject', type='run')
    depends_on('glib', type='run')
    depends_on('libx11', type='run')
    depends_on('pcre', type='run')
    depends_on('libffi', type='run')
    depends_on('libxcb', type='run')
    depends_on('libxau', type='run')

    def url_for_version(self, version):
        if version[0] == 2:
            return "https://download.sublimetext.com/Sublime%20Text%20{0}%20x64.tar.bz2".format(version)
        else:
            return "https://download.sublimetext.com/sublime_text_{0}_x64.tar.bz2".format(version)

    def install(self, spec, prefix):
        # Sublime text comes as a pre-compiled binary.
        install_tree('.', prefix)
