# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility module for dealing with Windows Registry.
"""

import os
import sys
from contextlib import contextmanager

from llnl.util import tty

if sys.platform == "win32":
    import winreg


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
        self._handle = handle
        self._keys = []
        self._values = {}

    @property
    def values(self):
        """Returns all subvalues of this key as RegistryValue objects in dictionary
        of value name : RegistryValue object
        """
        self._gather_value_info()
        return self._values

    @property
    def subkeys(self):
        """Returns list of all subkeys of this key as RegistryKey objects"""
        self._gather_subkey_info()
        return self._keys

    @property
    def hkey(self):
        return self._handle

    def __str__(self):
        return self.name

    def _gather_subkey_info(self):
        """Composes all subkeys into a list for access"""
        if self._keys:
            return
        sub_keys, _, _ = winreg.QueryInfoKey(self.hkey)
        for i in range(sub_keys):
            sub_name = winreg.EnumKey(self.hkey, i)
            sub_handle = winreg.OpenKeyEx(self.hkey, sub_name, access=winreg.KEY_READ)
            self._keys.append(RegistryKey(os.path.join(self.path, sub_name), sub_handle))

    def _gather_value_info(self):
        """Compose all values for this key into a dict of form value name: RegistryValue Object"""
        if self._values:
            return
        _, values, _ = winreg.QueryInfoKey(self.hkey)
        for i in range(values):
            value_name, value_data, _ = winreg.EnumValue(self.hkey, i)
            self._values[value_name] = RegistryValue(value_name, value_data, self.hkey)

    def get_subkey(self, sub_key):
        """Returns subkey of name sub_key in a RegistryKey objects"""
        return RegistryKey(
            os.path.join(self.path, sub_key),
            winreg.OpenKeyEx(self.hkey, sub_key, access=winreg.KEY_READ),
        )

    def get_value(self, val_name):
        """Returns value associated with this key in RegistryValue object"""
        return RegistryValue(val_name, winreg.QueryValueEx(self.hkey, val_name)[0], self.hkey)


class _HKEY_CONSTANT(RegistryKey):
    """Subclass of RegistryKey to represent the prebaked, always open registry HKEY constants"""

    def __init__(self, hkey_constant):
        hkey_name = hkey_constant
        # This class is instantiated at module import time
        # on non Windows platforms, winreg would not have been
        # imported. For this reason we can't reference winreg yet,
        # so handle is none for now to avoid invalid references to a module.
        # _handle provides a workaround to prevent null references to self.handle
        # when coupled with the handle property.
        super(_HKEY_CONSTANT, self).__init__(hkey_name, None)

    def _get_hkey(self, key):
        return getattr(winreg, key)

    @property
    def hkey(self):
        if not self._handle:
            self._handle = self._get_hkey(self.path)
        return self._handle


class HKEY(object):
    """
    Predefined, open registry HKEYs
    From the Microsoft docs:
    An application must open a key before it can read data from the registry.
    To open a key, an application must supply a handle to another key in
    the registry that is already open. The system defines predefined keys
    that are always open. Predefined keys help an application navigate in
    the registry."""

    HKEY_CLASSES_ROOT = _HKEY_CONSTANT("HKEY_CLASSES_ROOT")
    HKEY_CURRENT_USER = _HKEY_CONSTANT("HKEY_CURRENT_USER")
    HKEY_USERS = _HKEY_CONSTANT("HKEY_USERS")
    HKEY_LOCAL_MACHINE = _HKEY_CONSTANT("HKEY_LOCAL_MACHINE")
    HKEY_CURRENT_CONFIG = _HKEY_CONSTANT("HKEY_CURRENT_CONFIG")
    HKEY_PERFORMANCE_DATA = _HKEY_CONSTANT("HKEY_PERFORMANCE_DATA")


class WindowsRegistryView(object):
    """
    Interface to provide access, querying, and searching to Windows registry entries.
    This class represents a single key entrypoint into the Windows registry
    and provides an interface to this key's values, its subkeys, and those subkey's values.
    This class cannot be used to move freely about the registry, only subkeys/values of
    the root key used to instantiate this class.
    """

    def __init__(self, key, root_key=HKEY.HKEY_CURRENT_USER):
        """Constructs a Windows Registry entrypoint to key provided
        root_key should be an already open root key or an hkey constant if provided

        Args:
            key (str): registry key to provide root for registry key for this clas
            root_key: Already open registry key or HKEY constant to provide access into
                         the Windows registry. Registry access requires an already open key
                         to get an entrypoint, the HKEY constants are always open, or an already
                         open key can be used instead.
        """
        if sys.platform != "win32":
            raise RuntimeError(
                "Cannot instantiate Windows Registry class on non Windows platforms"
            )
        self.key = key
        self.root = root_key
        self._reg = None

    @contextmanager
    def invalid_reg_ref_error_handler(self):
        try:
            yield
        except FileNotFoundError as e:
            if sys.platform == "win32" and e.winerror == 2:
                tty.debug("Key %s at position %s does not exist" % (self.key, str(self.root)))
            else:
                raise e

    def __bool__(self):
        return self.reg != -1

    def _load_key(self):
        try:
            self._reg = RegistryKey(
                os.path.join(str(self.root), self.key),
                winreg.OpenKeyEx(self.root.hkey, self.key, access=winreg.KEY_READ),
            )
        except FileNotFoundError as e:
            if sys.platform == "win32" and e.winerror == 2:
                self._reg = -1
                tty.debug("Key %s at position %s does not exist" % (self.key, str(self.root)))
            else:
                raise e

    def _valid_reg_check(self):
        if self.reg == -1:
            tty.debug("Cannot perform operation for nonexistent key %s" % self.key)
            return False
        return True

    @property
    def reg(self):
        if not self._reg:
            self._load_key()
        return self._reg

    def get_value(self, value_name):
        """Return registry value corresponding to provided argument (if it exists)"""
        if not self._valid_reg_check():
            raise RegistryError("Cannot query value from invalid key %s" % self.key)
        with self.invalid_reg_ref_error_handler():
            return self.reg.get_value(value_name)

    def get_subkey(self, subkey_name):
        if not self._valid_reg_check():
            raise RegistryError("Cannot query subkey from invalid key %s" % self.key)
        with self.invalid_reg_ref_error_handler():
            return self.reg.get_subkey(subkey_name)

    def get_subkeys(self):
        if not self._valid_reg_check():
            raise RegistryError("Cannot query subkeys from invalid key %s" % self.key)
        with self.invalid_reg_ref_error_handler():
            return self.reg.subkeys

    def get_values(self):
        if not self._valid_reg_check():
            raise RegistryError("Cannot query values from invalid key %s" % self.key)
        with self.invalid_reg_ref_error_handler():
            return self.reg.values

    def _traverse_subkeys(self, stop_condition):
        """Perform simple BFS of subkeys, returning the key
        that successfully triggers the stop condition.
        Args:
            stop_condition: lambda or function pointer that takes a single argument
                            a key and returns a boolean value based on that key
        Return:
            the key if stop_condition is triggered, or None if not
        """
        if not self._valid_reg_check():
            raise RegistryError("Cannot query values from invalid key %s" % self.key)
        with self.invalid_reg_ref_error_handler():
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
            return self.get_subkey(subkey_name)

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
            return self.get_value(val_name)

        else:
            key = self._traverse_subkeys(lambda x: val_name in x.values)
            if not key:
                return None
            else:
                return key.values[val_name]


class RegistryError(RuntimeError):
    """Runtime Error describing issue with invalid key access to Windows registry"""
