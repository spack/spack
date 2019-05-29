# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
from datetime import datetime


class Stata(Package):
    """STATA is a general-purpose statistical software package developed
       by StataCorp."""

# Known limitations of this installer:
# * This really only installs the command line version of the program. To
#   install GUI support there are extra packages needed that I can't easily
#   test right now (should be installable via yum as a temp workaround):
#   libgtk-x11-2.0.so libgdk-x11-2.0.so libatk-1.0.so libgdk_pixbuf-2.0.so
#   Those libraries appear to be provided by: pango gdk-pixbuf2 gtk2
#
# * There are two popular environment variables that can be set, but vary from
#   place to place, so future enhancement maybe to support STATATMP and TMPDIR.
#
# * I haven't tested any installer version but 15.

    homepage = "https://www.stata.com/"
    # url      = "stata"

    version('15', '2486f4c7db1e7b453004c7bd3f8da40ba1e30be150613065c7b82b1915259016')

    # V15 depends on libpng v12 and fails with other versions of libpng
    depends_on('libpng@1.2.57')

    # STATA is downloaded from user/pass protected ftp as Stata15Linux64.tar.gz
    def url_for_version(self, version):
        return "file://{0}/Stata{1}Linux64.tar.gz".format(os.getcwd(), version)

    # STATA is simple and needs really just the PATH set.
    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix)
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['libpng'].prefix.lib)

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
        x = datetime.now()
        with open("installed.150", "w") as fh:
            fh.write(x.strftime("%a %b %d %H:%M:%S %Z %Y"))

        # Step 2.
        instlist = ['ado.taz', 'base.taz', 'bins.taz', 'docs.taz']
        for instfile in instlist:
            tar('-x', '-z', '-f', 'unix/linux64/' + instfile)

        # Step 3.
        install('unix/linux64/setrwxp', 'setrwxp')
        install('unix/linux64/inst2', 'inst2')

        # Step 4. Since the install script calls out specific permissions and
        # could change in the future (or old versions) I thought it best to
        # just use it.
        bash("./setrwxp", "now")

        # Install should now be good to copy into the installation directory.
        install_tree('.', prefix)
