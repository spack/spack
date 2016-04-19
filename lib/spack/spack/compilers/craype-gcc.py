##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.compilers.gcc import Gcc
from spack.cray_wrapper import CrayWrapper

class CraypeGcc(CrayWrapper, Gcc):
    cray_wrapper_config = {
        'vendor_module': 'PrgEnv-gnu',
        'compiler_module': 'gcc',
        'libsci_overrides': {
            'gcc/4.8.2': 'cray-libsci/13.0.0',
            'gcc/4.8.1': 'cray-libsci/13.0.0',
            'gcc/4.6.1': 'cray-libsci/13.0.0'
        }
    }
    @classmethod
    def cc_version(cls, cc):
        if CrayWrapper._detect_wrapper(cc, r'(Usage: cc \[options\] file)\.*'):
            return get_compiler_version(
                cc, '--version',
                r'gcc \(GCC\) (\d+\.\d+(?:\.\d+)?)')

    @classmethod
    def cxx_version(cls, cxx):
        if CrayWrapper._detect_wrapper(cxx, r'(Usage: CC \[options\] file)\.*'):
            return get_compiler_version(
                cxx, '--version',
                r'g\+\+ \(GCC\) (\d+\.\d+(?:\.\d+)?)')
