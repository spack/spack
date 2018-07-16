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


class Flann(CMakePackage):
    """FLANN is a library for performing fast approximate nearest neighbor
    searches in high dimensional spaces. It contains a collection of
    algorithms we found to work best for nearest neighbor search and a system
    for automatically choosing the best algorithm and optimum parameters
    depending on the dataset.

    FLANN is written in C++ and contains bindings for the following languages:
    C, MATLAB and Python.
    """

    homepage = "http://www.cs.ubc.ca/research/flann/"
    url      = "https://github.com/mariusmuja/flann/archive/1.9.1.tar.gz"

    version('1.9.1', '73adef1c7bf8e8b978987e7860926ea6')
    version('1.8.5', '02a81640b1e9c11796a0413976dc11f5')
    version('1.8.4', '774b74580e3cbc5b0d45c6ec345a64ae')
    version('1.8.1', '1f51500e172f5e11fbda05f033858eb6')
    version('1.8.0', '473150f592c2997e32d5ce31fd3c19a2')

    def url_for_version(self, version):
        if version > Version('1.8.1'):
            return "https://github.com/mariusmuja/flann/archive/{0}.tar.gz".format(version)
        else:
            return "https://github.com/mariusmuja/flann/archive/{0}-src.tar.gz".format(version)

    # Options available in the CMakeLists.txt
    # Language bindings
    variant("python",   default=False,
            description="Build the Python bindings. "
                        "Module: pyflann.")
    extends('python', when='+python')
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
    extends("python",      when="+python")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("matlab",   when="+matlab", type=("build", "run"))
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

    depends_on('hdf5', type='test')
    depends_on('gtest', type='test')

    def patch(self):
        # Fix up the python setup.py call inside the install(CODE
        filter_file("setup.py install",
                    'setup.py --no-user-cfg install --prefix=\\"{0}\\"'.format(
                        self.prefix
                    ),
                    "src/python/CMakeLists.txt")
        # Fix the install location so that spack activate works
        if '+python' in self.spec:
            filter_file("share/flann/python",
                        site_packages_dir,
                        "src/python/CMakeLists.txt")
        # Hack. Don't install setup.py
        filter_file("install( FILES",
                    "# install( FILES",
                    "src/python/CMakeLists.txt", string=True)

    def cmake_args(self):
        spec = self.spec
        args = []

        # Language bindings. Many default to true in CMakeLists, bypass all
        c_bind = "ON" if "+c" in spec else "OFF"
        args.append("-DBUILD_C_BINDINGS:BOOL={0}".format(c_bind))

        py_bind = "ON" if "+python" in spec else "OFF"
        args.append("-DBUILD_PYTHON_BINDINGS:BOOL={0}".format(py_bind))

        mat_bind = "ON" if "+matlab" in spec else "OFF"
        args.append("-DBUILD_MATLAB_BINDINGS:BOOL={0}".format(mat_bind))

        # Extra options
        cuda_lib = "ON" if "+cuda" in spec else "OFF"
        args.append("-DBUILD_CUDA_LIB:BOOL={0}".format(cuda_lib))

        examples = "ON" if "+examples" in spec else "OFF"
        args.append("-DBUILD_EXAMPLES:BOOL={0}".format(examples))

        use_openmp = "ON" if "+openmp" in spec else "OFF"
        args.append("-DUSE_OPENMP:BOOL={0}".format(use_openmp))

        use_mpi = "ON" if "+mpi" in spec else "OFF"
        args.append("-DUSE_MPI:BOOL={0}".format(use_mpi))

        # Configure the proper python executable
        if "+python" in spec:
            args.append(
                "-DPYTHON_EXECUTABLE={0}".format(spec["python"].command.path)
            )

        return args
