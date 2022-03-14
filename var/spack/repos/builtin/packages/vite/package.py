# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vite(CMakePackage):
    """ViTE is a trace explorer. It is a tool to visualize execution
    traces in Pajé or OTF2 format for debugging and profiling parallel or
    distributed applications."""

    homepage = "https://solverstack.gitlabpages.inria.fr/vite/"
    maintainers = ['trahay']
    git = "https://gitlab.inria.fr/solverstack/vite.git"

    version('master',  branch='master')

    depends_on('cmake@3.1:', type='build')
    depends_on('qt+opengl')
    depends_on('glm')
    depends_on('glew')
    depends_on('otf2', when='+otf2')
    depends_on('tau', when='+tau')

    variant('tau', default=False, description='Support for TAU trace format')
    variant('otf2', default=False, description='Support for OTF2 trace format')

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DUSE_QT5=ON",
            "-DUSE_OPENGL=ON",
            "-DUSE_VBO=OFF",
        ]

        if '+otf2' in self.spec:
            args.append("-DVITE_ENABLE_OTF2=ON")
        if '+tau' in self.spec:
            args.append("-DVITE_ENABLE_TAU=ON")
        
        return args
