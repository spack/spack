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
import os
import grp
from spack.package_prefs import get_package_permissions_mask, get_package_group


def forall_files(path, fn, args):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            fn(os.path.join(root, d), *args)
        for f in files:
            fn(os.path.join(root, f), *args)
    fn(path, *args)


def chmod_mask(entry, mask):
    mode = os.stat(entry).st_mode
    mode &= mask
    os.chmod(entry, mode)


def post_install(spec):
    if not spec.external:
        perms_mask = get_package_permissions_mask(spec)
        group = get_package_group(spec)

        forall_files(spec.prefix, chmod_mask, [perms_mask])

        if group:
            gid = grp.getgrnam(group).gr_gid
            forall_files(spec.prefix, os.chown, [-1, gid])
