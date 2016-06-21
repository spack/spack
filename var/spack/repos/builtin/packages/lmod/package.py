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

class Lmod(Package):
    """
    Lmod is a Lua based module system that easily handles the MODULEPATH
    Hierarchical problem. Environment Modules provide a convenient way to
    dynamically change the users' environment through modulefiles. This
    includes easily adding or removing directories to the PATH environment
    variable. Modulefiles for Library packages provide environment variables
    that specify where the library and header files can be found.
    """
    homepage = "https://www.tacc.utexas.edu/research-development/tacc-projects/lmod"
    url      = "http://sourceforge.net/projects/lmod/files/Lmod-6.0.1.tar.bz2/download"

    version('6.0.1', '91abf52fe5033bd419ffe2842ebe7af9')

    depends_on("lua@5.2:")

    def install(self, spec, prefix):
        # Add our lua to PATH
        os.environ['PATH'] = spec['lua'].prefix.bin + ';' + os.environ['PATH']
        
        configure('--prefix=%s' % prefix)
        make()
        make("install")
