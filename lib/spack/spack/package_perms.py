# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import stat

import spack.config as scon


def get_package_dir_permissions(spec):
    """Return the permissions configured for the spec or for ``all`` if no spec

    Include the GID bit if group permissions are on. This makes the group
    attribute sticky for the directory. Package-specific settings take
    precedent over settings for ``all``.

    Args:
        spec (Spec or None): spec instance or None if want all permissions

    Returns:
        perms (int): the appropriate stat permissions or mode
    """
    perms = get_package_permissions(spec)
    if perms & stat.S_IRWXG and scon.get('config:allow_sgid', True):
        perms |= stat.S_ISGID
    return perms


def get_package_permissions(spec):
    """Return the permissions configured for the spec or for ``all`` if no spec

    Package-specific settings take precedence over settings for ``all``.

    Args:
        spec (Spec or None): spec instance or None if want all permissions

    Returns:
        perms (int): the appropriate stat permissions or mode
    """
    names = ['all'] if spec is None else [spec.name, 'all']

    # Get read permissions level
    for name in names:
        try:
            readable = scon.get('packages:%s:permissions:read' % name, '')
            if readable:
                break
        except AttributeError:
            readable = 'world'

    # Get write permissions level
    for name in names:
        try:
            writable = scon.get('packages:%s:permissions:write' % name, '')
            if writable:
                break
        except AttributeError:
            writable = 'user'

    perms = stat.S_IRWXU
    if readable in ('world', 'group'):  # world includes group
        perms |= stat.S_IRGRP | stat.S_IXGRP
    if readable == 'world':
        perms |= stat.S_IROTH | stat.S_IXOTH

    if writable in ('world', 'group'):
        if readable == 'user':
            raise scon.ConfigError('Writable permissions may not be more' +
                                   ' permissive than readable permissions.\n' +
                                   '      Violating package is %s' % spec.name)
        perms |= stat.S_IWGRP
    if writable == 'world':
        if readable != 'world':
            raise scon.ConfigError('Writable permissions may not be more' +
                                   ' permissive than readable permissions.\n' +
                                   '      Violating package is %s' % spec.name)
        perms |= stat.S_IWOTH

    return perms


def get_package_group(spec):
    """Return the unix group associated with the spec or for ``all`` if no spec

    Package-specific settings take precedence over settings for ``all``.

    Args:
        spec (Spec or None): spec instance or None if want all permissions

    Returns:
        group (str): the appropriate group name
    """
    names = ['all'] if spec is None else [spec.name, 'all']

    for name in names:
        try:
            group = scon.get('packages:%s:permissions:group' % name, '')
            if group:
                break
        except AttributeError:
            group = ''
    return group
