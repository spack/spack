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


class PyNumexpr3(PythonPackage):
    """Numexpr3 is a fast numerical expression evaluator for NumPy. With it,
    expressions that operate on arrays (like "3*a+4*b") are accelerated and
    use less memory than doing the same calculation in Python.
    In addition, its multi-threaded capabilities can make use of all your
    cores, which may accelerate computations, most specially if they are not
    memory-bounded (e.g. those using transcendental functions).
    Compared to NumExpr 2.6, functions have been re-written in a fashion such
    that gcc can auto-vectorize them with SIMD instruction sets such as
    SSE2 or AVX2, if your processor supports them. Use of a newer version of
    gcc such as 5.4 is strongly recommended."""
    homepage = "https://github.com/pydata/numexpr/tree/numexpr-3.0"
    url = "https://pypi.io/packages/source/n/numexpr3/numexpr3-3.0.1a1.tar.gz"

    version('3.0.1.a1', '9fa8dc59b149aa1956fc755f982a78ad')
    # TODO: Add CMake build system for better control of passing flags related
    # to CPU ISA.

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-setuptools@18.2:', type='build')
