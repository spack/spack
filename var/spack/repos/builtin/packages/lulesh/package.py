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
import os


class Lulesh(Package):
    """Livermore Unstructured Lagrangian Explicit Shock Hydrodynamics (LULESH)
    """

    homepage = "https://codesign.llnl.gov/lulesh.php"
    url      = "https://codesign.llnl.gov/lulesh/lulesh2.0.3.tgz"

    version("2.0.3", "336644a8750f71c7c6b9d2960976e7aa")

    patch("remove_defaults.patch")

    variant('mpip', default=False)

    depends_on("mpi", type="build")
    depends_on("mpip", when="+mpip")

    def install(self, spec, prefix):
        if '+mpip' in spec:
            os.environ["LDFLAGS"] = " -lmpiP -ldwarf -lelf"

            if os.uname()[4] == "x86_64":
                os.environ["LDFLAGS"] += " -lunwind"

        os.environ["CXX"] = spec['mpi'].mpicxx + " -DUSE_MPI=1"
        os.environ["PREFIX"] = prefix
        make()
        make("install")
