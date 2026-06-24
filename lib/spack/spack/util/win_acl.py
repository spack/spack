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
        if not hasattr(other, "value"):
            raise TypeError(
                f"unsupported operand type(s) for |: {type(self).__name__!r} and"
                f" {type(other).__name__!r}"
            )
        return self.value + other.value

    def __ror__(self, other: str) -> str:
        if not isinstance(other, str):
            raise TypeError(f"Cannot combine {type(self)} with {type(other)}")
        # other is an already-accumulated SDDL string (e.g. "GRGW"); just append.
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


class AccessControlEntry:
    """A single SDDL Access Control Entry.

    Produces the standard SDDL ACE string format::

        (ace_type;ace_flags;rights;object_guid;inherit_object_guid;account_sid)
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
            through :meth:`~spack.llnl.util.win_acl.WindowsSecurityHelper.parse_sddl`,
            ``remove_ace`` filtering by individual rights values will not match
            that concatenated string.  Rights-based filtering is reliable only
            on ACEs parsed directly from a Windows SDDL string (where the rights
            field is always a single 2-letter code or a hex value).
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


if sys.platform == "win32":
    import ctypes
    import os
    from ctypes import wintypes

    class SID_AND_ATTRIBUTES(ctypes.Structure):  # type: ignore[no-redef]
        _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]

    class TOKEN_USER(ctypes.Structure):  # type: ignore[no-redef]
        _fields_ = [("User", SID_AND_ATTRIBUTES)]

    TOKEN_QUERY = 0x0008

    _advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

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

    _CloseHandle = _kernel32.CloseHandle
    _CloseHandle.argtypes = [wintypes.HANDLE]
    _CloseHandle.restype = wintypes.BOOL

    _SetNamedSecurityInfoW = _advapi32.SetNamedSecurityInfoW
    _SetNamedSecurityInfoW.argtypes = [
        wintypes.LPWSTR,  # pObjectName (mutable, not LPCWSTR)
        ctypes.c_int,  # ObjectType
        wintypes.DWORD,  # SecurityInfo
        wintypes.LPVOID,  # psidOwner
        wintypes.LPVOID,  # psidGroup
        wintypes.LPVOID,  # pDacl
        wintypes.LPVOID,  # pSacl
    ]
    _SetNamedSecurityInfoW.restype = wintypes.DWORD

    _LookupAccountSidW = _advapi32.LookupAccountSidW
    _LookupAccountSidW.argtypes = [
        wintypes.LPCWSTR,  # lpSystemName
        wintypes.LPVOID,  # Sid
        wintypes.LPWSTR,  # Name
        wintypes.LPDWORD,  # cchName
        wintypes.LPWSTR,  # ReferencedDomainName
        wintypes.LPDWORD,  # cchReferencedDomainName
        ctypes.POINTER(ctypes.c_int),  # peUse
    ]
    _LookupAccountSidW.restype = wintypes.BOOL

    _ConvertStringSecurityDescriptorToSecurityDescriptorW = (
        _advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW
    )
    _ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [
        wintypes.LPCWSTR,  # StringSecurityDescriptor
        wintypes.DWORD,  # StringSDRevision
        ctypes.POINTER(wintypes.LPVOID),  # SecurityDescriptor (out)
        ctypes.POINTER(wintypes.ULONG),  # SecurityDescriptorSize (optional out)
    ]
    _ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL

    _GetSecurityDescriptorOwner = _advapi32.GetSecurityDescriptorOwner
    _GetSecurityDescriptorOwner.argtypes = [
        wintypes.LPVOID,  # pSecurityDescriptor
        ctypes.POINTER(wintypes.LPVOID),  # pOwner (out)
        ctypes.POINTER(wintypes.BOOL),  # lpbOwnerDefaulted (out)
    ]
    _GetSecurityDescriptorOwner.restype = wintypes.BOOL

    _GetSecurityDescriptorGroup = _advapi32.GetSecurityDescriptorGroup
    _GetSecurityDescriptorGroup.argtypes = [
        wintypes.LPVOID,  # pSecurityDescriptor
        ctypes.POINTER(wintypes.LPVOID),  # pGroup (out)
        ctypes.POINTER(wintypes.BOOL),  # lpbGroupDefaulted (out)
    ]
    _GetSecurityDescriptorGroup.restype = wintypes.BOOL

    _GetSecurityDescriptorDacl = _advapi32.GetSecurityDescriptorDacl
    _GetSecurityDescriptorDacl.argtypes = [
        wintypes.LPVOID,  # pSecurityDescriptor
        ctypes.POINTER(wintypes.BOOL),  # lpbDaclPresent (out)
        ctypes.POINTER(wintypes.LPVOID),  # pDacl (out)
        ctypes.POINTER(wintypes.BOOL),  # lpbDaclDefaulted (out)
    ]
    _GetSecurityDescriptorDacl.restype = wintypes.BOOL

    def get_file_owner(path: str) -> str:  # type: ignore[no-redef]
        """Return the account name of the owner of *path*.

        Args:
            path: Absolute path to a file or directory.

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

            # First call with null buffers fills in the required sizes.
            # Expected to return False with ERROR_INSUFFICIENT_BUFFER (122).
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

    def copy_file_permissions(src: str, dst: str) -> None:  # type: ignore[no-redef]
        """Copy the DACL from *src* to *dst*.

        This is the Windows equivalent of ``os.chown`` for preserving access
        control when copying files into a view.

        Args:
            src: path whose DACL to read.
            dst: path to which the DACL is applied.

        Raises:
            OSError: on any Windows API failure.

        Note:
            Copies the binary DACL pointer directly without parsing, making it
            more efficient than :func:`set_file_sddl` for pure-copy operations.
            Use :meth:`SecurityDescriptor.apply` when you need to inspect or
            modify the DACL before writing it.
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
            ``Owner``, ``Group``, ``DACL``, ``SACL``, ``DACL_CONTROL``, and
            ``SACL_CONTROL``.  Control flags (e.g. ``AI``) that appear between
            the section prefix and the first ACE are preserved in the
            ``*_CONTROL`` keys so that roundtrips are lossless.

            The ``DACL`` and ``SACL`` values are ``list[AccessControlEntry]``.
            Pass the returned dict to :meth:`create_sddl` to serialise it back;
            do not substitute plain dicts for the ACE entries."""
            parsed: Dict[str, Any] = {
                "Owner": None,
                "Group": None,
                "DACL": [],
                "SACL": [],
                "DACL_CONTROL": "",
                "SACL_CONTROL": "",
            }

            tags = re.split(r"(?=[OGDS]:)", sddl_string)

            for tag in tags:
                if tag.startswith("O:"):
                    parsed["Owner"] = WindowsSecurityHelper._resolve_sid(tag[2:])
                elif tag.startswith("G:"):
                    parsed["Group"] = WindowsSecurityHelper._resolve_sid(tag[2:])
                elif tag.startswith("D:") or tag.startswith("S:"):
                    acl_key = "DACL" if tag.startswith("D:") else "SACL"
                    ctrl_key = "DACL_CONTROL" if acl_key == "DACL" else "SACL_CONTROL"
                    rest = tag[2:]
                    paren = rest.find("(")
                    parsed[ctrl_key] = rest[:paren] if paren >= 0 else rest
                    for ace_str in re.findall(r"\((.*?)\)", tag):
                        parsed[acl_key].append(WindowsSecurityHelper._parse_ace(ace_str))

            return parsed

        @staticmethod
        def _parse_ace(ace_str: str) -> AccessControlEntry:
            """Parse a single ACE string (e.g. ``A;CI;GR;;;BU``) into an
            ``AccessControlEntry``.

            Raises:
                ValueError: if *ace_str* does not contain the required 6 fields.
            """
            parts = ace_str.split(";")
            if len(parts) < 6:
                raise ValueError(f"Invalid ACE format: {ace_str!r}")

            return AccessControlEntry(
                ace_type=WindowsSecurityHelper._map_enum(parts[0], AceType),
                flags=WindowsSecurityHelper._map_flags(parts[1], AceFlags),
                rights=WindowsSecurityHelper._map_rights(parts[2]) if parts[2] else None,
                obj_guid=parts[3] if parts[3] else None,
                inh_obj_guid=parts[4] if parts[4] else None,
                sid=WindowsSecurityHelper._resolve_sid(parts[5]) if parts[5] else None,
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
            """Build an SDDL string from a dict produced by :meth:`parse_sddl`.

            The ``DACL`` and ``SACL`` lists must contain
            :class:`AccessControlEntry` instances.
            """

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

    class SecurityDescriptor:  # type: ignore[no-redef]
        """A mutable Windows security descriptor backed by an SDDL representation.

        Example::

            sd = SecurityDescriptor(get_file_sddl(path))
            sd.add_ace(sid, FileAccessRights.SDDL_FILE_READ)
        """

        def __init__(self, sddl_string: Optional[str] = None) -> None:
            if sddl_string:
                self._parsed: Dict[str, Any] = WindowsSecurityHelper.parse_sddl(sddl_string)
            else:
                self._parsed = {
                    "Owner": None,
                    "Group": None,
                    "DACL": [],
                    "SACL": [],
                    "DACL_CONTROL": "",
                    "SACL_CONTROL": "",
                }

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

        @classmethod
        def from_file(cls, path: str) -> "SecurityDescriptor":
            """Create a ``SecurityDescriptor`` from the security descriptor of *path*.

            Args:
                path: Absolute path to a file or directory.

            Raises:
                FileNotFoundError: if *path* does not exist.
                OSError: on any Windows API failure.
            """
            return cls(get_file_sddl(path))

        @property
        def dacl(self) -> List[AccessControlEntry]:
            """Return a deep copy of the DACL as a list of ``AccessControlEntry`` objects."""
            return copy.deepcopy(self._parsed["DACL"])

        @property
        def sacl(self) -> List[AccessControlEntry]:
            """Return a deep copy of the SACL as a list of ``AccessControlEntry`` objects.

            Note:
                Reading the SACL from a file requires ``SE_SECURITY_PRIVILEGE``,
                which standard user processes do not hold.  :func:`get_file_sddl`
                and :meth:`from_file` therefore do not request SACL information,
                so this list will always be empty for descriptors obtained from a
                file.  Existing SACL entries on a file are preserved by the OS
                when :meth:`apply` is called because ``SACL_SECURITY_INFORMATION``
                is never included in the ``SetNamedSecurityInfoW`` call.
            """
            return copy.deepcopy(self._parsed["SACL"])

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
                index: Insert position (0-based, inclusive of ``len(dacl)`` to
                    append at end).  Raises ``IndexError`` for negative values
                    or values greater than ``len(dacl)``.  Appends when
                    ``None``.
            """
            new_ace = AccessControlEntry(ace_type=ace_type, flags=flags, rights=rights, sid=sid)

            dacl = self._parsed["DACL"]
            if index is None:
                dacl.append(new_ace)
            elif 0 <= index <= len(dacl):
                dacl.insert(index, new_ace)
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
                remove_all_matches: Remove every match when ``True``; only the
                    first match when ``False``.

            Returns:
                Number of ACEs removed.
            """
            to_remove = []
            for i, ace in enumerate(self._parsed["DACL"]):
                if (
                    (sid is None or self._compare_val(ace.sid, sid))
                    and (rights is None or self._compare_val(ace.rights, rights))
                    and (ace_type is None or self._compare_val(ace.ace_type, ace_type))
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

        def to_sddl(self) -> str:
            """Compile the current state back into an SDDL string."""
            return WindowsSecurityHelper.create_sddl(self._parsed)

        def apply(self, path: str) -> None:
            """Write this security descriptor to *path*.

            Args:
                path: Absolute path to a file or directory.

            Raises:
                OSError: on any Windows API failure.
            """
            sddl = self.to_sddl()
            if not sddl:
                return
            set_file_sddl(path, sddl)

        def __str__(self) -> str:
            return self.to_sddl()

        @staticmethod
        def _compare_val(val_a: Any, val_b: Any) -> bool:
            if val_a is None or val_b is None:
                return val_a is val_b
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

    def set_file_sddl(path: str, sddl: str) -> None:  # type: ignore[no-redef]
        """Apply a security descriptor described by *sddl* to *path*.

        Only the components present in *sddl* (owner, group, DACL) are
        written; any component absent from the SDDL leaves the corresponding
        part of the file's existing security descriptor unchanged.  A NULL DACL
        (``D:`` with no ACEs and no ``dacl_present`` flag) is never applied
        silently — it would grant everyone full access.

        Args:
            path: Absolute path to a file or directory.
            sddl: SDDL string describing the security descriptor to apply.

        Raises:
            OSError: on any Windows API failure.

        Note:
            Setting the owner (``O:``) or group (``G:``) requires
            ``SE_TAKE_OWNERSHIP_PRIVILEGE`` or ``SE_RESTORE_PRIVILEGE``.
            Standard user processes lack these privileges; omit ``O:``/``G:``
            from *sddl* to write only the DACL without elevated rights.  For a
            pure DACL copy between two existing files, prefer
            :func:`copy_file_permissions`, which skips the SDDL roundtrip.
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

            # c_void_p.value is None for NULL; use that to distinguish a real
            # pointer from an unset one.  A NULL DACL (dacl_present=True but
            # pointer=NULL) grants everyone full access — never apply it silently.
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
