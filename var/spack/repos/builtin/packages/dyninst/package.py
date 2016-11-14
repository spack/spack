##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Dyninst(Package):
    """API for dynamic binary instrumentation.  Modify programs while they
    are executing without recompiling, re-linking, or re-executing."""

    homepage = "https://paradyn.org"
    url = "https://github.com/dyninst/dyninst/archive/v9.2.0.tar.gz"
    list_url = "http://www.dyninst.org/downloads/dyninst-8.x"

    # version 9.2.1b was the latest git commit when trying to port to a
    # ppc64le system to get fixes in computeAddrWidth independent of 
    # endianness. This version can be removed if the next release includes
    # this change. The actual commit was
    # b8596ad4023ec40ac07e669ff8ea3ec06e262703
    version('9.2.1b', git='https://github.com/dyninst/dyninst.git',
            commit='859cb778e20b619443c943c96dd1851da763142b')
    version('9.2.0', 'ad023f85e8e57837ed9de073b59d6bab',
            url="https://github.com/dyninst/dyninst/archive/v9.2.0.tar.gz")
    version('9.1.0', '5c64b77521457199db44bec82e4988ac',
            url="http://www.paradyn.org/release9.1.0/DyninstAPI-9.1.0.tgz")
    version('8.2.1', 'abf60b7faabe7a2e4b54395757be39c7',
            url="http://www.paradyn.org/release8.2/DyninstAPI-8.2.1.tgz")
    version('8.1.2', 'bf03b33375afa66fe0efa46ce3f4b17a',
            url="http://www.paradyn.org/release8.1.2/DyninstAPI-8.1.2.tgz")
    version('8.1.1', 'd1a04e995b7aa70960cd1d1fac8bd6ac',
            url="http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz")

    variant('stat_dysect', default=False,
            description="patch for STAT's DySectAPI")

    depends_on("libelf")
    depends_on("libdwarf")
    depends_on("boost@1.42:")
    depends_on('cmake', type='build')

    patch('stat_dysect.patch', when='+stat_dysect')
    patch('stackanalysis_h.patch', when='@9.2.0')

    # new version uses cmake
    def install(self, spec, prefix):
        if spec.satisfies('@:8.1'):
            configure("--prefix=" + prefix)
            make()
            make("install")
            return

        libelf = spec['libelf'].prefix
        libdwarf = spec['libdwarf'].prefix

        with working_dir('spack-build', create=True):
            args = ['..',
                    '-DBoost_INCLUDE_DIR=%s'    % spec['boost'].prefix.include,
                    '-DBoost_LIBRARY_DIR=%s'    % spec['boost'].prefix.lib,
                    '-DBoost_NO_SYSTEM_PATHS=TRUE',
                    '-DLIBELF_INCLUDE_DIR=%s'   % join_path(
                        libelf.include, 'libelf'),
                    '-DLIBELF_LIBRARIES=%s'     % join_path(
                        libelf.lib, 'libelf.so'),
                    '-DLIBDWARF_INCLUDE_DIR=%s' % libdwarf.include,
                    '-DLIBDWARF_LIBRARIES=%s'   % join_path(
                        libdwarf.lib, 'libdwarf.so')]
            if spec.satisfies('arch=linux-redhat7-ppc64le'):
                args.append('-Darch_ppc64_little_endian=1')
            args += std_cmake_args
            cmake(*args)
            make()
            make("install")

    @when('@:8.1')
    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
