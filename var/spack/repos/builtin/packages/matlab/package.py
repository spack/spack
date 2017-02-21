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
import subprocess


class Matlab(Package):
    """MATLAB (MATrix LABoratory) is a multi-paradigm numerical computing
    environment and fourth-generation programming language. A proprietary
    programming language developed by MathWorks, MATLAB allows matrix
    manipulations, plotting of functions and data, implementation of
    algorithms, creation of user interfaces, and interfacing with programs
    written in other languages, including C, C++, C#, Java, Fortran and Python.

    Note: MATLAB is licensed software. You will need to create an account on
    the MathWorks homepage and download MATLAB yourself. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.mathworks.com/products/matlab.html"

    version('R2016b', 'b0e0b688894282139fa787b5a86a5cf7')

    variant('mode', default='interactive', description='Installation mode (interactive, silent, or automated)')
    variant('key',  default='',            description='The file installation key to use')

    # Licensing
    license_required = True
    license_comment  = '#'
    license_files    = ['licenses/license.dat']
    license_vars     = ['LM_LICENSE_FILE']
    license_url      = 'https://www.mathworks.com/help/install/index.html'

    def url_for_version(self, version):
        return "file://{0}/matlab_{1}_glnxa64.zip".format(os.getcwd(), version)

    def configure(self, spec, prefix):
        config = {
            'destinationFolder':   prefix,
            'mode':                spec.variants['mode'].value,
            'fileInstallationKey': spec.variants['key'].value,
            'licensePath':         self.global_license_file
        }

        # Store values requested by the installer in a file
        with open('spack_installer_input.txt', 'w') as inputFile:
            for key in config:
                inputFile.write('{0}={1}\n'.format(key, config[key]))

    def install(self, spec, prefix):
        self.configure(spec, prefix)

        # Run silent installation script
        # Full path required
        inputFile = join_path(self.stage.source_path,
                              'spack_installer_input.txt')
        subprocess.call(['./install', '-inputFile', inputFile])
