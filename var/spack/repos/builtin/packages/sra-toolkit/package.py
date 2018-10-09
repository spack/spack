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


class SraToolkit(Package):
    """The NCBI SRA Toolkit enables reading ("dumping") of sequencing files
       from the SRA database and writing ("loading") files into the .sra
       format."""

    homepage = "https://trace.ncbi.nlm.nih.gov/Traces/sra"
    url      = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2-1/sratoolkit.2.8.2-1-centos_linux64.tar.gz"

    version('2.9.2', sha256='17dbe13aa1ed7955d31e1e76e8b62786e80a77e9ed9d396631162dc3ad8b716d')
    version('2.8.2-1', sha256='b053061aae7c6d00162fe0f514be4128a60365b4b2b5b36e7f4798b348b55cf5')

    def url_for_version(self, version):
        url = 'https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/{0}/sratoolkit.{0}-centos_linux64.tar.gz'
        return url.format(version)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin, symlinks=True)
        install_tree('example', prefix.example)
        install_tree('schema', prefix.schema)
