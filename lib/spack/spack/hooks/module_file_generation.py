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
import spack.modules
import spack.modules.common
import llnl.util.tty as tty

try:
    enabled = spack.config.get('modules:enable')
except KeyError:
    tty.debug('NO MODULE WRITTEN: list of enabled module files is empty')
    enabled = []


def _for_each_enabled(spec, method_name):
    """Calls a method for each enabled module"""
    for name in enabled:
        generator = spack.modules.module_types[name](spec)
        try:
            getattr(generator, method_name)()
        except RuntimeError as e:
            msg = 'cannot perform the requested {0} operation on module files'
            msg += ' [{1}]'
            tty.warn(msg.format(method_name, str(e)))


post_install = lambda spec: _for_each_enabled(spec, 'write')
post_uninstall = lambda spec: _for_each_enabled(spec, 'remove')
