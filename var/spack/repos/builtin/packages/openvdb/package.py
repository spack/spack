# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *


class Openvdb(CMakePackage):

    """OpenVDB - a sparse volume data format."""

    homepage = "https://github.com/AcademySoftwareFoundation/openvdb"
    url      = "https://github.com/AcademySoftwareFoundation/openvdb/archive/v8.0.1.tar.gz"
    git      = "https://github.com/AcademySoftwareFoundation/openvdb.git"

    # Github account name for Drew.Whitehouse@gmail.com
    maintainers = ['eloop']

    version('develop', branch='develop')
    version('8.0.1', 'a6845da7c604d2c72e4141c898930ac8a2375521e535f696c2cd92bebbe43c4f')
    version('7.1.0', '0c3588c1ca6e647610738654ec2c6aaf41a203fd797f609fbeab1c9f7c3dc116')

    variant('shared', default=True, description='Build as a shared library.')
    variant('python', default=False, description='Build the pyopenvdb python extension.')
    variant('vdb_print', default=False, description='Build the vdb_print tool.')
    variant('vdb_lod', default=False, description='Build the vdb_lod tool.')
    variant('vdb_render', default=False, description='Build the vdb_render tool.')
    variant('ax', default=False, description='Build the AX extension (untested).')

    depends_on('ilmbase')
    depends_on('openexr')
    depends_on('intel-tbb')

    # Openvdb officially suggests an old version of blosc but it doesn't seem to be
    # strictly neccessary and requires manual approval from spack.
    depends_on('c-blosc')  # depends_on('c-blosc@1.5:')

    extends('python', when='+python')
    depends_on('py-numpy', when='+python')

    depends_on('boost+iostreams+system+python+numpy', when='+python')
    depends_on('boost+iostreams+system', when='~python')

    # AX requires quite a few things. I've only managed to build llvm@8 under centos8.
    depends_on('llvm@8', when='+ax')
    depends_on('bison', when='+ax')
    depends_on('flex', when='+ax')

    depends_on('git', type='build', when='@develop')

    def cmake_args(self):

        spec = self.spec

        cmake_args = ['-DOPENVDB_BUILD_CORE=ON']

        if '+shared' in spec:
            cmake_args.extend([
                '-DBUILD_SHARED_LIBS=ON'
            ])
        else:
            cmake_args.extend([
                '-DBUILD_SHARED_LIBS=OFF'
            ])
        if '+ax' in spec:
            cmake_args.extend([
                '-DOPENVDB_BUILD_AX=ON',
                '-DOPENVDB_BUILD_AX_BINARIES=ON'
            ])
        else:
            cmake_args.extend([
                '-DOPENVDB_BUILD_AX=OFF',
                '-DOPENVDB_BUILD_AX_BINARIES=OFF'
            ])

        if '+vdb_print' in spec:
            cmake_args.extend([
                '-DOPENVDB_BUILD_VDB_PRINT=ON'
            ])
        else:
            cmake_args.extend([
                '-DOPENVDB_BUILD_VDB_PRINT=OFF'
            ])

        if '+vdb_lod' in spec:
            cmake_args.extend([
                '-DOPENVDB_BUILD_VDB_LOD=ON'
            ])
        else:
            cmake_args.extend([
                '-DOPENVDB_BUILD_VDB_LOD=OFF'
            ])

        if '+vdb_render' in spec:
            cmake_args.extend([
                '-DOPENVDB_BUILD_VDB_RENDER=ON'
            ])
        else:
            cmake_args.extend([
                '-DOPENVDB_BUILD_VDB_RENDER=OFF'
            ])

        if '+python' in spec:
            cmake_args.extend([
                '-DUSE_NUMPY:BOOL=ON',
                '-DOPENVDB_BUILD_PYTHON_MODULE:BOOL=ON'])
        else:
            cmake_args.extend([
                '-DUSE_NUMPY:BOOL=OFF',
                '-DOPENVDB_BUILD_PYTHON_MODULE:BOOL=OFF'])

        return cmake_args

    # The python extension is being put in the wrong directory
    # by OpenVDB's cmake, instead it needs to be in
    # site_packages_dir. For RHEL systems we seem to get the
    # dso in lib64/ instead of lib/
    @run_after('install')
    def post_install(self):

        spec = self.spec

        if '+python' in spec:

            if sys.platform == "darwin":
                pyso = "pyopenvdb.dylib"
            else:
                pyso = "pyopenvdb.so"
            pyver = 'python{0}'.format(spec['python'].package.version.up_to(2))

            src = prefix.lib.join(pyver).join(pyso)
            if not os.path.isfile(src):
                src = prefix.lib64.join(pyver).join(pyso)
            mkdirp(site_packages_dir)
            os.rename(src, os.path.join(site_packages_dir, pyso))
