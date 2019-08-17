# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgtextutils(AutotoolsPackage):
    """Gordon's Text utils Library."""

    homepage = "https://github.com/agordon/libgtextutils"
    url      = "https://github.com/agordon/libgtextutils/releases/download/0.7/libgtextutils-0.7.tar.gz"

    patch('text_line_reader.patch')
    version('0.7', '593c7c62e3c76ec49f5736eed4f96806')
