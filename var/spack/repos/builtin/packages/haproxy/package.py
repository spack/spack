# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Haproxy(MakefilePackage):
    """
    HAProxy is a single-threaded, event-driven, non-blocking engine
    combining a very fast I/O layer with a priority-based scheduler.
    """

    homepage = "https://www.haproxy.org"
    url      = "https://www.haproxy.org/download/2.1/src/haproxy-2.1.0.tar.gz"

    version('2.1.1', sha256='57e75c1a380fc6f6aa7033f71384370899443c7f4e8a4ba289b5d4350bc76d1a')
    version('2.1.0', sha256='f268efb360a0e925137b4b8ed431f2f8f3b68327efb2c418b266e535d8e335a0')

    def build(self, spec, prefix):
        sh = Executable('make TARGET=generic PREFIX=' + prefix)
        sh()

    def install(self, spec, prefix):
        sh = Executable('make install PREFIX=' + prefix)
        sh()
