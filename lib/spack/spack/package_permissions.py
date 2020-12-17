# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import grp
import os
import stat

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.config as cfg


#: The format for specifying the key to specific spec permissions in
#: packages.yaml files.
permissions_key = 'packages:{0}:permissions:{1}'

#: SetGID-Read-Write permissions mask since those are relevant to package
#: options
srw_perms = (stat.S_ISGID | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) & \
    ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _add_gid_bit(perms):
    """Adds the GID bit for directories if group permissions are on.

    Args
        perms (int): the appropriate directory stat permissions or mode
    """
    if perms & stat.S_IRWXG and cfg.get('config:allow_sgid', True):
        perms |= stat.S_ISGID
    return perms


def _check_perms(path, perms, group):
    """Checks permissions for the specified path against those given.

    Args:
        path (str): path whose permissions are to be checked
        perms (int): the appropriate stat permissions or mode
        group (str): the appropriate group name or empty string if the group
            option does not apply

    Returns: (None or tuple) of (<groups>, <perms>, <path>) where groups and
        perms are formatted as <current>-><expected> and are only returned
        when there is a mismatch
    """
    status = os.stat(path)

    # Check the path's group.
    name = group
    if group:
        name, _, _, _ = grp.getgrgid(status.st_gid)
    gdiff = '' if name == group else '{0}->{1}'.format(name, group)

    # Check the path's permissions, but only look at the ones that can
    # be set by os.chmod().
    mode = stat.S_IMODE(status.st_mode)

    # Ignore execute bits UNLESS add logic to infer need for executable
    # from the file type
    expected = perms & srw_perms
    if os.path.isdir(path):
        expected = _add_gid_bit(expected)
    actual = mode & srw_perms
    if name == group and actual == expected:
        return None

    # Only report ugo
    pdiff = '' if actual == expected else \
        '{0}->{1}'.format(oct(actual), oct(expected))

    return (gdiff, pdiff, path)


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
        contents (bool): ``True`` to process the contents of the directory
            and ``False`` to apply the permissions only to the specified
            directory

    Returns: (list) of (<groups>, <perms>, <path>) where groups and perms
        are formatted as <current>-><expected> and only includes mismatches
    """
    entries = []

    if not os.path.exists(path):
        tty.warn('Cannot process permissions for missing path {0}'
                 .format(path))
        return entries

    func = _set_perms if update else _check_perms

    group = get_package_group(spec)
    perms = get_package_permissions(spec)

    entry = func(path, perms, group)
    if entry:
        entries.append(entry)

    # We're done if the path is a file OR we don't need to process
    # permissions for the directory's contents.
    if not (os.path.isdir(path) and contents):
        return entries

    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        for d in dirs:
            dir_name = os.path.join(root, d)
            entry = func(dir_name, perms, group)
            if entry:
                entries.append(entry)
                dirs.remove(d)
        for f in files:
            file_name = os.path.join(root, f)
            if not os.path.islink(file_name):
                entry = func(file_name, perms, group)
                if entry:
                    entries.append(entry)

    return entries

def _set_perms(path, perms, group):
    """Set permissions for the specified path to the given permissions.

    Args:
        path (str): path whose permissions are to be set
        perms (int): the appropriate stat permissions or mode
        group (str): the appropriate group name or empty string if the group
            option does not apply

    Returns: (bool) ``True`` if successful, ``False`` otherwise
    """
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


def check_permissions(path, spec, contents=True, header=False):
    """Checks permissions against those expected by the configuration.

    Args:
        path (str): path whose permissions are to be checked
        spec (Spec or None): spec instance or None if want all permissions
        contents (bool): ``True`` to process the contents of the
            and files and ``False`` to apply the permissions only to the
            specified directory
        header (bool): ``True`` to output a header before processing
            permissions; ``False`` if the header should not be output
    """
    if header:
        print('\nChecking Permissions...\n\nGroup Diff:Perms Diff')
        tty.colify.colify(['paths(s)'], indent=4)
        print('')

    entries = _process_permissions(path, spec, False, contents)
    if entries:
        org = collections.defaultdict(list)
        for group, perms, path in sorted(entries):
            org['{0}:{1}'.format(group, perms)].append(path)

        for key in sorted(org):
            print(key)
            tty.colify.colify(org[key], indent=4)
            print('')
        print('')

def update_permissions(path, spec, contents=True, header=False):
    """Repairs permissions using those expected by the configuration.

    Args:
        path (str): path whose permissions are to be updated if needed
        spec (Spec or None): spec instance or None if want all permissions
        contents (bool): ``True`` to process the contents of the
            and files and ``False`` to apply the permissions only to the
            specified directory
        header (bool): ``True`` to output a header before processing
            permissions; ``False`` if the header should not be output
    """
    if header:
        print('\nRepairing Permissions...')

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
