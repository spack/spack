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


class SspaceStandard(Package):
    """SSPACE standard is a stand-alone program for scaffolding pre-assembled
       contigs using NGS paired-read data

       Note: A manual download is required for SSPACE-Standard.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE"
    url      = "file://{0}/41SSPACE-STANDARD-3.0_linux-x86_64.tar.gz".format(os.getcwd())

    version('3.0', '7e171b4861b9d514e80aafc3d9cdf554')

    depends_on('perl', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('bowtie', prefix.bowtie)
        install_tree('bwa', prefix.bwa)
        install_tree('dotlib', prefix.dotlib)
        install_tree('tools', prefix.tools)
        install('SSPACE_Standard_v{0}.pl'.format(self.version), prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.set('SSPACE_HOME', prefix)
        run_env.prepend_path('PATH', prefix)
