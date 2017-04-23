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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install flann
#
# You can edit this file again by typing:
#
#     spack edit flann
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Flann(CMakePackage):
    """
    FLANN is a library for performing fast approximate nearest neighbor
    searches in high dimensional spaces. It contains a collection of
    algorithms we found to work best for nearest neighbor search and a system
    for automatically choosing the best algorithm and optimum parameters
    depending on the dataset.

    FLANN is written in C++ and contains bindings for the following languages:
    C, MATLAB and Python.

    NOTE: The author of the package was careful to support HDF5 without
    parallel support, so the dependencies do not require this, but you will
    likely want to make sure that you are giving hdf5+mpi as the dependency,
    this is the spack default so it should be fine.
    """

    homepage = "http://www.cs.ubc.ca/research/flann/"
    url      = "https://github.com/mariusmuja/flann/archive/1.9.1.tar.gz"

    version('1.9.1', '73adef1c7bf8e8b978987e7860926ea6')
    version('1.8.5', '02a81640b1e9c11796a0413976dc11f5')
    version('1.8.4', '774b74580e3cbc5b0d45c6ec345a64ae')
    version('1.8.1', '1f51500e172f5e11fbda05f033858eb6')
    version('1.8.0', '473150f592c2997e32d5ce31fd3c19a2')

    # Options available in the CMakeLists.txt
    # Language bindings
    variant("python",   default=False,
            description="Build the Python bindings. Module: pyflann.  Python2 only.")
    variant("matlab",   default=False, description="Build the Matlab bindings.")
    # default to true for C because it's a C++ library, nothing extra needed
    variant("c",        default=True,  description="Build the C bindings.")

    # Must build C bindings for Python / Matlab
    conflicts("+python", when="~c")
    conflicts("+matlab", when="~c")

    # Additional options
    variant("cuda",     default=False, description="Build the CUDA library.")
    variant("examples", default=False, description="Build the examples.")
    variant("doc",      default=False, description="Build the documentation.")
    variant("openmp",   default=True,  description="Use OpenMP multi-threading.")
    # mpi and hdf5 are the bread and butter of this library, use 'em
    variant("mpi",      default=True,  description="Use MPI.")
    variant("hdf5",     default=True,  description="Enable HDF5 support.")

    # Dependencies
    extends("python",      when="+python") # creates a site-packages pyflann folder
    depends_on("py-numpy", when="+python") # imports ctypes and numpy
    depends_on("matlab",   when="+matlab")
    depends_on("cuda",     when="+cuda")
    depends_on("mpi",      when="+mpi")
    depends_on("hdf5",     when="+hdf5")
    # HDF5_IS_PARALLEL actually comes from hdf5+mpi
    # https://github.com/mariusmuja/flann/blob/06a49513138009d19a1f4e0ace67fbff13270c69/CMakeLists.txt#L108-L112
    depends_on("boost+mpi+system+serialization+thread", when="+mpi ^hdf5+mpi")

    # Doc deps
    depends_on("latex", when="+doc")

    # Example uses hdf5.
    depends_on("hdf5", when="+examples")

    # Tests: require hdf5 and gtest, don't know what to do so ignore...

    def patch(self):
        # TODO: when #3367 is merged:
        # filter_file("python2", self.spec["python"].command.name, "src/python/setup.py.tpl")
        if self.spec.satisfies("^python@3:"):
            filter_file("python2", "python3", "src/python/setup.py.tpl")

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_BUILD_TYPE:STRING=Release") # Default is RelWithDebugInfo

        # Language bindings. Many default to true in CMakeLists, bypass all
        c_bind   = "ON" if self.spec.satisfies("+c")      else "OFF"
        args.append("-DBUILD_C_BINDINGS:BOOL={}".format(c_bind))

        py_bind  = "ON" if self.spec.satisfies("+python") else "OFF"
        args.append("-DBUILD_PYTHON_BINDINGS:BOOL={}".format(py_bind))

        mat_bind = "ON" if self.spec.satisfies("+matlab") else "OFF"
        args.append("-DBUILD_MATLAB_BINDINGS:BOOL={}".format(mat_bind))

        # Extra options
        cuda_lib   = "ON" if self.spec.satisfies("+cuda")     else "OFF"
        args.append("-DBUILD_CUDA_LIB:BOOL={}".format(cuda_lib))

        examples   = "ON" if self.spec.satisfies("+examples") else "OFF"
        args.append("-DBUILD_EXAMPLES:BOOL={}".format(examples))

        use_openmp = "ON" if self.spec.satisfies("+openmp")   else "OFF"
        args.append("-DUSE_OPENMP:BOOL={}".format(use_openmp))

        use_mpi    = "ON" if self.spec.satisfies("+mpi")      else "OFF"
        args.append("-DUSE_MPI:BOOL={}".format(use_mpi))

        return args
