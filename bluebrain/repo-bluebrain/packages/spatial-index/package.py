# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class SpatialIndex(PythonPackage):
    """Spatial indexer for geometries and morphologies"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/SpatialIndex"
    git      = "git@bbpgitlab.epfl.ch:hpc/SpatialIndex.git"
    url      = "git@bbpgitlab.epfl.ch:hpc/SpatialIndex.git"

    version('develop', branch='main', submodules=True)
    version('0.5.0', tag='0.5.0', submodules=True)
    version('0.4.9', tag='0.4.9', submodules=True)
    version('0.4.8', tag='0.4.8', submodules=True)
    version('0.4.7', tag='0.4.7', submodules=True)
    version('0.4.6', tag='0.4.6', submodules=True)
    version('0.4.5', tag='0.4.5', submodules=True)
    version('0.4.4', tag='0.4.4', submodules=True)
    version('0.4.3', tag='0.4.3', submodules=True)
    version('0.4.2', tag='0.4.2', submodules=True)
    version('0.4.1', tag='0.4.1', submodules=True)
    version('0.4.0', tag='0.4.0', submodules=True)
    version('0.3.0', tag='0.3.0', submodules=True)
    version('0.2.1', tag='0.2.1', submodules=True)
    version('0.1.0', tag='0.1.0', submodules=True)

    depends_on("py-setuptools")
    depends_on("cmake@3.2:", type="build")
    depends_on("boost@:1.70.0")
    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-libsonata", type=("build", "run"), when="@0.2.2:")
    depends_on("py-morphio", type=("build", "run"))
    depends_on("py-morpho-kit", type=("build", "run"))
    depends_on("py-mvdtool~mpi", type=("build", "run"))
    depends_on("py-numpy-quaternion", type=("build", "run"), when="@0.2.1:")
    depends_on("py-numpy", type=("build", "run"))

    @run_after('install')
    def install_headers(self):
        install_tree('include', self.prefix.include)
