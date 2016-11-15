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
import glob
import os


class StarCcmPlus(Package):
    """STAR-CCM+ (Computational Continuum Mechanics) CFD solver."""

    homepage = "http://mdx.plm.automation.siemens.com/star-ccm-plus"

    version('11.06.010_02', 'd349c6ac8293d8e6e7a53533d695588f')

    variant('docs', default=False, description='Install the documentation')

    # Licensing
    license_required = True
    license_vars = ['CDLMD_LICENSE_FILE', 'LM_LICENSE_FILE']

    def url_for_version(self, version):
        return "file://{0}/STAR-CCM+{1}_linux-x86_64.tar.gz".format(
            os.getcwd(), version)

    def install(self, spec, prefix):
        # There is a known issue with the LaunchAnywhere application.
        # Specifically, it cannot handle long prompts or prompts
        # containing special characters and backslashes. It results in
        # the following error message:
        #
        # An internal LaunchAnywhere application error has occured and this
        # application cannot proceed. (LAX)
        #
        # Stack Trace:
        #     java.lang.IllegalArgumentException: Malformed \uxxxx encoding.
        #     at java.util.Properties.loadConvert(Unknown Source)
        #     at java.util.Properties.load0(Unknown Source)
        #     at java.util.Properties.load(Unknown Source)
        #     at com.zerog.common.java.util.PropertiesUtil.loadProperties(
        #         Unknown Source)
        #     at com.zerog.lax.LAX.<init>(Unknown Source)
        #     at com.zerog.lax.LAX.main(Unknown Source)
        #
        # https://www.maplesoft.com/support/faqs/detail.aspx?sid=35272
        env['PS1'] = '>'
        env['PROMPT_COMMAND'] = ''

        installer = Executable(glob.glob('*.bin')[0])

        installer(
            '-i', 'silent',
            '-DINSTALLDIR={0}'.format(prefix),
            '-DINSTALLFLEX=false',
            '-DADDSYSTEMPATH=false',
            '-DNODOC={0}'.format('false' if '+docs' in spec else 'true')
        )
