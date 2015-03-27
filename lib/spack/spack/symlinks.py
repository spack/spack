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
import exceptions
import llnl.util.tty as tty
from spack.spec import Spec
from llnl.util.filesystem import mkdirp

def _all_sorted_specs(packages, uninstalled_specs=None):
    all_specs = spack.install_layout.all_specs()
    filtered_specs = None
    if packages:
        filtered_specs = [spec for spec in all_specs if spec.name in packages]
    else:
        filtered_specs = all_specs
    if uninstalled_specs:
        filtered_specs = [spec for spec in filtered_specs if not spec in uninstalled_specs]
    return sorted(filtered_specs, cmp=Spec.__cmp__)


def _symlinks_for_specs(specs):
    symlinks = {}
    for spec in specs:
        pkglinks = spack.pkgconfig.symlinks_for_spec(spec)
        formated_pkglinks = [spec.format(link) for link in pkglinks]
        target = spack.install_layout.path_for_spec(spec)
        all_links = [(link, target) for link in formated_pkglinks]

        deep_pkglinks = spack.pkgconfig.deep_symlinks_for_spec(spec)
        for link in deep_pkglinks:
            pair = link.split(' ')
            if len(pair) != 2:
                tty.die("Ill-formated deep link '%s' in spack config.  Expected 'link deep_part'." % link)
            all_links.append((spec.format(pair[0]), target + '/' + spec.format(pair[1])))

        for link_pairs in all_links:
            link = link_pairs[0]
            link_target = link_pairs[1]
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
            
            symlinks[link] = (link_target, original_target)
    return symlinks


def _create_symlinks(symlinks, during_uninstall=False):
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
        (head, tail) = os.path.split(link)
        try:
            if not tail:
                tty.die("Symlink %s cannot be a directory" % (link))
            if os.path.isfile(head):
                tty.die("Symlink %s has path component that is not a directory" % (link))
            if not os.path.exists(head):
                mkdirp(head)
        except exceptions.OSError, e:
            tty.die("Could not access directory %s for symlink %s" % (tail, target))
        try:
            os.symlink(target, link)
        except exceptions.OSError, e:
            tty.die("Could create symlink %s to %s" % (link, target))
        if original_target:
            tty.msg("Spack updating symlink: %s\n    from: %s\n    to:   %s" % (link, original_target, target))
        elif during_uninstall:
            tty.msg("Spack updating symlink: %s\n    to: %s" % (link, target))
        else:
            tty.msg("Spack creating symlink: %s\n    to %s" % (link, target))    


def update_symlinks(packages=None):
    sorted_specs = _all_sorted_specs(packages)
    symlinks = _symlinks_for_specs(sorted_specs)
    _create_symlinks(symlinks)


def uninstall_symlinks(uninstalled_packages):
    uninstalled_specs = [pkg.spec for pkg in uninstalled_packages]
    symlinks = _symlinks_for_specs(uninstalled_specs)
    uninstalled_locations = [spack.install_layout.path_for_spec(spec) for spec in uninstalled_specs]
    uninstalled_names = [spec.name for spec in uninstalled_specs]

    for link in symlinks:
        target = symlinks[link][0]
        original_target = symlinks[link][1]
        if target in uninstalled_locations or original_target == '[dead link]':
            try:
                os.unlink(link)
            except exceptions.OSError, e:
                tty.die("Could not remove existing symlink %s" % link)
            tty.msg("Spack removing symlink: %s" % link)
    sorted_specs = _all_sorted_specs(uninstalled_names, uninstalled_specs)
    symlinks = _symlinks_for_specs(sorted_specs)
    _create_symlinks(symlinks, True)


def list_symlinks():
    sorted_specs = _all_sorted_specs(None)
    symlinks = _symlinks_for_specs(sorted_specs)

    for link in symlinks:
        target = symlinks[link][0]
        actual_target = symlinks[link][1]
        print("%s -> %s" % (link, actual_target))
        if target != actual_target:
            tty.warn('Symlink out of date! %s should point to %s' % (link, target))
