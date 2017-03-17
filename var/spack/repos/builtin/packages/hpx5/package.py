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


class Hpx5(AutotoolsPackage):
    """The HPX-5 Runtime System. HPX-5 (High Performance ParalleX) is an
    open source, portable, performance-oriented runtime developed at
    CREST (Indiana University). HPX-5 provides a distributed
    programming model allowing programs to run unmodified on systems
    from a single SMP to large clusters and supercomputers with
    thousands of nodes. HPX-5 supports a wide variety of Intel and ARM
    platforms. It is being used by a broad range of scientific
    applications enabling scientists to write code that performs and
    scales better than contemporary runtimes."""
    homepage = "http://hpx.crest.iu.edu"
    url      = "http://hpx.crest.iu.edu/release/hpx-3.1.0.tar.gz"

    version('4.0.0', 'b40dc03449ae1039cbb48ee149952b22')
    version('3.1.0', '9e90b8ac46788c009079632828c77628')
    version('2.0.0', '3d2ff3aab6c46481f9ec65c5b2bfe7a6')
    version('1.3.0', '2260ecc7f850e71a4d365a43017d8cee')
    version('1.2.0', '4972005f85566af4afe8b71afbf1480f')
    version('1.1.0', '646afb460ecb7e0eea713a634933ce4f')
    version('1.0.0', '8020822adf6090bd59ed7fe465f6c6cb')

    variant('cuda', default=False, description='Enable CUDA support')
    variant('cxx11', default=False, description='Enable C++11 hpx++ interface')
    variant('debug', default=False, description='Build debug version of HPX-5')
    variant('instrumentation', default=False, description='Enable instrumentation (may affect performance)')
    variant('metis', default=False, description='Enable METIS support')
    variant('mpi', default=False, description='Enable MPI support')
    variant('opencl', default=False, description='Enable OpenCL support')
    variant('photon', default=False, description='Enable Photon support')
    variant('pic', default=True, description='Produce position-independent code')

    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("hwloc")
    depends_on("hwloc +cuda", when='+cuda')
    # Note: We could disable CUDA support via "hwloc ~cuda"
    depends_on("jemalloc")
    # depends_on("libffi")
    depends_on("libtool", type='build')
    # depends_on("lz4")   # hpx5 always builds its own lz4
    depends_on("m4", type='build')
    depends_on("metis", when='+metis')
    depends_on("mpi", when='+mpi')
    depends_on("mpi", when='+photon')
    depends_on("opencl", when='+opencl')
    # depends_on("papi")
    depends_on("pkg-config", type='build')

    configure_directory = "hpx"
    build_directory = "spack-build"

    def configure_args(self):
        spec = self.spec
        args = [
            '--enable-agas',          # make this a variant?
            '--enable-jemalloc',      # make this a variant?
            '--enable-percolation',   # make this a variant?
            # '--enable-rebalancing',   # this seems broken
            '--with-hwloc=hwloc',
            '--with-jemalloc=jemalloc',
            # Spack's libffi installs its headers strangely,
            # leading to problems
            '--with-libffi=contrib',
            # '--with-papi=papi',   # currently disabled in HPX
        ]

        if '+cxx11' in spec:
            args += ['--enable-hpx++']

        if '+debug' in spec:
            args += ['--enable-debug']

        if '+instrumentation' in spec:
            args += ['--enable-instrumentation']

        if '+mpi' in spec or '+photon' in spec:
            # photon requires mpi
            args += ['--enable-mpi']
            # Choose pkg-config name for MPI library
            if '^openmpi' in spec:
                args += ['--with-mpi=ompi-cxx']
            elif '^mpich' in spec:
                args += ['--with-mpi=mpich']
            elif '^mvapich2' in spec:
                args += ['--with-mpi=mvapich2-cxx']
            else:
                args += ['--with-mpi=system']

        # METIS does not support pkg-config; HPX will pick it up automatically
        # if '+metis' in spec:
        #     args += ['--with-metis=???']

        if '+opencl' in spec:
            args += ['--enable-opencl']
            if '^pocl' in spec:
                args += ['--with-opencl=pocl']
            else:
                args += ['--with-opencl=system']

        if '+photon' in spec:
            args += ['--enable-photon']

        if '+pic' in spec:
            args += ['--with-pic']

        return args
