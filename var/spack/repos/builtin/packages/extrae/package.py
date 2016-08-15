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
    homepage = "http://www.bsc.es/computer-sciences/extrae"
    url      = "http://www.bsc.es/ssl/apps/performanceTools/files/extrae-3.3.0.tar.bz2"
    version('3.3.0', 'f46e3f1a6086b5b3ac41c9585b42952d')

    depends_on("mpi")
    depends_on("dyninst")
    depends_on("libunwind")
    depends_on("boost")
    depends_on("libdwarf")
    depends_on("papi")
    depends_on("libelf")
    depends_on("libxml2")
    depends_on("binutils+libiberty")

    def install(self, spec, prefix):
        if 'openmpi' in spec:
            mpi = spec['openmpi']
        elif 'mpich' in spec:
            mpi = spec['mpich']
        elif 'mvapich2' in spec:
            mpi = spec['mvapich2']

        configure("--prefix=%s" % prefix,
                  "--with-mpi=%s" % mpi.prefix,
                  "--with-unwind=%s" % spec['libunwind'].prefix,
                  "--with-dyninst=%s" % spec['dyninst'].prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--with-dwarf=%s" % spec['libdwarf'].prefix,
                  "--with-papi=%s" % spec['papi'].prefix,
                  "--with-dyninst-headers=%s" % spec[
                      'dyninst'].prefix.include,
                  "--with-elf=%s" % spec['libelf'].prefix,
                  "--with-xml-prefix=%s" % spec['libxml2'].prefix,
                  "--with-binutils=%s" % spec['binutils'].prefix,
                  "--with-dyninst-libs=%s" % spec['dyninst'].prefix.lib)

        make()
        make("install", parallel=False)
