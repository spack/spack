##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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

    def fedora_patch(commit, file, **kwargs):
        prefix = 'https://src.fedoraproject.org/rpms/tcsh/raw/{0}/f/'.format(commit)
        patch('{0}{1}'.format(prefix, file), **kwargs)

    # Upstream patches
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-000-add-all-flags-for-gethost-build.patch', when='@6.20.00', md5='05f85110bf2dd17324fc9825590df63e')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-001-delay-arginp-interpreting.patch', when='@6.20.00', md5='7df17b51be5c24bc02f854f3b4237324')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-002-type-of-read-in-prompt-confirm.patch', when='@6.20.00', md5='27941364ec07e797b533902a6445e0de')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-003-fix-out-of-bounds-read.patch', when='@6.20.00', md5='da300b7bf28667ee69bbdc5219f8e0b3')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-004-do-not-use-old-pointer-tricks.patch', when='@6.20.00', md5='702a0011e96495acb93653733f36b073')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-005-reset-fixes-numbering.patch', when='@6.20.00', md5='8a0fc5b74107b4d7ea7b10b1d6aebe9d')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-006-cleanup-in-readme-files.patch', when='@6.20.00', md5='2c8fec7652af53229eb22535363e9eac')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-007-look-for-tgetent-in-libtinfo.patch', when='@6.20.00', md5='69eacbbe9d9768164f1272c303df44aa')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-008-guard-ascii-only-reversion.patch', when='@6.20.00', md5='0415789a4804cf6320cc83f5c8414a63')  # noqa: E501
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-009-fix-regexp-for-backlash-quoting-tests.patch', when='@6.20.00', md5='90b3f10eb744c2b26155618d8232a4e9')  # noqa: E501

    # Downstream patches
    fedora_patch('8a6066c901fb4fc75013dd488ba958387f00c74d', 'tcsh-6.20.00-manpage-memoryuse.patch', md5='1fd35c430992aaa52dc90261e331acd5')  # noqa: E501

    depends_on('ncurses')

    @run_after('install')
    def link_csh(self):
        symlink('tcsh', '{0}/csh'.format(self.prefix.bin))
        symlink('tcsh.1', '{0}/csh.1'.format(self.prefix.share.man.man1))
