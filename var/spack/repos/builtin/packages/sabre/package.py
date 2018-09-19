##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Sabre(MakefilePackage):
    """Sabre is a tool that will demultiplex barcoded reads into separate
       files. It will work on both single-end and paired-end data in fastq
       format. It simply compares the provided barcodes with each read and
       separates the read into its appropriate barcode file, after stripping
       the barcode from the read (and also stripping the quality values of
       the barcode bases). If a read does not have a recognized barcode,
       then it is put into the unknown file.
    """

    homepage = "https://github.com/najoshi/sabre"
    git      = "https://github.com/najoshi/sabre.git"

    version('2013-09-27', commit='039a55e500ba07b7e6432ea6ec2ddcfb3471d949')

    depends_on('zlib')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('sabre', prefix.bin)
