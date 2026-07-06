# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``util/win_acl.py`` and Windows ACL integration in ``util/filesystem.py``."""

import sys

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

import spack.util.filesystem as fs
from spack.util.win_acl import (
    AccessControlEntry,
    AceFlags,
    AceType,
    FileAccessRights,
    GenericAccessRights,
    SecurityDescriptor,
    copy_file_permissions,
    get_file_owner,
    get_file_sddl,
    set_file_sddl,
)


def test_access_control_entry_to_sddl_string():
    # Without flags: only ace_type, rights, and sid fields are populated
    ace = AccessControlEntry(
        AceType.SDDL_ACCESS_ALLOWED, sid="BA", rights=GenericAccessRights.GENERIC_READ
    )
    assert str(ace) == "(A;;GR;;;BA)"

    # With a flag: the flags field appears in the second position
    ace_with_flags = AccessControlEntry(
        AceType.SDDL_ACCESS_ALLOWED,
        flags=AceFlags.SDDL_CONTAINER_INHERIT,
        rights=GenericAccessRights.GENERIC_READ,
        sid="BA",
    )
    assert str(ace_with_flags) == "(A;CI;GR;;;BA)"


def test_access_control_entry_add_right_accumulates():
    """Successive add_right calls OR masks together; the serialised SDDL reflects the union.

    Covers both generic rights (GR/GW/GX) and file-specific rights (FR/FW).
    """
    ace_generic = AccessControlEntry(AceType.SDDL_ACCESS_ALLOWED, sid="BA")
    ace_generic.add_right(GenericAccessRights.GENERIC_READ)
    ace_generic.add_right(GenericAccessRights.GENERIC_WRITE)
    ace_generic.add_right(GenericAccessRights.GENERIC_EXECUTE)
    assert str(ace_generic) == "(A;;GRGWGX;;;BA)"

    ace_file = AccessControlEntry(AceType.SDDL_ACCESS_ALLOWED, sid="BA")
    ace_file.add_right(FileAccessRights.FILE_GENERIC_READ)
    ace_file.add_right(FileAccessRights.FILE_GENERIC_WRITE)
    assert str(ace_file) == "(A;;FRFW;;;BA)"


def test_security_descriptor_sacl_property(tmp_path):
    """from_file never populates the SACL (requires SE_SECURITY_PRIVILEGE); sacl returns a copy."""
    f = tmp_path / "test.txt"
    f.write_text("hello")
    sd = SecurityDescriptor.from_file(str(f))
    # Standard processes cannot read SACL; from_file does not request it
    assert sd.sacl == []
    # sacl returns a copy; mutations do not feed back into the descriptor
    sd.sacl.append("mutation")
    assert sd.sacl == []


def test_get_sid_for_current_user():
    sid = SecurityDescriptor.get_sid_for_user()
    assert sid.startswith("S-1-")


def test_get_sid_for_named_user():
    # "SYSTEM" is always resolvable on Windows
    sid = SecurityDescriptor.get_sid_for_user("SYSTEM")
    assert sid.startswith("S-1-")


def test_get_file_sddl_returns_string(tmp_path):
    f = tmp_path / "acl_test.txt"
    f.write_text("hello")
    sddl = get_file_sddl(str(f))
    assert isinstance(sddl, str)
    assert "D:" in sddl  # must contain a DACL


def test_get_file_sddl_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        get_file_sddl(str(tmp_path / "nonexistent.txt"))


def test_security_descriptor_add_remove_ace():
    """add_ace must store all ACE fields; remove_ace must excise the entry and update the SDDL."""
    sd = SecurityDescriptor()
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=GenericAccessRights.GENERIC_READ, sid="BA"
        )
    )
    stored = sd.dacl[0]
    assert stored.sid == "BA"
    assert stored.rights == GenericAccessRights.GENERIC_READ
    assert stored.ace_type == AceType.SDDL_ACCESS_ALLOWED
    assert "(A;;GR;;;BA)" in sd.to_sddl()

    removed = sd.remove_ace(sid="BA")
    assert removed == 1
    assert len(sd.dacl) == 0
    assert "(A;;GR;;;BA)" not in sd.to_sddl()


def test_security_descriptor_clear_dacl():
    sd = SecurityDescriptor()
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=FileAccessRights.FILE_GENERIC_READ, sid="BA"
        )
    )
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=FileAccessRights.FILE_GENERIC_WRITE, sid="BA"
        )
    )
    assert len(sd.dacl) == 2
    sd.clear_dacl()
    assert len(sd.dacl) == 0


def test_parse_sddl_roundtrip():
    raw = "O:BAG:SYD:(A;;GR;;;BU)(A;;GW;;;BA)"
    sd = SecurityDescriptor(raw)
    assert sd.owner == "BA"
    assert sd.group == "SY"
    assert len(sd.dacl) == 2

    ace0 = sd.dacl[0]
    assert ace0.ace_type == AceType.SDDL_ACCESS_ALLOWED
    assert ace0.sid == "BU"
    assert ace0.rights == GenericAccessRights.GENERIC_READ

    ace1 = sd.dacl[1]
    assert ace1.ace_type == AceType.SDDL_ACCESS_ALLOWED
    assert ace1.sid == "BA"
    assert ace1.rights == GenericAccessRights.GENERIC_WRITE

    assert sd.to_sddl() == raw


def test_parse_sddl_roundtrip_with_dacl_control_flags():
    """DACL control flags (e.g. AI = auto-inherited) must survive a parse/create roundtrip."""
    raw = "O:BAG:SYD:AI(A;ID;GR;;;BU)"
    sd = SecurityDescriptor(raw)
    assert len(sd.dacl) == 1
    assert sd.to_sddl() == raw


def test_security_descriptor_from_file_sddl(tmp_path):
    f = tmp_path / "sd_test.txt"
    f.write_text("hello")
    sd = SecurityDescriptor.from_file(str(f))
    assert sd.owner is not None
    assert len(sd.dacl) > 0
    count_before = len(sd.dacl)

    guest_ace = AccessControlEntry(
        AceType.SDDL_ACCESS_ALLOWED, rights=FileAccessRights.FILE_GENERIC_READ, sid="BG"
    )
    sd.add_ace(guest_ace)
    sd.apply(str(f))

    sd2 = SecurityDescriptor.from_file(str(f))
    assert len(sd2.dacl) == count_before + 1

    # Round-trip
    sd3 = SecurityDescriptor(get_file_sddl(str(f)))
    assert sd3.owner == sd2.owner
    assert len(sd3.dacl) == len(sd2.dacl)


def test_get_file_owner_returns_string(tmp_path):
    """get_file_owner must return a human-readable account name that resolves to a valid SID."""
    f = tmp_path / "owner_test.txt"
    f.write_text("hello")
    owner_name = get_file_owner(str(f))

    # Must be a human-readable account name, not a raw SID
    assert isinstance(owner_name, str) and owner_name
    assert not owner_name.startswith("S-1-")

    # Must resolve back to a valid SID, confirming the name is a real, known account
    owner_sid = SecurityDescriptor.get_sid_for_user(owner_name)
    assert owner_sid.startswith("S-1-")


def test_get_file_owner_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        get_file_owner(str(tmp_path / "nonexistent.txt"))


def test_copy_file_permissions_preserves_dacl(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("source")
    dst.write_text("dest")

    copy_file_permissions(str(src), str(dst))

    src_sddl = get_file_sddl(str(src))
    dst_sddl = get_file_sddl(str(dst))

    def dacl_aces(sddl):
        dacl_part = sddl.split("D:")[1] if "D:" in sddl else ""
        paren = dacl_part.find("(")
        return dacl_part[paren:] if paren != -1 else dacl_part

    assert dacl_aces(src_sddl) != "", "source DACL must have at least one ACE"
    assert dacl_aces(src_sddl) == dacl_aces(dst_sddl)


def test_security_descriptor_modify_ace():
    sd = SecurityDescriptor()
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=GenericAccessRights.GENERIC_READ, sid="BA"
        )
    )
    assert sd.dacl[0].rights == GenericAccessRights.GENERIC_READ

    sd.modify_ace(0, rights=FileAccessRights.FILE_ALL_ACCESS)
    assert sd.dacl[0].rights == FileAccessRights.FILE_ALL_ACCESS
    assert sd.dacl[0].sid == "BA"  # unchanged field


def test_security_descriptor_remove_ace_all_matches():
    sd = SecurityDescriptor()
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=GenericAccessRights.GENERIC_READ, sid="SY"
        )
    )
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=GenericAccessRights.GENERIC_WRITE, sid="SY"
        )
    )
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=FileAccessRights.FILE_ALL_ACCESS, sid="BA"
        )
    )
    assert len(sd.dacl) == 3

    removed = sd.remove_ace(sid="SY", remove_all_matches=True)
    assert removed == 2
    assert len(sd.dacl) == 1
    assert sd.dacl[0].sid == "BA"


def test_security_descriptor_add_ace_out_of_range_raises():
    def _ace(sid, rights):
        return AccessControlEntry(AceType.SDDL_ACCESS_ALLOWED, rights=rights, sid=sid)

    sd = SecurityDescriptor()
    sd.add_ace(_ace("BA", GenericAccessRights.GENERIC_READ))

    with pytest.raises(IndexError):
        sd.add_ace(_ace("SY", GenericAccessRights.GENERIC_ALL), index=99)

    with pytest.raises(IndexError):
        sd.add_ace(_ace("SY", GenericAccessRights.GENERIC_ALL), index=-1)


def test_security_descriptor_add_ace_at_index_boundary():
    """index == len(dacl) is a valid append-at-end; the existing ACE must not move."""

    def _ace(sid, rights):
        return AccessControlEntry(AceType.SDDL_ACCESS_ALLOWED, rights=rights, sid=sid)

    sd = SecurityDescriptor()
    sd.add_ace(_ace("BA", GenericAccessRights.GENERIC_READ))

    sd.add_ace(_ace("SY", GenericAccessRights.GENERIC_ALL), index=len(sd.dacl))
    assert sd.dacl[0].sid == "BA"
    assert sd.dacl[1].sid == "SY"
    assert sd.dacl[1].rights == GenericAccessRights.GENERIC_ALL


def test_dacl_entries_are_access_control_entries():
    """DACL entries returned by SecurityDescriptor must be AccessControlEntry objects."""
    sd = SecurityDescriptor()
    sd.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=GenericAccessRights.GENERIC_READ, sid="BA"
        )
    )
    ace = sd.dacl[0]
    assert isinstance(ace, AccessControlEntry)
    assert ace.sid == "BA"
    assert ace.rights == GenericAccessRights.GENERIC_READ
    assert ace.ace_type == AceType.SDDL_ACCESS_ALLOWED
    assert ace.flags == []


def test_dacl_entries_from_parsed_sddl_are_access_control_entries():
    """The SDDL parser must populate all ACE fields correctly from both Allow and Deny entries."""
    raw = "O:SYD:(A;;FR;;;WD)(D;;FW;;;BG)"
    sd = SecurityDescriptor(raw)
    dacl = sd.dacl
    assert len(dacl) == 2
    assert all(isinstance(ace, AccessControlEntry) for ace in dacl)

    allow_ace = dacl[0]
    assert allow_ace.ace_type == AceType.SDDL_ACCESS_ALLOWED
    assert allow_ace.sid == "WD"
    assert allow_ace.rights == FileAccessRights.FILE_GENERIC_READ

    deny_ace = dacl[1]
    assert deny_ace.ace_type == AceType.SDDL_ACCESS_DENIED
    assert deny_ace.sid == "BG"
    assert deny_ace.rights == FileAccessRights.FILE_GENERIC_WRITE


def test_security_descriptor_from_file(tmp_path):
    """from_file must populate owner and DACL from the real file, and the descriptor must
    round-trip faithfully through to_sddl."""
    f = tmp_path / "from_file.txt"
    f.write_text("hello")

    sd = SecurityDescriptor.from_file(str(f))

    # Owner field must be populated and consistent with the serialized SDDL
    assert sd.owner is not None
    sddl = sd.to_sddl()
    assert f"O:{sd.owner}" in sddl

    # Every sensible DACL contains at least one Allow entry
    assert any(ace.ace_type == AceType.SDDL_ACCESS_ALLOWED for ace in sd.dacl)

    # Round-trip: parsing the SDDL we just produced must yield identical output
    assert SecurityDescriptor(sddl).to_sddl() == sddl


def test_set_file_sddl_roundtrip(tmp_path):
    f = tmp_path / "sddl_rw.txt"
    f.write_text("hello")

    original = get_file_sddl(str(f))
    set_file_sddl(str(f), original)
    after = get_file_sddl(str(f))

    def dacl_aces(sddl):
        dacl_part = sddl.split("D:")[1] if "D:" in sddl else ""
        paren = dacl_part.find("(")
        return dacl_part[paren:] if paren != -1 else dacl_part

    assert dacl_aces(after) == dacl_aces(original)


def test_security_descriptor_apply(tmp_path):
    """Applying a descriptor to a file with a different DACL must make their DACLs identical."""
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("source")
    dst.write_text("dest")

    # Give dst a known minimal DACL that differs from whatever src inherits.
    minimal = SecurityDescriptor()
    minimal.add_ace(
        AccessControlEntry(
            AceType.SDDL_ACCESS_ALLOWED, rights=FileAccessRights.FILE_ALL_ACCESS, sid="BA"
        )
    )
    minimal.apply(str(dst))

    def dacl_aces(sddl):
        dacl_part = sddl.split("D:")[1] if "D:" in sddl else ""
        paren = dacl_part.find("(")
        return dacl_part[paren:] if paren != -1 else dacl_part

    src_aces = dacl_aces(get_file_sddl(str(src)))
    dst_aces_before = dacl_aces(get_file_sddl(str(dst)))
    assert src_aces and dst_aces_before, "both files must have non-empty DACLs"
    assert dst_aces_before != src_aces, (
        "dst must start with a different DACL for this test to be meaningful"
    )

    SecurityDescriptor(get_file_sddl(str(src))).apply(str(dst))

    assert dacl_aces(get_file_sddl(str(dst))) == src_aces


def test_security_descriptor_apply_null_dacl_is_rejected(tmp_path):
    """Applying a descriptor with an explicit but empty DACL must raise ValueError.

    A NULL DACL on Windows grants all users full access; the implementation must refuse
    to apply it rather than silently skipping or permitting it.
    """
    f = tmp_path / "test.txt"
    f.write_text("hello")

    sd = SecurityDescriptor("D:")
    with pytest.raises(ValueError, match="null DACL"):
        sd.apply(str(f))


def test_set_install_permissions_file_acl(tmp_path):
    """set_install_permissions sets 644-equivalent permissions on a file.

    The owner receives Allow(read+write); Everyone receives Allow(read).
    """
    f = tmp_path / "test.txt"
    f.write_text("hello")
    owner_sid = SecurityDescriptor.from_file(str(f)).owner
    fs.set_install_permissions(str(f))

    sd = SecurityDescriptor.from_file(str(f))
    _FRFW = int(FileAccessRights.FILE_GENERIC_READ) | int(FileAccessRights.FILE_GENERIC_WRITE)
    _FR = int(FileAccessRights.FILE_GENERIC_READ)

    assert any(
        a.sid == owner_sid and a.ace_type == AceType.SDDL_ACCESS_ALLOWED and a.grants(_FRFW)
        for a in sd.dacl
    ), "owner must have Allow ACE granting read+write"
    assert any(
        a.sid == "WD" and a.ace_type == AceType.SDDL_ACCESS_ALLOWED and a.grants(_FR)
        for a in sd.dacl
    ), "Everyone must have Allow ACE granting read"


def test_set_install_permissions_directory_acl(tmp_path):
    """set_install_permissions sets 755-equivalent permissions on a directory.

    The owner receives Allow(full access); Everyone receives Allow(read+execute).
    """
    d = tmp_path / "subdir"
    d.mkdir()
    owner_sid = SecurityDescriptor.from_file(str(d)).owner
    fs.set_install_permissions(str(d))

    sd = SecurityDescriptor.from_file(str(d))
    _FA = int(FileAccessRights.FILE_ALL_ACCESS)
    _FRFX = int(FileAccessRights.FILE_GENERIC_READ) | int(FileAccessRights.FILE_GENERIC_EXECUTE)

    assert any(
        a.sid == owner_sid and a.ace_type == AceType.SDDL_ACCESS_ALLOWED and a.grants(_FA)
        for a in sd.dacl
    ), "owner must have Allow ACE granting full access"
    assert any(
        a.sid == "WD" and a.ace_type == AceType.SDDL_ACCESS_ALLOWED and a.grants(_FRFX)
        for a in sd.dacl
    ), "Everyone must have Allow ACE granting read+execute"


def test_set_install_permissions_expands_restricted_dacl(tmp_path):
    """set_install_permissions adds Everyone-read even when the initial DACL excludes them."""
    f = tmp_path / "test.txt"
    f.write_text("hello")
    owner_sid = SecurityDescriptor.from_file(str(f)).owner

    # Restrict to owner-only (600-equivalent): no Everyone in DACL
    set_file_sddl(str(f), f"D:P(A;;FRFW;;;{owner_sid})")
    assert not any(a.sid == "WD" for a in SecurityDescriptor.from_file(str(f)).dacl)

    fs.set_install_permissions(str(f))

    sd = SecurityDescriptor.from_file(str(f))
    assert any(
        a.sid == "WD"
        and a.ace_type == AceType.SDDL_ACCESS_ALLOWED
        and a.grants(int(FileAccessRights.FILE_GENERIC_READ))
        for a in sd.dacl
    ), "Everyone must have read access after set_install_permissions"


def test_copy_mode_propagates_execute_on_windows(tmp_path):
    """copy_mode ORs FILE_GENERIC_EXECUTE into dst Allow ACEs when src grants execute."""
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("source")
    dst.write_text("dest")

    _FX = int(FileAccessRights.FILE_GENERIC_EXECUTE)

    # Give src execute-only; give dst read-only.  The P flag blocks inheritance so no
    # inherited execute-granting ACEs from the parent directory can slip into dst.
    set_file_sddl(str(src), "D:P(A;;FX;;;WD)")
    set_file_sddl(str(dst), "D:P(A;;FR;;;WD)")

    # Sanity: dst must not grant execute before copy_mode
    assert not any(a.grants(_FX) for a in SecurityDescriptor.from_file(str(dst)).dacl)

    fs.copy_mode(str(src), str(dst))

    dst_dacl = SecurityDescriptor.from_file(str(dst)).dacl
    assert any(
        a.sid == "WD" and a.ace_type == AceType.SDDL_ACCESS_ALLOWED and a.grants(_FX)
        for a in dst_dacl
    ), "Everyone Allow ACE must include FILE_GENERIC_EXECUTE after copy_mode"


def test_copy_mode_only_changes_execute_on_windows(tmp_path):
    """copy_mode leaves dst DACL unchanged when src grants no execute rights."""
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("source")
    dst.write_text("dest")

    # Write a protected DACL with only read access.  The P flag suppresses inheritance so
    # Windows does not re-add execute-granting inherited ACEs from the parent directory.
    set_file_sddl(str(src), "D:P(A;;FR;;;WD)")

    before = get_file_sddl(str(dst))
    fs.copy_mode(str(src), str(dst))
    assert get_file_sddl(str(dst)) == before
