# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import re


class Ccache(CMakePackage):
    """ccache is a compiler cache. It speeds up recompilation by caching
    previous compilations and detecting when the same compilation is being done
    again."""

    homepage = "https://ccache.dev/"
    url      = "https://github.com/ccache/ccache/releases/download/v4.2/ccache-4.2.tar.gz"

    executables = ['^ccache$']

    version('4.2', sha256='dbf139ff32031b54cb47f2d7983269f328df14b5a427882f89f7721e5c411b7e')

    depends_on('asciidoc')
    depends_on('zstd')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'ccache.*version\s+(\S+)', output)
        return match.group(1) if match else None
