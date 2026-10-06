# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.main
import spack.modules.tcl
import spack.store
import spack.util.tty

install = spack.main.SpackCommand("install")
uninstall = spack.main.SpackCommand("uninstall")
module = spack.main.SpackCommand("module")

pytestmark = pytest.mark.not_on_windows("does not run on windows")

writer_cls = spack.modules.tcl.TclModulefileWriter


@pytest.mark.db
def test_find_variants(mutable_database, module_configuration):
    """Test found module is returned with its variant specification if enabled."""
    module_configuration("variants_all")

    module("tcl", "refresh", "-y", "--delete-tree")
    out = module("tcl", "find", "mpileaks ^zmpi")
    assert " build_system=generic ~debug ~fortran ~opt +shared +static" in out


@pytest.mark.db
def test_loads_variants(mutable_database, module_configuration):
    """Test module to load is returned with its variant specification if enabled."""
    module_configuration("variants_all")

    module("tcl", "refresh", "-y", "--delete-tree")
    out = module("tcl", "loads", "mpileaks ^zmpi")
    assert " build_system=generic ~debug ~fortran ~opt +shared +static" in out


def test_refresh_fold_variants(install_mockery, module_configuration, modulefile_filenames):
    """Test same module version is folded into one module file after refresh."""
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)

    module_configuration("variants_none")
    module_file_a = modulefile_filenames("tcl", spec_a)[0]
    module_file_b = modulefile_filenames("tcl", spec_b)[0]
    assert module_file_a != module_file_b

    module_configuration("fold_variants_all")
    module("tcl", "refresh", "-y", "--delete-tree")
    module_file_a = module("tcl", "find", "--full-path", spec_a)
    module_file_b = module("tcl", "find", "--full-path", spec_b)
    assert module_file_a == module_file_b


def test_refresh_name_clash_without_variants(install_mockery, module_configuration):
    """Test refresh still reports a name clash when variants are disabled."""
    install("--fake", "--add", "mpileaks@2.3 ~debug ^zmpi")
    install("--fake", "--add", "mpileaks@2.3 +debug ^zmpi")

    module_configuration("fold_variants_none")
    out = module("tcl", "refresh", "-y", "--delete-tree", fail_on_error=False)
    assert module.returncode == 1
    assert "Name clashes detected in module files" in out
    assert "installations of different versions cannot share a module file" not in out


def test_rm_fold_variants(install_mockery, module_configuration, modulefile_filenames):
    """Test rm command removes the given installations from a module file holding several, and
    deletes the module file only when no installation remains."""
    module_configuration("fold_variants_all")

    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"

    # remove module file holding one installation
    install("--fake", "--add", spec_a)
    module_file = modulefile_filenames("tcl", spec_a)[0]
    module("tcl", "rm", "-y", spec_a)
    assert not os.path.exists(module_file)

    # remove one installation from a module file holding two of them
    install("--fake", "--add", spec_b)
    module("tcl", "refresh", "-y", "--delete-tree")
    concrete_a = spack.store.STORE.db.query_one(spec_a)
    concrete_b = spack.store.STORE.db.query_one(spec_b)
    module("tcl", "rm", "-y", spec_b)
    assert os.path.exists(module_file)
    with open(module_file, encoding="utf-8") as f:
        content = f.read()
    assert concrete_a.dag_hash(7) in content
    assert concrete_b.dag_hash(7) not in content

    # remove all the installations of the module file at once
    module("tcl", "rm", "-y", "mpileaks@2.3 ^zmpi")
    assert not os.path.exists(module_file)


def test_rm_prompt_lists_kept_installations(
    install_mockery, module_configuration, modulefile_filenames, monkeypatch
):
    """Test rm command tells which installations are removed from a shared module file, and
    which ones the module file keeps."""
    module_configuration("fold_variants_all")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    module_file = modulefile_filenames("tcl", spec_a)[0]
    concrete_a = spack.store.STORE.db.query_one(spec_a)
    concrete_b = spack.store.STORE.db.query_one(spec_b)

    monkeypatch.setattr(spack.util.tty, "get_yes_or_no", lambda *args, **kwargs: False)
    out = module("tcl", "rm", spec_b, fail_on_error=False)
    assert module.returncode == 1
    assert "module files shared with other installations" in out
    assert "written again for the installations they keep" in out
    assert concrete_a.dag_hash(7) in out
    assert concrete_b.dag_hash(7) in out
    assert os.path.exists(module_file)


def test_rm_excluded_installation(install_mockery, module_configuration, modulefile_filenames):
    """Test rm command does not delete the module file of the other installations when given an
    installation excluded from it."""
    module_configuration("fold_variants_exclude")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    module_file = modulefile_filenames("tcl", spec_b)[0]

    out = module("tcl", "rm", "-y", spec_a, fail_on_error=False)
    assert module.returncode == 1
    assert "No module file matches your query" in out
    assert os.path.exists(module_file)


def test_refresh_prompt_lists_folded_installations(
    install_mockery, module_configuration, monkeypatch
):
    """Test refresh command tells which installations share a module file with the given ones,
    as the module file is written again for all of them."""
    module_configuration("fold_variants_all")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    concrete_a = spack.store.STORE.db.query_one(spec_a)

    monkeypatch.setattr(spack.util.tty, "get_yes_or_no", lambda *args, **kwargs: False)
    out = module("tcl", "refresh", spec_b, fail_on_error=False)
    assert module.returncode == 1
    assert "share a module file with them" in out
    assert concrete_a.dag_hash(7) in out


def test_find_shared_module_file(install_mockery, module_configuration):
    """Test find command prints the bare module name when the constraint matches several
    installations folded in one module file, and still fails on several module files."""
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)

    module_configuration("fold_variants_all")
    module("tcl", "refresh", "-y", "--delete-tree")
    module_file = module("tcl", "find", "--full-path", spec_a).strip()
    assert module("tcl", "find", "--full-path", "mpileaks@2.3 ^zmpi").strip() == module_file
    module_name = module("tcl", "find", "mpileaks@2.3 ^zmpi").strip()
    assert module_file.endswith(module_name)
    assert "debug" not in module_name

    module_configuration("variants_none")
    module("tcl", "refresh", "-y", "--delete-tree")
    out = module("tcl", "find", "mpileaks@2.3 ^zmpi", fail_on_error=False)
    assert module.returncode == 1
    assert "matches multiple packages" in out


def test_loads_excluded_installation(install_mockery, module_configuration):
    """Test loads command reports an installation excluded from a module file holding other
    installations as having no module, although the module file exists."""
    module_configuration("fold_variants_exclude")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    module("tcl", "refresh", "-y", "--delete-tree")

    out = module("tcl", "loads", spec_a)
    assert "## excluded or missing from upstream: mpileaks@=2.3" in out
    assert "module load" not in out
    assert "module load mpileaks/2.3" in module("tcl", "loads", spec_b)


def test_loads_shared_module_file(install_mockery, module_configuration):
    """Test loads command leaves only the load line of the first installation folded in a module
    file active, as a module file can only be loaded once."""
    module_configuration("fold_variants_all")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    module("tcl", "refresh", "-y", "--delete-tree")

    out = module("tcl", "loads", "mpileaks@2.3 ^zmpi")
    load_lines = [line for line in out.splitlines() if "module load" in line]
    assert len(load_lines) == 2
    assert load_lines[0].startswith("module load mpileaks/2.3")
    assert load_lines[1].startswith("## module load mpileaks/2.3")
    assert "# shares its module file with" in out
    assert "cannot be loaded together" in out

    out = module("tcl", "loads", "--input-only", "mpileaks@2.3 ^zmpi")
    load_lines = [line for line in out.splitlines() if "mpileaks/2.3" in line]
    assert len(load_lines) == 2
    assert load_lines[0].startswith("mpileaks/2.3")
    assert load_lines[1].startswith("## mpileaks/2.3")


def test_setdefault_shared_module_file(install_mockery, module_configuration):
    """Test setdefault command refuses an installation folded with others, as the default
    symlink points to the whole module file."""
    module_configuration("fold_variants_all")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    module("tcl", "refresh", "-y", "--delete-tree")

    out = module("tcl", "setdefault", spec_b, fail_on_error=False)
    assert module.returncode == 1
    assert "its module file holds other installations" in out


def test_refresh_name_clash_across_versions(install_mockery, module_configuration):
    """Test refresh reports a name clash when installations of different versions project to
    the same module file name, as only installations of one version are folded."""
    install("--fake", "--add", "mpileaks@2.2 ~debug ^zmpi")
    install("--fake", "--add", "mpileaks@2.3 ~debug ^zmpi")
    install("--fake", "--add", "mpileaks@2.3 +debug ^zmpi")

    module_configuration("fold_variants_name_projection")
    out = module("tcl", "refresh", "-y", "--delete-tree", fail_on_error=False)
    assert module.returncode == 1
    assert "Name clashes detected in module files" in out
    assert "mpileaks@=2.2" in out
    assert "mpileaks@=2.3" in out
    assert "installations of different versions cannot share a module file" in out


def test_uninstall_does_not_recreate_module(
    install_mockery, module_configuration, modulefile_filenames
):
    """Test uninstalling a folded installation does not write back a module file that was
    removed beforehand."""
    module_configuration("fold_variants_all")
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)
    module_file = modulefile_filenames("tcl", spec_a)[0]
    module("tcl", "rm", "-y", "mpileaks@2.3 ^zmpi")
    assert not os.path.exists(module_file)

    uninstall("-y", spec_b)
    assert not os.path.exists(module_file)
