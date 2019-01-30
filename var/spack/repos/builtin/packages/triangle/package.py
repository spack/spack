# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Triangle(Package):
    """Triangle is a two-dimensional mesh generator and Delaunay
       triangulator. Triangle generates exact Delaunay triangulations,
       constrained Delaunay triangulations, conforming Delaunay
       triangulations, Voronoi diagrams, and high-quality triangular
       meshes."""

    homepage = "http://www.cs.cmu.edu/~quake/triangle.html"
    url      = "http://www.netlib.org/voronoi/triangle.zip"

    version('1.6', '10aff8d7950f5e0e2fb6dd2e340be2c9')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)

        install('triangle', prefix.bin)
        install('showme', prefix.bin)
