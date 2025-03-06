# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import itertools
import re
import string
from typing import Tuple

import spack.error

__all__ = [
    "pkg_name_to_class_name",
    "valid_module_name",
    "validate_module_name",
    "possible_spack_module_names",
    "simplify_name",
    "NamespaceTrie",
]

# Valid module names can contain '-' but can't start with it.
_valid_module_re_v1 = re.compile(r"^\w[\w-]*$")
_valid_module_re_v2 = re.compile(r"^[a-z_][a-z0-9_]*$")


def pkg_name_to_class_name(pkg_name: str):
    """Convert a Spack package name to a class name, based on
    `PEP-8 <http://legacy.python.org/dev/peps/pep-0008/>`_:

       * Module and package names use lowercase_with_underscores.
       * Class names use the CapWords convention.

    Not all package names are valid Python identifiers:

       * They can contain '-', but cannot start with '-'.
       * They can start with numbers, e.g. "3proxy".

    This function converts from the package name to the class convention by removing _ and - and
    converting surrounding lowercase text to CapWords.  If package name starts with a number, the
    class name returned will be prepended with '_' to make a valid Python identifier.
    """
    class_name = re.sub(r"[-_]+", "-", pkg_name)
    class_name = string.capwords(class_name, "-")
    class_name = class_name.replace("-", "")

    # If a class starts with a number, prefix it with _ to make it a valid Python class name.
    if re.match(r"^[0-9]", class_name):
        class_name = "_%s" % class_name

    return class_name


def mod_to_pkg_name(dirname: str, package_api: Tuple[int, int]) -> str:
    """Translate a module name to its corresponding package name"""
    if package_api[0] == 1:
        return dirname
    return dirname.lstrip("_").replace("_", "-")


def pkg_name_to_mod(name: str, package_api: Tuple[int, int]) -> str:
    """Translate a package name to its corresponding module name"""
    if package_api[0] == 1:
        return name
    name = name.replace("-", "_")
    return f"_{name}" if re.match(r"^[0-9]", name) else name


def possible_spack_module_names(python_mod_name):
    """Given a Python module name, return a list of all possible spack module
    names that could correspond to it."""
    mod_name = re.sub(r"^num(\d)", r"\1", python_mod_name)

    parts = re.split(r"(_)", mod_name)
    options = [["_", "-"]] * mod_name.count("_")

    results = []
    for subs in itertools.product(*options):
        s = list(parts)
        s[1::2] = subs
        results.append("".join(s))

    return results


def simplify_name(name):
    """Simplify package name to only lowercase, digits, and dashes.

    Simplifies a name which may include uppercase letters, periods,
    underscores, and pluses. In general, we want our package names to
    only contain lowercase letters, digits, and dashes.

    Args:
        name (str): The original name of the package

    Returns:
        str: The new name of the package
    """
    # Convert CamelCase to Dashed-Names
    # e.g. ImageMagick -> Image-Magick
    # e.g. SuiteSparse -> Suite-Sparse
    # name = re.sub('([a-z])([A-Z])', r'\1-\2', name)

    # Rename Intel downloads
    # e.g. l_daal, l_ipp, l_mkl -> daal, ipp, mkl
    if name.startswith("l_"):
        name = name[2:]

    # Convert UPPERCASE to lowercase
    # e.g. SAMRAI -> samrai
    name = name.lower()

    # Replace '_' and '.' with '-'
    # e.g. backports.ssl_match_hostname -> backports-ssl-match-hostname
    name = name.replace("_", "-")
    name = name.replace(".", "-")

    # Replace "++" with "pp" and "+" with "-plus"
    # e.g. gtk+   -> gtk-plus
    # e.g. voro++ -> voropp
    name = name.replace("++", "pp")
    name = name.replace("+", "-plus")

    # Simplify Lua package names
    # We don't want "lua" to occur multiple times in the name
    name = re.sub("^(lua)([^-])", r"\1-\2", name)

    # Simplify Bio++ package names
    name = re.sub("^(bpp)([^-])", r"\1-\2", name)

    return name


def valid_module_name(mod_name: str, package_api: Tuple[int, int]) -> bool:
    """Return whether mod_name is valid for use in Spack."""
    regex = _valid_module_re_v1 if package_api[0] == 1 else _valid_module_re_v2
    return bool(regex.match(mod_name))


def validate_module_name(mod_name: str, package_api: Tuple[int, int]) -> None:
    """Raise an exception if mod_name is not valid."""
    if not valid_module_name(mod_name, package_api):
        raise InvalidModuleNameError(mod_name)


class InvalidModuleNameError(spack.error.SpackError):
    """Raised when we encounter a bad module name."""

    def __init__(self, name):
        super().__init__("Invalid module name: " + name)
        self.name = name


class NamespaceTrie:
    class Element:
        def __init__(self, value):
            self.value = value

    def __init__(self, separator="."):
        self._subspaces = {}
        self._value = None
        self._sep = separator

    def __setitem__(self, namespace, value):
        first, sep, rest = namespace.partition(self._sep)

        if not first:
            self._value = NamespaceTrie.Element(value)
            return

        if first not in self._subspaces:
            self._subspaces[first] = NamespaceTrie()

        self._subspaces[first][rest] = value

    def _get_helper(self, namespace, full_name):
        first, sep, rest = namespace.partition(self._sep)
        if not first:
            if not self._value:
                raise KeyError("Can't find namespace '%s' in trie" % full_name)
            return self._value.value
        elif first not in self._subspaces:
            raise KeyError("Can't find namespace '%s' in trie" % full_name)
        else:
            return self._subspaces[first]._get_helper(rest, full_name)

    def __getitem__(self, namespace):
        return self._get_helper(namespace, namespace)

    def is_prefix(self, namespace):
        """True if the namespace has a value, or if it's the prefix of one that
        does."""
        first, sep, rest = namespace.partition(self._sep)
        if not first:
            return True
        elif first not in self._subspaces:
            return False
        else:
            return self._subspaces[first].is_prefix(rest)

    def is_leaf(self, namespace):
        """True if this namespace has no children in the trie."""
        first, sep, rest = namespace.partition(self._sep)
        if not first:
            return bool(self._subspaces)
        elif first not in self._subspaces:
            return False
        else:
            return self._subspaces[first].is_leaf(rest)

    def has_value(self, namespace):
        """True if there is a value set for the given namespace."""
        first, sep, rest = namespace.partition(self._sep)
        if not first:
            return self._value is not None
        elif first not in self._subspaces:
            return False
        else:
            return self._subspaces[first].has_value(rest)

    def __contains__(self, namespace):
        """Returns whether a value has been set for the namespace."""
        return self.has_value(namespace)

    def _str_helper(self, stream, level=0):
        indent = level * "    "
        for name in sorted(self._subspaces):
            stream.write(indent + name + "\n")
            if self._value:
                stream.write(indent + "  " + repr(self._value.value))
            stream.write(self._subspaces[name]._str_helper(stream, level + 1))

    def __str__(self):
        stream = io.StringIO()
        self._str_helper(stream)
        return stream.getvalue()
