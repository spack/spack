##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import os
import spack
import spack.spec
import llnl.util.tty as tty
from spack.spec import Spec

def update_symlinks(packages=None):
    all_specs = spack.install_layout.all_specs()
    filtered_specs = None
    if packages:
        filtered_specs = [spec for spec in all_specs if spec.name in packages]
    else:
        filtered_specs = all_specs
    sorted_specs = sorted(filtered_specs, cmp=Spec.__cmp__)
    
    symlinks = {}
    for spec in sorted_specs:
        pkgname = spec.name
        pkglinks = spack.pkgconfig.symlinks_for_pkgname(pkgname)
        formated_pkglinks = [spec.format(link) for link in pkglinks]
        target = spack.install_layout.path_for_spec(spec)

        for link in formated_pkglinks:
            if link in symlinks:
                # A higher-priority spec is already installing a symlink here
                continue

            original_target = None
            try:
                exists = os.path.exists(link)
                lexists = os.path.lexists(link)
                islink = os.path.islink(link)
                if not exists and lexists:
                    original_target = '[dead link]'
                elif not exists:
                    original_target = None
                elif not islink:
                    tty.error("Could not create symlink %s because a real file exists at that location" % link)
                else:
                    original_target = os.readlink(link)
            except exceptions.OSError, e:
                tty.die("Could not access symlink %s for package %s" % link, spec)
            
            symlinks[link] = (target, original_target)

    for link in symlinks:
        targets = symlinks[link]
        target = targets[0]
        original_target = targets[1]
        if target == original_target:
            # The existing symlink points to the correct location
            continue
        if original_target:
            # Remove existing symlinks
            try:
                os.unlink(link)
            except exceptions.OSError, e:
                tty.die("Could not remove existing symlink %s" % link)
        try:
            os.symlink(target, link)
        except exceptions.OSError, e:
            tty.die("Could create symlink %s to %s" % (link, target))
        if original_target:
            tty.msg("Spack updating symlink: %s\n    from: %s\n    to:   %s" % (link, original_target, target))
        else:
            tty.msg("Spack creating symlink %s to %s" % (link, target))
