# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility module for dealing with Windows Registry.
"""

import os
import sys

is_windows = sys.platform == "win32"
if is_windows:
    import winreg

    # we alias all the HKEY constants to avoid needing to import winreg
    # where we use this registry interface as importing winreg involves the
    # messy import we see above.
    # any references to these constants should be made only after confirming
    # the codeblock will ONLY be run on Windows
    HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
    HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
    HKEY_USERS = winreg.HKEY_USERS
    HKEY_LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
    HKEY_CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG
    HKEY_PERFORMANCE_DATA = winreg.HKEY_PERFORMANCE_DATA


class RegistryValue(object):
    """
    Class defining a Windows registry entry
    """

    def __init__(self, name, value, parent_key):
        self.path = name
        self.value = value
        self.key = parent_key


class RegistryKey(object):
    """
    Class wrapping a Windows registry key
    """

    def __init__(self, name, handle):
        self.path = name
        self.name = os.path.split(name)[-1]
        self.handle = handle
        self._keys = []
        self._values = {}

    @property
    def values(self):
        """Returns all subvalues of this key as RegistryValue objects in dictionary
        of value name : RegistryValue object
        """
        self.gather_value_info()
        return self._values

    @property
    def subkeys(self):
        """Returns list of all subkeys of this key as RegistryKey objects"""
        self.gather_subkey_info()
        return self._keys

    def gather_subkey_info(self):
        """Composes all subjeys into a list for access"""
        if self._keys:
            return
        sub_keys, _, _ = winreg.QueryInfoKey(self.handle)
        for i in range(sub_keys):
            sub_name = winreg.EnumKey(self.handle, i)
            sub_handle = winreg.OpenKeyEx(self.handle, sub_name, access=winreg.KEY_READ)
            self._keys.append(RegistryKey(os.path.join(self.name, sub_name), sub_handle))

    def gather_value_info(self):
        """Compose all values for this key into a dict of form value name: RegistryValue Object"""
        if self._values:
            return
        _, values, _ = winreg.QueryInfoKey(self.handle)
        for i in range(values):
            value_name, value_data, _ = winreg.EnumValue(self.handle, i)
            self._values[value_name] = RegistryValue(value_name, value_data, self.handle)

    def get_subkey(self, sub_key):
        """Returns subkey of name sub_key in a RegistryKey objects"""
        return RegistryKey(
            os.path.join(self.path, sub_key),
            winreg.OpenKeyEx(self.handle, sub_key, access=winreg.KEY_READ),
        )

    def get_value(self, val_name):
        """Returns value associated with this key in RegistryValue object"""
        return RegistryValue(val_name, winreg.QueryValue(self.handle, val_name), self.handle)


class WindowsRegistry(object):
    """
    Interface to provide access, querying, and searching to Windows registry entries.
    This class represents a single key entrypoint into the Windows registry
    and provides an interface to this key's values, its subkeys, and those subkey's values.
    This class cannot be used to move freely about the registry, only subkeys/values of
    the root key used to instantiate this class.
    """

    def __init__(self, key, root_string=winreg.HKEY_CLASSES_ROOT):
        """Constructs a Windows Registry entrypoint to key provided
        root_string should be an already open root key or an hkey constant if provided

        Args:
            key (str): registry key to provide root for registry key for this clas
            root_string: Already open registry key or HKEY constant to provide access into
                         the Windows registry. Registry access requires an already open key
                         to get an entrypoint, the HKEY constants are always open, or an already
                         open key can be used instead.
        """
        if not is_windows:
            raise RuntimeError(
                "Cannot instantiate Windows Registry class on non Windows platforms"
            )
        self.key = key
        self.root = root_string
        try:
            self.reg = RegistryKey(
                os.path.join(self.root, self.key),
                winreg.OpenKeyEx(self.root_string, self.key, access=winreg.KEY_READ),
            )
        except FileNotFoundError as e:
            if e.winerror == 2:
                self.reg = None
            else:
                raise e

    def get_value(self, value_name):
        return self.reg.get_value(value_name)

    def get_subkey(self, subkey_name):
        return self.reg.get_subkey(subkey_name)

    def _traverse_subkeys(self, stop_condition):
        """Perform simple BFS of subkeys, returning the key
        that successfully triggers the stop condition.
        Args:
            stop_condition: lambda or function pointer that takes a single argument
                            a key and returns a boolean value based on that key
        Return:
            the key if stop_condition is triggered, or None if not
        """
        queue = self.reg.subkeys
        for key in queue:
            if stop_condition(key):
                return key
            queue.extend(key.subkeys)
        return None

    def find_subkey(self, subkey_name, recursive=True):
        """If non recursive, this method is the same as get subkey with error handling
        Otherwise perform a BFS of subkeys until desired key is found
        Returns None or RegistryKey object corresponding to requested key name

        Args:
            subkey_name (str): string representing subkey to be searched for
            recursive (bool): optional argument, if True, subkey need not be a direct
                                sub key of this registry entry, and this method will
                                search all subkeys recursively.
                                Default is True
        Return:
            the desired subkey as a RegistryKey object, or none
        """
        if not recursive:
            try:
                self.get_subkey(subkey_name)
            except FileNotFoundError as e:
                if e.winerror == 2:
                    return None
                else:
                    raise e
        else:
            return self._traverse_subkeys(lambda x: x.name == subkey_name)

    def find_value(self, val_name, recursive=True):
        """
        If non recursive, return RegistryValue object corresponding to name

        Args:
            val_name (str): name of value desired from registry
            recursive (bool): optional argument, if True, the registry is searched recursively
                              for the value of name val_name, else only the current key is searched
        Return:
            The desired registry value as a RegistryValue object if it exists, otherwise, None
        """
        if not recursive:
            try:
                self.get_value(val_name)
            except FileNotFoundError as e:
                if e.winerror == 2:
                    return None
                else:
                    raise e
        else:
            key = self._traverse_subkeys(lambda x: val_name in x.values)
            return key if not key else key.values[val_name]


def open_key(root, subkey):
    """Returns registry key handle derived from root and its subkey
    root can be either a WindowsRegistry or RegistryKey object, or an existing
    PyHKEY object. If it is the former, a RegistryKey is returned, otherwise,
    another PyHKEY.
    """
    if type(root) == WindowsRegistry or type(root) == RegistryKey:
        return root.get_subkey(subkey)
    return winreg.OpenKeyEx(root, subkey, access=winreg.KEY_READ)


def get_value(root, value):
    """
    Returns registry value of name `value` associated with the key `root`
    `root` must be an already open RegistryKey object or PyHKEY object
    """
    if type(root) == WindowsRegistry or type(root) == RegistryKey:
        return root.get_value(value)
    return winreg.QueryValue(root, value)
