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


class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: The PGI compilers are licensed software. You will need to create
    an account on the PGI homepage and download PGI yourself. Once the download
    finishes, rename the file (which may contain information such as the
    architecture) to the format: pgi-<version>.tar.gz. Spack will search your
    current directory for a file of this format. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.pgroup.com/"

    version('16.10', '9bb6bfb7b1052f9e6a45829ba7a24e47')
    version('16.5',  'a40e8852071b5d600cb42f31631b3de1')
    version('16.3',  '618cb7ddbc57d4e4ed1f21a0ab25f427')
    version('15.7',  '84a689217b17cdaf78c39270c70bea5d')

    variant('network', default=True,
            description="Perform a network install")
    variant('single',  default=False,
            description="Perform a single system install")
    variant('nvidia',  default=False,
            description="Enable installation of optional NVIDIA components")
    variant('amd',     default=False,
            description="Enable installation of optional AMD components")
    variant('java',    default=False,
            description="Enable installation of Java Runtime Environment")
    variant('mpi',     default=False,
            description="Enable installation of Open MPI")

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['license.dat']
    license_vars = ['PGROUPD_LICENSE_FILE', 'LM_LICENSE_FILE']
    license_url = 'http://www.pgroup.com/doc/pgiinstall.pdf'

    def url_for_version(self, version):
        return "file://{0}/pgilinux-20{1}-{2}-x86_64.tar.gz".format(
            os.getcwd(), version.up_to(1), version.joined)

    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['PGI_SILENT'] = "true"
        os.environ['PGI_ACCEPT_EULA'] = "accept"
        os.environ['PGI_INSTALL_DIR'] = prefix

        if '+network' in spec and '~single' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "network"
            os.environ['PGI_INSTALL_LOCAL_DIR'] = "%s/%s/share_objects" % \
                (prefix, self.version)
        elif '+single' in spec and '~network' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "single"
        else:
            msg  = 'You must choose either a network install or a single '
            msg += 'system install.\nYou cannot choose both.'
            raise RuntimeError(msg)

        if '+nvidia' in spec:
            os.environ['PGI_INSTALL_NVIDIA'] = "true"

        if '+amd' in spec:
            os.environ['PGI_INSTALL_AMD'] = "true"

        if '+java' in spec:
            os.environ['PGI_INSTALL_JAVA'] = "true"

        if '+mpi' in spec:
            os.environ['PGI_INSTALL_MPI'] = "true"

        # Run install script
        os.system("./install")
