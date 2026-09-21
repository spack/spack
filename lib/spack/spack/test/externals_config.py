# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.compilers.libraries
import spack.context
import spack.platforms
import spack.spec
from spack.externals_config import create_external_parser, external_config_with_implicit_externals

pytestmark = pytest.mark.usefixtures("mock_packages")


@pytest.fixture()
def libc_compatibility(monkeypatch):
    monkeypatch.setattr(spack.platforms, "using_libc_compatibility", lambda: True)


def _libc_dependencies(entry):
    return [d for d in entry.get("dependencies", []) if d.get("virtuals") == "libc"]


def test_compilers_depend_on_implicit_libc(mutable_config, libc_compatibility):
    """Every external compiler gets a link dependency on the libc detected for it."""
    context = spack.context.default()
    packages = external_config_with_implicit_externals(context)

    # The stub libc in conftest.py is shared by all compilers
    libcs = packages["glibc"]["externals"]
    assert len(libcs) == 1 and libcs[0]["prefix"] == "/some/path" and "id" in libcs[0]
    for name in ("gcc", "llvm"):
        for entry in packages[name]["externals"]:
            (dep,) = _libc_dependencies(entry)
            assert dep == {"id": libcs[0]["id"], "deptypes": "link", "virtuals": "libc"}

    parser = create_external_parser(packages, context=context)
    for compiler in parser.query(spack.spec.Spec("gcc")):
        assert compiler["libc"].external_path == "/some/path"


def test_user_declared_libc_is_reused(mutable_config, libc_compatibility):
    """A libc declared by the user with the same version and prefix is not duplicated."""
    packages = mutable_config.get("packages", scope="site")
    packages["glibc"] = {"externals": [{"spec": "glibc@2.28", "prefix": "/some/path"}]}
    mutable_config.set("packages", packages, scope="site")

    packages = external_config_with_implicit_externals(spack.context.default())
    (libc,) = packages["glibc"]["externals"]
    (dep,) = _libc_dependencies(packages["gcc"]["externals"][0])
    assert dep["id"] == libc["id"]


def test_explicit_libc_dependency_skips_detection(mutable_config, libc_compatibility, monkeypatch):
    """A compiler with an explicit libc dependency is not inspected."""
    packages = mutable_config.get("packages", scope="site")
    packages["glibc"] = {"externals": [{"spec": "glibc@2.35", "prefix": "/opt", "id": "mylibc"}]}
    for entry in packages["gcc"]["externals"] + packages["llvm"]["externals"]:
        entry["dependencies"] = [{"id": "mylibc", "deptypes": "link", "virtuals": "libc"}]
    mutable_config.set("packages", packages, scope="site")

    def fail(self):
        raise AssertionError("libc detection should not run")

    monkeypatch.setattr(spack.compilers.libraries.CompilerPropertyDetector, "default_libc", fail)
    packages = external_config_with_implicit_externals(spack.context.default())
    assert [x["id"] for x in packages["glibc"]["externals"]] == ["mylibc"]
    parser = create_external_parser(packages, context=spack.context.default())
    for compiler in parser.query(spack.spec.Spec("gcc")):
        assert compiler["libc"].satisfies("glibc@2.35")


def test_inline_dependencies_are_canonicalized(mutable_config, libc_compatibility):
    """Inline dependencies of a compiler move to the 'dependencies' list before the libc joins."""
    packages = mutable_config.get("packages", scope="site")
    entry = packages["gcc"]["externals"][0]
    entry["spec"] += " ^externaltool@1.0"
    mutable_config.set("packages", packages, scope="site")

    context = spack.context.default()
    packages = external_config_with_implicit_externals(context)
    entry = packages["gcc"]["externals"][0]
    assert "^" not in entry["spec"]
    assert [d.get("spec") for d in entry["dependencies"]][0] == "externaltool@1.0"
    assert len(_libc_dependencies(entry)) == 1

    parser = create_external_parser(packages, context=context)
    gcc = parser.specs_by_external_id[entry["id"]].spec
    assert gcc["externaltool"].satisfies("@1.0") and gcc["libc"].satisfies("glibc@2.28")
