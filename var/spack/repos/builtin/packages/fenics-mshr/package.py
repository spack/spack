# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsMshr(CMakePackage):
    """mshr is the mesh generation component of FEniCS. It generates
    simplicial DOLFIN meshes in 2D and 3D from geometries described by
    Constructive Solid Geometry (CSG) or from surface files, utilizing
    CGAL and Tetgen as mesh generation backends."""

    homepage = "https://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/mshr.git"
    url      = "https://bitbucket.org/fenics-project/mshr/get/2018.1.0.tar.gz"

    version('2018.1.0',       sha256='84ee27b70996486efaa8a7920fdd79c1df97666c9376a5682627b2dd40e3f03c')
    version('2017.2.0',       sha256='1d77c7040f406fe63e1560184b7f1f9b13da74f3d79509b070f1b74c0ae094bb')
    version('2017.1.0.post0', sha256='1838ceed36f92cf7d09fcf728cc671db3c9d3ee7f64419f0674455d568dc1666')
    version('2017.1.0',       sha256='66c2793aaf7a8274132756d4f6f7fee9099760a0699d2d68690e2e8381fbc1dc')
    version('2016.2.0',       sha256='9ec0864a0ef0f031e4676ec83bf209a62a7864765468edb8e228b4b58c50bc09')
    version('2016.1.0',       sha256='dcc82685c43aaa2f7368d14e7ff65b70861be84cc4be1341460d17fe3e91e5c6')
    version('1.6.0',          sha256='6037a731c18084b33a6cbb3af55fb227dd49af4e00d6a31a2952dcebdf896a77')
    version('1.5.0',          sha256='a2237535eed3feeda7e68b0451412a18237fbf95c701fc74d411d5efc0d1ccfd')

    variant('python', default=False, description='Compile with mshr Python interface')

    extends('python', when='+python')

    depends_on('fenics-dolfin+python', when='+python')
    depends_on('fenics-dolfin', when='~python')

    def url_for_version(self, version):
        url = "https://bitbucket.org/fenics-project/mshr/get"
        if version >= Version('2017.1.0'):
            url += "/{0}.tar.gz".format(version)
        else:
            url += "/mshr-{0}.tar.gz".format(version)
        return url

    # FIXME: install python interface
