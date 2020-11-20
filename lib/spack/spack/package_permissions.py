# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import grp
import os
import stat

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.config as cfg


#: The format for specifying the key to specific spec permissions in
#: packages.yaml files.
permissions_key = 'packages:{0}:permissions:{1}'

#: Column width for reporting group differences
group_width = 20

#: Column width for reporting permission differences
perm_width = 9


def _add_gid_bit(perms):
    """Adds the GID bit for directories if group permissions are on.

    Args
        perms (int): the appropriate directory stat permissions or mode
    """
    if perms & stat.S_IRWXG and cfg.get('config:allow_sgid', True):
        perms |= stat.S_ISGID
    return perms


def _check_perms(path, perms, group, trim='', check_exists=False):
    """Checks permissions for the specified path against those given.

    Args:
        path (str): path whose permissions are to be checked
        perms (int): the appropriate stat permissions or mode
        group (str): the appropriate group name or empty string if the group
            option does not apply
        trim (str): root path to trim off of the output path
        check_exists (bool): ``True`` if the path existence should be checked;
            otherwise, skip the existence check

    Returns: (bool) ``True`` if match configuration, ``False`` otherwise
    """
    if check_exists and not os.path.exists(path):
        tty.warn('Cannot check permissions on missing path {0}'
                 .format(path))
        return False

    status = os.stat(path)

    trim = trim if not trim else \
        '{0}{1}'.format(trim, os.sep)

    errs = ['', '', '']

    # Check the path's group.
    name = group
    if group:
        name, _, _, _ = grp.getgrgid(status.st_gid)
        if group != name:
            errs[0] = name.center(group_width)
        else:
            errs[0] = group.center(group_width)

    # Check the path's permissions.
    mode = status.st_mode
    if mode != perms:
        # Only want the ugo values of the mode and permissions
        errs[1] = oct(mode)[-3:].center(perm_width)
        errs[2] = oct(perms)[-3:].center(perm_width)
    else:
        errs[1] = errs[2] = ' ' * perm_width

    if name != group or mode != perms:
        name = '.' if trim and path == trim else path.replace(trim, '')
        print('{0}: {1}'.format(': '.join(errs), name))
        return False

    return True


def _process_permissions(path, spec, update, contents):
    """
    Permissions for the path and, optionally contents for directories, are
    either updated or checked against those specified in the configuration
    (i.e., the packages.yaml file).

    Permissions are determined based on the (packages.yaml) configuration
    that applies to the spec.

    Args:
        path (str): path whose permissions are being
        spec (Spec or None): spec instance or None if want all permissions
        update (bool): ``True`` to set permissions, ``False`` to check them
        contents (bool): ``True`` to process the contents of the
            and files and ``False`` to apply the permissions only to the
            specified directory

    Returns:  (bool) ``True`` for success, ``False`` otherwise
    """
    if not os.path.exists(path):
        tty.warn('Cannot process permissions for missing path {0}'
                 .format(path))
        return

    func = _set_perms if update else _check_perms

    group = get_package_group(spec)
    perms = get_package_permissions(spec)
    dir_perms = _add_gid_bit(perms)

    is_dir = os.path.isdir(path)
    path_perms = dir_perms if is_dir else perms

    func(path, path_perms, group, path)

    # We're done if the path is a file OR we don't need to process
    # permissions for the directory's contents.
    if not (is_dir and contents):
        return

    for root, dirs, files in os.walk(path, topdown=True):
        for d in dirs:
            dir_name = os.path.join(root, d)
            success = func(dir_name, dir_perms, group, path)
            if not success:
                dirs.remove(d)
        for f in files:
            file_name = os.path.join(root, f)
            func(file_name, perms, group, path)
        if path in dirs:
            dirs.remove(path)


def _set_perms(path, perms, group, trim='', check_exists=False):
    """Set permissions for the specified path to the given permissions.

    Args:
        path (str): path whose permissions are to be set
        perms (int): the appropriate stat permissions or mode
        group (str): the appropriate group name or empty string if the group
            option does not apply
        trim (str): root path to trim off of the output path
        check_exists (bool): ``True`` if the path existence should be checked;
            otherwise, skip the existence check

    Returns: (bool) ``True`` if successful, ``False`` otherwise
    """
    if check_exists and not os.path.exists(path):
        tty.warn('Cannot set permissions on missing path {0}'
                 .format(path))
        return False

    # Set the path's group.
    if group:
        fs.chgrp(path, group)

    # Set the path's permissions.
    #
    # This has to be done *after* any group change because doing so removes
    # the SGID bit on directories.
    mode = os.stat(path).st_mode
    if mode != perms:
        os.chmod(path, perms)

    return True


def check_permissions(path, spec, contents=True):
    """Checks permissions against those expected by the configuration."""
    print('\nChecking Permissions for {0}\n'.format(path))
    print('{0}: {1}: {2}: {3}'.format(
        'Actual Group'.center(group_width),
        'Act Perms'.center(perm_width),
        'Exp Perms'.center(perm_width),
        'Path'))
    _process_permissions(path, spec, False, contents)


def update_permissions(path, spec, contents=True):
    """Updates permissions using those expected by the configuration."""
    _process_permissions(path, spec, True, contents)


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
    return _add_gid_bit(get_package_permissions(spec))


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
            readable = cfg.get(permissions_key.format(name, 'read'), '')
            if readable:
                break
        except AttributeError:
            readable = 'world'

    # Get write permissions level
    for name in names:
        try:
            writable = cfg.get(permissions_key.format(name, 'write'), '')
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
            raise cfg.ConfigError('Writable permissions may not be more' +
                                  ' permissive than readable permissions.\n' +
                                  '      Violating package is {0}'
                                  .format(spec.name))
        perms |= stat.S_IWGRP
    if writable == 'world':
        if readable != 'world':
            raise cfg.ConfigError('Writable permissions may not be more' +
                                  ' permissive than readable permissions.\n' +
                                  '      Violating package is {0}'
                                  .format(spec.name))
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
            group = cfg.get(permissions_key.format(name, 'group'), '')
            if group:
                break
        except AttributeError:
            group = ''
    return group
