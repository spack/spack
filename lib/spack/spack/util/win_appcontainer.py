# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Raw ctypes bindings for Windows AppContainer isolation, used by
:class:`spack.sandbox.WindowsAppContainerSandbox`.

This module is Windows-only and must only ever be imported lazily (never at module scope) by
platform-neutral code, since it calls into ``ctypes.WinDLL`` at import time. Spack avoids pywin32
and hand-rolls Windows interop via ``ctypes``/``ctypes.wintypes``, and this module follows the
same style.

Scope is limited to what is genuinely AppContainer-specific: creating and deleting container
profiles, deriving capability SIDs, and spawning a process inside a container. Editing the
DACLs that make a path reachable from inside the container is ordinary ACL work, so it is
delegated to :mod:`spack.util.win_acl`.
"""

import ctypes
import ctypes.wintypes as wintypes
import subprocess
import threading
from typing import BinaryIO, Dict, List, NamedTuple, Optional, Tuple, Union

import spack.util.win_acl as win_acl

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
_userenv = ctypes.WinDLL("userenv", use_last_error=True)
_msvcrt = ctypes.WinDLL("msvcrt", use_last_error=True)

# DeriveCapabilitySidsFromName is exported by KernelBase.dll, not kernel32/advapi32.
_kernelbase = ctypes.WinDLL("kernelbase", use_last_error=True)

SE_GROUP_ENABLED = 0x00000004

ERROR_SUCCESS = 0
ERROR_ALREADY_EXISTS = 183

EXTENDED_STARTUPINFO_PRESENT = 0x00080000
CREATE_UNICODE_ENVIRONMENT = 0x00000400
STARTF_USESTDHANDLES = 0x00000100
PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES = 0x00020009

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

HANDLE_FLAG_INHERIT = 0x00000001
DUPLICATE_SAME_ACCESS = 0x00000002

INFINITE = 0xFFFFFFFF
WAIT_TIMEOUT = 0x00000102


class _SID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Sid", ctypes.c_void_p), ("Attributes", wintypes.DWORD)]


class _SECURITY_CAPABILITIES(ctypes.Structure):
    _fields_ = [
        ("AppContainerSid", ctypes.c_void_p),
        ("Capabilities", ctypes.POINTER(_SID_AND_ATTRIBUTES)),
        ("CapabilityCount", wintypes.DWORD),
        ("Reserved", wintypes.DWORD),
    ]


class _STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.c_void_p),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class _STARTUPINFOEXW(ctypes.Structure):
    _fields_ = [("StartupInfo", _STARTUPINFOW), ("lpAttributeList", ctypes.c_void_p)]


class _PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


# Explicit argtypes/restype for every API used below. This matters more than usual here: handles
# and SIDs are pointer-sized, and ctypes silently truncates unprototyped calls to a 32-bit `int`
# return/argument, which would produce a wrong-but-not-crashing security-relevant bug (e.g. a
# corrupted pseudo-handle from GetCurrentProcess()).

_userenv.CreateAppContainerProfile.restype = ctypes.c_long
_userenv.CreateAppContainerProfile.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    ctypes.POINTER(_SID_AND_ATTRIBUTES),
    wintypes.DWORD,
    ctypes.POINTER(ctypes.c_void_p),
]

_userenv.DeriveAppContainerSidFromAppContainerName.restype = ctypes.c_long
_userenv.DeriveAppContainerSidFromAppContainerName.argtypes = [
    wintypes.LPCWSTR,
    ctypes.POINTER(ctypes.c_void_p),
]

_userenv.DeleteAppContainerProfile.restype = ctypes.c_long
_userenv.DeleteAppContainerProfile.argtypes = [wintypes.LPCWSTR]

_kernelbase.DeriveCapabilitySidsFromName.restype = wintypes.BOOL
_kernelbase.DeriveCapabilitySidsFromName.argtypes = [
    wintypes.LPCWSTR,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)),
    ctypes.POINTER(wintypes.DWORD),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)),
    ctypes.POINTER(wintypes.DWORD),
]

_advapi32.FreeSid.restype = ctypes.c_void_p
_advapi32.FreeSid.argtypes = [ctypes.c_void_p]

_kernel32.LocalFree.restype = wintypes.HLOCAL
_kernel32.LocalFree.argtypes = [wintypes.HLOCAL]

_kernel32.GetCurrentProcess.restype = wintypes.HANDLE
_kernel32.GetCurrentProcess.argtypes = []

_kernel32.GetStdHandle.restype = wintypes.HANDLE
_kernel32.GetStdHandle.argtypes = [wintypes.DWORD]

_kernel32.DuplicateHandle.restype = wintypes.BOOL
_kernel32.DuplicateHandle.argtypes = [
    wintypes.HANDLE,
    wintypes.HANDLE,
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.HANDLE),
    wintypes.DWORD,
    wintypes.BOOL,
    wintypes.DWORD,
]

_kernel32.SetHandleInformation.restype = wintypes.BOOL
_kernel32.SetHandleInformation.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD]

_kernel32.CloseHandle.restype = wintypes.BOOL
_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

_kernel32.CreatePipe.restype = wintypes.BOOL
_kernel32.CreatePipe.argtypes = [
    ctypes.POINTER(wintypes.HANDLE),
    ctypes.POINTER(wintypes.HANDLE),
    ctypes.c_void_p,
    wintypes.DWORD,
]

_kernel32.ReadFile.restype = wintypes.BOOL
_kernel32.ReadFile.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.c_void_p,
]

_kernel32.WaitForSingleObject.restype = wintypes.DWORD
_kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]

_kernel32.GetExitCodeProcess.restype = wintypes.BOOL
_kernel32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]

_kernel32.TerminateProcess.restype = wintypes.BOOL
_kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]

_kernel32.InitializeProcThreadAttributeList.restype = wintypes.BOOL
_kernel32.InitializeProcThreadAttributeList.argtypes = [
    ctypes.c_void_p,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.POINTER(ctypes.c_size_t),
]

_kernel32.UpdateProcThreadAttribute.restype = wintypes.BOOL
_kernel32.UpdateProcThreadAttribute.argtypes = [
    ctypes.c_void_p,
    wintypes.DWORD,
    ctypes.c_size_t,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_void_p,
    ctypes.c_void_p,
]

_kernel32.DeleteProcThreadAttributeList.restype = None
_kernel32.DeleteProcThreadAttributeList.argtypes = [ctypes.c_void_p]

_kernel32.CreateProcessW.restype = wintypes.BOOL
_kernel32.CreateProcessW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPWSTR,
    ctypes.c_void_p,
    ctypes.c_void_p,
    wintypes.BOOL,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.LPCWSTR,
    ctypes.c_void_p,  # LPSTARTUPINFOW; we actually pass &STARTUPINFOEXW (shares the same prefix)
    ctypes.POINTER(_PROCESS_INFORMATION),
]

_msvcrt._get_osfhandle.restype = wintypes.HANDLE
_msvcrt._get_osfhandle.argtypes = [ctypes.c_int]


def _win_error(code: int, name: str) -> OSError:
    """Build an OSError that keeps *both* the failing API and the system error text.

    ``ctypes.WinError(code, descr)`` *replaces* the system message with ``descr``, so passing
    the API name alone silently throws away the only useful part of the diagnostic.
    """
    return ctypes.WinError(code, f"{name}: {ctypes.FormatError(code).strip()}")


def _check_bool(result, name: str):
    if not result:
        raise _win_error(ctypes.get_last_error(), name)
    return result


def _check_win32(code: int, name: str) -> int:
    """Check a Win32 error code returned directly (not via SetLastError)."""
    if code != ERROR_SUCCESS:
        raise _win_error(code, name)
    return code


def _check_hresult(hr: int, name: str) -> int:
    # HRESULTs from these APIs are 0 (S_OK) on success; negative on failure.
    if hr < 0:
        # Most failures here are HRESULT_FROM_WIN32(x), i.e. 0x8007xxxx; unwrap those back to
        # the underlying Win32 code so FormatError produces a meaningful message.
        code = hr & 0xFFFF if (hr & 0xFFFF0000) == 0x80070000 else hr & 0xFFFFFFFF
        raise _win_error(code, name)
    return hr


def probe_support() -> None:
    """Cheaply verify the required AppContainer APIs are resolvable. Side-effect-free."""
    try:
        _userenv.CreateAppContainerProfile
        _userenv.DeriveAppContainerSidFromAppContainerName
        _userenv.DeleteAppContainerProfile
        _kernelbase.DeriveCapabilitySidsFromName
        _advapi32.FreeSid
        _kernel32.InitializeProcThreadAttributeList
        _kernel32.UpdateProcThreadAttribute
        _kernel32.CreateProcessW
    except (AttributeError, OSError) as e:
        raise OSError(f"Windows AppContainer APIs are unavailable: {e}") from e


def create_or_derive_app_container_sid(name: str) -> int:
    """Create (or derive, if already existing) an AppContainer profile and return its SID.

    The returned SID is owned by the caller and must eventually be released via
    :func:`delete_app_container_profile`.
    """
    sid = ctypes.c_void_p()
    hr = _userenv.CreateAppContainerProfile(name, name, name, None, 0, ctypes.byref(sid))
    if hr < 0 and (hr & 0xFFFF) == ERROR_ALREADY_EXISTS:
        hr = _userenv.DeriveAppContainerSidFromAppContainerName(name, ctypes.byref(sid))
    _check_hresult(hr, f"CreateAppContainerProfile({name})")
    assert sid.value is not None
    return sid.value


def delete_app_container_profile(name: str, sid: Optional[int] = None) -> None:
    """Best-effort teardown of an AppContainer profile and its associated SID memory.

    The SID is released even if deleting the profile fails, so a failure here leaks at most
    the (inert) profile registration, never process memory.
    """
    try:
        hr = _userenv.DeleteAppContainerProfile(name)
        _check_hresult(hr, f"DeleteAppContainerProfile({name})")
    finally:
        if sid is not None:
            _advapi32.FreeSid(sid)


def derive_capability_sids(names: List[str]) -> List[int]:
    """Derive capability SIDs (e.g. "internetClient") for use in a SECURITY_CAPABILITIES struct.

    Returned SID memory is owned by the caller (LocalAlloc'd by Windows) and must eventually be
    released via :func:`release_capability_sids`.
    """
    result: List[int] = []
    for name in names:
        group_sids = ctypes.POINTER(ctypes.c_void_p)()
        group_count = wintypes.DWORD(0)
        cap_sids = ctypes.POINTER(ctypes.c_void_p)()
        cap_count = wintypes.DWORD(0)

        ok = _kernelbase.DeriveCapabilitySidsFromName(
            name,
            ctypes.byref(group_sids),
            ctypes.byref(group_count),
            ctypes.byref(cap_sids),
            ctypes.byref(cap_count),
        )
        _check_bool(ok, f"DeriveCapabilitySidsFromName({name})")

        try:
            for i in range(group_count.value):
                _kernel32.LocalFree(group_sids[i])
        finally:
            if group_sids:
                _kernel32.LocalFree(ctypes.cast(group_sids, wintypes.HLOCAL))

        for i in range(cap_count.value):
            result.append(cap_sids[i])
        if cap_sids:
            _kernel32.LocalFree(ctypes.cast(cap_sids, wintypes.HLOCAL))

    return result


def release_capability_sids(sids: List[int]) -> None:
    """Best-effort release of SIDs returned by :func:`derive_capability_sids`."""
    for sid in sids:
        _kernel32.LocalFree(sid)


def grant_access(path: str, sid: int, mask: int) -> None:
    """Add an ACE granting `mask` access to `sid` on `path`, inherited by child files/dirs."""
    sd = win_acl.SecurityDescriptor.from_file(path)
    sd.add_ace(
        win_acl.AccessControlEntry(
            win_acl.AceType.SDDL_ACCESS_ALLOWED,
            flags=[win_acl.AceFlags.SDDL_OBJECT_INHERIT, win_acl.AceFlags.SDDL_CONTAINER_INHERIT],
            rights=mask,
            sid=win_acl.sid_to_string(sid),
        )
    )
    sd.apply(path)


def revoke_access(path: str, sid: int) -> None:
    """Remove every ACE granted to `sid` on `path`. Safe to call even if none exist."""
    sd = win_acl.SecurityDescriptor.from_file(path)
    if sd.remove_ace(sid=win_acl.sid_to_string(sid), remove_all_matches=True):
        sd.apply(path)


def _duplicate_inheritable(handle: int) -> int:
    proc = _kernel32.GetCurrentProcess()
    out = wintypes.HANDLE()
    _check_bool(
        _kernel32.DuplicateHandle(
            proc, handle, proc, ctypes.byref(out), 0, True, DUPLICATE_SAME_ACCESS
        ),
        "DuplicateHandle",
    )
    assert out.value is not None
    return out.value


def _create_pipe() -> Tuple[int, int]:
    class _SECURITY_ATTRIBUTES(ctypes.Structure):
        _fields_ = [
            ("nLength", wintypes.DWORD),
            ("lpSecurityDescriptor", ctypes.c_void_p),
            ("bInheritHandle", wintypes.BOOL),
        ]

    sa = _SECURITY_ATTRIBUTES(
        nLength=ctypes.sizeof(_SECURITY_ATTRIBUTES), lpSecurityDescriptor=None, bInheritHandle=True
    )
    read_h = wintypes.HANDLE()
    write_h = wintypes.HANDLE()
    _check_bool(
        _kernel32.CreatePipe(ctypes.byref(read_h), ctypes.byref(write_h), ctypes.byref(sa), 0),
        "CreatePipe",
    )
    assert read_h.value is not None and write_h.value is not None
    return read_h.value, write_h.value


class _ChildStream(NamedTuple):
    """How one std stream is wired up for a spawn.

    `handle` is the child's end, `parent_end` the parent's end of a pipe (set only when the
    caller asked for ``subprocess.PIPE``), and `owned` says whether `handle` was created for
    this spawn and must therefore be closed once the child has inherited it. Handles borrowed
    from :func:`GetStdHandle` are the *parent's own* stdio and must never be closed -- doing so
    tears down Spack's own console streams.
    """

    handle: Optional[int]
    parent_end: Optional[int]
    owned: bool


def _resolve_std_handle(stream: Union[None, int, BinaryIO], std_handle_const: int) -> _ChildStream:
    """Resolve an executable.py-style stream spec to an inheritable handle for the child."""
    if stream is None:
        h = _kernel32.GetStdHandle(std_handle_const)
        return _ChildStream(h if h else None, None, owned=False)
    if stream is subprocess.PIPE:
        read_h, write_h = _create_pipe()
        # Whichever end stays here must not be inheritable: a copy of it in the child would
        # keep the pipe open forever and the parent's reader would never see EOF.
        if std_handle_const == STD_INPUT_HANDLE:
            # Not exercised by Executable.__call__ today (it never passes PIPE as input), but
            # handled for completeness: the child reads stdin, the parent writes to it.
            _kernel32.SetHandleInformation(write_h, HANDLE_FLAG_INHERIT, 0)
            return _ChildStream(read_h, write_h, owned=True)
        _kernel32.SetHandleInformation(read_h, HANDLE_FLAG_INHERIT, 0)
        return _ChildStream(write_h, read_h, owned=True)
    # A concrete file-like object (e.g. from open()).
    assert not isinstance(stream, int)
    raw = _msvcrt._get_osfhandle(stream.fileno())
    return _ChildStream(_duplicate_inheritable(raw), None, owned=True)


def _build_environment_block(env: Dict[str, str]) -> ctypes.Array:
    # CreateProcess documents the environment block as sorted case-insensitively by name.
    parts = [f"{k}={v}" for k, v in sorted(env.items(), key=lambda kv: kv[0].upper())]
    block = "\0".join(parts) + "\0\0"
    return ctypes.create_unicode_buffer(block)


def _close_handles(*handles: Optional[int]) -> None:
    """Release handles prepared for a spawn that never happened."""
    for h in handles:
        if h is not None:
            _kernel32.CloseHandle(h)


class AppContainerProcess:
    """Minimal ``subprocess.Popen`` stand-in for a process launched inside an AppContainer.

    Only the subset :meth:`spack.util.executable.Executable.__call__` actually uses is
    implemented: ``communicate()``, ``kill()``, ``returncode`` and ``pid``.
    """

    def __init__(
        self,
        process_handle: int,
        thread_handle: int,
        pid: int,
        cmd: List[str],
        stdout_pipe: Optional[int],
        stderr_pipe: Optional[int],
        child_side_handles: List[int],
    ) -> None:
        self._process_handle: Optional[int] = process_handle
        self.pid = pid
        self._cmd = cmd
        self.returncode: Optional[int] = None
        self._results: Dict[str, bytes] = {}
        self._communicated = False

        _kernel32.CloseHandle(thread_handle)
        # The parent's copies of the child's ends must go away before any read: an anonymous
        # pipe only reports EOF once *every* write handle to it is closed.
        for h in child_side_handles:
            _kernel32.CloseHandle(h)

        # Drain concurrently from the moment the child exists, so a child that fills the pipe
        # buffer before communicate() is called cannot deadlock.
        self._threads = [
            self._start_drain(name, pipe)
            for name, pipe in (("stdout", stdout_pipe), ("stderr", stderr_pipe))
            if pipe is not None
        ]

    def _start_drain(self, name: str, handle: int) -> threading.Thread:
        def _drain() -> None:
            try:
                self._results[name] = self._read_all(handle)
            finally:
                _kernel32.CloseHandle(handle)

        t = threading.Thread(target=_drain, name=f"appcontainer-{name}", daemon=True)
        t.start()
        return t

    @staticmethod
    def _read_all(handle: int) -> bytes:
        chunks = []
        buf = ctypes.create_string_buffer(65536)
        bytes_read = wintypes.DWORD(0)
        while True:
            ok = _kernel32.ReadFile(handle, buf, len(buf), ctypes.byref(bytes_read), None)
            if not ok or bytes_read.value == 0:
                break
            chunks.append(buf.raw[: bytes_read.value])
        return b"".join(chunks)

    def communicate(self, timeout: Optional[float] = None) -> Tuple[bytes, bytes]:
        # Callers may re-enter after a TimeoutExpired (Executable.__call__ does exactly that,
        # via kill() then communicate()), so this must be safe to call more than once: the
        # drain threads are started once in __init__ and simply re-joined here.
        if self._communicated:
            return self._results.get("stdout", b""), self._results.get("stderr", b"")

        assert self._process_handle is not None, "process handle is only closed once reaped"
        deadline_ms = INFINITE if timeout is None else int(timeout * 1000)
        wait_result = _kernel32.WaitForSingleObject(self._process_handle, deadline_ms)

        for t in self._threads:
            t.join(timeout=0 if wait_result == WAIT_TIMEOUT else None)

        if wait_result == WAIT_TIMEOUT or any(t.is_alive() for t in self._threads):
            # Only reachable when a finite deadline was given: with timeout=None,
            # deadline_ms is INFINITE and WaitForSingleObject never returns WAIT_TIMEOUT,
            # and thread.join(timeout=None) blocks until the thread finishes.
            assert timeout is not None
            raise subprocess.TimeoutExpired(cmd=self._cmd, timeout=timeout)

        exit_code = wintypes.DWORD(0)
        _check_bool(
            _kernel32.GetExitCodeProcess(self._process_handle, ctypes.byref(exit_code)),
            "GetExitCodeProcess",
        )
        self.returncode = exit_code.value
        self._communicated = True
        _kernel32.CloseHandle(self._process_handle)
        self._process_handle = None

        return self._results.get("stdout", b""), self._results.get("stderr", b"")

    def kill(self) -> None:
        if self._process_handle is not None:
            _kernel32.TerminateProcess(self._process_handle, 1)


def create_process(
    cmd: List[str],
    *,
    env: Dict[str, str],
    cwd: Optional[str] = None,
    stdin: Union[None, int, BinaryIO],
    stdout: Union[None, int, BinaryIO],
    stderr: Union[None, int, BinaryIO],
    sid: int,
    capabilities: List[int],
) -> AppContainerProcess:
    """Launch `cmd` inside the AppContainer identified by `sid`, granted `capabilities`."""
    # SECURITY_CAPABILITIES.Capabilities MUST be NULL when CapabilityCount is 0. Handing
    # CreateProcessW a valid pointer with a zero count fails the whole spawn with
    # ERROR_INVALID_PARAMETER -- which is precisely the no-capabilities, network-blocked case.
    cap_array = (_SID_AND_ATTRIBUTES * len(capabilities))()
    for i, cap_sid in enumerate(capabilities):
        cap_array[i].Sid = cap_sid
        cap_array[i].Attributes = SE_GROUP_ENABLED

    sec_cap = _SECURITY_CAPABILITIES(
        AppContainerSid=sid,
        Capabilities=(
            ctypes.cast(cap_array, ctypes.POINTER(_SID_AND_ATTRIBUTES)) if capabilities else None
        ),
        CapabilityCount=len(capabilities),
        Reserved=0,
    )

    startup_info = _STARTUPINFOEXW()
    startup_info.StartupInfo.cb = ctypes.sizeof(startup_info)

    child_side_handles: List[int] = []
    stdout_pipe = stderr_pipe = None

    any_redirect = stdin is not None or stdout is not None or stderr is not None
    if any_redirect:
        # STARTF_USESTDHANDLES is all-or-nothing, so streams the caller left as None are
        # resolved to the parent's own std handles rather than being left unset.
        in_stream = _resolve_std_handle(stdin, STD_INPUT_HANDLE)
        out_stream = _resolve_std_handle(stdout, STD_OUTPUT_HANDLE)
        err_stream = _resolve_std_handle(stderr, STD_ERROR_HANDLE)
        stdout_pipe, stderr_pipe = out_stream.parent_end, err_stream.parent_end
        startup_info.StartupInfo.dwFlags |= STARTF_USESTDHANDLES
        startup_info.StartupInfo.hStdInput = in_stream.handle or 0
        startup_info.StartupInfo.hStdOutput = out_stream.handle or 0
        startup_info.StartupInfo.hStdError = err_stream.handle or 0
        for stream in (in_stream, out_stream, err_stream):
            if stream.owned and stream.handle:
                child_side_handles.append(stream.handle)

    try:
        # First call is expected to fail with ERROR_INSUFFICIENT_BUFFER; it reports the size.
        attr_list_size = ctypes.c_size_t(0)
        _kernel32.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(attr_list_size))
        attr_list_buf = ctypes.create_string_buffer(attr_list_size.value)
        startup_info.lpAttributeList = ctypes.cast(attr_list_buf, ctypes.c_void_p)
        _check_bool(
            _kernel32.InitializeProcThreadAttributeList(
                startup_info.lpAttributeList, 1, 0, ctypes.byref(attr_list_size)
            ),
            "InitializeProcThreadAttributeList",
        )
        try:
            # `sec_cap` and `cap_array` are only referenced by pointer from the attribute list,
            # so both must stay alive (and unmoved) until CreateProcessW has consumed them.
            _check_bool(
                _kernel32.UpdateProcThreadAttribute(
                    startup_info.lpAttributeList,
                    0,
                    ctypes.c_size_t(PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES),
                    ctypes.byref(sec_cap),
                    ctypes.sizeof(sec_cap),
                    None,
                    None,
                ),
                "UpdateProcThreadAttribute",
            )

            cmd_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(cmd))
            env_block = _build_environment_block(env)
            process_info = _PROCESS_INFORMATION()

            _check_bool(
                _kernel32.CreateProcessW(
                    None,
                    cmd_line,
                    None,
                    None,
                    True,
                    EXTENDED_STARTUPINFO_PRESENT | CREATE_UNICODE_ENVIRONMENT,
                    env_block,
                    cwd,
                    ctypes.cast(ctypes.byref(startup_info), ctypes.c_void_p),
                    ctypes.byref(process_info),
                ),
                f"CreateProcessW({cmd[0]})",
            )
        finally:
            _kernel32.DeleteProcThreadAttributeList(startup_info.lpAttributeList)
    except OSError:
        # No child exists to inherit these, so nothing else will ever close them.
        _close_handles(*child_side_handles, stdout_pipe, stderr_pipe)
        raise

    return AppContainerProcess(
        process_handle=process_info.hProcess,
        thread_handle=process_info.hThread,
        pid=process_info.dwProcessId,
        cmd=cmd,
        stdout_pipe=stdout_pipe,
        stderr_pipe=stderr_pipe,
        child_side_handles=child_side_handles,
    )
