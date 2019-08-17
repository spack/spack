# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tantan(MakefilePackage):
    """tantan is a tool to mask simple regions (low complexity and
    short-period tandem repeats) in DNA, RNA, and protein sequences."""

    homepage = "http://cbrc3.cbrc.jp/~martin/tantan"
    url      = "http://cbrc3.cbrc.jp/~martin/tantan/tantan-13.zip"

    version('13', '90a30284a7d0cd04d797527d47bc8bd0')

    def install(self, spec, prefix):
        make('prefix={0}'.format(self.prefix), 'install')
