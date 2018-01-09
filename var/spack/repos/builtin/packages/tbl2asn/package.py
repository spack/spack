##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Tbl2asn(Package):
    """Tbl2asn is a command-line program that automates the creation of
    sequence records for submission to GenBank."""

    homepage = "https://www.ncbi.nlm.nih.gov/genbank/tbl2asn2"

    version('25.6', 'acf3575909b4d28aa74dcd46f17c281f', expand=False)

    def url_for_version(self, version):
        return 'https://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/tbl2asn/linux64.tbl2asn.gz'

    def install(self, spec, prefix):
        gunzip = which('gunzip')
        gunzip(self.stage.archive_file)

        # Documentation instructs to remove the platform designation
        install('linux64.tbl2asn', os.path.join(prefix, 'tbl2asn'))
        set_executable(os.path.join(prefix, 'tbl2asn'))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix)
