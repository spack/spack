# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os

import pytest

import spack.concretize
import spack.paths
import spack.repo
from spack.hooks.sbom_generate import generate_spdx_2_3, post_install, sbom_path


def test_sbom_generated_with_post_install(mock_packages, install_mockery):
    """SBOM is generated correctly for a trivial package."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    post_install(spec)

    path = sbom_path(spec, "spdx-2.3")
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


def test_sbom_document_spdx_id_is_spec_compliant(mock_packages, install_mockery):
    """The document SPDXID must be the literal "SPDXRef-DOCUMENT", and the DESCRIBES
    relationship must reference it, or SPDX validators reject the document."""

    spec = spack.concretize.concretize_one("mpileaks")

    generate_spdx_2_3(spec)

    with open(sbom_path(spec, "spdx-2.3"), encoding="utf-8") as f:
        sbom = json.load(f)

    assert sbom["SPDXID"] == "SPDXRef-DOCUMENT"

    describes = [r for r in sbom["relationships"] if r["relationshipType"] == "DESCRIBES"]
    assert len(describes) == 1
    assert describes[0]["spdxElementId"] == "SPDXRef-DOCUMENT"

    # Every relationship endpoint must resolve to the document or a declared package.
    known_ids = {sbom["SPDXID"]} | {p["SPDXID"] for p in sbom["packages"]}
    for rel in sbom["relationships"]:
        assert rel["spdxElementId"] in known_ids
        assert rel["relatedSpdxElement"] in known_ids


def test_sbom_contains_dependencies(mock_packages, install_mockery):
    """Dependencies appear in SBOM with CONTAINS relationship."""

    # Use a mock package that has dependencies
    spec = spack.concretize.concretize_one("mpileaks")

    generate_spdx_2_3(spec)

    path = sbom_path(spec, "spdx-2.3")
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
    assert len(describes_rels) == 1


def test_sbom_has_document_namespace(mock_packages, install_mockery):
    """Each SBOM document has a namespace and describes the root package."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    generate_spdx_2_3(spec)

    path = sbom_path(spec, "spdx-2.3")
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    assert "documentNamespace" in sbom
    assert sbom["documentNamespace"] == f"https://spack.io/sbom/{spec.dag_hash()}"


def test_sbom_external_package_skipped(mock_packages, install_mockery):
    """External packages should not generate SBOM."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")
    spec.external_path = "/fake/external/path"

    generate_spdx_2_3(spec)

    path = sbom_path(spec, "spdx-2.3")
    assert not os.path.exists(path)


def test_sbom_license_and_download_defaults(mock_packages, install_mockery):
    """Default license and download fields reflect package metadata."""

    spec = spack.concretize.concretize_one("trivial-install-test-package")

    generate_spdx_2_3(spec)

    path = sbom_path(spec, "spdx-2.3")
    with open(path, encoding="utf-8") as f:
        sbom = json.load(f)

    pkg = sbom["packages"][0]

    assert pkg["licenseDeclared"] == "NOASSERTION"
    assert pkg["licenseConcluded"] == "NOASSERTION"
    assert pkg["downloadLocation"] == spec.package.url


@pytest.fixture
def sbom_repo(install_mockery):
    with spack.repo.use_repositories(
        os.path.join(spack.paths.test_repos_path, "spack_repo", "sbom_test")
    ) as repo:
        yield repo


def _sbom_packages(spec):
    generate_spdx_2_3(spec)
    with open(sbom_path(spec), encoding="utf-8") as f:
        return {pkg["name"]: pkg for pkg in json.load(f)["packages"]}


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
    monkeypatch.setattr(spec.package, "git", git_url, raising=False)

    assert _sbom_packages(spec)[spec.name]["supplier"] == expected


def test_sbom_package_metadata(sbom_repo):
    """Tests that supplier, license, download location and checksum come from the recipe, and
    that the supplier attribute takes precedence over the git URL."""
    pkg = _sbom_packages(spack.concretize.concretize_one("sbom-supplier"))["sbom-supplier"]

    assert pkg["supplier"] == "Person: Unit Test"
    assert pkg["licenseDeclared"] == "MIT"
    assert pkg["downloadLocation"] == "https://example.com/sbom-supplier-1.0.tar.gz"
    assert pkg["checksums"] == [{"algorithm": "SHA256", "checksumValue": "a" * 64}]


def test_sbom_dependency_metadata(sbom_repo):
    """Tests that each dependency entry is filled from the dependency's own recipe."""
    packages = _sbom_packages(spack.concretize.concretize_one("sbom-root"))

    assert packages["sbom-root"]["supplier"] == "Organization: root-org"
    assert packages["sbom-dep"]["supplier"] == "Organization: dep-org"
    assert packages["sbom-dep"]["versionInfo"] == "2.0"
    assert packages["sbom-dep"]["downloadLocation"] == "https://example.com/sbom-dep-2.0.tar.gz"
    assert packages["sbom-dep"]["checksums"] == [
        {"algorithm": "SHA256", "checksumValue": "b" * 64}
    ]


@pytest.mark.require_provenance
def test_sbom_git_commit_version(sbom_repo):
    """Tests that a version pinned to a commit reports the git URL and the commit as SHA1."""
    pkg = _sbom_packages(spack.concretize.concretize_one("sbom-git@1.0"))["sbom-git"]

    assert pkg["downloadLocation"] == "https://github.com/example/sbom-git.git"
    assert pkg["checksums"] == [{"algorithm": "SHA1", "checksumValue": "c" * 40}]


@pytest.mark.regression("52864")
def test_sbom_git_branch_version_does_not_call_url_for_version(sbom_repo):
    """Tests that a branch version reports the git URL, without calling a url_for_version that
    fails on non-numeric versions.
    """
    pkg = _sbom_packages(spack.concretize.concretize_one("sbom-git@main"))["sbom-git"]

    assert pkg["downloadLocation"] == "https://github.com/example/sbom-git.git"
