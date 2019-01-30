# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Opennurbs(Package):
    """OpenNURBS is an open-source NURBS-based geometric modeling library
    and toolset, with meshing and display / output functions.
    """

    homepage = "https://github.com/OpenNURBS/OpenNURBS"
    git      = "https://github.com/OpenNURBS/OpenNURBS.git"

    maintainers = ['jrood-nrel']

    version('develop', branch='develop')

    version('percept', '59163fd085a24c7a4c2170c70bb60fea',
            url='https://github.com/PerceptTools/percept/raw/master/build-cmake/opennurbs-percept.tar.gz')

    variant('shared', default=True,
            description="Build shared libraries")

    # CMake installation method
    def install(self, spec, prefix):
        cmake_args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF')
        ]

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    # Pre-cmake installation method
    @when('@percept')
    def install(self, spec, prefix):
        make(parallel=False)

        # Install manually
        mkdir(prefix.lib)
        mkdir(prefix.include)
        install('libopenNURBS.a', prefix.lib)
        install_tree('zlib', join_path(prefix.include, 'zlib'))
        headers = glob.glob(join_path('.', '*.h'))
        for h in headers:
            install(h, prefix.include)
