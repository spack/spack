# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Generate a Software Bill of Materials (SBOM) for each Spack installation."""

import hashlib
import os
import time
import urllib.parse

import spack.util.spack_json as sjson
from spack.llnl.util import tty
from spack.store import STORE


# SPDX 2.3 Generation
def post_install(spec, explicit=None):

    pkg = spec.package

    if spec.external:
        return

    # Get the URL location
    download_url = None
    if hasattr(pkg, "versions") and str(spec.version) in pkg.versions:
        # grab url associated with specific version
        version_data = pkg.versions[str(spec.version)]
        download_url = getattr(version_data, "url", None) or "NOASSERTION"

    # Get the license
    def get_license(pkg):

        if not pkg:
            return "NOASSERTION"

        license_data = getattr(pkg, "licenses", None)

        if not license_data:
            return "NOASSERTION"

        licenses = [license for when, lic in license_data.items() if pkg.spec.satisfies(when)]

        return " OR ".join(licenses) if licenses else "NOASSERTION"

    # Get the supplier
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

            repo_path = path.strip("/")
            if repo_path.endswith(".git"):
                repo_path = repo_path[:-4]

            parts = [part for part in repo_path.split("/") if part]
            if len(parts) >= 2:
                namespace = "/".join(parts[:-1])
                return f"Organization: {namespace}"

        return "NOASSERTION"

    # Get the checksums from package version metadata
    def get_checksums(spec):
        vmeta = spec.package.versions.get(spec.version) or {}
        sha256 = vmeta.get("sha256")
        if not sha256:
            return []
        return [{"algorithm": "SHA256", "checksumValue": sha256}]

    # Document information
    t = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)

    # Create path and dir for sbom
    sbom_path = os.path.join(STORE.layout.metadata_path(spec), "spdx-2.3-sbom.json")
    os.makedirs(os.path.dirname(sbom_path), exist_ok=True)

    unique_str = f"{spec.name}-{spec.version}-{spec.dag_hash()}"
    unique_hash = hashlib.sha256(unique_str.encode("utf-8")).hexdigest()
    document_namespace = f"https://spack.io/sbom/{unique_hash}"

    # Package entry for each installation.
    # Represents the top-level component in the SBOM (the package being installed).
    pkg_entry = {
        "SPDXID": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        "name": spec.name,
        "versionInfo": str(spec.version),
        "supplier": get_supplier(pkg),
        "downloadLocation": str(download_url or getattr(pkg, "url", None) or "NOASSERTION"),
        "filesAnalyzed": False,
        "licenseDeclared": get_license(pkg),
        "licenseConcluded": "NOASSERTION",
        "checksum": get_checksums(spec),
    }

    # Package entry for each dependency of a spec.
    # Each dependency becomes its own entry, linked to the top-level component.
    deps = []
    relationships = [
        {
            "spdxElementId": f"SPDXRef-DOCUMENT-{spec.name}-{str(spec.version)}",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        }
    ]

    for dep in spec.dependencies(deptype="all"):
        dep_name = dep.name
        dep_spec = dep
        dep_pkg = getattr(dep, "package", None)

        license_declared = get_license(dep_pkg) if dep_pkg else "NOASSERTION"

        dep_entry = {
            "SPDXID": f"SPDXRef-PACKAGE-{dep_name}-{str(dep_spec.version)}",
            "name": dep_name,
            "versionInfo": str(spec.version),
            "supplier": get_supplier(pkg),
            "downloadLocation": str(getattr(dep_pkg, "url", None) or "NOASSERTION"),
            "filesAnalyzed": False,
            "licenseDeclared": license_declared,
            "licenseConcluded": "NOASSERTION",
            "checksum": get_checksums(spec),
        }
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
    with open(sbom_path, "w", encoding="utf-8") as f:
        sjson.dump(sbom, f)
    tty.msg(f"[SBOM] Wrote SPDX 2.3 SBOM to {sbom_path}")
