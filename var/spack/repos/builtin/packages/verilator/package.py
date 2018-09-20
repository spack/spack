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


class Verilator(AutotoolsPackage):
    """Verilator is the fastest free Verilog HDL simulator.

    It compiles synthesizable Verilog (not test-bench code!), plus some PSL,
    SystemVerilog and Synthesis assertions into C++ or SystemC code. It is
    designed for large projects where fast simulation performance is of primary
    concern, and is especially well suited to generate executable models of
    CPUs for embedded software design teams.

    Please do not download this program if you are expecting a full featured
    replacement for NC-Verilog, VCS or another commercial Verilog simulator
    or Verilog compiler for a little project! (Try Icarus instead.) However, if
    you are looking for a path to migrate synthesizable Verilog to C++ or
    SystemC, and writing just a touch of C code and Makefiles doesn't scare you
    off, this is the free Verilog compiler for you.

    Verilator supports the synthesis subset of Verilog, plus initial
    statements, proper blocking/non-blocking assignments, functions, tasks,
    multi-dimensional arrays, and signed numbers. It also supports very simple
    forms of SystemVerilog assertions and coverage analysis. Verilator supports
    the more important Verilog 2005 constructs, and some SystemVerilog
    features, with additional constructs being added as users request them.

    Verilator has been used to simulate many very large multi-million gate
    designs with thousands of modules."""

    homepage = "https://www.veripool.org/projects/verilator"
    url      = "https://www.veripool.org/ftp/verilator-3.920.tgz"

    version('3.920', '71de7b9ddb27a72e96ed2a04e5ccf933')
    version('3.904', '7d4dc8e61d5e0e564c3016a06f0b9d07')

    depends_on('bison', type='build')
    depends_on('flex',  type='build')
    depends_on('perl',  type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('VERILATOR_ROOT', self.prefix)

    # verilator requires access to its shipped scripts (bin) and include
    # but the standard make doesn't put it in the correct places
    @run_before('install')
    def install_include(self):
        install_tree('include', prefix.include)
        install_tree('bin', prefix.bin)

    # we need to fix the CXX and LINK paths, as they point to the spack
    # wrapper scripts which aren't usable without spack
    @run_after('install')
    def patch_cxx(self):
        filter_file(r'^CXX\s*=.*', 'CXX = {0}'.format(self.compiler.cxx),
                    join_path(self.prefix.include, 'verilated.mk'))
        filter_file(r'^LINK\s*=.*', 'LINK = {0}'.format(self.compiler.cxx),
                    join_path(self.prefix.include, 'verilated.mk'))
