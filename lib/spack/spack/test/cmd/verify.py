# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the `spack verify` command"""
import os
import pathlib
import platform

import pytest

import spack.cmd.verify
import spack.concretize
import spack.installer
import spack.llnl.util.filesystem as fs
import spack.store
import spack.util.executable
import spack.util.spack_json as sjson
import spack.verify
from spack.main import SpackCommand, SpackCommandError

verify = SpackCommand("verify")
install = SpackCommand("install")


def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(platform.system()) != "Linux", reason="only tested on linux for now"
    )(f)


def test_single_file_verify_cmd(tmp_path: pathlib.Path):
    # Test the verify command interface to verifying a single file.
    filedir = tmp_path / "a" / "b" / "c" / "d"
    filepath = filedir / "file"
    metadir = tmp_path / spack.store.STORE.layout.metadata_dir

    fs.mkdirp(str(filedir))
    fs.mkdirp(str(metadir))

    with open(str(filepath), "w", encoding="utf-8") as f:
        f.write("I'm a file")

    data = spack.verify.create_manifest_entry(str(filepath))

    manifest_file = metadir / spack.store.STORE.layout.manifest_file_name

    with open(str(manifest_file), "w", encoding="utf-8") as f:
        sjson.dump({str(filepath): data}, f)

    results = verify("manifest", "-f", str(filepath), fail_on_error=False)
    assert not results

    os.utime(str(filepath), (0, 0))
    with open(str(filepath), "w", encoding="utf-8") as f:
        f.write("I changed.")

    results = verify("manifest", "-f", str(filepath), fail_on_error=False)

    expected = ["hash"]
    mtime = os.stat(str(filepath)).st_mtime
    if mtime != data["time"]:
        expected.append("mtime")

    assert results
    assert str(filepath) in results
    assert all(x in results for x in expected)

    results = verify("manifest", "-fj", str(filepath), fail_on_error=False)
    res = sjson.load(results)
    assert len(res) == 1
    errors = res.pop(str(filepath))
    assert sorted(errors) == sorted(expected)


def test_single_spec_verify_cmd(mock_packages, mock_archive, mock_fetch, install_mockery):
    # Test the verify command interface to verify a single spec
    install("--fake", "libelf")
    s = spack.concretize.concretize_one("libelf")
    prefix = s.prefix
    hash = s.dag_hash()

    results = verify("manifest", "/%s" % hash, fail_on_error=False)
    assert not results

    new_file = os.path.join(prefix, "new_file_for_verify_test")
    with open(new_file, "w", encoding="utf-8") as f:
        f.write("New file")

    results = verify("manifest", "/%s" % hash, fail_on_error=False)
    assert new_file in results
    assert "added" in results

    results = verify("manifest", "-j", "/%s" % hash, fail_on_error=False)
    res = sjson.load(results)
    assert len(res) == 1
    assert res[new_file] == ["added"]


@pytest.mark.requires_executables("gcc")
@skip_unless_linux
def test_libraries(tmp_path: pathlib.Path, install_mockery, mock_fetch):
    gcc = spack.util.executable.which("gcc", required=True)
    s = spack.concretize.concretize_one("libelf")
    spack.installer.PackageInstaller([s.package], fake=True).install()

    # There are no ELF files so the verification should pass
    verify("libraries", f"/{s.dag_hash()}")

    # Now put main_with_rpath linking to libf.so inside the prefix and verify again. This should
    # work because libf.so can be located in the rpath.
    (tmp_path / "f.c").write_text("void f(void){return;}")
    (tmp_path / "main.c").write_text("void f(void); int main(void){f();return 0;}")

    gcc("-shared", "-fPIC", "-o", str(tmp_path / "libf.so"), str(tmp_path / "f.c"))
    gcc(
        "-o",
        str(s.prefix.bin.main_with_rpath),
        str(tmp_path / "main.c"),
        "-L",
        str(tmp_path),
        f"-Wl,-rpath,{tmp_path}",
        "-lf",
    )
    verify("libraries", f"/{s.dag_hash()}")

    # Now put main_without_rpath linking to libf.so inside the prefix and verify again. This should
    # fail because libf.so cannot be located in the rpath.
    gcc(
        "-o",
        str(s.prefix.bin.main_without_rpath),
        str(tmp_path / "main.c"),
        "-L",
        str(tmp_path),
        "-lf",
    )

    with pytest.raises(SpackCommandError):
        verify("libraries", f"/{s.dag_hash()}")

    # Check the error message
    msg = spack.cmd.verify._verify_libraries(s, [])
    assert msg is not None and "libf.so => not found" in msg

    # And check that we can make it pass by ignoring it.
    assert spack.cmd.verify._verify_libraries(s, ["libf.so"]) is None
