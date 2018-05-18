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
import os.path


class Snpeff(Package):
    """SnpEff is a variant annotation and effect prediction tool. It
    annotates and predicts the effects of genetic variants (such as
    amino acid changes)."""

    homepage = "http://snpeff.sourceforge.net/"
    url      = "https://kent.dl.sourceforge.net/project/snpeff/snpEff_latest_core.zip"

    version('2017-11-24', '1fa84a703580a423e27f1e14a945901c')

    depends_on('jdk', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('snpEff', prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "snpEff.sh")
        script = prefix.bin.snpEff
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'backup': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('snpEff.jar', join_path(prefix.bin, 'snpEff.jar'),
                    script, **kwargs)
