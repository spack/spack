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
# pack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SentieonGenomics(Package):
    """Sentieon provides complete solutions for secondary DNA analysis.
    Our software improves upon BWA, GATK, Mutect, and Mutect2 based pipelines.
    The Sentieon tools are deployable on any CPU-based computing system.
    Please set the path to the sentieon server with:
    export SENTIEON_LICENSE=[FQDN]:[PORT]"""

    homepage = "https://www.sentieon.com/"
    url      = "file://{0}/sentieon-genomics-201808.01.tar.gz".format(os.getcwd())

    version('201808.01', sha256='6d77bcd5a35539549b28eccae07b19a3b353d027720536e68f46dcf4b980d5f7')

    # Licensing.
    license_require = True
    license_vars = ['SENTIEON_LICENSE']

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('doc', prefix.doc)
        install_tree('etc', prefix.etc)
        install_tree('lib', prefix.lib)
        install_tree('libexec', prefix.libexec)
        install_tree('share', prefix.share)
