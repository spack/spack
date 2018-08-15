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


class Tcsh(AutotoolsPackage):
    """Tcsh is an enhanced but completely compatible version of csh, the C
    shell. Tcsh is a command language interpreter which can be used both as
    an interactive login shell and as a shell script command processor. Tcsh
    includes a command line editor, programmable word completion, spelling
    correction, a history mechanism, job control and a C language like
    syntax."""

    homepage = "http://www.tcsh.org/"
    url      = "ftp://ftp.astron.com/pub/tcsh/tcsh-6.20.00.tar.gz"

    version('6.20.00', '59d40ef40a68e790d95e182069431834')

    def fedora_patch(commit, file, **kwargs):  # noqa
        prefix = 'https://src.fedoraproject.org/rpms/tcsh/raw/{0}/f/'.format(commit)
        patch('{0}{1}'.format(prefix, file), **kwargs)

    # Upstream patches
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-000-add-all-flags-for-gethost-build.patch',       when='@6.20.00', sha256='f8266916189ebbdfbad5c2c28ac00ed25f07be70f054d9830eb84ba84b3d03ef')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-001-delay-arginp-interpreting.patch',             when='@6.20.00', sha256='57c7a9b0d94dd41e4276b57b0a4a89d91303d36180c1068b9e3ab8f6149b18dd')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-002-type-of-read-in-prompt-confirm.patch',        when='@6.20.00', sha256='837a6a82f815c0905cf7ea4c4ef0112f36396fc8b2138028204000178a1befa5')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-003-fix-out-of-bounds-read.patch',                when='@6.20.00', sha256='f973bd33a7fd8af0002a9b8992216ffc04fdf2927917113e42e58f28b702dc14')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-004-do-not-use-old-pointer-tricks.patch',         when='@6.20.00', sha256='333e111ed39f7452f904590b47b996812590b8818f1c51ad68407dc05a1b18b0')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-005-reset-fixes-numbering.patch',                 when='@6.20.00', sha256='d1b54b5c5432faed9791ffde813560e226896a68fc5933d066172bcf3b2eb8bd')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-006-cleanup-in-readme-files.patch',               when='@6.20.00', sha256='b4e7428ac6c2918beacc1b73f33e784ac520ef981d87e98285610b1bfa299d7b')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-007-look-for-tgetent-in-libtinfo.patch',          when='@6.20.00', sha256='e6c88ffc291c9d4bda4d6bedf3c9be89cb96ce7dc245163e251345221fa77216')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-008-guard-ascii-only-reversion.patch',            when='@6.20.00', sha256='7ee195e4ce4c9eac81920843b4d4d27254bec7b43e0b744f457858a9f156e621')
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-009-fix-regexp-for-backlash-quoting-tests.patch', when='@6.20.00', sha256='d2358c930d5ab89e5965204dded499591b42a22d0a865e2149b8c0f1446fac34')

    # Downstream patches
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-manpage-memoryuse.patch', sha256='3a4e60fe56a450632140c48acbf14d22850c1d72835bf441e3f8514d6c617a9f')  # noqa: E501

    depends_on('ncurses')

    @run_after('install')
    def link_csh(self):
        symlink('tcsh', '{0}/csh'.format(self.prefix.bin))
        symlink('tcsh.1', '{0}/csh.1'.format(self.prefix.share.man.man1))
