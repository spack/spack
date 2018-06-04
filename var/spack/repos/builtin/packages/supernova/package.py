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


class Supernova(Package):
    """Supernova is a software package for de novo assembly from Chromium
    Linked-Reads that are made from a single whole-genome library from an
    individual DNA source.

    A key feature of Supernova is that it creates diploid assemblies, thus
    separately representing maternal and paternal chromosomes over very long
    distances. Almost all other methods instead merge homologous chromosomes
    into single incorrect 'consensus' sequences. Supernova is the only
    practical method for creating diploid assemblies of large genomes.

    To install this package, you will need to go to the supernova download
    page of supernova, register with your email address and download
    supernova yourself. Spack will search your current directory for the
    download file. Alternatively, add this file yo a mirror so that Spack
    can find it. For instructions on how to set up a mirror, see
    http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/welcome"

    version('2.0.1', '3697ce043c798fcb672fe0a66c56d6f0')

    depends_on('bcl2fastq2')

    def url_for_version(self, version):
        return "file://{0}/supernova-{1}.tar.gz".format(os.getcwd(), version)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix)

    def install(self, spec, prefix):
        rm = which('rm')
        # remove the broken symlinks
        rm('anaconda-cs/2.2.0-anaconda-cs-c7/lib/libtcl.so',
            'anaconda-cs/2.2.0-anaconda-cs-c7/lib/libtk.so')
        install_tree('.', prefix)
