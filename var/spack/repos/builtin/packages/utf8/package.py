# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Utf8(Package):
    """A simple, portable and lightweight generic library for handling UTF-8
    encoded strings."""

    homepage = "http://utfcpp.sourceforge.net/"
    url      = "https://sourceforge.net/projects/utfcpp/files/utf8cpp_2x/Release%202.3.4/utf8_v2_3_4.zip"

    version('2.3.4', sha256='3373cebb25d88c662a2b960c4d585daf9ae7b396031ecd786e7bb31b15d010ef')

    def install(self, spec, prefix):
        install_tree('doc', prefix.share.doc)
        install_tree('source', prefix.include)
