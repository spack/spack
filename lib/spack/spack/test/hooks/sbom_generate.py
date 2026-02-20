# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os

import spack.concretize
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
