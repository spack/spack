##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
    git      = "https://github.com/dyninst/dyninst.git"

    version('develop', branch='master')
    version('9.3.2', tag='v9.3.2')
    version('9.3.0', tag='v9.3.0')
    version('9.2.0', tag='v9.2.0')
    version('9.1.0', tag='v9.1.0')
    version('8.2.1', tag='v8.2.1')
    version('8.1.2', tag='v8.1.2')
    version('8.1.1', tag='v8.1.1')

    variant('stat_dysect', default=False,
            description="patch for STAT's DySectAPI")

    # Dyninst depends on libelf and libdwarf prior to @9.3.0
    # Dyninst depends on elfutils and libdwarf from @9.3.0 to but
    # not including @develop
    # Dyninst depends on elfutils and elfutils libdw from @develop forward
    # elf@0 is an abstaction for libelf
    # elf@1 is an abstaction for elfutils
    depends_on("elf@0", type='link', when='@:9.2.99')
    # The sorting algorithm puts numbered releases as newer than alphabetic
    # releases, but spack has special logic in place to ensure that
    # develop is considered newer than all other releases.
    # So, develop is included in the elf@1 line below.
    depends_on("elf@1", type='link', when='@9.3.0:')
    depends_on("libdwarf", when='@:9')
    depends_on("boost@1.42:")
    depends_on('libiberty+pic')
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

        libelf = spec['elf'].prefix
        if spec.satisfies('@:9'):
            libdwarf = spec['libdwarf'].prefix

        with working_dir('spack-build', create=True):
            args = ['..',
                    '-DBoost_INCLUDE_DIR=%s'    % spec['boost'].prefix.include,
                    '-DBoost_LIBRARY_DIR=%s'    % spec['boost'].prefix.lib,
                    '-DBoost_NO_SYSTEM_PATHS=TRUE',
                    '-DLIBELF_INCLUDE_DIR=%s'   % join_path(
                        libelf.include, 'libelf'),
                    '-DLIBELF_LIBRARIES=%s'     % join_path(
                        libelf.lib, "libelf." + dso_suffix)]
            if spec.satisfies('@:9'):
                args.append('-DLIBDWARF_INCLUDE_DIR=%s' % libdwarf.include)
                args.append('-DLIBDWARF_LIBRARIES=%s'   % join_path(
                    libdwarf.lib, "libdwarf." + dso_suffix))
            # For @develop + use elfutils libdw, libelf is an abstraction
            # we are really using elfutils here
            if spec.satisfies('@develop'):
                args.append('-DLIBDWARF_INCLUDE_DIR=%s' % libelf.include)
                args.append('-DLIBDWARF_LIBRARIES=%s'   % join_path(
                    libelf.lib, "libdw." + dso_suffix))
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
