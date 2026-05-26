# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows Access Control List (ACL) utilities.

On Windows, file permissions are represented as a list of Access Control Entries (ACEs).
Each entry expresses something like "User 1 can read this file".  This module provides
the building blocks to inspect and modify those permissions.

Public API:

- :class:`SecurityDescriptor` -- mutable security descriptor; supports reading from/writing
  to files (:meth:`~SecurityDescriptor.from_file`, :meth:`~SecurityDescriptor.apply`),
  adding/removing/modifying ACEs, and querying ownership.
- :class:`AccessControlEntry` -- a single ACE; built with the semantic enum types below and
  passed to :meth:`SecurityDescriptor.add_ace`.
- :func:`get_file_owner` -- return the account name of the owner of a file.
- :func:`copy_file_permissions` -- copy the DACL from one file to another.
- :func:`get_file_sddl` / :func:`set_file_sddl` -- low-level SDDL string read/write;
  intended primarily (but not exclusively) for testing and debugging rather than general use.

Terminology:

- **ACE** (Access Control Entry): a single permission entry describing a principal and
  what they may do, e.g. "User 1 can read and write".
- **DACL** (Discretionary Access Control List): the ordered list of ACEs that governs
  file access.  Owner, group, and DACL together form a *Security Descriptor*.
- **Owner**: the principal who owns the file; the owner always has the right to change
  the DACL regardless of what the DACL itself says.
- **SDDL** (Security Descriptor Definition Language): the text format used by Windows to
  represent security descriptors, e.g. ``O:BAG:SYD:(A;;GR;;;WD)``.
- **SACL** (System Access Control List): like the DACL but controls auditing (e.g. "log
  when User 1 reads this file") rather than access.  Reading or writing the SACL requires
  ``SE_SECURITY_PRIVILEGE``, which standard user processes do not hold; Spack never
  modifies the SACL.
"""

import copy
import ctypes
import itertools
import os
import re
from contextlib import contextmanager
from ctypes import wintypes  # type: ignore[attr-defined]
from enum import Enum, IntEnum
from typing import Any, Dict, Generator, List, Optional, Union


class AccessRightsEnum(IntEnum):
    """Base class for all access-rights enums.

    Members are 32-bit Windows access-mask integers so they compose naturally with
    bitwise operators and compare directly with ``ace.rights`` (which is also an
    ``int``).  No ``.value`` dereferencing is needed.
    """


class AceType(Enum):
    """ACE type strings for the ``AceType`` field of the ACE_HEADER structure."""

    SDDL_ACCESS_ALLOWED = "A"
    SDDL_ACCESS_DENIED = "D"
    SDDL_OBJECT_ACCESS_ALLOWED = "OA"
    SDDL_OBJECT_ACCESS_DENIED = "OD"
    SDDL_AUDIT = "AU"
    SDDL_ALARM = "AL"
    SDDL_OBJECT_AUDIT = "OU"
    SDDL_OBJECT_ALARM = "OL"
    SDDL_MANDATORY_LABEL = "ML"
    SDDL_CALLBACK_ACCESS_ALLOWED = "XA"
    SDDL_CALLBACK_ACCESS_DENIED = "XD"
    SDDL_RESOURCE_ATTRIBUTE = "RA"
    SDDL_SCOPED_POLICY_ID = "SP"
    SDDL_CALLBACK_AUDIT = "XU"
    SDDL_CALLBACK_OBJECT_ACCESS_ALLOWED = "ZA"
    SDDL_PROCESS_TRUST_LABEL = "TL"
    SDDL_ACCESS_FILTER = "FL"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_sddl(cls, token: str) -> "Union[AceType, str]":
        """Return the ``AceType`` whose SDDL token matches *token*.

        Returns *token* unchanged for unrecognised codes so that security
        descriptors containing future or exotic ACE types survive a
        parse/apply roundtrip without crashing.
        """
        for member in cls:
            if member.value == token:
                return member
        return token


class AceFlags(Enum):
    """ACE flags strings for the ``AceFlags`` field of the ACE_HEADER structure."""

    SDDL_CONTAINER_INHERIT = "CI"
    SDDL_OBJECT_INHERIT = "OI"
    SDDL_NO_PROPAGATE = "NP"
    SDDL_INHERIT_ONLY = "IO"
    SDDL_INHERITED = "ID"
    SDDL_AUDIT_SUCCESS = "SA"
    SDDL_AUDIT_FAILURE = "FA"
    SDDL_TRUST_PROTECTED_FILTER = "TP"
    SDDL_CRITICAL = "CR"


class GenericAccessRights(AccessRightsEnum):
    """Generic access rights (mapped by the OS to object specific rights at access check time)."""

    GENERIC_ALL = 0x10000000
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    GENERIC_EXECUTE = 0x20000000


class StandardAccessRights(AccessRightsEnum):
    """Standard rights present on every securable object."""

    DELETE = 0x00010000
    READ_CONTROL = 0x00020000
    WRITE_DAC = 0x00040000
    WRITE_OWNER = 0x00080000


class FileAccessRights(AccessRightsEnum):
    """File and directory access rights (SDDL tokens FA/FR/FW/FX)."""

    FILE_ALL_ACCESS = 0x001F01FF
    FILE_GENERIC_READ = 0x00120089
    FILE_GENERIC_WRITE = 0x00120116
    FILE_GENERIC_EXECUTE = 0x001200A0


class RegistryKeyAccessRights(AccessRightsEnum):
    """Registry key access rights (SDDL tokens KA/KR/KW/KX)."""

    KEY_ALL_ACCESS = 0x000F003F
    KEY_READ = 0x00020019
    KEY_WRITE = 0x00020006
    KEY_EXECUTE = 0x00020019  # alias for KEY_READ


class MandatoryLabelRights(AccessRightsEnum):
    """Mandatory integrity label rights (SDDL tokens NW/NR/NX)."""

    NO_WRITE_UP = 0x00000001
    NO_READ_UP = 0x00000002
    NO_EXECUTE_UP = 0x00000004


class DirectoryServiceObjectAccessRights(AccessRightsEnum):
    """Active Directory object access rights (SDDL tokens CC/DC/LC/SW/RP/WP/DT/LO/CR)."""

    DS_CREATE_CHILD = 0x00000001
    DS_DELETE_CHILD = 0x00000002
    DS_LIST = 0x00000004
    DS_SELF = 0x00000008
    DS_READ_PROP = 0x00000010
    DS_WRITE_PROP = 0x00000020
    DS_DELETE_TREE = 0x00000040
    DS_LIST_OBJECT = 0x00000080
    DS_CONTROL_ACCESS = 0x00000100


class ResourceAttributeAceDataType(Enum):
    """Resource attribute ACE data type strings."""

    SDDL_INT = "TI"
    SDDL_UINT = "TU"
    SDDL_WSTRING = "TS"
    SDDL_SID = "TD"
    SDDL_BLOB = "TX"
    SDDL_BOOLEAN = "TB"


# SDDL code: 32-bit access mask for every named right token.  Used by _map_rights to
# parse SDDL strings ("FRFW", "GR", ...) into integer masks during ACE construction.
_NAMED_RIGHT_MASKS: Dict[str, int] = {
    # File access rights
    "FA": int(FileAccessRights.FILE_ALL_ACCESS),
    "FR": int(FileAccessRights.FILE_GENERIC_READ),
    "FW": int(FileAccessRights.FILE_GENERIC_WRITE),
    "FX": int(FileAccessRights.FILE_GENERIC_EXECUTE),
    # Generic access rights
    "GA": int(GenericAccessRights.GENERIC_ALL),
    "GR": int(GenericAccessRights.GENERIC_READ),
    "GW": int(GenericAccessRights.GENERIC_WRITE),
    "GX": int(GenericAccessRights.GENERIC_EXECUTE),
    # Standard access rights
    "SD": int(StandardAccessRights.DELETE),
    "RC": int(StandardAccessRights.READ_CONTROL),
    "WD": int(StandardAccessRights.WRITE_DAC),
    "WO": int(StandardAccessRights.WRITE_OWNER),
    # Registry key access rights
    "KA": int(RegistryKeyAccessRights.KEY_ALL_ACCESS),
    "KR": int(RegistryKeyAccessRights.KEY_READ),
    "KW": int(RegistryKeyAccessRights.KEY_WRITE),
    "KX": int(RegistryKeyAccessRights.KEY_EXECUTE),
    # Mandatory label rights
    "NW": int(MandatoryLabelRights.NO_WRITE_UP),
    "NR": int(MandatoryLabelRights.NO_READ_UP),
    "NX": int(MandatoryLabelRights.NO_EXECUTE_UP),
    # Directory service object access rights
    "CC": int(DirectoryServiceObjectAccessRights.DS_CREATE_CHILD),
    "DC": int(DirectoryServiceObjectAccessRights.DS_DELETE_CHILD),
    "LC": int(DirectoryServiceObjectAccessRights.DS_LIST),
    "SW": int(DirectoryServiceObjectAccessRights.DS_SELF),
    "RP": int(DirectoryServiceObjectAccessRights.DS_READ_PROP),
    "WP": int(DirectoryServiceObjectAccessRights.DS_WRITE_PROP),
    "DT": int(DirectoryServiceObjectAccessRights.DS_DELETE_TREE),
    "LO": int(DirectoryServiceObjectAccessRights.DS_LIST_OBJECT),
    "CR": int(DirectoryServiceObjectAccessRights.DS_CONTROL_ACCESS),
}


# Reverse lookup:  SDDL code string to int mask for file/generic rights.
# Used during SDDL serialisation to convert stored integer masks back to readable tokens.
# Limited to the 8 file+generic codes since those are what ConvertSecurityDescriptor
# emits for file objects; other masks fall back to hex in _to_ace_string.
_FILE_GENERIC_SDDL_CODES: Dict[str, int] = {
    k: _NAMED_RIGHT_MASKS[k] for k in ("FA", "FR", "FW", "FX", "GA", "GR", "GW", "GX")
}


def _build_mask_to_named_rights(codes: Dict[str, int]) -> Dict[int, str]:
    result: Dict[int, str] = {}
    items = list(codes.items())
    for r in range(1, len(items) + 1):
        for combo in itertools.combinations(items, r):
            mask = 0
            for _, m in combo:
                mask |= m
            if mask not in result:
                result[mask] = "".join(c for c, _ in combo)
    return result


_MASK_TO_NAMED_RIGHTS: Dict[int, str] = _build_mask_to_named_rights(_FILE_GENERIC_SDDL_CODES)


class AccessControlEntry:
    """A single SDDL Access Control Entry.

    Produces the standard SDDL ACE string format::

        (ace_type;ace_flags;rights;object_guid;inherit_object_guid;account_sid)

    The three most important fields are:

    - **sid**: the account this ACE applies to, as an SDDL SID string (e.g. ``"WD"`` for
      Everyone, ``"BA"`` for Builtin Administrators, or ``"S-1-5-21-..."`` for a domain
      account).  Use :meth:`SecurityDescriptor.get_sid_for_user` to resolve a username.
    - **rights**: a bitmask of access rights, built from :class:`FileAccessRights`,
      :class:`GenericAccessRights`, or other ``AccessRightsEnum`` subclasses.  Multiple
      rights are OR-ed together (or accumulated with :meth:`add_right`).
    - **flags**: zero or more :class:`AceFlags` controlling inheritance behaviour (e.g.
      whether child objects inherit this ACE).  Most file ACEs leave this empty.

    Build an ACE using the semantic enum types, then pass it to
    :meth:`SecurityDescriptor.add_ace`::

        ace = AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED,
            flags=AceFlags.SDDL_CONTAINER_INHERIT,
            rights=FileAccessRights.FILE_GENERIC_READ,
            sid="BA",
        )
        sd.add_ace(ace)
    """

    def __init__(
        self,
        ace_type: Union[AceType, str],
        flags: Optional[Union[AceFlags, List[AceFlags]]] = None,
        rights: Optional[int] = None,
        obj_guid: Optional[str] = None,
        inh_obj_guid: Optional[str] = None,
        sid: Optional[str] = None,
        resource_attr: Optional[ResourceAttributeAceDataType] = None,
    ):
        # str arm: AceType.from_sddl preserves unrecognised tokens as raw strings
        # so that security descriptors with future/exotic ACE types round-trip safely.
        self._type: Union[AceType, str] = ace_type
        # str arm: _map_flags preserves unrecognised 2-char flag codes as raw strings.
        if flags is None:
            self._flags: List[Union[AceFlags, str]] = []
        elif isinstance(flags, list):
            self._flags = list(flags)
        else:
            self._flags = [flags]
        self._rights: Optional[int] = rights
        self._obj_guid = obj_guid
        self._inh_obj_guid = inh_obj_guid
        self._sid = sid
        self._resource_attr = resource_attr

    @property
    def ace_type(self) -> Union[AceType, str]:
        return self._type

    @ace_type.setter
    def ace_type(self, val: Union[AceType, str]) -> None:
        self._type = val

    @property
    def flags(self) -> List[Union[AceFlags, str]]:
        return self._flags

    @flags.setter
    def flags(self, val: Optional[Union[AceFlags, List[AceFlags]]]) -> None:
        if val is None:
            self._flags = []
        elif isinstance(val, list):
            self._flags = val  # ty: ignore[invalid-assignment]  # List[AceFlags] widens safely
        else:
            self._flags = [val]

    @property
    def rights(self) -> Optional[int]:
        return self._rights

    @rights.setter
    def rights(self, val: Optional[int]) -> None:
        self._rights = val

    @property
    def sid(self) -> Optional[str]:
        return self._sid

    @sid.setter
    def sid(self, val: Optional[str]) -> None:
        self._sid = val

    @property
    def obj_guid(self) -> Optional[str]:
        return self._obj_guid

    @property
    def inh_obj_guid(self) -> Optional[str]:
        return self._inh_obj_guid

    def grants(self, mask: int) -> bool:
        """Return ``True`` if this ACE's rights include all bits in *mask*.

        Uses subset semantics: ``ace.grants(FX)`` is True only when every bit of
        FILE_GENERIC_EXECUTE is present, not merely when the masks share any bit.
        """
        return self._rights is not None and (self._rights & mask) == mask

    def add_right(self, mask: int) -> None:
        """OR *mask* into the accumulated rights."""
        self._rights = (self._rights or 0) | mask

    def _to_ace_string(self) -> str:
        if self._rights is not None:
            rights_str = _MASK_TO_NAMED_RIGHTS.get(self._rights, hex(self._rights))
        else:
            rights_str = ""
        parts = [
            str(self._type),  # AceType.__str__ returns .value; str passthrough for unknowns
            "".join(f if isinstance(f, str) else f.value for f in self._flags),
            rights_str,
            self._obj_guid or "",
            self._inh_obj_guid or "",
            self._sid or "",
        ]
        if self._resource_attr is not None:
            parts.append(self._resource_attr.value)
        return "(" + ";".join(parts) + ")"

    def __repr__(self) -> str:
        return f"AccessControlEntry({self._to_ace_string()!r})"

    def __str__(self) -> str:
        return self._to_ace_string()


class SID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]


class TOKEN_USER(ctypes.Structure):
    _fields_ = [("User", SID_AND_ATTRIBUTES)]


TOKEN_QUERY = 0x0008


_advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)  # ty: ignore[unresolved-attribute]
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # ty: ignore[unresolved-attribute]
_WinError = ctypes.WinError  # ty: ignore[unresolved-attribute]
_get_last_error = ctypes.get_last_error  # ty: ignore[unresolved-attribute]


def _bind(dll: ctypes.WinDLL, name: str, argtypes: list, restype: type) -> Any:  # ty: ignore[unresolved-attribute]
    """Set argtypes/restype on a DLL function and return it."""
    fn = getattr(dll, name)
    fn.argtypes = argtypes
    fn.restype = restype
    return fn


_PPVOID = ctypes.POINTER(wintypes.LPVOID)  # out void**
_PBOOL = ctypes.POINTER(wintypes.BOOL)  # out BOOL*
_PDWORD = ctypes.POINTER(wintypes.DWORD)  # out DWORD*
_PULONG = ctypes.POINTER(wintypes.ULONG)  # out ULONG*
_PPWSTR = ctypes.POINTER(wintypes.LPWSTR)  # out LPWSTR* (LocalAlloc'd strings)
_PINT = ctypes.POINTER(ctypes.c_int)  # out int* (enums)
_PHANDLE = ctypes.POINTER(wintypes.HANDLE)  # out HANDLE*

_OpenProcessToken = _bind(
    _advapi32, "OpenProcessToken", [wintypes.HANDLE, wintypes.DWORD, _PHANDLE], wintypes.BOOL
)

_GetTokenInformation = _bind(
    _advapi32,
    "GetTokenInformation",
    [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, _PDWORD],
    wintypes.BOOL,
)

_LookupAccountNameW = _bind(
    _advapi32,
    "LookupAccountNameW",
    [
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.LPVOID,
        _PDWORD,
        wintypes.LPWSTR,
        _PDWORD,
        _PINT,
    ],
    wintypes.BOOL,
)

_ConvertSidToStringSidW = _bind(
    _advapi32, "ConvertSidToStringSidW", [wintypes.LPVOID, _PPWSTR], wintypes.BOOL
)

_GetNamedSecurityInfoW = _bind(
    _advapi32,
    "GetNamedSecurityInfoW",
    [wintypes.LPCWSTR, ctypes.c_int, wintypes.DWORD, _PPVOID, _PPVOID, _PPVOID, _PPVOID, _PPVOID],
    wintypes.DWORD,
)

_ConvertSecurityDescriptorToStringSecurityDescriptorW = _bind(
    _advapi32,
    "ConvertSecurityDescriptorToStringSecurityDescriptorW",
    [wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, _PPWSTR, _PULONG],
    wintypes.BOOL,
)

_LocalFree = _bind(_kernel32, "LocalFree", [wintypes.HLOCAL], wintypes.HLOCAL)

_GetCurrentProcess = _bind(_kernel32, "GetCurrentProcess", [], wintypes.HANDLE)

_CloseHandle = _bind(_kernel32, "CloseHandle", [wintypes.HANDLE], wintypes.BOOL)

# pObjectName is LPWSTR (mutable) per the Windows SDK header, not LPCWSTR.
_SetNamedSecurityInfoW = _bind(
    _advapi32,
    "SetNamedSecurityInfoW",
    [
        wintypes.LPWSTR,
        ctypes.c_int,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.LPVOID,
        wintypes.LPVOID,
        wintypes.LPVOID,
    ],
    wintypes.DWORD,
)

_LookupAccountSidW = _bind(
    _advapi32,
    "LookupAccountSidW",
    [wintypes.LPCWSTR, wintypes.LPVOID, wintypes.LPWSTR, _PDWORD, wintypes.LPWSTR, _PDWORD, _PINT],
    wintypes.BOOL,
)

_ConvertStringSecurityDescriptorToSecurityDescriptorW = _bind(
    _advapi32,
    "ConvertStringSecurityDescriptorToSecurityDescriptorW",
    [wintypes.LPCWSTR, wintypes.DWORD, _PPVOID, _PULONG],
    wintypes.BOOL,
)

_GetSecurityDescriptorOwner = _bind(
    _advapi32, "GetSecurityDescriptorOwner", [wintypes.LPVOID, _PPVOID, _PBOOL], wintypes.BOOL
)

_GetSecurityDescriptorGroup = _bind(
    _advapi32, "GetSecurityDescriptorGroup", [wintypes.LPVOID, _PPVOID, _PBOOL], wintypes.BOOL
)

_GetSecurityDescriptorDacl = _bind(
    _advapi32,
    "GetSecurityDescriptorDacl",
    [wintypes.LPVOID, _PBOOL, _PPVOID, _PBOOL],
    wintypes.BOOL,
)


@contextmanager
def _local_ptr(ptr_factory: Optional[type] = None) -> Generator[Any, None, None]:
    """Yield a ``LocalFree``-able pointer and free it unconditionally on exit.

    Args:
        ptr_factory: Callable returning the ctypes pointer type (default: ``wintypes.LPVOID``).
            Pass ``wintypes.LPWSTR`` for Windows string out-parameters.
    """
    ptr = (ptr_factory or wintypes.LPVOID)()
    try:
        yield ptr
    finally:
        _LocalFree(ptr)


class _SddlHelper:
    """Private static helpers for parsing and serialising SDDL strings."""

    @staticmethod
    def parse_sddl(sddl_string: str) -> Dict[str, Any]:
        """Parse an SDDL string into a dict with keys
        ``Owner``, ``Group``, ``DACL``, ``SACL``, ``DACL_CONTROL``, ``SACL_CONTROL``.

        Control flags (e.g. ``AI``) between the section prefix and the first ACE are preserved
        in the ``*_CONTROL`` keys so that roundtrips are lossless.  The ``DACL`` and ``SACL``
        values are ``list[AccessControlEntry]``.
        """
        parsed: Dict[str, Any] = {
            "Owner": None,
            "Group": None,
            "DACL": [],
            "SACL": [],
            "DACL_CONTROL": "",
            "SACL_CONTROL": "",
            "DACL_PRESENT": False,
        }

        for tag in re.split(r"(?=[OGDS]:)", sddl_string):
            if tag.startswith("O:"):
                parsed["Owner"] = tag[2:]
            elif tag.startswith("G:"):
                parsed["Group"] = tag[2:]
            elif tag.startswith("D:") or tag.startswith("S:"):
                acl_key = "DACL" if tag.startswith("D:") else "SACL"
                ctrl_key = "DACL_CONTROL" if acl_key == "DACL" else "SACL_CONTROL"
                if acl_key == "DACL":
                    parsed["DACL_PRESENT"] = True
                rest = tag[2:]
                paren = rest.find("(")
                parsed[ctrl_key] = rest[:paren] if paren >= 0 else rest
                for ace_str in re.findall(r"\((.*?)\)", tag):
                    parsed[acl_key].append(_SddlHelper._parse_ace(ace_str))

        return parsed

    @staticmethod
    def _parse_ace(ace_str: str) -> AccessControlEntry:
        parts = ace_str.split(";")
        if len(parts) < 6:
            raise ValueError(f"Invalid ACE format: {ace_str!r}")

        # Resource-attribute ACEs have a 7th field; we intentionally ignore it since
        # Spack never generates such ACEs and write-back preserves the OS SACL intact.
        return AccessControlEntry(
            ace_type=AceType.from_sddl(parts[0]),
            flags=_SddlHelper._map_flags(parts[1], AceFlags),  # ty: ignore[invalid-argument-type]
            rights=_SddlHelper._map_rights(parts[2]) if parts[2] else None,
            obj_guid=parts[3] if parts[3] else None,
            inh_obj_guid=parts[4] if parts[4] else None,
            sid=parts[5] if parts[5] else None,
        )

    @staticmethod
    def _map_flags(flag_str: str, enum_cls: type) -> List[Union[AceFlags, str]]:
        flags: List[Union[AceFlags, str]] = []
        if not flag_str:
            return flags
        for chunk in (flag_str[i : i + 2] for i in range(0, len(flag_str), 2)):
            for member in enum_cls:  # ty: ignore[not-iterable]
                if member.value == chunk:
                    flags.append(member)
                    break
            else:
                # Unknown flag code: preserve as raw string for roundtrip fidelity.
                flags.append(chunk)
        return flags

    @staticmethod
    def _map_rights(rights_str: str) -> int:
        """Parse an SDDL rights token to its 32-bit integer access mask.

        Handles hex strings (``"0x12019f"``), decimal strings, and named SDDL code
        sequences (``"FR"``, ``"FRFW"``).  Raises ``ValueError`` for unrecognised codes.
        """
        try:
            return int(rights_str, 0)
        except ValueError:
            pass
        mask = 0
        for i in range(0, len(rights_str), 2):
            code = rights_str[i : i + 2]
            val = _NAMED_RIGHT_MASKS.get(code)
            if val is None:
                raise ValueError(f"Unknown SDDL rights code: {code!r}")
            mask |= val
        return mask

    @staticmethod
    def create_sddl(security_descriptor: Dict[str, Any]) -> str:
        """Serialise a parsed security descriptor dict back to an SDDL string."""
        parts = []

        if security_descriptor.get("Owner"):
            parts.append(f"O:{security_descriptor['Owner']}")

        if security_descriptor.get("Group"):
            parts.append(f"G:{security_descriptor['Group']}")

        for acl_key, prefix, ctrl_key in [
            ("DACL", "D:", "DACL_CONTROL"),
            ("SACL", "S:", "SACL_CONTROL"),
        ]:
            aces: List[AccessControlEntry] = security_descriptor.get(acl_key, [])
            control: str = security_descriptor.get(ctrl_key, "")
            if not aces and not control:
                continue
            parts.append(prefix + control + "".join(str(ace) for ace in aces))

        return "".join(parts)


def _get_file_sddl_raw(path: str) -> str:
    """Read the security descriptor of *path* and return it as an SDDL string.

    Only Owner, Group, and DACL are requested.  The SACL is deliberately omitted:
    reading it requires ``SE_SECURITY_PRIVILEGE``, which standard user processes do not
    hold, and Spack never needs to inspect or modify audit entries.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    SE_FILE_OBJECT = 1
    OWNER_SECURITY_INFORMATION = 0x00000001
    GROUP_SECURITY_INFORMATION = 0x00000002
    DACL_SECURITY_INFORMATION = 0x00000004
    security_info = (
        OWNER_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION | DACL_SECURITY_INFORMATION
    )
    SDDL_REVISION_1 = 1

    with _local_ptr() as pp_sd:
        res = _GetNamedSecurityInfoW(
            path, SE_FILE_OBJECT, security_info, None, None, None, None, ctypes.byref(pp_sd)
        )
        if res != 0:
            raise _WinError(res)
        with _local_ptr(wintypes.LPWSTR) as string_ptr:
            if not _ConvertSecurityDescriptorToStringSecurityDescriptorW(
                pp_sd, SDDL_REVISION_1, security_info, ctypes.byref(string_ptr), None
            ):
                raise _WinError(_get_last_error())
            return string_ptr.value or ""


def _set_file_sddl_raw(path: str, sddl: str) -> None:
    """Apply the security descriptor described by *sddl* to *path*.

    Only components present in *sddl* (owner, group, DACL) are written.  A NULL DACL
    (``D:`` with no ACEs and no present flag) is never applied silently as it would grant
    everyone full access.

    Setting owner (``O:``) or group (``G:``) requires ``SE_TAKE_OWNERSHIP_PRIVILEGE`` or
    ``SE_RESTORE_PRIVILEGE``; standard user processes lack these.  For a pure DACL copy
    prefer ``SecurityDescriptor.copy_permissions``, which skips the SDDL round-trip.
    """
    SDDL_REVISION_1 = 1
    SE_FILE_OBJECT = 1
    OWNER_SECURITY_INFORMATION = 0x00000001
    GROUP_SECURITY_INFORMATION = 0x00000002
    DACL_SECURITY_INFORMATION = 0x00000004
    # Required to actually set/clear SE_DACL_PROTECTED; DACL_SECURITY_INFORMATION alone does not.
    PROTECTED_DACL_SECURITY_INFORMATION = 0x80000000

    with _local_ptr() as pp_sd:
        if not _ConvertStringSecurityDescriptorToSecurityDescriptorW(
            sddl, SDDL_REVISION_1, ctypes.byref(pp_sd), None
        ):
            raise _WinError(_get_last_error())

        owner = wintypes.LPVOID()
        owner_defaulted = wintypes.BOOL()
        if not _GetSecurityDescriptorOwner(
            pp_sd, ctypes.byref(owner), ctypes.byref(owner_defaulted)
        ):
            raise _WinError(_get_last_error())

        group = wintypes.LPVOID()
        group_defaulted = wintypes.BOOL()
        if not _GetSecurityDescriptorGroup(
            pp_sd, ctypes.byref(group), ctypes.byref(group_defaulted)
        ):
            raise _WinError(_get_last_error())

        dacl_present = wintypes.BOOL()
        dacl = wintypes.LPVOID()
        dacl_defaulted = wintypes.BOOL()
        if not _GetSecurityDescriptorDacl(
            pp_sd, ctypes.byref(dacl_present), ctypes.byref(dacl), ctypes.byref(dacl_defaulted)
        ):
            raise _WinError(_get_last_error())

        # c_void_p.value is None for NULL; use that to distinguish a real pointer from an unset
        # one.  A NULL DACL (dacl_present=True but pointer=NULL) grants everyone full access
        # never apply it silently.
        security_info = 0
        owner_ptr = owner if owner.value is not None else None
        group_ptr = group if group.value is not None else None
        dacl_ptr = dacl if (dacl_present and dacl.value is not None) else None

        if owner_ptr is not None:
            security_info |= OWNER_SECURITY_INFORMATION
        if group_ptr is not None:
            security_info |= GROUP_SECURITY_INFORMATION
        if dacl_ptr is not None:
            security_info |= DACL_SECURITY_INFORMATION
            # D:P in the SDDL requests a protected DACL (no inheritance from parent).
            # SetNamedSecurityInfoW only honours this when the dedicated bit is also set.
            if re.search(r"D:[^(]*P", sddl):
                security_info |= PROTECTED_DACL_SECURITY_INFORMATION

        if security_info == 0:
            return

        res = _SetNamedSecurityInfoW(
            path, SE_FILE_OBJECT, security_info, owner_ptr, group_ptr, dacl_ptr, None
        )
        if res != 0:
            raise _WinError(res)


class SecurityDescriptor:
    """A mutable Windows security descriptor backed by an SDDL representation.

    Typical usage::

        # Read, modify, and write back
        sd = SecurityDescriptor.from_file(path)
        sd.add_ace(AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED,
            rights=FileAccessRights.FILE_GENERIC_READ,
            sid=SecurityDescriptor.get_sid_for_user(),
        ))
        sd.apply(path)

        # Copy permissions between files
        SecurityDescriptor.copy_permissions(src, dst)
    """

    def __init__(self, sddl_string: Optional[str] = None) -> None:
        if sddl_string:
            self._parsed: Dict[str, Any] = _SddlHelper.parse_sddl(sddl_string)
        else:
            self._parsed = {
                "Owner": None,
                "Group": None,
                "DACL": [],
                "SACL": [],
                "DACL_CONTROL": "",
                "SACL_CONTROL": "",
                "DACL_PRESENT": False,
            }

    @classmethod
    def from_file(cls, path: str) -> "SecurityDescriptor":
        """Create a ``SecurityDescriptor`` from the security descriptor of *path*.

        Raises:
            FileNotFoundError: if *path* does not exist.
            OSError: raised by ``ctypes.WinError`` on Windows API failure (carries ``winerror``).
        """
        return cls(_get_file_sddl_raw(path))

    @property
    def owner(self) -> Optional[str]:
        return self._parsed["Owner"]

    @owner.setter
    def owner(self, sid: Optional[str]) -> None:
        self._parsed["Owner"] = sid

    @property
    def group(self) -> Optional[str]:
        return self._parsed["Group"]

    @group.setter
    def group(self, sid: Optional[str]) -> None:
        self._parsed["Group"] = sid

    @property
    def dacl(self) -> List[AccessControlEntry]:
        """Return the DACL as a list of ``AccessControlEntry`` objects."""
        return self._parsed["DACL"]

    @property
    def sacl(self) -> List[AccessControlEntry]:
        """Return a deep copy of the SACL as a list of ``AccessControlEntry`` objects.

        Note:
            Reading the SACL from a file requires ``SE_SECURITY_PRIVILEGE``, which standard
            user processes do not hold.  ``from_file`` therefore does not request SACL
            information, so this list will always be empty for descriptors obtained from a
            file.  Existing SACL entries on a file are preserved by the OS when ``apply``
            is called because ``SACL_SECURITY_INFORMATION`` is never passed to
            ``SetNamedSecurityInfoW``.
        """
        return copy.deepcopy(self._parsed["SACL"])

    def add_ace(self, ace: AccessControlEntry, index: Optional[int] = None) -> None:
        """Add an ``AccessControlEntry`` to the DACL.

        Args:
            ace: The ACE to add.  Build it using the semantic enum types::

                    ace = AccessControlEntry(
                        AceType.SDDL_ACCESS_ALLOWED,
                        rights=FileAccessRights.FILE_GENERIC_READ,
                        sid="BA",
                    )

            index: Insert position (0-based, inclusive of ``len(dacl)`` to append at end).
                Raises ``IndexError`` for negative values or values greater than
                ``len(dacl)``.  Appends when ``None``.
        """
        dacl = self._parsed["DACL"]
        if index is None:
            dacl.append(ace)
        elif 0 <= index <= len(dacl):
            dacl.insert(index, ace)
        else:
            raise IndexError(f"ACE index {index} out of range for DACL of length {len(dacl)}")

    def remove_ace(
        self,
        sid: Optional[str] = None,
        rights: Optional[int] = None,
        ace_type: Optional[Union[AceType, str]] = None,
        remove_all_matches: bool = False,
    ) -> int:
        """Remove ACEs from the DACL that match all supplied criteria.

        Args:
            sid: Filter by account SID (``None`` = wildcard).
            rights: Filter by rights value (``None`` = wildcard).
            ace_type: Filter by ACE type (``None`` = wildcard).
            remove_all_matches: Remove every match when ``True``; only the first when ``False``.

        Returns:
            Number of ACEs removed.
        """
        to_remove = []
        for i, ace in enumerate(self._parsed["DACL"]):
            if (
                (sid is None or ace.sid == sid)
                and (rights is None or ace.rights == rights)
                and (ace_type is None or ace.ace_type == ace_type)
            ):
                to_remove.append(i)
                if not remove_all_matches:
                    break

        for i in sorted(to_remove, reverse=True):
            del self._parsed["DACL"][i]

        return len(to_remove)

    def modify_ace(
        self,
        index: int,
        sid: Optional[str] = None,
        rights: Optional[int] = None,
        flags: Optional[Union[AceFlags, List[AceFlags]]] = None,
        ace_type: Optional[Union[AceType, str]] = None,
    ) -> None:
        """Modify an existing ACE in-place by index."""
        dacl = self._parsed["DACL"]
        if index < 0 or index >= len(dacl):
            raise IndexError("ACE index out of range")

        ace = dacl[index]
        if sid is not None:
            ace.sid = sid
        if rights is not None:
            ace.rights = rights
        if ace_type is not None:
            ace.ace_type = ace_type
        if flags is not None:
            ace.flags = flags

    def clear_dacl(self) -> None:
        """Remove all ACEs from the DACL."""
        self._parsed["DACL"] = []

    def to_sddl(self) -> str:
        """Compile the current state back into an SDDL string."""
        return _SddlHelper.create_sddl(self._parsed)

    def apply(self, path: str, update_ownership: bool = False) -> None:
        """Write this security descriptor to *path*.

        By default only the DACL is written (``DACL_SECURITY_INFORMATION``).  Pass
        ``update_ownership=True`` to also write owner and group fields, which is needed
        for ``chown``-style operations.  Doing so requires ``WRITE_OWNER`` access to the
        file or ``SE_TAKE_OWNERSHIP_PRIVILEGE`` in the process token; if neither is
        present a ``PermissionError`` is raised with an explanation.

        Raises:
            ValueError: if the descriptor has an explicit but empty DACL (null DACL).
            PermissionError: if ``update_ownership=True`` and the caller lacks ``WRITE_OWNER``
                access or ``SE_TAKE_OWNERSHIP_PRIVILEGE``.
            OSError: on any other Windows API failure (carries ``winerror``).
        """
        if self._parsed.get("DACL_PRESENT") and not self._parsed["DACL"]:
            raise ValueError(
                "Refusing to apply a null DACL: D: section is present but contains no ACEs. "
                "A null DACL on Windows grants all users full access."
            )
        # AI (auto-inherited) and AR (auto-inherit-required) are kernel-computed flags that
        # describe how the *existing* DACL was built.  Passing them back to SetNamedSecurityInfoW
        # causes the kernel to re-process parent inheritance, producing a different (and larger)
        # ACE set than the one we wrote.  Strip them so the kernel treats our ACEs as explicit.
        # Build a view for serialisation without mutating self._parsed.
        # Scalar values (Owner, Group, DACL_CONTROL) are reassigned on the copy;
        # DACL is a shared list reference but create_sddl only reads it.
        parsed = dict(self._parsed)
        if not update_ownership:
            parsed["Owner"] = None
            parsed["Group"] = None
        parsed["DACL_CONTROL"] = re.sub(r"AI|AR", "", parsed.get("DACL_CONTROL", ""))
        sddl = _SddlHelper.create_sddl(parsed)
        if not sddl:
            return
        try:
            _set_file_sddl_raw(path, sddl)
        except OSError as exc:
            if (
                update_ownership and hasattr(exc, "winerror") and exc.winerror == 5
            ):  # ERROR_ACCESS_DENIED
                raise PermissionError(
                    f"Cannot update owner/group on {path!r}: the current process lacks "
                    "WRITE_OWNER access to the file and does not hold "
                    "SE_TAKE_OWNERSHIP_PRIVILEGE.  Acquire the necessary privilege before "
                    "calling apply(update_ownership=True), or omit update_ownership to "
                    "update only the DACL."
                ) from exc
            raise

    def __str__(self) -> str:
        return self.to_sddl()

    @staticmethod
    def get_owner(path: str) -> str:
        """Return the account name (e.g. ``"SYSTEM"``) of the owner of *path*.

        Unlike ``owner`` (which gives the SID string from the SDDL), this performs a
        ``LookupAccountSidW`` call to resolve the human-readable account name.

        Raises:
            FileNotFoundError: if *path* does not exist.
            OSError: raised by ``ctypes.WinError`` on Windows API failure (carries ``winerror``).
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"No such file or directory: '{path}'")

        SE_FILE_OBJECT = 1
        OWNER_SECURITY_INFORMATION = 0x00000001

        p_sid_owner = wintypes.LPVOID()
        with _local_ptr() as pp_sd:
            res = _GetNamedSecurityInfoW(
                path,
                SE_FILE_OBJECT,
                OWNER_SECURITY_INFORMATION,
                ctypes.byref(p_sid_owner),
                None,
                None,
                None,
                ctypes.byref(pp_sd),
            )
            if res != 0:
                raise _WinError(res, f"Failed to get security info for {path}")

            dw_name = wintypes.DWORD(0)
            dw_domain = wintypes.DWORD(0)
            e_use = ctypes.c_int(0)

            # First call fills in the required buffer sizes (expects ERROR_INSUFFICIENT_BUFFER).
            if not _LookupAccountSidW(
                None,
                p_sid_owner,
                None,
                ctypes.byref(dw_name),
                None,
                ctypes.byref(dw_domain),
                ctypes.byref(e_use),
            ):
                err = _get_last_error()
                if err != 122:  # ERROR_INSUFFICIENT_BUFFER
                    raise _WinError(err, f"Cannot determine owner buffer size for: {path}")

            acct_name_buf = ctypes.create_unicode_buffer(dw_name.value)
            domain_name_buf = ctypes.create_unicode_buffer(dw_domain.value)

            if not _LookupAccountSidW(
                None,
                p_sid_owner,
                acct_name_buf,
                ctypes.byref(dw_name),
                domain_name_buf,
                ctypes.byref(dw_domain),
                ctypes.byref(e_use),
            ):
                raise _WinError(_get_last_error(), f"Could not determine owner for: {path}")

            return acct_name_buf.value

    @staticmethod
    def copy_permissions(src: str, dst: str) -> None:
        """Copy the DACL from *src* to *dst*.

        This is the Windows equivalent of ``os.chown`` for preserving access control when
        copying installed files.  Copies the binary DACL pointer directly without
        parsing, making it more efficient than :meth:`apply` for pure-copy operations.

        Raises:
            OSError: raised by ``ctypes.WinError`` on Windows API failure (carries ``winerror``).
        """
        SE_FILE_OBJECT = 1
        DACL_SECURITY_INFORMATION = 0x00000004

        p_dacl = wintypes.LPVOID()
        with _local_ptr() as pp_sd:
            res = _GetNamedSecurityInfoW(
                src,
                SE_FILE_OBJECT,
                DACL_SECURITY_INFORMATION,
                None,
                None,
                ctypes.byref(p_dacl),
                None,
                ctypes.byref(pp_sd),
            )
            if res != 0:
                raise _WinError(res)
            res = _SetNamedSecurityInfoW(
                dst, SE_FILE_OBJECT, DACL_SECURITY_INFORMATION, None, None, p_dacl, None
            )
            if res != 0:
                raise _WinError(res)

    @staticmethod
    def get_sid_for_user(username: Optional[str] = None) -> str:
        """Return the string SID (e.g. ``S-1-5-21-...``) for *username*.

        If *username* is ``None``, return the SID of the current process owner.
        """
        if not username:
            process_handle = _GetCurrentProcess()
            token_handle = wintypes.HANDLE()

            if not _OpenProcessToken(process_handle, TOKEN_QUERY, ctypes.byref(token_handle)):
                raise _WinError(_get_last_error())

            try:
                return_length = wintypes.DWORD()
                _GetTokenInformation(
                    token_handle, 1, None, 0, ctypes.byref(return_length)
                )  # 1 = TokenUser

                buffer = ctypes.create_string_buffer(return_length.value)
                if not _GetTokenInformation(
                    token_handle, 1, buffer, return_length, ctypes.byref(return_length)
                ):
                    raise _WinError(_get_last_error())

                token_user = ctypes.cast(buffer, ctypes.POINTER(TOKEN_USER)).contents
                sid_ptr = token_user.User.Sid
            finally:
                _CloseHandle(token_handle)

        else:
            sid_size = wintypes.DWORD(0)
            domain_size = wintypes.DWORD(0)
            pe_use = ctypes.c_int(0)

            _LookupAccountNameW(
                None,
                username,
                None,
                ctypes.byref(sid_size),
                None,
                ctypes.byref(domain_size),
                ctypes.byref(pe_use),
            )

            if sid_size.value == 0:
                raise _WinError(_get_last_error())

            sid_buffer = ctypes.create_string_buffer(sid_size.value)
            domain_buffer = ctypes.create_unicode_buffer(domain_size.value)

            if not _LookupAccountNameW(
                None,
                username,
                sid_buffer,
                ctypes.byref(sid_size),
                domain_buffer,
                ctypes.byref(domain_size),
                ctypes.byref(pe_use),
            ):
                raise _WinError(_get_last_error())

            sid_ptr = sid_buffer

        with _local_ptr(wintypes.LPWSTR) as string_sid_ptr:
            if not _ConvertSidToStringSidW(sid_ptr, ctypes.byref(string_sid_ptr)):
                raise _WinError(_get_last_error())
            return string_sid_ptr.value or ""


def get_file_owner(path: str) -> str:
    """Return the account name of the owner of *path*.

    Delegates to :meth:`SecurityDescriptor.get_owner`.
    """
    return SecurityDescriptor.get_owner(path)


def copy_file_permissions(src: str, dst: str) -> None:
    """Copy the DACL from *src* to *dst*.

    Delegates to :meth:`SecurityDescriptor.copy_permissions`.
    """
    SecurityDescriptor.copy_permissions(src, dst)


def get_file_sddl(path: str) -> str:
    """Return the SDDL string for the security descriptor of *path*.

    Raises:
        FileNotFoundError: if *path* does not exist.
        WindowsError: on any Windows API failure.
    """
    return SecurityDescriptor.from_file(path).to_sddl()


def set_file_sddl(path: str, sddl: str) -> None:
    """Apply a security descriptor described by *sddl* to *path*.

    Only the DACL is written; ``O:`` and ``G:`` components in *sddl* are ignored.
    To also transfer ownership pass ``update_ownership=True`` to
    :meth:`SecurityDescriptor.apply` directly.

    Raises:
        WindowsError: on any Windows API failure.
    """
    SecurityDescriptor(sddl).apply(path)
