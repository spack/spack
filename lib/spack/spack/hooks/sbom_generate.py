# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Generate a Software Bill of Materials (SBOM) for each Spack installation."""

import os
import time
import urllib.parse

import spack.error
import spack.util.spack_json as sjson
from spack.llnl.util import tty
from spack.store import STORE


def get_license(pkg):
    if not pkg:
        return None

    license_data = getattr(pkg, "licenses", None)

    if not license_data:
        return None

    licenses = [lic for when, lic in license_data.items() if pkg.spec.satisfies(when)]

    return " OR ".join(licenses) if licenses else None


def get_supplier(pkg):
    supplier = getattr(pkg, "supplier", None)
    if supplier:
        return supplier

    git_url = getattr(pkg, "git", None)
    if git_url:
        path = None

        # Support SCP-style SSH remotes such as git@host:owner/repo.git.
        if git_url.startswith("git@") and ":" in git_url:
            path = git_url.split(":", 1)[1]
        else:
            path = urllib.parse.urlparse(git_url).path

        parts = [part for part in path.split("/") if part]
        if len(parts) >= 2:
            namespace = "/".join(parts[:-1])
            return f"Organization: {namespace}"

    return None


def get_checksums(spec):
    checksums = []

    # Get SHA256 from version metadata if available
    version_metadata = getattr(spec.package, "versions", {})
    vmeta = version_metadata.get(spec.version) or {}
    sha256 = vmeta.get("sha256", None)
    if sha256:
        checksums.append({"algorithm": "SHA256", "checksumValue": sha256})

    # Also include git commit SHA1 when available
    git_commit = get_git_commit(spec)
    if git_commit:
        checksums.append({"algorithm": "SHA1", "checksumValue": git_commit})

    return checksums


def get_git_commit(spec):
    pkg = spec.package

    if "commit" in spec.variants:
        return spec.variants["commit"].value

    if getattr(spec.version, "commit_sha", None):
        return spec.version.commit_sha

    version_metadata = getattr(pkg, "versions", {})
    vmeta = version_metadata.get(spec.version) or {}
    return vmeta.get("commit")


def get_download_location(spec):
    pkg = spec.package

    try:
        return str(pkg.url_for_version(spec.version))
    except spack.error.NoURLError:
        pass

    git_url = pkg.version_or_package_attr("git", spec.version, default=None)
    if git_url and pkg.needs_commit(spec.version):
        return str(git_url)

    return None


def make_spdx_2_3_package_entry(spec):
    pkg = getattr(spec, "package", None)
    return {
        "SPDXID": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        "name": spec.name,
        "versionInfo": str(spec.version),
        "supplier": get_supplier(pkg) or "NOASSERTION",
        "downloadLocation": get_download_location(spec) or "NOASSERTION",
        "filesAnalyzed": False,
        "licenseDeclared": get_license(pkg) or "NOASSERTION",
        "licenseConcluded": "NOASSERTION",
        "checksum": get_checksums(spec),
    }


def sbom_path(spec, sbom_type="spdx-2.3"):
    """Return the path to an SBOM file for a spec.

    Args:
        spec: The package spec
        sbom_type: The type of SBOM (default: spdx-2.3)

    Returns:
        Path to the SBOM file
    """
    sbom_dir = os.path.join(STORE.layout.metadata_path(spec), "sbom")
    return os.path.join(sbom_dir, f"{sbom_type}.json")


# SPDX 2.3 Generation
def generate_spdx_2_3(spec):

    if spec.external:
        return

    # Document information
    t = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)

    # Create path and dir for sbom
    path = sbom_path(spec, "spdx-2.3")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    unique_str = f"{spec.name}-{spec.version}-{spec.dag_hash()}"
    document_namespace = f"https://spack.io/sbom/{spec.dag_hash()}"

    # Package entry for each installation.
    # Represents the top-level component in the SBOM (the package being installed).
    pkg_entry = make_spdx_2_3_package_entry(spec)

    # Package entry for each dependency in the concretized DAG.
    # Each dependency becomes its own entry, linked to the top-level component.
    deps = []
    relationships = [
        {
            "spdxElementId": f"SPDXRef-DOCUMENT-{spec.name}-{str(spec.version)}",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        }
    ]

    for dep in spec.traverse(root=False, deptype="all"):
        dep_entry = make_spdx_2_3_package_entry(dep)
        deps.append(dep_entry)

        relationships.append(
            {
                "spdxElementId": f"SPDXRef-PACKAGE-{spec.name}-{str(spec.version)}",
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": dep_entry["SPDXID"],
            }
        )

    # Compose SPDX document
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": f"SPDXRef-DOCUMENT-{spec.name}-{str(spec.version)}",
        "documentNamespace": document_namespace,
        "creationInfo": {
            "created": created_time,
            "creators": ["Organization: Spack Project", "Tool: Spack"],
        },
        "name": unique_str,
        "packages": [pkg_entry] + deps,
        "relationships": relationships,
    }

    # Write to SBOM file
    with open(path, "w", encoding="utf-8") as f:
        sjson.dump(sbom, f)
    tty.debug(f"[SBOM] Wrote SPDX 2.3 SBOM to {path}")


# Call SBOM generation in post-install hook
def post_install(spec, explicit=None):
    generate_spdx_2_3(spec)
