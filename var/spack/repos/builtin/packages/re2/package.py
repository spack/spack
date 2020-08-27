# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Re2(CMakePackage):
    """RE2 is a fast, safe, thread-friendly alternative to backtracking
    regular expression engines like those used in PCRE, Perl, and Python."""

    homepage = "https://github.com/google/re2"
    git      = "https://github.com/google/re2.git"

    version('master', commit='ca11026a032ce2a3de4b3c389ee53d2bdc8794d6')
