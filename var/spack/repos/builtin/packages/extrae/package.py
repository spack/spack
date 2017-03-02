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

# typical working line with extrae 3.0.1
# ./configure
#   --prefix=/usr/local
#   --with-mpi=/usr/lib64/mpi/gcc/openmpi
#   --with-unwind=/usr/local
#   --with-papi=/usr
#   --with-dwarf=/usr
#   --with-elf=/usr
#   --with-dyninst=/usr
#   --with-binutils=/usr
#   --with-xml-prefix=/usr
#   --enable-openmp
#   --enable-nanos
#   --enable-pthread
#   --disable-parallel-merge
#
# LDFLAGS=-pthread


class Extrae(Package):
    """Extrae is the package devoted to generate tracefiles which can
       be analyzed later by Paraver. Extrae is a tool that uses
       different interposition mechanisms to inject probes into the
       target application so as to gather information regarding the
       application performance. The Extrae instrumentation package can
       instrument the MPI programin model, and the following parallel
       programming models either alone or in conjunction with MPI :
       OpenMP, CUDA, OpenCL, pthread, OmpSs"""
    homepage = "https://tools.bsc.es/extrae"
    url      = "https://ftp.tools.bsc.es/extrae/extrae-3.4.1-src.tar.bz2"
    version('3.4.1', '69001f5cfac46e445d61eeb567bc8844')

    depends_on("mpi")
    depends_on("dyninst")
    depends_on("libunwind")
    depends_on("boost")
    depends_on("libdwarf")
    depends_on("papi")
    depends_on("elf", type="link")
    depends_on("libxml2")

    # gettext dependency added to find -lintl
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
    depends_on("gettext")
    depends_on("binutils+libiberty")

    def install(self, spec, prefix):
        if 'openmpi' in spec:
            mpi = spec['openmpi']
        elif 'mpich' in spec:
            mpi = spec['mpich']
        elif 'mvapich2' in spec:
            mpi = spec['mvapich2']

        extra_config_args = []

        # This was added due to configure failure
        # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
        extra_config_args.append('LDFLAGS=-lintl')

        if spec.satisfies("^dyninst@9.3.0:"):
            make.add_default_arg('CXXFLAGS=-std=c++11')
            extra_config_args.append('CXXFLAGS=-std=c++11')

        configure("--prefix=%s" % prefix,
                  "--with-mpi=%s" % mpi.prefix,
                  "--with-unwind=%s" % spec['libunwind'].prefix,
                  "--with-dyninst=%s" % spec['dyninst'].prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--with-dwarf=%s" % spec['libdwarf'].prefix,
                  "--with-papi=%s" % spec['papi'].prefix,
                  "--with-dyninst-headers=%s" % spec[
                      'dyninst'].prefix.include,
                  "--with-elf=%s" % spec['elf'].prefix,
                  "--with-xml-prefix=%s" % spec['libxml2'].prefix,
                  "--with-binutils=%s" % spec['binutils'].prefix,
                  "--with-dyninst-libs=%s" % spec['dyninst'].prefix.lib,
                  *extra_config_args)

        make()
        make("install", parallel=False)
