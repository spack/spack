# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
import types

import pytest

import spack.concretize
import spack.spec
from spack.hooks.sbom_generate import post_install
from spack.store import STORE


def _sbom_path(spec):
    return os.path.join(STORE.layout.metadata_path(spec), "spdx-2.3-sbom.json")


def test_sbom_generated_with_post_install(mock_packages, install_mockery):
    """SBOM is generated correctly for a trivial package."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = _sbom_path(spec)
    assert os.path.isfile(path)

    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    # Document-level assertions
    assert sbom["spdxVersion"] == "SPDX-2.3"
    assert len(sbom["packages"]) >= 1

    # Package-level assertions
    pkg = sbom["packages"][0]

    assert pkg["name"] == spec.name
    assert pkg["versionInfo"] == str(spec.version)
    assert pkg["filesAnalyzed"] is False
    assert pkg["licenseConcluded"] == "NOASSERTION"
    assert "SPDXID" in pkg


def test_sbom_contains_dependencies(mock_packages, install_mockery):
    """Dependencies appear in SBOM with CONTAINS relationship."""

    # Use a mock package that has dependencies
    spec = spack.concretize.concretize_one("mpileaks")

    post_install(spec)

    path = _sbom_path(spec)
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    package_names = {p["name"] for p in sbom["packages"]}

    # mpileaks depends on callpath + mpi in mock repo
    assert "callpath" in package_names

    relationships = sbom["relationships"]

    contains_rels = [r for r in relationships if r["relationshipType"] == "CONTAINS"]

    assert len(contains_rels) >= 1


def test_sbom_has_document_namespace(mock_packages, install_mockery):
    """Each SBOM document has a namespace and describes the root package."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = _sbom_path(spec)
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    assert "documentNamespace" in sbom
    assert sbom["documentNamespace"].startswith("https://")

    describes = [r for r in sbom["relationships"] if r["relationshipType"] == "DESCRIBES"]

    assert len(describes) == 1


def test_sbom_external_package_skipped(mock_packages, install_mockery):
    """External packages should not generate SBOM."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    spec.external_path = "/fake/external/path"

    post_install(spec)

    path = _sbom_path(spec)
    assert not os.path.exists(path)


def test_sbom_license_and_download_fields(mock_packages, install_mockery):
    """SBOM contains expected license and download fields."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = _sbom_path(spec)
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    pkg = sbom["packages"][0]

    # SPDX requires these fields even if NOASSERTION
    assert "licenseDeclared" in pkg
    assert "licenseConcluded" in pkg
    assert "downloadLocation" in pkg


def test_sbom_supplier_prefers_package_supplier(mock_packages, install_mockery, monkeypatch):
    """When present, the package supplier field is used."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    monkeypatch.setattr(spec.package, "supplier", "Person: Unit Test", raising=False)

    post_install(spec)

    with open(_sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["packages"][0]["supplier"] == "Person: Unit Test"


@pytest.mark.parametrize(
    "git_url,expected",
    [
        ("git@github.com:spack/spack.git", "Organization: spack"),
        ("https://github.com/spack/spack.git", "Organization: spack"),
        ("ssh://git@github.com/spack/spack.git", "Organization: spack"),
        ("git://github.com/spack/spack.git", "Organization: spack"),
        ("https://gitlab.com/group/subgroup/repo.git", "Organization: group/subgroup"),
        ("git@gitlab.com:group/subgroup/repo.git", "Organization: group/subgroup"),
        ("git@github.com", "NOASSERTION"),  # malformed/unsupported ssh URL
    ],
)
def test_sbom_supplier_derived_from_git_url(
    mock_packages, install_mockery, monkeypatch, git_url, expected
):
    """Supplier is derived from common git URL formats when no explicit supplier is set."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    monkeypatch.setattr(spec.package, "supplier", None, raising=False)
    monkeypatch.setattr(spec.package, "git", git_url, raising=False)

    post_install(spec)

    with open(_sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["packages"][0]["supplier"] == expected


def test_sbom_dependency_supplier_uses_dependency_package(
    mock_packages, install_mockery, monkeypatch
):
    """Dependency supplier data should come from the dependency package, not the root package."""

    spec = spack.concretize.concretize_one("mpileaks")
    root_pkg = spec.package
    dep = next(d for d in spec.dependencies(deptype="all") if d.name == "callpath")

    monkeypatch.setattr(root_pkg, "supplier", None, raising=False)
    monkeypatch.setattr(root_pkg, "git", "https://github.com/root-org/mpileaks.git", raising=False)
    monkeypatch.setattr(dep.package, "supplier", None, raising=False)
    monkeypatch.setattr(dep.package, "git", "https://github.com/dep-org/callpath.git", raising=False)

    post_install(spec)

    with open(_sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    packages_by_name = {pkg["name"]: pkg for pkg in sbom["packages"]}

    assert packages_by_name["mpileaks"]["supplier"] == "Organization: root-org"
    assert packages_by_name["callpath"]["supplier"] == "Organization: dep-org"


@pytest.mark.parametrize(
    "licenses,expected",
    [({spack.spec.Spec(): "MIT"}, "MIT"), ({}, "NOASSERTION"), (None, "NOASSERTION")],
)
def test_sbom_license_declared_from_package_licenses(
    mock_packages, install_mockery, monkeypatch, licenses, expected
):
    """License declared comes from the package's licenses attribute (including dict forms)."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    monkeypatch.setattr(spec.package, "licenses", licenses, raising=False)

    post_install(spec)

    with open(_sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["packages"][0]["licenseDeclared"] == expected


def test_sbom_download_location_and_checksum_from_version_metadata(
    mock_packages, install_mockery, monkeypatch
):
    """Download URL and SHA256 are taken from package version metadata when present."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    version = spec.version

    # The hook looks up version metadata by both string and Version key in different places.
    monkeypatch.setattr(
        spec.package,
        "versions",
        {
            str(version): types.SimpleNamespace(url="https://example.com/src.tar.gz"),
            version: {"sha256": "a" * 64},
        },
        raising=False,
    )

    post_install(spec)

    with open(_sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    pkg = sbom["packages"][0]
    assert pkg["downloadLocation"] == "https://example.com/src.tar.gz"
    assert pkg["checksum"] == [{"algorithm": "SHA256", "checksumValue": "a" * 64}]
