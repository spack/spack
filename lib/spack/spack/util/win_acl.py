# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows Access Control List (ACL) utilities.

The SDDL enum types and ``AccessControlEntry`` are pure Python and importable on
all platforms.  The ctypes-backed helpers (``WindowsSecurityHelper``,
``SecurityDescriptor``, ``get_file_sddl``) are only available on Windows; they
live inside the ``if sys.platform == "win32":`` block at the bottom of this file.
"""

import copy
import re
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class AceStringEnum(Enum):
    """Base enum whose members can be combined with ``|`` to build SDDL strings."""

    def __or__(self, other: "AceStringEnum") -> str:
        return self.value + other.value

    def __ror__(self, other: str) -> str:
        if not isinstance(other, str):
            raise TypeError(f"Cannot combine {type(self)} with {type(other)}")
        valid_value_classes = [
            AceFlags,
            GenericAccessRights,
            StandardAccessRights,
            DirectoryServiceObjectAccessRights,
            FileAccessRights,
            RegistryKeyAccessRights,
            MandatoryLabelRights,
        ]
        valid_values = [y for x in valid_value_classes for y in x.__members__.values()]
        if other not in valid_values:
            raise TypeError(f"Cannot join ACE rights with invalid value {other!r}")
        return self.value + other


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


class DirectoryServiceObjectAccessRights(Enum):
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


class FileAccessRights(Enum):
    """File access rights strings."""

    SDDL_FILE_ALL = "FA"
    SDDL_FILE_READ = "FR"
    SDDL_FILE_WRITE = "FW"
    SDDL_FILE_EXECUTE = "FX"


class RegistryKeyAccessRights(Enum):
    """Registry key access rights strings."""

    SDDL_KEY_ALL = "KA"
    SDDL_KEY_READ = "KR"
    SDDL_KEY_WRITE = "KW"
    SDDL_KEY_EXECUTE = "KX"


class MandatoryLabelRights(Enum):
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


class AccessControlEntry:
    """A single SDDL Access Control Entry.

    Produces the standard SDDL ACE string format::

        (ace_type;ace_flags;rights;object_guid;inherit_object_guid;account_sid)
    """

    def __init__(
        self,
        ace_type: AceType,
        flags: Optional[AceFlags] = None,
        rights: Optional[AccessRightsEnum] = None,
        obj_guid: Optional[str] = None,
        inh_obj_guid: Optional[str] = None,
        sid: Optional[str] = None,
        resource_attr: Optional[ResourceAttributeAceDataType] = None,
    ):
        self._type = ace_type
        self._flags = flags
        self._rights = rights
        self._obj_guid = obj_guid
        self._inh_obj_guid = inh_obj_guid
        self._sid = sid
        self._resource_attr = resource_attr

    @property
    def rights(self) -> Optional[AccessRightsEnum]:
        return self._rights

    @rights.setter
    def rights(self, val: AccessRightsEnum) -> None:
        self._rights = val

    def add_right(self, right: AccessRightsEnum) -> None:
        if self._rights:
            self._rights = self._rights | right  # type: ignore[assignment]
        else:
            self._rights = right

    @property
    def ace_type(self) -> AceType:
        return self._type

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

    def __str__(self) -> str:
        return self._to_ace_string()


if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    class SID_AND_ATTRIBUTES(ctypes.Structure):  # type: ignore[no-redef]
        _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]

    class TOKEN_USER(ctypes.Structure):  # type: ignore[no-redef]
        _fields_ = [("User", SID_AND_ATTRIBUTES)]

    TOKEN_QUERY = 0x0008

    _advapi32 = ctypes.windll.advapi32
    _kernel32 = ctypes.windll.kernel32

    _OpenProcessToken = _advapi32.OpenProcessToken
    _OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    _OpenProcessToken.restype = wintypes.BOOL

    _GetTokenInformation = _advapi32.GetTokenInformation
    _GetTokenInformation.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,  # TOKEN_INFORMATION_CLASS enum
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    _GetTokenInformation.restype = wintypes.BOOL

    _LookupAccountNameW = _advapi32.LookupAccountNameW
    _LookupAccountNameW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.LPVOID,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(ctypes.c_int),
    ]
    _LookupAccountNameW.restype = wintypes.BOOL

    _ConvertSidToStringSidW = _advapi32.ConvertSidToStringSidW
    _ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
    _ConvertSidToStringSidW.restype = wintypes.BOOL

    _GetNamedSecurityInfoW = _advapi32.GetNamedSecurityInfoW
    _GetNamedSecurityInfoW.argtypes = [
        wintypes.LPCWSTR,
        ctypes.c_int,  # SE_OBJECT_TYPE
        wintypes.DWORD,  # SECURITY_INFORMATION
        ctypes.POINTER(wintypes.LPVOID),  # ppsidOwner
        ctypes.POINTER(wintypes.LPVOID),  # ppsidGroup
        ctypes.POINTER(wintypes.LPVOID),  # ppDacl
        ctypes.POINTER(wintypes.LPVOID),  # ppSacl
        ctypes.POINTER(wintypes.LPVOID),  # ppSecurityDescriptor
    ]
    _GetNamedSecurityInfoW.restype = wintypes.DWORD

    _ConvertSecurityDescriptorToStringSecurityDescriptorW = (
        _advapi32.ConvertSecurityDescriptorToStringSecurityDescriptorW
    )
    _ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes = [
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.LPWSTR),
        ctypes.POINTER(wintypes.ULONG),
    ]
    _ConvertSecurityDescriptorToStringSecurityDescriptorW.restype = wintypes.BOOL

    _LocalFree = _kernel32.LocalFree
    _LocalFree.argtypes = [wintypes.HLOCAL]
    _LocalFree.restype = wintypes.HLOCAL

    _GetCurrentProcess = _kernel32.GetCurrentProcess
    _GetCurrentProcess.restype = wintypes.HANDLE

    class WindowsSecurityHelper:  # type: ignore[no-redef]
        """Static helpers for working with Windows SIDs and SDDL strings."""

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

        @staticmethod
        def _resolve_sid(sid: str) -> str:
            """Return *sid* unchanged.

            SDDL well-known aliases (e.g. ``BA``, ``SY``) are already
            human-readable; full name resolution via ``LookupAccountSidW``
            can be added here if needed.
            """
            return sid

        @staticmethod
        def parse_sddl(sddl_string: str) -> Dict[str, Any]:
            """Parse an SDDL string into a dictionary with keys
            ``Owner``, ``Group``, ``DACL``, and ``SACL``."""
            parsed: Dict[str, Any] = {"Owner": None, "Group": None, "DACL": [], "SACL": []}

            tags = re.split(r"(?=[OGDS]:)", sddl_string)

            for tag in tags:
                if tag.startswith("O:"):
                    parsed["Owner"] = WindowsSecurityHelper._resolve_sid(tag[2:])
                elif tag.startswith("G:"):
                    parsed["Group"] = WindowsSecurityHelper._resolve_sid(tag[2:])
                elif tag.startswith("D:") or tag.startswith("S:"):
                    acl_key = "DACL" if tag.startswith("D:") else "SACL"
                    for ace_str in re.findall(r"\((.*?)\)", tag):
                        parsed[acl_key].append(WindowsSecurityHelper._parse_ace(ace_str))

            return parsed

        @staticmethod
        def _parse_ace(ace_str: str) -> Dict[str, Any]:
            """Parse a single ACE string (e.g. ``A;CI;GR;;;BU``) into a dict."""
            parts = ace_str.split(";")
            if len(parts) < 6:
                return {"raw": ace_str, "error": "Invalid ACE format"}

            return {
                "Type": WindowsSecurityHelper._map_enum(parts[0], AceType),
                "Flags": WindowsSecurityHelper._map_flags(parts[1], AceFlags),
                "Rights": WindowsSecurityHelper._map_rights(parts[2]),
                "ObjectGuid": parts[3] if parts[3] else None,
                "InheritObjectGuid": parts[4] if parts[4] else None,
                "Account": WindowsSecurityHelper._resolve_sid(parts[5]),
            }

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
            chunks = [flag_str[i : i + 2] for i in range(0, len(flag_str), 2)]
            for chunk in chunks:
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
            for enum_cls in [GenericAccessRights, StandardAccessRights, FileAccessRights]:
                for member in enum_cls:
                    if member.value == rights_str:
                        return member
            return rights_str

        @staticmethod
        def create_sddl(security_descriptor: Dict[str, Any]) -> str:
            """Build an SDDL string from a dict produced by :meth:`parse_sddl`."""

            def _val(item: Any) -> str:
                if item is None:
                    return ""
                if hasattr(item, "value"):
                    return item.value
                return str(item)

            parts = []

            if security_descriptor.get("Owner"):
                parts.append(f"O:{_val(security_descriptor['Owner'])}")

            if security_descriptor.get("Group"):
                parts.append(f"G:{_val(security_descriptor['Group'])}")

            for acl_key, prefix in [("DACL", "D:"), ("SACL", "S:")]:
                aces = security_descriptor.get(acl_key)
                if not aces:
                    continue
                ace_strings = []
                for ace in aces:
                    flags_raw = ace.get("Flags", [])
                    ace_flags = (
                        "".join(_val(f) for f in flags_raw)
                        if isinstance(flags_raw, list)
                        else _val(flags_raw)
                    )
                    ace_strings.append(
                        "({};{};{};{};{};{})".format(
                            _val(ace.get("Type")),
                            ace_flags,
                            _val(ace.get("Rights")),
                            _val(ace.get("ObjectGuid")),
                            _val(ace.get("InheritObjectGuid")),
                            _val(ace.get("Account")),
                        )
                    )
                parts.append(prefix + "".join(ace_strings))

            return "".join(parts)

    class SecurityDescriptor:  # type: ignore[no-redef]
        """A mutable Windows security descriptor backed by an SDDL representation.

        Example::

            sd = SecurityDescriptor(get_file_sddl(path))
            sd.add_ace(sid, FileAccessRights.SDDL_FILE_READ)
        """

        def __init__(self, sddl_string: Optional[str] = None) -> None:
            if sddl_string:
                self._raw_data: Dict[str, Any] = WindowsSecurityHelper.parse_sddl(sddl_string)
            else:
                self._raw_data = {"Owner": None, "Group": None, "DACL": [], "SACL": []}

        @property
        def owner(self) -> Any:
            return self._raw_data["Owner"]

        @owner.setter
        def owner(self, sid: Any) -> None:
            self._raw_data["Owner"] = sid

        @property
        def group(self) -> Any:
            return self._raw_data["Group"]

        @group.setter
        def group(self, sid: Any) -> None:
            self._raw_data["Group"] = sid

        @property
        def dacl(self) -> List[Dict[str, Any]]:
            """Return a copy of the DACL list."""
            return copy.deepcopy(self._raw_data["DACL"])

        def add_ace(
            self,
            sid: Any,
            rights: Any,
            ace_type: AceType = AceType.SDDL_ACCESS_ALLOWED,
            flags: Optional[Union[AceFlags, List[AceFlags]]] = None,
            index: Optional[int] = None,
        ) -> None:
            """Add an ACE to the DACL.

            Args:
                sid: SID string or well-known alias (e.g. ``"BA"``).
                rights: Rights enum or hex string.
                ace_type: Allow or deny; defaults to ``SDDL_ACCESS_ALLOWED``.
                flags: Optional ``AceFlags`` or list thereof.
                index: Insert position; appends if ``None``.
            """
            if flags is None:
                flags = []
            if not isinstance(flags, list):
                flags = [flags]

            new_ace: Dict[str, Any] = {
                "Type": ace_type,
                "Flags": flags,
                "Rights": rights,
                "ObjectGuid": None,
                "InheritObjectGuid": None,
                "Account": sid,
            }

            dacl = self._raw_data["DACL"]
            if index is not None and 0 <= index < len(dacl):
                dacl.insert(index, new_ace)
            else:
                dacl.append(new_ace)

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
                remove_all_matches: Remove every match when ``True``; only the
                    first match when ``False``.

            Returns:
                Number of ACEs removed.
            """
            to_remove = []
            for i, ace in enumerate(self._raw_data["DACL"]):
                if (
                    (sid is None or self._compare_val(ace["Account"], sid))
                    and (rights is None or self._compare_val(ace["Rights"], rights))
                    and (ace_type is None or self._compare_val(ace["Type"], ace_type))
                ):
                    to_remove.append(i)
                    if not remove_all_matches:
                        break

            for i in sorted(to_remove, reverse=True):
                del self._raw_data["DACL"][i]

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
            dacl = self._raw_data["DACL"]
            if index < 0 or index >= len(dacl):
                raise IndexError("ACE index out of range")

            ace = dacl[index]
            if sid is not None:
                ace["Account"] = sid
            if rights is not None:
                ace["Rights"] = rights
            if ace_type is not None:
                ace["Type"] = ace_type
            if flags is not None:
                ace["Flags"] = flags if isinstance(flags, list) else [flags]

        def clear_dacl(self) -> None:
            """Remove all ACEs from the DACL."""
            self._raw_data["DACL"] = []

        def to_sddl(self) -> str:
            """Compile the current state back into an SDDL string."""
            return WindowsSecurityHelper.create_sddl(self._raw_data)

        def __str__(self) -> str:
            return self.to_sddl()

        @staticmethod
        def _compare_val(val_a: Any, val_b: Any) -> bool:
            a = val_a.value if hasattr(val_a, "value") else str(val_a)
            b = val_b.value if hasattr(val_b, "value") else str(val_b)
            return a == b

    def get_file_sddl(path: str) -> str:  # type: ignore[no-redef]
        """Return the SDDL string for the security descriptor of *path*.

        Args:
            path: Absolute path to a file or directory.

        Raises:
            FileNotFoundError: if *path* does not exist.
            OSError: on any Windows API failure.
        """
        import os

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
