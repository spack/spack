# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Voropp(MakefilePackage):
    """Voro++ is a open source software library for the computation of the
    Voronoi diagram, a widely-used tessellation that has applications in many
    scientific fields."""

    homepage = "http://math.lbl.gov/voro++/about.html"
    url      = "http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz"

    version('0.4.6', '2338b824c3b7b25590e18e8df5d68af9')

    def edit(self, spec, prefix):
        filter_file(r'CC=g\+\+',
                    'CC={0}'.format(self.compiler.cxx),
                    'config.mk')
        filter_file(r'PREFIX=/usr/local',
                    'PREFIX={0}'.format(self.prefix),
                    'config.mk')
