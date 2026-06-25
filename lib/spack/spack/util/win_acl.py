# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows Access Control List (ACL) utilities.

This module is Windows-only — it imports ``ctypes.wintypes`` at the top level and will fail to
import on non-Windows platforms.  Callers must guard the import with
``if sys.platform == "win32":``.

Public API
----------
Semantic types (build ACEs):
    ``AceType``, ``AceFlags``, ``GenericAccessRights``, ``StandardAccessRights``,
    ``FileAccessRights``, ``RegistryKeyAccessRights``, ``MandatoryLabelRights``,
    ``DirectoryServiceObjectAccessRights``, ``AccessControlEntry``

High-level descriptor:
    ``SecurityDescriptor``  — read, modify, and write Windows security descriptors.

Convenience helpers (thin delegates to ``SecurityDescriptor``):
    ``get_file_owner``, ``copy_file_permissions``, ``get_file_sddl``, ``set_file_sddl``
"""

import copy
import ctypes
import os
import re
from ctypes import wintypes  # type: ignore[attr-defined]
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# ── Semantic enum types ────────────────────────────────────────────────────────


class AceStringEnum(Enum):
    """Base enum whose members can be combined with ``|`` to build SDDL strings."""

    def __or__(self, other: "AceStringEnum") -> str:
        if not hasattr(other, "value"):
            raise TypeError(
                f"unsupported operand type(s) for |: {type(self).__name__!r} and"
                f" {type(other).__name__!r}"
            )
        return self.value + other.value

    def __ror__(self, other: str) -> str:
        if not isinstance(other, str):
            raise TypeError(f"Cannot combine {type(self)} with {type(other)}")
        return other + self.value


class AccessRightsEnum(AceStringEnum):
    """Base class for all access-rights enums."""


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
    """Generic access rights strings."""

    SDDL_GENERIC_ALL = "GA"
    SDDL_GENERIC_READ = "GR"
    SDDL_GENERIC_WRITE = "GW"
    SDDL_GENERIC_EXECUTE = "GX"


class StandardAccessRights(AccessRightsEnum):
    """Standard access rights strings."""

    SDDL_READ_CONTROL = "RC"
    SDDL_STANDARD_DELETE = "SD"
    SDDL_WRITE_DAC = "WD"
    SDDL_WRITE_OWNER = "WO"


class DirectoryServiceObjectAccessRights(AccessRightsEnum):
    """Directory service object access rights strings."""

    SDDL_READ_PROPERTY = "RP"
    SDDL_WRITE_PROPERTY = "WP"
    SDDL_CREATE_CHILD = "CC"
    SDDL_DELETE_CHILD = "DC"
    SDDL_LIST_CHILDREN = "LC"
    SDDL_SELF_WRITE = "SW"
    SDDL_LIST_OBJECT = "LO"
    SDDL_DELETE_TREE = "DT"
    SDDL_CONTROL_ACCESS = "CR"


class FileAccessRights(AccessRightsEnum):
    """File access rights strings."""

    SDDL_FILE_ALL = "FA"
    SDDL_FILE_READ = "FR"
    SDDL_FILE_WRITE = "FW"
    SDDL_FILE_EXECUTE = "FX"


class RegistryKeyAccessRights(AccessRightsEnum):
    """Registry key access rights strings."""

    SDDL_KEY_ALL = "KA"
    SDDL_KEY_READ = "KR"
    SDDL_KEY_WRITE = "KW"
    SDDL_KEY_EXECUTE = "KX"


class MandatoryLabelRights(AccessRightsEnum):
    """Mandatory label rights strings."""

    SDDL_NO_READ_UP = "NR"
    SDDL_NO_WRITE_UP = "NW"
    SDDL_NO_EXECUTE_UP = "NX"


class ResourceAttributeAceDataType(Enum):
    """Resource attribute ACE data type strings."""

    SDDL_INT = "TI"
    SDDL_UINT = "TU"
    SDDL_WSTRING = "TS"
    SDDL_SID = "TD"
    SDDL_BLOB = "TX"
    SDDL_BOOLEAN = "TB"


# ── AccessControlEntry ────────────────────────────────────────────────────────


class AccessControlEntry:
    """A single SDDL Access Control Entry.

    Produces the standard SDDL ACE string format::

        (ace_type;ace_flags;rights;object_guid;inherit_object_guid;account_sid)

    Build an ACE using the semantic enum types, then pass it to
    :meth:`SecurityDescriptor.add_ace`::

        ace = AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED,
            flags=AceFlags.SDDL_CONTAINER_INHERIT,
            rights=FileAccessRights.SDDL_FILE_READ,
            sid="BA",
        )
        sd.add_ace(ace)
    """

    def __init__(
        self,
        ace_type: AceType,
        flags: Optional[Union[AceFlags, List[AceFlags]]] = None,
        rights: Optional[Union[AccessRightsEnum, str]] = None,
        obj_guid: Optional[str] = None,
        inh_obj_guid: Optional[str] = None,
        sid: Optional[str] = None,
        resource_attr: Optional[ResourceAttributeAceDataType] = None,
    ):
        self._type = ace_type
        if flags is None:
            self._flags: List[Any] = []
        elif isinstance(flags, list):
            self._flags = list(flags)
        else:
            self._flags = [flags]
        self._rights: Optional[Union[AccessRightsEnum, str]] = rights
        self._obj_guid = obj_guid
        self._inh_obj_guid = inh_obj_guid
        self._sid = sid
        self._resource_attr = resource_attr

    @property
    def ace_type(self) -> AceType:
        return self._type

    @ace_type.setter
    def ace_type(self, val: AceType) -> None:
        self._type = val

    @property
    def flags(self) -> List[Any]:
        return self._flags

    @flags.setter
    def flags(self, val: Optional[Union[AceFlags, List[AceFlags]]]) -> None:
        if val is None:
            self._flags = []
        elif isinstance(val, list):
            self._flags = val
        else:
            self._flags = [val]

    @property
    def rights(self) -> Optional[Union[AccessRightsEnum, str]]:
        return self._rights

    @rights.setter
    def rights(self, val: Union[AccessRightsEnum, str]) -> None:
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

    def add_right(self, right: AccessRightsEnum) -> None:
        """Append *right* to the accumulated rights string.

        Note:
            After multiple ``add_right`` calls the stored rights value becomes a
            concatenated string (e.g. ``"GRFW"``).  If this ACE is round-tripped
            through :meth:`SecurityDescriptor` parsing, ``remove_ace`` filtering by
            individual rights values will not match that concatenated string.  Rights-based
            filtering is reliable only on ACEs parsed directly from a Windows SDDL string
            (where the rights field is always a single 2-letter code or a hex value).
        """
        if self._rights:
            self._rights = self._rights | right  # type: ignore[assignment]
        else:
            self._rights = right

    def _to_ace_string(self) -> str:
        def _fmt(v: Any) -> str:
            if v is None:
                return ""
            if isinstance(v, list):
                return "".join(i.value if hasattr(i, "value") else str(i) for i in v)
            return v.value if hasattr(v, "value") else str(v)

        parts = [
            _fmt(self._type),
            _fmt(self._flags),
            _fmt(self._rights),
            self._obj_guid or "",
            self._inh_obj_guid or "",
            self._sid or "",
        ]
        if self._resource_attr is not None:
            parts.append(_fmt(self._resource_attr))
        return "(" + ";".join(parts) + ")"

    def __repr__(self) -> str:
        return f"AccessControlEntry({self._to_ace_string()!r})"

    def __str__(self) -> str:
        return self._to_ace_string()


# ── Windows ctypes structures ──────────────────────────────────────────────────


class SID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]


class TOKEN_USER(ctypes.Structure):
    _fields_ = [("User", SID_AND_ATTRIBUTES)]


TOKEN_QUERY = 0x0008


# ── DLL handles, _bind helper, and pointer-type aliases ───────────────────────

_advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)  # type: ignore[attr-defined]
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]


def _bind(dll: Any, name: str, argtypes: list, restype: Any) -> Any:
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


# ── Private SDDL parse/create helper ─────────────────────────────────────────


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
        }

        for tag in re.split(r"(?=[OGDS]:)", sddl_string):
            if tag.startswith("O:"):
                parsed["Owner"] = tag[2:]
            elif tag.startswith("G:"):
                parsed["Group"] = tag[2:]
            elif tag.startswith("D:") or tag.startswith("S:"):
                acl_key = "DACL" if tag.startswith("D:") else "SACL"
                ctrl_key = "DACL_CONTROL" if acl_key == "DACL" else "SACL_CONTROL"
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
            ace_type=_SddlHelper._map_enum(parts[0], AceType),
            flags=_SddlHelper._map_flags(parts[1], AceFlags),
            rights=_SddlHelper._map_rights(parts[2]) if parts[2] else None,
            obj_guid=parts[3] if parts[3] else None,
            inh_obj_guid=parts[4] if parts[4] else None,
            sid=parts[5] if parts[5] else None,
        )

    @staticmethod
    def _map_enum(value: str, enum_cls: type) -> Any:
        for member in enum_cls:  # type: ignore[attr-defined]
            if member.value == value:
                return member
        return value

    @staticmethod
    def _map_flags(flag_str: str, enum_cls: type) -> List[Any]:
        flags: List[Any] = []
        if not flag_str:
            return flags
        for chunk in (flag_str[i : i + 2] for i in range(0, len(flag_str), 2)):
            for member in enum_cls:  # type: ignore[attr-defined]
                if member.value == chunk:
                    flags.append(member)
                    break
            else:
                flags.append(chunk)
        return flags

    @staticmethod
    def _map_rights(rights_str: str) -> Any:
        if rights_str.startswith("0x"):
            return rights_str
        for enum_cls in [
            GenericAccessRights,
            StandardAccessRights,
            FileAccessRights,
            RegistryKeyAccessRights,
            MandatoryLabelRights,
            DirectoryServiceObjectAccessRights,
        ]:
            for member in enum_cls:
                if member.value == rights_str:
                    return member
        return rights_str

    @staticmethod
    def create_sddl(security_descriptor: Dict[str, Any]) -> str:
        """Serialise a parsed security descriptor dict back to an SDDL string."""

        def _sid_str(item: Any) -> str:
            return item.value if hasattr(item, "value") else str(item)

        parts = []

        if security_descriptor.get("Owner"):
            parts.append(f"O:{_sid_str(security_descriptor['Owner'])}")

        if security_descriptor.get("Group"):
            parts.append(f"G:{_sid_str(security_descriptor['Group'])}")

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


# ── Private ctypes file-level SD operations ───────────────────────────────────


def _get_file_sddl_raw(path: str) -> str:
    """Read the security descriptor of *path* and return it as an SDDL string."""
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

    pp_sd = wintypes.LPVOID()
    res = _GetNamedSecurityInfoW(
        path, SE_FILE_OBJECT, security_info, None, None, None, None, ctypes.byref(pp_sd)
    )
    if res != 0:
        raise ctypes.WinError(res)

    try:
        string_ptr = wintypes.LPWSTR()
        if not _ConvertSecurityDescriptorToStringSecurityDescriptorW(
            pp_sd, SDDL_REVISION_1, security_info, ctypes.byref(string_ptr), None
        ):
            raise ctypes.WinError()
        try:
            return string_ptr.value or ""
        finally:
            _LocalFree(string_ptr)
    finally:
        _LocalFree(pp_sd)


def _set_file_sddl_raw(path: str, sddl: str) -> None:
    """Apply the security descriptor described by *sddl* to *path*.

    Only components present in *sddl* (owner, group, DACL) are written.  A NULL DACL
    (``D:`` with no ACEs and no present flag) is never applied silently — it would grant
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

    pp_sd = wintypes.LPVOID()
    if not _ConvertStringSecurityDescriptorToSecurityDescriptorW(
        sddl, SDDL_REVISION_1, ctypes.byref(pp_sd), None
    ):
        raise ctypes.WinError()

    try:
        owner = wintypes.LPVOID()
        owner_defaulted = wintypes.BOOL()
        if not _GetSecurityDescriptorOwner(
            pp_sd, ctypes.byref(owner), ctypes.byref(owner_defaulted)
        ):
            raise ctypes.WinError()

        group = wintypes.LPVOID()
        group_defaulted = wintypes.BOOL()
        if not _GetSecurityDescriptorGroup(
            pp_sd, ctypes.byref(group), ctypes.byref(group_defaulted)
        ):
            raise ctypes.WinError()

        dacl_present = wintypes.BOOL()
        dacl = wintypes.LPVOID()
        dacl_defaulted = wintypes.BOOL()
        if not _GetSecurityDescriptorDacl(
            pp_sd, ctypes.byref(dacl_present), ctypes.byref(dacl), ctypes.byref(dacl_defaulted)
        ):
            raise ctypes.WinError()

        # c_void_p.value is None for NULL; use that to distinguish a real pointer from an unset
        # one.  A NULL DACL (dacl_present=True but pointer=NULL) grants everyone full access
        # — never apply it silently.
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

        if security_info == 0:
            return

        res = _SetNamedSecurityInfoW(
            path, SE_FILE_OBJECT, security_info, owner_ptr, group_ptr, dacl_ptr, None
        )
        if res != 0:
            raise ctypes.WinError(res)
    finally:
        _LocalFree(pp_sd)


# ── Comparison helper used by SecurityDescriptor.remove_ace ──────────────────


def _compare_val(val_a: Any, val_b: Any) -> bool:
    """Compare two ACE field values for equality, handling ``None`` correctly."""
    if val_a is None or val_b is None:
        return val_a is val_b
    a = val_a.value if hasattr(val_a, "value") else str(val_a)
    b = val_b.value if hasattr(val_b, "value") else str(val_b)
    return a == b


# ── SecurityDescriptor — the high-level public API ───────────────────────────


class SecurityDescriptor:
    """A mutable Windows security descriptor backed by an SDDL representation.

    Typical usage::

        # Read, modify, and write back
        sd = SecurityDescriptor.from_file(path)
        sd.add_ace(AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED,
            rights=FileAccessRights.SDDL_FILE_READ,
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
            }

    # ── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def from_file(cls, path: str) -> "SecurityDescriptor":
        """Create a ``SecurityDescriptor`` from the security descriptor of *path*.

        Raises:
            FileNotFoundError: if *path* does not exist.
            OSError: on any Windows API failure.
        """
        return cls(_get_file_sddl_raw(path))

    # ── Properties ───────────────────────────────────────────────────────────

    @property
    def owner(self) -> Any:
        return self._parsed["Owner"]

    @owner.setter
    def owner(self, sid: Any) -> None:
        self._parsed["Owner"] = sid

    @property
    def group(self) -> Any:
        return self._parsed["Group"]

    @group.setter
    def group(self, sid: Any) -> None:
        self._parsed["Group"] = sid

    @property
    def dacl(self) -> List[AccessControlEntry]:
        """Return a deep copy of the DACL as a list of ``AccessControlEntry`` objects."""
        return copy.deepcopy(self._parsed["DACL"])

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

    # ── DACL mutation ────────────────────────────────────────────────────────

    def add_ace(self, ace: AccessControlEntry, index: Optional[int] = None) -> None:
        """Add an ``AccessControlEntry`` to the DACL.

        Args:
            ace: The ACE to add.  Build it using the semantic enum types::

                    ace = AccessControlEntry(
                        AceType.SDDL_ACCESS_ALLOWED,
                        rights=FileAccessRights.SDDL_FILE_READ,
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
        sid: Any = None,
        rights: Any = None,
        ace_type: Any = None,
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
                (sid is None or _compare_val(ace.sid, sid))
                and (rights is None or _compare_val(ace.rights, rights))
                and (ace_type is None or _compare_val(ace.ace_type, ace_type))
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
        sid: Any = None,
        rights: Any = None,
        flags: Any = None,
        ace_type: Any = None,
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

    # ── Serialisation and write-back ─────────────────────────────────────────

    def to_sddl(self) -> str:
        """Compile the current state back into an SDDL string."""
        return _SddlHelper.create_sddl(self._parsed)

    def apply(self, path: str) -> None:
        """Write this security descriptor to *path*.

        Raises:
            OSError: on any Windows API failure.
        """
        sddl = self.to_sddl()
        if not sddl:
            return
        _set_file_sddl_raw(path, sddl)

    def __str__(self) -> str:
        return self.to_sddl()

    # ── Windows-specific static helpers ──────────────────────────────────────

    @staticmethod
    def get_owner(path: str) -> str:
        """Return the account name (e.g. ``"SYSTEM"``) of the owner of *path*.

        Unlike ``owner`` (which gives the SID string from the SDDL), this performs a
        ``LookupAccountSidW`` call to resolve the human-readable account name.

        Raises:
            FileNotFoundError: if *path* does not exist.
            OSError: on any Windows API failure.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"No such file or directory: '{path}'")

        SE_FILE_OBJECT = 1
        OWNER_SECURITY_INFORMATION = 0x00000001

        p_sid_owner = wintypes.LPVOID()
        pp_sd = wintypes.LPVOID()

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
            raise ctypes.WinError(res, f"Failed to get security info for {path}")

        try:
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
                err = ctypes.get_last_error()
                if err != 122:  # ERROR_INSUFFICIENT_BUFFER
                    raise ctypes.WinError(err, f"Cannot determine owner buffer size for: {path}")

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
                raise ctypes.WinError(
                    ctypes.get_last_error(), f"Could not determine owner for: {path}"
                )
        finally:
            _LocalFree(pp_sd)

        return acct_name_buf.value

    @staticmethod
    def copy_permissions(src: str, dst: str) -> None:
        """Copy the DACL from *src* to *dst*.

        This is the Windows equivalent of ``os.chown`` for preserving access control when
        copying files into a view.  Copies the binary DACL pointer directly without
        parsing, making it more efficient than :meth:`apply` for pure-copy operations.

        Raises:
            OSError: on any Windows API failure.
        """
        SE_FILE_OBJECT = 1
        DACL_SECURITY_INFORMATION = 0x00000004

        p_dacl = wintypes.LPVOID()
        pp_sd = wintypes.LPVOID()

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
            raise ctypes.WinError(res)

        try:
            res = _SetNamedSecurityInfoW(
                dst, SE_FILE_OBJECT, DACL_SECURITY_INFORMATION, None, None, p_dacl, None
            )
            if res != 0:
                raise ctypes.WinError(res)
        finally:
            _LocalFree(pp_sd)

    @staticmethod
    def get_sid_for_user(username: Optional[str] = None) -> str:
        """Return the string SID (e.g. ``S-1-5-21-...``) for *username*.

        If *username* is ``None``, return the SID of the current process owner.
        """
        if not username:
            process_handle = _GetCurrentProcess()
            token_handle = wintypes.HANDLE()

            if not _OpenProcessToken(process_handle, TOKEN_QUERY, ctypes.byref(token_handle)):
                raise ctypes.WinError()

            try:
                return_length = wintypes.DWORD()
                _GetTokenInformation(
                    token_handle, 1, None, 0, ctypes.byref(return_length)
                )  # 1 = TokenUser

                buffer = ctypes.create_string_buffer(return_length.value)
                if not _GetTokenInformation(
                    token_handle, 1, buffer, return_length, ctypes.byref(return_length)
                ):
                    raise ctypes.WinError()

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
                raise ctypes.WinError()

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
                raise ctypes.WinError()

            sid_ptr = sid_buffer

        string_sid_ptr = wintypes.LPWSTR()
        if not _ConvertSidToStringSidW(sid_ptr, ctypes.byref(string_sid_ptr)):
            raise ctypes.WinError()

        try:
            return string_sid_ptr.value or ""
        finally:
            _LocalFree(string_sid_ptr)


# ── Public module-level helpers ───────────────────────────────────────────────


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
        OSError: on any Windows API failure.
    """
    return SecurityDescriptor.from_file(path).to_sddl()


def set_file_sddl(path: str, sddl: str) -> None:
    """Apply a security descriptor described by *sddl* to *path*.

    Only the components present in *sddl* (owner, group, DACL) are written.

    Raises:
        OSError: on any Windows API failure.
    """
    SecurityDescriptor(sddl).apply(path)
