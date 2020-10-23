# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openipmi(AutotoolsPackage):
    """The Open IPMI project aims to develop an open code base
    to allow access to platform information using Intelligent
    Platform Management Interface (IPMI)."""

    homepage = "https://sourceforge.net/projects/openipmi/"
    url      = "https://sourceforge.net/projects/openipmi/files/OpenIPMI%202.0%20Library/OpenIPMI-2.0.29.tar.gz"

    version('2.0.28', sha256='8e8b1de2a9a041b419133ecb21f956e999841cf2e759e973eeba9a36f8b40996')
    version('2.0.27', sha256='f3b1fafaaec2e2bac32fec5a86941ad8b8cb64543470bd6d819d7b166713d20b')

    depends_on('popt')
    depends_on('python')
    depends_on('termcap')
    depends_on('ncurses')

    def configure_args(self):
        args = ['LIBS=' + self.spec['ncurses'].libs.link_flags]
        return args

    def install(self, spec, prefix):
        make('install', parallel=False)
