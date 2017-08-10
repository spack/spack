##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Signalp(Package):
    """SignalP predicts the presence and location of signal peptide cleavage
       sites in amino acid sequences from different organisms: Gram-positive
       bacteria, Gram-negative bacteria, and eukaryotes.

       Note: A manual download is required for SignalP.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.example.com"

    version('4.1f', 'a9aeb66259202649c959846f3f4d9744')

    def url_for_version(self, version):
        return "file://{0}/signalp-{1}.Linux.tar.gz".format(os.getcwd(), version)

    depends_on('perl', type=('build', 'run'))
    depends_on('gnuplot')

    phases = ['edit', 'install']

    def edit(self, spec, prefix):
        edit = FileFilter('signalp')
        edit.filter('ENV{SIGNALP} = \'/usr/cbs/bio/src/signalp-4.1\'',
                    'ENV{SIGNALP} = \'%s\'' % prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.share.man)
        install('signalp', prefix)
        install('signalp.1', prefix.share.man)
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('syn', prefix.syn)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix)
