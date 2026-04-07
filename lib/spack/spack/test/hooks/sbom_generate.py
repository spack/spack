# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os

import pytest

import spack.concretize
import spack.spec
from spack.hooks.sbom_generate import post_install, sbom_path


def test_sbom_generated_with_post_install(mock_packages, install_mockery):
    """SBOM is generated correctly for a trivial package."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = sbom_path(spec)
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

    path = sbom_path(spec)
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    traversed_nodes = list(spec.traverse(root=True, deptype="all"))
    package_names = {p["name"] for p in sbom["packages"]}

    # mpileaks depends on callpath + mpi in mock repo
    assert "callpath" in package_names
    assert len(sbom["packages"]) == len(traversed_nodes)

    relationships = sbom["relationships"]
    contains_rels = [r for r in relationships if r["relationshipType"] == "CONTAINS"]
    describes_rels = [r for r in relationships if r["relationshipType"] == "DESCRIBES"]

    assert len(contains_rels) == len(traversed_nodes) - 1
    assert len(relationships) == len(traversed_nodes)
    assert len(describes_rels) == 1


def test_sbom_has_document_namespace(mock_packages, install_mockery):
    """Each SBOM document has a namespace and describes the root package."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = sbom_path(spec)
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    assert "documentNamespace" in sbom
    assert sbom["documentNamespace"] == f"https://spack.io/sbom/{spec.dag_hash()}"

    describes = [r for r in sbom["relationships"] if r["relationshipType"] == "DESCRIBES"]

    assert len(describes) == 1


def test_sbom_external_package_skipped(mock_packages, install_mockery):
    """External packages should not generate SBOM."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    spec.external_path = "/fake/external/path"

    post_install(spec)

    path = sbom_path(spec)
    assert not os.path.exists(path)


def test_sbom_license_and_download_defaults(mock_packages, install_mockery):
    """Default license and download fields reflect package metadata."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = sbom_path(spec)
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    pkg = sbom["packages"][0]

    assert pkg["licenseDeclared"] == "NOASSERTION"
    assert pkg["licenseConcluded"] == "NOASSERTION"
    assert pkg["downloadLocation"] == spec.package.url


def test_sbom_supplier_prefers_package_supplier(mock_packages, install_mockery, monkeypatch):
    """When present, the package supplier field is used."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    monkeypatch.setattr(spec.package, "supplier", "Person: Unit Test", raising=False)

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
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

    with open(sbom_path(spec), encoding="utf-8") as f:
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
    monkeypatch.setattr(
        dep.package, "git", "https://github.com/dep-org/callpath.git", raising=False
    )

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
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

    with open(sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["packages"][0]["licenseDeclared"] == expected


def test_sbom_download_location_and_checksum_from_version_metadata(
    mock_packages, install_mockery, monkeypatch
):
    """Checksum comes from version metadata while download location uses url_for_version."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    version = spec.version

    # The hook looks up version metadata by both string and Version key in different places.
    monkeypatch.setattr(spec.package, "versions", {version: {"sha256": "a" * 64}}, raising=False)
    monkeypatch.setattr(
        spec.package, "url_for_version", lambda version: "https://example.com/src.tar.gz"
    )

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    pkg = sbom["packages"][0]
    assert pkg["downloadLocation"] == "https://example.com/src.tar.gz"
    assert pkg["checksum"] == [{"algorithm": "SHA256", "checksumValue": "a" * 64}]


def test_sbom_download_location_from_git_url(mock_packages, install_mockery):
    """Download location should come from the package-level git URL."""

    spec = spack.concretize.concretize_one("git-sparsepaths-version@1.0")

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["packages"][0]["downloadLocation"] == "https://a/really.com/big/repo.git"


def test_sbom_download_location_from_package_url(mock_packages, install_mockery, monkeypatch):
    """Download location should come from the package-level URL."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    monkeypatch.setattr(
        spec.package,
        "url",
        "https://example.com/trivial-install-test-package-1.0.tar.gz",
        raising=False,
    )

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["packages"][0]["downloadLocation"] == spec.package.url


def test_sbom_download_location_from_package_url_with_different_version(
    mock_packages, install_mockery, monkeypatch
):
    """Package-level URLs should respect version interpolation for the concretized version."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    monkeypatch.setattr(
        spec.package,
        "url",
        "https://example.com/trivial-install-test-package-9.9.tar.gz",
        raising=False,
    )

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    assert (
        sbom["packages"][0]["downloadLocation"]
        == "https://example.com/trivial-install-test-package-1.0.tar.gz"
    )


def test_sbom_dependency_entry_uses_dependency_version_and_checksum(
    mock_packages, install_mockery, monkeypatch
):
    """Dependency entries should use dependency-specific version and checksum data."""

    spec = spack.concretize.concretize_one("mpileaks")
    dep = next(d for d in spec.dependencies(deptype="all") if d.name == "callpath")

    monkeypatch.setattr(
        spec.package, "versions", {spec.version: {"sha256": "a" * 64}}, raising=False
    )
    monkeypatch.setattr(
        dep.package, "versions", {dep.version: {"sha256": "b" * 64}}, raising=False
    )
    monkeypatch.setattr(
        dep.package, "url_for_version", lambda version: "https://example.com/callpath.tar.gz"
    )

    post_install(spec)

    with open(sbom_path(spec), encoding="utf-8") as f:
        sbom = json.load(f)

    packages_by_name = {pkg["name"]: pkg for pkg in sbom["packages"]}
    dep_entry = packages_by_name["callpath"]

    assert dep_entry["versionInfo"] == str(dep.version)
    assert dep_entry["downloadLocation"] == "https://example.com/callpath.tar.gz"
    assert dep_entry["checksum"] == [{"algorithm": "SHA256", "checksumValue": "b" * 64}]
