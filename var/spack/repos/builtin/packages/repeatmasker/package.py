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
import inspect


class Repeatmasker(Package):
    """RepeatMasker is a program that screens DNA sequences for interspersed
       repeats and low complexity DNA sequences."""

    homepage = "http://www.repeatmasker.org"
    url      = "http://www.repeatmasker.org/RepeatMasker-open-4-0-7.tar.gz"

    version('4.0.7', '4dcbd7c88c5343e02d819f4b3e6527c6')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-text-soundex', type=('build', 'run'))
    depends_on('hmmer')
    depends_on('ncbi-rmblastn')
    depends_on('trf')

    def url_for_version(self, version):
        url = 'http://www.repeatmasker.org/RepeatMasker-open-{0}.tar.gz'
        return url.format(version.dashed)

    def install(self, spec, prefix):
        # Config questions consist of:
        #
        # <PRESS ENTER TO CONTINUE>
        # Enter perl path
        # Enter where repeatmasker is being configured from
        # Enter trf path
        # Add a Search Engine:
        #    1. CrossMatch
        #    2. RMBlast - NCBI Blast with RepeatMasker extensions
        #    3. WUBlast/ABBlast (required by DupMasker)
        #    4. HMMER3.1 & DFAM
        #    5. Done
        # Enter RMBlast path
        # Do you want RMBlast to be your default search engine for
        #    Repeatmasker? (Y/N)
        # Add a Search Engine: Done

        config_answers = ['\n', '%s\n' % self.spec['perl'].command.path,
                          '%s\n' % self.stage.source_path,
                          '%s\n' % self.spec['trf'].prefix.bin.trf, '2\n',
                          '%s\n' % self.spec['ncbi-rmblastn'].prefix.bin,
                          'Y\n', '5\n']

        config_answers_filename = 'spack-config.in'

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            inspect.getmodule(self).perl('configure', input=f)

        install_tree('.', prefix.bin)
