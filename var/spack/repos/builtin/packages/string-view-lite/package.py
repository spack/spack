# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from shutil import copytree


class StringViewLite(Package):
    """
    A single-file header-only version of a C++17-like string_view for C++98,
    C++11 and later
    """

    homepage = "https://github.com/martinmoene/string-view-lite"
    url      = "https://github.com/martinmoene/string-view-lite/archive/v1.0.0.tar.gz"

    version('1.1.0', sha256='88fb33ad7a345a25aca4ddf3244afd81b8d54787e5fb316a7ed60f702bc646cd')
    version('1.0.0', sha256='44e30dedd6f4777e646da26528f9d2d5cc96fd0fa79e2e5c0adc14817d048d63')
    version('0.2.0', sha256='c8ae699dfd2ccd15c5835e9b1d246834135bbb91b82f7fc4211b8ac366bffd34')
    version('0.1.0', sha256='7de87d6595230a6085655dab6145340bc423f2cf206263ef73c9b78f7b153340')

    def install(self, spec, prefix):
        copytree('include', prefix.include)
