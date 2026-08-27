# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the Windows PE relocation support built on the MSVC compiler wrapper.
"""

import io
import os
import pathlib

import pytest

import spack.binary_distribution as bd
import spack.concretize
import spack.package_base
import spack.paths
import spack.platforms
import spack.relocate
import spack.spec
import spack.store
import spack.user_environment
import spack.util.executable
import spack.util.filesystem as fsys
import spack.util.spack_yaml as syaml
from spack.util.environment import EnvironmentModifications

pytestmark = pytest.mark.only_windows("Windows PE relocation via the MSVC compiler wrapper")

data_path = os.path.join(spack.paths.test_path, "data", "windows_pe")

#: The compiler wrapper pads every path it records in a PE or an import library out to
#: exactly this many characters. Taken from the source rather than restated here, so the
#: fixtures and the limit check can never disagree about it.
WRAPPER_NAME_LEN = spack.relocate.WRAPPER_NAME_LEN


def wrapper_pad(path: str, pad_char: str = "\\") -> str:
    """Reproduce the wrapper's ``pad_path``: keep the drive letter and colon, insert
    padding, then append the rest of the path, for a total of exactly
    ``WRAPPER_NAME_LEN`` characters."""
    assert len(path) <= WRAPPER_NAME_LEN, f"path too long to pad: {path}"
    return path[:2] + pad_char * (WRAPPER_NAME_LEN - len(path)) + path[2:]


def _load_link_paths():
    """Read the manifest ``generate_fixtures.bat`` writes alongside the fixtures.

    The absolute path each fixture PE was linked at is machine specific, so it is
    recorded at generation time rather than hard coded here.
    """
    manifest = {}
    path = os.path.join(data_path, "fixtures.txt")
    if not os.path.exists(path):
        return manifest
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, _, value = line.partition("=")
            manifest[name.strip()] = value.strip()
    return manifest


FIXTURE_LINK_PATHS = _load_link_paths()


def fixture(name: str) -> str:
    """Absolute path to a checked-in fixture, skipping the test if it is absent.

    ``sfn_calc.*`` in particular can only be produced on a volume with 8.3 short
    filename creation enabled, so it may legitimately be missing.
    """
    path = os.path.join(data_path, name)
    if not os.path.exists(path):
        pytest.skip(f"PE fixture {name} is not checked in; run generate_fixtures.bat")
    return path


def link_path(name: str) -> str:
    """The absolute path fixture ``name`` was linked at, per the manifest."""
    if name not in FIXTURE_LINK_PATHS:
        pytest.skip(f"no recorded link path for {name}; run generate_fixtures.bat")
    return FIXTURE_LINK_PATHS[name]


class _FakeSpec:
    """Minimal stand-in for a Spec on the relocation path.

    ``relocate()`` is faked out in these tests, so the only things the spec is asked
    for are its name and prefix.
    """

    def __init__(self, name="pkg", prefix=None):
        self.name = name
        self.prefix = prefix

    def __getitem__(self, key):
        raise KeyError(key)


class FakeRelocateExe:
    """Stand-in for the compiler wrapper's ``relocate.exe``.

    Answers ``--coff <lib> --report`` and ``--coff <lib> --verify`` out of a registry
    populated by the tests, and records every argv and environment it is handed so
    tests can assert on the exact command lines Spack constructs. Nothing is executed.

    The three ``--verify`` outcomes mirror the wrapper's ``CoffParser::Verify``:
    0 for an import library, 1 for a valid archive that is a static library, and 2 for
    something it cannot parse.

    Exit codes are turned into exceptions the same way :class:`Executable` does, so a
    non-zero exit that the caller did not explicitly excuse raises here too. Without
    that the fake can produce outcomes the real thing never will -- exit 2 out of
    ``--verify`` reaches ``verify_import_lib`` only as a ``ProcessError``, because that
    call passes ``ignore_errors=[1]`` and nothing else.
    """

    def __init__(self):
        self._report = {}
        self._verify = {}
        self.calls = []
        self.envs = []
        self.kwargs = []
        #: argv of every call that came back as a ProcessError rather than a return code
        self.raised = []
        self.returncode = 0
        #: exit code for a relocation (``--pe``) run; non-zero to simulate the wrapper
        #: failing partway through
        self.pe_returncode = 0

    def add_import_lib(self, lib: str, dll_link_path: str) -> None:
        """Register ``lib`` as an import library for the DLL linked at
        ``dll_link_path``. The reported path is padded, exactly as the wrapper
        reports it."""
        self._report[lib] = wrapper_pad(dll_link_path)
        self._verify[lib] = 0

    def add_import_lib_raw(self, lib: str, reported: str) -> None:
        """Register ``lib`` with a verbatim ``DLL:`` payload, for tests that need to
        control the reported text exactly."""
        self._report[lib] = reported
        self._verify[lib] = 0

    def add_static_lib(self, lib: str) -> None:
        """Register ``lib`` as a true static archive (``--verify`` exits 1)."""
        self._report[lib] = None
        self._verify[lib] = 1

    def add_unparsable(self, lib: str) -> None:
        """Register ``lib`` as something the wrapper cannot parse (exits 2)."""
        self._report[lib] = None
        self._verify[lib] = 2

    def __call__(self, *args, **kwargs):
        self.calls.append(args)
        self.envs.append(kwargs.get("extra_env"))
        self.kwargs.append(kwargs)

        if "--coff" in args:
            lib = args[args.index("--coff") + 1]
        else:
            lib = None

        if "--verify" in args:
            self.returncode = self._verify.get(lib, 2)
            out = ""
        elif "--report" in args:
            self.returncode = 0
            reported = self._report.get(lib)
            # An archive with no longnames member prints nothing and still exits 0
            out = "" if reported is None else f"DLL: {reported}\r\n"
        else:
            self.returncode = self.pe_returncode
            out = ""

        self._raise_for_returncode(args, kwargs)
        return out

    def _raise_for_returncode(self, args, kwargs) -> None:
        """Mirror ``Executable.__call__``: a non-zero exit raises unless the caller
        listed it in ``ignore_errors`` or turned ``fail_on_error`` off."""
        ignored = kwargs.get("ignore_errors", ())
        if isinstance(ignored, int):
            ignored = (ignored,)
        if (
            kwargs.get("fail_on_error", True)
            and self.returncode != 0
            and self.returncode not in ignored
        ):
            self.raised.append(args)
            raise spack.util.executable.ProcessError(
                f"Command exited with status {self.returncode}:", " ".join(args)
            )


@pytest.fixture()
def reloc_exe(monkeypatch):
    """A :class:`FakeRelocateExe` substituted for every path that would otherwise
    resolve or bootstrap the real ``relocate.exe``."""
    exe = FakeRelocateExe()
    monkeypatch.setattr(spack.relocate, "relocate", lambda spec=None: exe)
    return exe


def _raise_runtime_error(*args, **kwargs):
    raise RuntimeError("boom")


def env_of(envmod: EnvironmentModifications) -> dict:
    """Apply an EnvironmentModifications to an empty environment and return it."""
    env: dict = {}
    envmod.apply_modifications(env)
    return env


@pytest.mark.parametrize("name", ["calc.dll", "tester.exe"])
def test_extract_spack_id_returns_padded_absolute_path(name):
    """A wrapper-linked PE carries its link-time absolute path, padded to the
    wrapper's fixed width."""
    raw = spack.relocate.extract_spack_id_from_win_pe(fixture(name))

    assert raw is not None
    assert len(raw) == WRAPPER_NAME_LEN, "resource is not padded to the wrapper's width"
    assert "\x00" not in raw, "null terminator was not stripped"
    # normpath is how the padding is collapsed back into a real path
    unpadded = os.path.normpath(raw)
    assert os.path.isabs(unpadded)
    assert os.path.basename(unpadded) == name
    assert unpadded == link_path(name)
    # the padded form is exactly what the wrapper would have produced
    assert raw == wrapper_pad(link_path(name))


def test_extract_spack_id_sfn_fixture():
    """When the link-time path exceeds the wrapper's width, the wrapper falls back to
    an 8.3 short path, which Windows renders upper case."""
    name = "sfn_calc.dll"
    raw = spack.relocate.extract_spack_id_from_win_pe(fixture(name))

    assert raw is not None
    assert len(raw) == WRAPPER_NAME_LEN
    unpadded = os.path.normpath(raw)
    assert unpadded == link_path(name)
    # 8.3 components are upper case and carry a ~N disambiguator
    shortened = [c for c in unpadded.split(os.sep) if "~" in c]
    assert shortened, f"expected 8.3 components in {unpadded}"
    assert all(c == c.upper() for c in shortened)


def test_extract_spack_id_pe_without_resource():
    """A DLL linked by stock link.exe carries no spack resource."""
    assert spack.relocate.extract_spack_id_from_win_pe(fixture("plain.dll")) is None


@pytest.mark.parametrize("name", ["calc.lib", "static.lib"])
def test_extract_spack_id_on_coff_archive(name):
    """COFF archives are not loadable modules, so there is nothing to extract."""
    assert spack.relocate.extract_spack_id_from_win_pe(fixture(name)) is None


def _not_a_pe(tmp_path: pathlib.Path) -> str:
    target = tmp_path / "notabinary.dll"
    target.write_text("this is not a PE file\n", encoding="utf-8")
    return str(target)


@pytest.mark.parametrize(
    "make_target",
    [
        pytest.param(lambda p: str(p / "does-not-exist.dll"), id="missing"),
        pytest.param(str, id="directory"),
        pytest.param(_not_a_pe, id="not-a-pe"),
    ],
)
def test_extract_spack_id_when_the_module_will_not_load(make_target, tmp_path: pathlib.Path):
    """``relocate_win_rpath`` inspects every file it finds in a prefix, so anything
    LoadLibraryExW refuses has to come back as "no resource" rather than raising. All
    three of these land on the same null-handle branch."""
    assert spack.relocate.extract_spack_id_from_win_pe(make_target(tmp_path)) is None


def synth_pe(pe_offset: int = 0x40, signature: bytes = b"PE\x00\x00", size: int = 0x200) -> bytes:
    """Build a byte blob with a DOS header whose e_lfanew points at ``pe_offset``.

    Pass ``signature=b""`` to leave whatever is already at ``pe_offset`` in place.
    """
    buf = bytearray(b"\x00" * size)
    buf[0:2] = b"MZ"
    buf[0x3C:0x40] = pe_offset.to_bytes(4, "little")
    if signature and 0 <= pe_offset <= size - len(signature):
        buf[pe_offset : pe_offset + len(signature)] = signature
    return bytes(buf)


@pytest.mark.parametrize("name", ["calc.dll", "tester.exe", "plain.dll", "calc.lib", "static.lib"])
def test_is_msvc_magic_on_fixtures(name):
    with open(fixture(name), "rb") as f:
        assert spack.relocate.is_msvc_magic(f) is True


@pytest.mark.parametrize(
    "data,expected",
    [
        (b"", False),
        (b"short", False),
        # a COFF archive (import or static library)
        (b"!<arch>\n" + b"\x00" * 64, True),
        # too small to hold an e_lfanew
        (b"MZ" + b"\x00" * 0x30, False),
        # well formed
        (synth_pe(), True),
        # e_lfanew points past the end of the file
        (synth_pe(pe_offset=0x10000), False),
        # e_lfanew points at something that is not the PE signature
        (synth_pe(signature=b"NE\x00\x00"), False),
        # e_lfanew of 0 lands back on the "MZ" of the DOS header
        (synth_pe(pe_offset=0, signature=b""), False),
        # plain text of sufficient length
        (b"#!/bin/sh\n" + b"echo hello\n" * 16, False),
    ],
)
def test_is_msvc_magic_synthetic(data, expected):
    assert spack.relocate.is_msvc_magic(io.BytesIO(data)) is expected


@pytest.mark.parametrize("name", ["calc.dll", "calc.lib"])
def test_file_type_classifies_pe_as_binary(name):
    """``file_type`` is what keeps PEs out of the text-relocation path. One of each
    shape is enough: the exe and the static lib go down the same two branches as the
    dll and the import lib respectively, and ``is_msvc_magic`` is covered directly."""
    with open(fixture(name), "rb") as f:
        assert bd.file_type(f) == bd.FileTypes.BINARY


def test_verify_import_lib_only_excuses_the_static_library_exit(reloc_exe):
    """``ignore_errors=[1]`` is what keeps a static library from raising. Exit 2 is not
    excused, so a wrapper that cannot parse the file raises and must be caught -- one
    unreadable .lib cannot abort the whole relocation pass."""
    static, broken = r"C:\opt\pkg\lib\static.lib", r"C:\opt\pkg\lib\broken.lib"
    reloc_exe.add_static_lib(static)
    reloc_exe.add_unparsable(broken)

    assert spack.relocate.verify_import_lib(static, reloc_exe=reloc_exe) is False
    assert reloc_exe.raised == [], "exit 1 is excused, so it must not raise at all"

    assert spack.relocate.verify_import_lib(broken, reloc_exe=reloc_exe) is False
    assert len(reloc_exe.raised) == 1, "exit 2 is not excused, so it must raise"


def test_get_importlib_target_unpads_nothing_and_strips_cr(reloc_exe):
    """The reported path is returned verbatim, minus the trailing carriage return."""
    lib = r"C:\opt\pkg\lib\calc.lib"
    dll = r"C:\opt\pkg\bin\calc.dll"
    reloc_exe.add_import_lib(lib, dll)

    reported = spack.relocate.get_importlib_target(lib, reloc_exe=reloc_exe)

    assert reported == wrapper_pad(dll)
    assert not reported.endswith("\r")
    assert os.path.normpath(reported) == dll


def test_get_importlib_target_no_output(reloc_exe):
    """An archive with no longnames member reports nothing and still exits 0."""
    lib = r"C:\opt\pkg\lib\static.lib"
    reloc_exe.add_static_lib(lib)

    assert spack.relocate.get_importlib_target(lib, reloc_exe=reloc_exe) is None


def test_import_lib_targets_maps_padded_report(reloc_exe):
    """The padded path the wrapper reports is normalized before it is matched."""
    lib = r"C:\stage\pkg\lib\calc.lib"
    reloc_exe.add_import_lib(lib, r"C:\stage\pkg\bin\calc.dll")

    result = spack.relocate._import_lib_targets(
        [lib, r"C:\install\pkg\bin\calc.dll"],
        {r"C:\stage\pkg": r"C:\install\pkg"},
        reloc_exe=reloc_exe,
    )

    assert result == {r"C:\install\pkg\bin\calc.dll": lib}


def test_import_lib_targets_is_case_insensitive(reloc_exe):
    """Windows paths are case insensitive, and the wrapper reports whatever casing
    the linker recorded, so a prefix must match regardless of case."""
    lib = r"C:\stage\pkg\lib\calc.lib"
    reloc_exe.add_import_lib(lib, r"c:\StAgE\PkG\bin\calc.dll")

    result = spack.relocate._import_lib_targets(
        [lib], {r"C:\STAGE\PKG": r"C:\install\pkg"}, reloc_exe=reloc_exe
    )

    assert result == {r"C:\install\pkg\bin\calc.dll": lib}


def test_import_lib_targets_matches_uppercase_sfn_prefix(reloc_exe):
    """8.3 prefixes come back from GetShortPathNameW upper cased; the DLL reference
    inside the import library may be in any case."""
    lib = r"C:\install\pkg\lib\calc.lib"
    reloc_exe.add_import_lib(lib, r"C:\progra~1\spack\bin\calc.dll")

    result = spack.relocate._import_lib_targets(
        [lib], {r"C:\PROGRA~1\SPACK": r"C:\install\pkg"}, reloc_exe=reloc_exe
    )

    assert result == {r"C:\install\pkg\bin\calc.dll": lib}


def test_import_lib_targets_longest_prefix_wins(reloc_exe):
    """A nested prefix must beat its parent, however the mapping is ordered."""
    lib = r"C:\install\pkg\lib\calc.lib"
    reloc_exe.add_import_lib(lib, r"C:\opt\spack\pkg\bin\calc.dll")

    result = spack.relocate._import_lib_targets(
        [lib],
        {r"C:\opt": r"C:\wrong", r"C:\opt\spack\pkg": r"C:\install\pkg"},
        reloc_exe=reloc_exe,
    )

    assert result == {r"C:\install\pkg\bin\calc.dll": lib}


def test_import_lib_targets_empty_prefix_map(reloc_exe):
    """An empty alternation compiles to a regex that matches everything with an empty
    match, which must not be mistaken for a prefix hit."""
    lib = r"C:\install\pkg\lib\calc.lib"
    reloc_exe.add_import_lib(lib, r"C:\stage\pkg\bin\calc.dll")

    assert spack.relocate._import_lib_targets([lib], {}, reloc_exe=reloc_exe) == {}
    # the wrapper is never consulted when there is nothing to map
    assert reloc_exe.calls == []


def test_import_lib_targets_mixed_case_extension(reloc_exe):
    """Windows filenames are case insensitive, so .LIB is still an import library."""
    lib = r"C:\stage\pkg\lib\CALC.LIB"
    reloc_exe.add_import_lib(lib, r"C:\stage\pkg\bin\calc.dll")

    result = spack.relocate._import_lib_targets(
        [lib], {r"C:\stage\pkg": r"C:\install\pkg"}, reloc_exe=reloc_exe
    )

    assert result == {r"C:\install\pkg\bin\calc.dll": lib}


def test_import_lib_targets_stage_mode_maps_whole_file(reloc_exe):
    """In the stage flow the mapping keys are full file paths, not directories, and
    the value is already the final location of that one PE."""
    lib = r"C:\install\pkg\lib\calc.lib"
    stage_dll = r"C:\stage\pkg\build\calc.dll"
    install_dll = r"C:\install\pkg\bin\calc.dll"
    reloc_exe.add_import_lib(lib, stage_dll)

    result = spack.relocate._import_lib_targets(
        [lib], {stage_dll: install_dll}, reloc_exe=reloc_exe, stage=True
    )

    assert result == {install_dll: lib}


def test_import_lib_targets_unmatched_lib_is_skipped(reloc_exe):
    """An import library pointing outside every known prefix is left alone."""
    lib = r"C:\install\pkg\lib\system.lib"
    reloc_exe.add_import_lib(lib, r"C:\Windows\System32\kernel32.dll")

    result = spack.relocate._import_lib_targets(
        [lib], {r"C:\stage\pkg": r"C:\install\pkg"}, reloc_exe=reloc_exe
    )

    assert result == {}


def test_import_lib_targets_static_lib_is_skipped(reloc_exe):
    """.lib covers both import and static libraries; only the former are relocated."""
    static = r"C:\install\pkg\lib\static.lib"
    reloc_exe.add_static_lib(static)

    result = spack.relocate._import_lib_targets(
        [static], {r"C:\stage\pkg": r"C:\install\pkg"}, reloc_exe=reloc_exe
    )

    assert result == {}


def test_import_lib_targets_ignores_non_lib_targets(reloc_exe):
    """DLLs and EXEs are relocation targets, but the association is driven off the
    import libraries."""
    targets = [r"C:\install\pkg\bin\calc.dll", r"C:\install\pkg\bin\tester.exe"]

    result = spack.relocate._import_lib_targets(
        targets, {r"C:\stage\pkg": r"C:\install\pkg"}, reloc_exe=reloc_exe
    )

    assert result == {}
    assert reloc_exe.calls == []


class _WrapperPackage:
    def __init__(self, bin_dir: pathlib.Path):
        self._bin_dir = bin_dir

    def bin_dir(self) -> pathlib.Path:
        return self._bin_dir


class _WrapperSpec:
    """Stand-in for a concrete ``compiler-wrapper`` node."""

    def __init__(self, bin_dir: pathlib.Path):
        self.package = _WrapperPackage(bin_dir)


class _SpecWithWrapper(_FakeSpec):
    def __init__(self, wrapper, **kwargs):
        super().__init__(**kwargs)
        self._wrapper = wrapper

    def __getitem__(self, key):
        if key == "compiler-wrapper":
            return self._wrapper
        raise KeyError(key)


@pytest.fixture()
def wrapper_env(monkeypatch):
    """Capture which spec the vcvars environment is derived from."""
    derived = []

    def _envmod(spec, set_package_py_globals=True):
        derived.append(spec)
        env = EnvironmentModifications()
        env.set("VCVARS_APPLIED", "yes")
        return env

    monkeypatch.setattr(spack.user_environment, "environment_modifications_for_specs", _envmod)
    return derived


def test_setup_relocate_run_attaches_the_wrapper_environment(tmp_path, wrapper_env):
    """relocate.exe shells out to link.exe, lib.exe and dumpbin, so it is useless
    without the wrapper's INCLUDE/LIB/PATH attached to it."""
    wrapper = _WrapperSpec(tmp_path / "bin")

    exe = spack.relocate.setup_relocate_run(wrapper)

    assert exe.exe[0] == str(tmp_path / "bin" / "relocate.exe")
    assert wrapper_env == [wrapper], "the environment came from the wrapper spec"
    assert env_of(exe._default_envmod)["VCVARS_APPLIED"] == "yes"


def test_relocate_uses_the_wrapper_already_in_the_spec(tmp_path, wrapper_env, monkeypatch):
    """A package built with the wrapper carries it as a dependency, so there is nothing
    to bootstrap."""
    monkeypatch.setattr(
        spack.relocate,
        "bootstrap_relocate",
        _raise_runtime_error,  # must not be reached
    )
    wrapper = _WrapperSpec(tmp_path / "bin")

    exe = spack.relocate.relocate(_SpecWithWrapper(wrapper, name="pkg"))

    assert exe.exe[0] == str(tmp_path / "bin" / "relocate.exe")


@pytest.mark.parametrize("spec", [None, _FakeSpec(name="pkg")], ids=["no-spec", "no-wrapper"])
def test_relocate_bootstraps_when_the_spec_cannot_provide_the_wrapper(spec, monkeypatch):
    """Relocating a buildcache tarball happens without the wrapper in hand, so it has to
    be bootstrapped. ``_FakeSpec`` raises KeyError exactly as a Spec without the
    dependency does."""
    sentinel = object()
    monkeypatch.setattr(spack.relocate, "bootstrap_relocate", lambda: sentinel)

    assert spack.relocate.relocate(spec) is sentinel


def test_wrapper_failure_during_relocation_propagates(temporary_store, reloc_exe):
    """``relocate_pe`` passes ``fail_on_error=True`` on purpose. A wrapper that dies
    partway through has left some binaries rewritten and others not, so the install has
    to fail rather than land a prefix whose DLL references half point at the stage."""
    reloc_exe.pe_returncode = 1

    with pytest.raises(spack.util.executable.ProcessError):
        spack.relocate.relocate_windows_binaries(
            [r"C:\install\pkg\bin\a.dll", r"C:\install\pkg\bin\b.dll"],
            _FakeSpec(name="pkg", prefix=r"C:\install\pkg"),
            {r"C:\stage\pkg": r"C:\install\pkg"},
        )

    # it gave up on the first failure instead of plowing through the rest
    assert len([c for c in reloc_exe.calls if "--pe" in c]) == 1


def pe_of_length(total: int, root: str = r"C:\install") -> str:
    """An absolute PE path exactly ``total`` characters long."""
    suffix = r"\calc.dll"
    filler = total - len(root) - len(suffix)
    assert filler > 0, "requested path is too short to build"
    return root + "\\" + "a" * (filler - 1) + suffix


class _SfnProbe:
    """Stands in for the 8.3 probe, recording the paths it is asked about so tests can
    assert both the answer used and whether the filesystem was touched at all."""

    def __init__(self, enabled: bool):
        self.enabled = enabled
        self.paths: list = []

    def __call__(self, path=None):
        self.paths.append(path)
        return self.enabled


@pytest.fixture()
def sfn_enabled(monkeypatch):
    probe = _SfnProbe(True)
    monkeypatch.setattr(spack.relocate.fs, "short_filenames_enabled", probe)
    return probe


@pytest.fixture()
def sfn_disabled(monkeypatch):
    probe = _SfnProbe(False)
    monkeypatch.setattr(spack.relocate.fs, "short_filenames_enabled", probe)
    return probe


@pytest.mark.parametrize("length", [30, WRAPPER_NAME_LEN - 1, WRAPPER_NAME_LEN])
def test_paths_within_the_budget_are_recorded_directly(
    length, sfn_disabled, temporary_store, reloc_exe
):
    """Up to and including the wrapper's width the path is stored as-is, so 8.3 support
    is irrelevant and must not even be probed."""
    pe = pe_of_length(length)

    spack.relocate.relocate_windows_binaries(
        [pe], _FakeSpec(name="pkg", prefix=r"C:\install"), {r"C:\stage": r"C:\install"}
    )

    assert sfn_disabled.paths == []
    assert [c[c.index("--pe") + 1] for c in reloc_exe.calls if "--pe" in c] == [pe]


def test_overlong_path_falls_back_to_sfn_when_available(sfn_enabled, temporary_store, reloc_exe):
    """Past the budget the wrapper stores the path's 8.3 form instead, which is fine so
    long as the volume actually creates short names."""
    pe = pe_of_length(WRAPPER_NAME_LEN + 1)
    prefix = r"C:\install"

    spack.relocate.relocate_windows_binaries(
        [pe], _FakeSpec(name="pkg", prefix=prefix), {r"C:\stage": prefix}
    )

    assert sfn_enabled.paths == [prefix], "the install volume is what gets probed"
    assert [c[c.index("--pe") + 1] for c in reloc_exe.calls if "--pe" in c] == [pe]


def test_overlong_path_without_sfn_is_an_error(sfn_disabled, temporary_store, reloc_exe):
    """With no room to record the path and no short form to fall back on, the wrapper
    cannot describe where this DLL lives. Relocating anyway would leave the binary
    pointing at nothing, so fail before writing it."""
    pe = pe_of_length(WRAPPER_NAME_LEN + 1)
    prefix = r"C:\a-very-long-install-tree-root\that-the-user-should-shorten"

    with pytest.raises(spack.relocate.WindowsPathTooLongError) as excinfo:
        spack.relocate.relocate_windows_binaries(
            [pe], _FakeSpec(name="pkg", prefix=prefix), {r"C:\stage": prefix}
        )

    assert reloc_exe.calls == [], "nothing is rewritten once the check fails"
    message = str(excinfo.value)
    assert str(WRAPPER_NAME_LEN) in message
    assert pe in message
    # the prefix is the knob the user can actually turn, so it belongs in the message
    # even though the check is per binary, and either remedy works so name both
    assert prefix in message
    assert "config:install_tree:root" in message
    assert "fsutil 8dot3name set 0" in message


@pytest.fixture()
def stage_tree(tmp_path: pathlib.Path, monkeypatch, sfn_enabled):
    """An install prefix populated with PEs, plus the stage locations they were
    linked at. Returns (spec, stage_root, resources).

    The 8.3 probe is pinned because these prefixes are real ``tmp_path`` paths: they sit
    close enough to the wrapper's width that a long enough TEMP or user name would push
    them over it, and the outcome would then depend on how the machine happens to be
    configured. The budget itself is covered separately.
    """
    prefix = tmp_path / "install" / "pkg"
    stage = tmp_path / "stage" / "pkg"
    (prefix / "bin").mkdir(parents=True)
    (prefix / "lib").mkdir(parents=True)

    files = {
        "bin/calc.dll": "build/calc.dll",
        "bin/tester.exe": "build/tester.exe",
        # a PE with no spack resource, e.g. a vendored third party DLL
        "bin/vendor.dll": None,
    }
    resources = {}
    for rel, stage_rel in files.items():
        path = prefix / rel
        path.write_bytes(b"MZ")
        if stage_rel:
            # the wrapper stores the padded absolute stage path
            resources[str(path)] = wrapper_pad(str(stage / stage_rel))
    (prefix / "lib" / "calc.lib").write_bytes(b"!<arch>\n")

    monkeypatch.setattr(
        spack.relocate, "extract_spack_id_from_win_pe", lambda pe: resources.get(pe)
    )
    return _FakeSpec(name="pkg", prefix=str(prefix)), stage, resources


def test_relocate_win_rpath_maps_stage_to_install(temporary_store, reloc_exe, stage_tree):
    spec, stage, _ = stage_tree
    lib = os.path.join(spec.prefix, "lib", "calc.lib")
    reloc_exe.add_import_lib(lib, str(stage / "build" / "calc.dll"))

    spack.relocate.relocate_win_rpath(spec)

    env = env_of(reloc_exe.envs[-1])
    mapping = dict(p.split("|") for p in env["SPACK_RELOCATE_PATH"].split(os.pathsep))

    # keys are normalized full stage file paths, values the installed file
    assert mapping == {
        str(stage / "build" / "calc.dll"): os.path.join(spec.prefix, "bin", "calc.dll"),
        str(stage / "build" / "tester.exe"): os.path.join(spec.prefix, "bin", "tester.exe"),
    }
    # every key names a PE, which is what puts the wrapper into exact-match stage mode
    assert all(k.lower().endswith((".dll", ".exe")) for k in mapping)


def test_relocate_win_rpath_pairs_import_lib_with_its_dll(temporary_store, reloc_exe, stage_tree):
    spec, stage, _ = stage_tree
    lib = os.path.join(spec.prefix, "lib", "calc.lib")
    reloc_exe.add_import_lib(lib, str(stage / "build" / "calc.dll"))

    spack.relocate.relocate_win_rpath(spec)

    coff_calls = {
        c[c.index("--pe") + 1]: c[c.index("--coff") + 1]
        for c in reloc_exe.calls
        if "--pe" in c and "--coff" in c
    }
    assert coff_calls == {os.path.join(spec.prefix, "bin", "calc.dll"): lib}


def test_relocate_win_rpath_skips_pe_without_resource(temporary_store, reloc_exe, stage_tree):
    """A PE Spack did not link has no stage location to map, so it contributes no
    prefix entry -- but it is still a relocation target, since it may reference
    DLLs that moved."""
    spec, _, _ = stage_tree

    spack.relocate.relocate_win_rpath(spec)

    env = env_of(reloc_exe.envs[-1])
    assert "vendor.dll" not in env["SPACK_RELOCATE_PATH"]
    relocated = [c[c.index("--pe") + 1] for c in reloc_exe.calls if "--pe" in c]
    assert os.path.join(spec.prefix, "bin", "vendor.dll") in relocated


def test_relocate_win_rpath_skips_symlinks(temporary_store, reloc_exe, stage_tree):
    """Symlinked DLLs point at a real file that is relocated on its own; rewriting
    them would corrupt the link target."""
    spec, stage, resources = stage_tree
    link = os.path.join(spec.prefix, "bin", "alias.dll")
    try:
        fsys.symlink(os.path.join(spec.prefix, "bin", "calc.dll"), link)
    except Exception as e:
        pytest.skip(f"cannot create symlinks in this environment: {e}")
    if not fsys.islink(link):
        pytest.skip("symlink was materialized as a real file in this environment")
    # even if it somehow carried a resource, it must not contribute a mapping
    resources[link] = wrapper_pad(str(stage / "build" / "alias.dll"))

    spack.relocate.relocate_win_rpath(spec)

    env = env_of(reloc_exe.envs[-1])
    assert "alias.dll" not in env["SPACK_RELOCATE_PATH"]


def test_relocate_win_rpath_enforces_the_path_budget(
    tmp_path: pathlib.Path, sfn_disabled, temporary_store, reloc_exe, monkeypatch
):
    """The stage-to-install pass goes through the same check, so an install tree deep
    enough to push its DLLs past the wrapper's width fails there too rather than only on
    the buildcache path."""
    prefix = tmp_path / ("d" * 50) / "pkg"
    (prefix / "bin").mkdir(parents=True)
    dll = prefix / "bin" / "calc.dll"
    dll.write_bytes(b"MZ")
    assert len(str(dll)) > WRAPPER_NAME_LEN, "test needs a path past the wrapper's budget"
    monkeypatch.setattr(
        spack.relocate,
        "extract_spack_id_from_win_pe",
        lambda pe: wrapper_pad(r"C:\stage\pkg\build\calc.dll"),
    )

    with pytest.raises(spack.relocate.WindowsPathTooLongError):
        spack.relocate.relocate_win_rpath(_FakeSpec(name="pkg", prefix=str(prefix)))

    assert reloc_exe.calls == [], "nothing is rewritten once the check fails"


class _FakeWrapperNode:
    def __init__(self, has_code):
        self.package = type("_Pkg", (), {"has_code": has_code})()


class _DispatchSpec:
    """Spec stand-in for the WindowsRPath dispatch, which only consults
    ``external``, ``satisfies("%compiler-wrapper")`` and the wrapper node."""

    def __init__(self, has_wrapper=True, has_code=True, external=False):
        self.external = external
        self._has_wrapper = has_wrapper
        self._wrapper = _FakeWrapperNode(has_code)

    def satisfies(self, query):
        assert query == "%compiler-wrapper"
        return self._has_wrapper

    def __getitem__(self, key):
        if key == "compiler-wrapper" and self._has_wrapper:
            return self._wrapper
        raise KeyError(key)


class _DispatchPkg(spack.package_base.WindowsRPath):
    def __init__(self, spec):
        self.spec = spec


@pytest.fixture()
def dispatch_recorder(monkeypatch):
    """Record which of the two runtime-linkage strategies gets used."""
    calls = {"relocate": [], "simulated": []}

    class _RecordingSimulatedRPath:
        def __init__(self, pkg):
            calls["simulated"].append(pkg)

        def add_library_dependent(self, *dest):
            pass

        def add_rpath(self, *paths):
            pass

        def establish_link(self):
            pass

    monkeypatch.setattr(
        spack.package_base, "relocate_win_rpath", lambda spec: calls["relocate"].append(spec)
    )
    monkeypatch.setattr(spack.package_base, "WindowsSimulatedRPath", _RecordingSimulatedRPath)
    return calls


def test_dispatch_uses_wrapper_when_available(dispatch_recorder):
    """A compiler-wrapper package that carries code is the real MSVC wrapper, so
    relocation is driven through it."""
    spec = _DispatchSpec(has_code=True)

    _DispatchPkg(spec).windows_establish_runtime_linkage()

    assert dispatch_recorder["relocate"] == [spec]
    assert dispatch_recorder["simulated"] == []


def test_dispatch_falls_back_without_wrapper_code(dispatch_recorder):
    """On Windows the stock compiler-wrapper package sets ``has_code = False`` and
    installs a placeholder, so the symlink-based simulated rpath is used."""
    spec = _DispatchSpec(has_code=False)

    pkg = _DispatchPkg(spec)
    pkg.windows_establish_runtime_linkage()

    assert dispatch_recorder["relocate"] == []
    assert dispatch_recorder["simulated"] == [pkg]


def test_dispatch_noop_without_compiler_wrapper(dispatch_recorder):
    _DispatchPkg(_DispatchSpec(has_wrapper=False)).windows_establish_runtime_linkage()

    assert dispatch_recorder["relocate"] == []
    assert dispatch_recorder["simulated"] == []


@pytest.mark.parametrize("has_code", [True, False])
def test_dispatch_skips_externals(dispatch_recorder, has_code):
    """Spack should not modify the bin directory of something it did not install."""
    spec = _DispatchSpec(has_code=has_code, external=True)

    _DispatchPkg(spec).windows_establish_runtime_linkage()

    assert dispatch_recorder["relocate"] == []
    assert dispatch_recorder["simulated"] == []


@pytest.fixture()
def mock_spec(install_mockery):
    """A concretized mock spec whose prefix lives in a temporary store.

    ``default_mock_concretization`` cannot be used here: it pulls in the ``config``
    fixture, which conflicts with the ``mutable_config`` that ``install_mockery``
    requires.
    """
    return spack.concretize.concretize_one(spack.spec.Spec("trivial-install-test-package"))


class _PePlatform:
    """Platform stub that selects the PE branch of ``relocate_package``.

    The test suite swaps in ``spack.platforms.Test``, which reports ELF (or Mach-O on
    macOS) binaries, so the PE branch is unreachable without this.
    """

    binary_formats = ["pe"]


@pytest.fixture()
def relocation_recorder(monkeypatch):
    """Capture the arguments ``relocate_package`` forwards to the PE relocator."""
    recorded = []
    monkeypatch.setattr(spack.platforms, "by_name", lambda name: _PePlatform())
    monkeypatch.setattr(
        bd.relocate,
        "relocate_windows_binaries",
        lambda binaries, spec, prefixes, sfn_prefixes=None, stage=False: recorded.append(
            (binaries, spec, prefixes, sfn_prefixes)
        ),
    )
    return recorded


def _stage_installed_spec(spec, buildinfo):
    """Write ``buildinfo`` into an on-disk prefix for ``spec``."""
    prefix = pathlib.Path(spec.prefix)
    (prefix / ".spack").mkdir(parents=True, exist_ok=True)
    with open(bd.buildinfo_file_name(str(prefix)), "w", encoding="utf-8") as f:
        syaml.dump(buildinfo, f)
    return prefix


def _buildinfo(spec, old_root, **extra):
    info = {
        "buildpath": old_root,
        "spackprefix": old_root,
        "relative_prefix": "",
        "hardlinks_deduped": True,
        "relocate_textfiles": [],
        "relocate_binaries": [],
        "relocate_links": [],
        "hash_to_prefix": {spec.dag_hash(): os.path.join(old_root, "pkg")},
    }
    info.update(extra)
    return info


def test_relocate_package_relocates_on_sfn_map_alone(mock_spec, relocation_recorder):
    """When every long-form mapping is an identity, an SFN mapping is still work to
    do and must not be short circuited away."""
    spec = mock_spec
    layout_root = str(spack.store.STORE.layout.root)
    _stage_installed_spec(
        spec,
        _buildinfo(
            spec,
            layout_root,
            # identity: the old prefix is exactly where the spec already lives
            hash_to_prefix={spec.dag_hash(): str(spec.prefix)},
            hash_to_prefix_sfn={spec.dag_hash(): r"C:\old\opt\SPACK~1\PKG"},
        ),
    )

    bd.relocate_package(spec)

    assert relocation_recorder, "SFN-only mapping was dropped"
    _, _, prefixes, sfn_prefixes = relocation_recorder[-1]
    assert prefixes == {}
    assert sfn_prefixes == {r"C:\old\opt\SPACK~1\PKG": str(spec.prefix)}

