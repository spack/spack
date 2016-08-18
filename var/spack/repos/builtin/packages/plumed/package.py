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


class Plumed(Package):
    """PLUMED is an open source library for free energy calculations in
       molecular systems which works together with some of the most popular
       molecular dynamics engines."""

    # PLUMED homepage. The source is available on github.
    homepage = "http://www.plumed.org/home"
    url      = "https://github.com/plumed/plumed2"

    version('2.2.3', git="https://github.com/plumed/plumed2.git", tag='v2.2.3')

    # Variants. PLUMED by default builds a number of optional modules.
    # The ones listed here are not built by default for various reasons,
    # such as stability, lack of testing, or lack of demand.
    variant('crystallization', default=False,
            description='Build support for optional crystallization module.')
    variant('imd', default=False,
            description='Build support for optional imd module.')
    variant('manyrestraints', default=False,
            description='Build support for optional manyrestraints module.')
    variant('mpi', default=False,
            description='Enable MPI support.')

    # Dependencies. LAPACK and BLAS are recommended but not essential.
    depends_on("mpi", when="+mpi")
    depends_on("netlib-lapack")
    depends_on("openblas")

    def install(self, spec, prefix):
        # Prefix is the only compulsory argument.
        config_args = ["--prefix=" + prefix]

        # Construct list of optional modules
        module_opts=[]
        module_opts.extend([
            '+crystallization' if '+crystallization' in spec else '-crystallization',
            '+imd' if '+imd' in spec else '-imd',
            '+manyrestraints' if '+manyrestraints' in spec else '-manyrestraints'
        ])

        # If we have specified any optional modules then add the argument ro
        # enable or disable them.
        if module_opts:
            config_args.extend(["--enable-modules=%s" % "".join(module_opts)])

        # If using MPI then ensure the correct compiler wrapper is used.
        if '+mpi' in spec:
            config_args.extend([
                "--enable-mpi",
                "CC=%s" % self.spec['mpi'].mpicc,
                "CXX=%s" % self.spec['mpi'].mpicxx,
                "FC=%s" % self.spec['mpi'].mpifc,
                "F77=%s" % self.spec['mpi'].mpif77
            ])

        # Add remaining variant flags.
#        config_args.extend([
#            "--enable-mpi" if '+mpi' in spec else "--disable-mpi"
#        ])

        # Configure
        configure(*config_args)

        make()
        make("install")
