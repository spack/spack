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
import os
import llnl.util.filesystem as fs
from datetime import datetime

class Stata(Package):
    """STATA is a general-purpose statistical software package developed
       by StataCorp."""

# Known limitations of this installer:
# * STATA requires libpng v12 that ships with EL enterprise distros. Spack
#   provides version 16 with a "depends_on('libpng')" and STATA checks
#   explicitly for 12. So until 12 is packaged, `yum install libpng`. :-)
#
# * This really only installs the command line version of the program. To
#   install GUI support there are extra packages needed that I can't easily test
#   right now (should be installable via yum too as a temp workaround):
#   libgtk-x11-2.0.so libgdk-x11-2.0.so libatk-1.0.so libgdk_pixbuf-2.0.so
#
# * There are two popular environment variables that can be set, but vary from
#   place to place, so future enhancement maybe to support STATATMP and TMPDIR.
#
# * I haven't tested any installer version but 15.

    homepage = "https://www.stata.com/"
    #url      = "stata"

    version('15', '2486f4c7db1e7b453004c7bd3f8da40ba1e30be150613065c7b82b1915259016')

    # STATA is downloaded from user/pass protected ftp as Stata15Linux64.tar.gz
    def url_for_version(self, version):
        return "file://{0}/Stata{1}Linux64.tar.gz".format(os.getcwd(), version)

    # STATA is simple and needs really just the PATH set.
    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix)

    # Extracting the file provides the following:
    # ./unix/
    # ./unix/linux64/
    # ./unix/linux64/docs.taz
    # ./unix/linux64/setrwxp
    # ./unix/linux64/ado.taz
    # ./unix/linux64/inst2
    # ./unix/linux64/base.taz
    # ./unix/linux64/bins.taz
    # ./license.pdf
    # ./stata15.ico
    # ./install
    #
    # The installation scripts aren't really necessary:
    # ./install is a shell script that sets up the environment.
    # ./unix/linux64/setrwxp is a shell script that ensures permissions.
    # ./unix/linux64/inst2 is the actual installation script.
    #
    # 1. There is a markfile that is the version number. Stata uses this for
    # for doing version checks/updates.
    # echo $(date) > installed.150
    #
    # 2. Then it extracts the tar.gz files: ado.taz base.taz bins.taz docs.taz
    # 
    # 3. It copies installer scripts to root directory
    # cp ./unix/linux64/setrwxp setrwxp
    # cp ./unix/linux64/inst2 inst2
    #
    # 4. Then it checks for proper permissions:
    # chmod 750 setrwxp inst2
    # ./setrwxp now
    #
    # 5. The last step has to be run manually since it is an interactive binary
    # for configuring the license key. Load the module and run:
    # $ stinit

    def install(self, spec, prefix):
        bash = which('bash')
        tar = which('tar')

        # Step 1.
        x=datetime.now()
        file = open("installed.150","w")
        file.write(x.strftime("%a %b %d %H:%M:%S %Z %Y"))
        file.close()

        # Step 2.
        instlist = [ 'ado.taz', 'base.taz', 'bins.taz', 'docs.taz' ]
        for instfile in instlist:
            tar('-x', '-z', '-f', 'unix/linux64/' + instfile)

        # Step 3.
        fs.install('unix/linux64/setrwxp','setrwxp')
        fs.install('unix/linux64/inst2','inst2')

        # Step 4. Since the install script calls out specific permissions and could change
        # in the future (or old versions) I thought it best to just use it.
        bash("./setrwxp","now")

        # The install should now be good to copy into the installation directory.
        #install("installed.150",prefix)
        install_tree(os.getcwd(),prefix)
