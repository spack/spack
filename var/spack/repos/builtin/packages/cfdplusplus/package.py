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
from spack import *


class Cfdplusplus(Package):
    """Metacomp's Computational Fluid Dynamics (CFD) software suite."""

    homepage = "http://www.metacomptech.com/index.php/features/icfd"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('16.1')

    def install(self, spec, prefix):
        pass

    def setup_environment(self, spack_env, run_env):
        run_env.set('CFDPLUSPLUS_ROOT', '/ssoft/spack/external/CFD++/2016.05')  # noqa: E501
        run_env.set('CFDPLUSPLUS_INCLUDE', '/ssoft/spack/external/CFD++/2016.05/include')  # noqa: E501
        run_env.set('CFDPLUSPLUS_LIBRARY', '/ssoft/spack/external/CFD++/2016.05/lib')  # noqa: E501
        run_env.set('CFDPLUSPLUS_PATH', '/ssoft/spack/external/CFD++/2016.05/mlib/mcfd.16.1/exec')  # noqa: E501
        run_env.prepend_path('LD_LIBRARY_PATH', '/ssoft/spack/external/CFD++/2016.05/lib')  # noqa: E501
        run_env.prepend_path('LD_LIBRARY_PATH', '/ssoft/spack/external/CFD++/2016.05/glib')  # noqa: E501
        run_env.prepend_path('PATH', '/ssoft/spack/external/CFD++/2016.05/mlib/mcfd.16.1/exec')  # noqa: E501
        run_env.set('METACOMP_LICENSE_FILE', '/ssoft/spack/external/CFD++/2016.05/Lics/Metacomp.lic')  # noqa: E501
        run_env.set('METACOMP_HOME', '/ssoft/spack/external/CFD++/2016.05')  # noqa: E501
        run_env.set('MCFD_HOME', '/ssoft/spack/external/CFD++/2016.05/mlib/mcfd.16.1')  # noqa: E501
        run_env.set('MCFD_VERSION', '16.1')
        run_env.set('MCFD_PAR_LIC_MODE', '2')
        run_env.set('MCFD_MAXMEM', '512G')
        run_env.set('MCFD_PROCMEM', '32G')
        run_env.set('MCFD_TCLTK', '/ssoft/spack/external/CFD++/2016.05/mlib/mcfd.16.1/exec/gui_src')  # noqa: E501
        run_env.set('MCFD_HTML', '/ssoft/spack/external/CFD++/2016.05/mlib/mcfd.16.1/html')  # noqa: E501
        run_env.set('MCFD_GUIOPT1', 'MCFD_GUI_TNEQC')
        run_env.set('MCFD_TOGL', 'yes')
        run_env.set('TCL_LIBRARY', '/ssoft/spack/external/CFD++/2016.05/mlib/tcltk8/lib/tcl8.0')  # noqa: E501
        run_env.set('TK_LIBRARY', '/ssoft/spack/external/CFD++/2016.05/mlib/tcltk8/lib/tk8.0')  # noqa: E501
        run_env.set('MPATH', '/ssoft/spack/external/CFD++/2016.05/mbin')  # noqa: E501
