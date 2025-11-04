import json
import os
import spack.hooks
import time
from spack.llnl.util import tty

"""Generate a Software Bill of Materials (SBOM) for each successful Spack installation."""

# SPDX 2.3 Generation
def post_install(spec, explicit=None):
    pkg = spec.package

    # License handling
    def get_license(pkg):
        license_field = getattr(pkg, "licenses", None)
        if isinstance(license_field, (list, tuple)) and license_field:
            return license_field[0]
        elif isinstance(license_field, str):
            return license_field
        else:
            return "NOASSERTION"

    # Document information
    t = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)
    document_namespace = f"http://spack.io/sbom/{spec.name}-{spec.version}-{spec.dag_hash()}"
    document_name = f"SBOM of {spec.name}-{spec.version} built with Spack"

    # ---- Package entry for this spec ----
    pkg_entry = {
        "SPDXID": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        "name": spec.name,
        "versionInfo": str(spec.version),
        "supplier": getattr(pkg, "homepage", None) or "NOASSERTION",
        "downloadLocation": getattr(pkg, "url", None) or "NOASSERTION",
        "filesAnalyzed": False,
        "licenseDeclared": get_license(pkg)
    }

    # ---- Package entries for dependencies ----
    deps = []
    relationships = [
        {
            "relatedSpdxElement": f"SPDXRef-DOCUMENT-{spec.name}-{spec.version}",
            "relationshipType": "DESCRIBES",
            "spdxElementId": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        }
    ]

    for dep in spec.dependencies():
        dep_name = dep.name
        dep_spec = dep
        
        dep_pkg = getattr(dep, "package", None)
        license_declared = get_license(dep_pkg) if dep_pkg else "NOASSERTION"

        dep_entry = {
            "SPDXID": f"SPDXRef-PACKAGE-{dep_name}-{dep_spec.version}",
            "name": dep_name,
            "versionInfo": str(dep_spec.version),
            "supplier": getattr(dep_pkg, "homepage", None) or "NOASSERTION",
            "downloadLocation": getattr(dep_pkg, "url", None) or "NOASSERTION",
            "filesAnalyzed": False,
            "licenseDeclared": license_declared,
            "licenseConcluded":, "NOASSERTION"
        }
        deps.append(dep_entry)

        relationships.append(
            {
                "spdxElementId": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": dep_entry["SPDXID"],
            }
        )

    # Compose SPDX document
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": f"SPDXRef-DOCUMENT-{spec.name}-{spec.version}",
        "documentNamespace": document_namespace,
        "creationInfo": {
            "created": created_time,
            "creators": ["Organization: Spack SBOM Generator"],
        },
        "name": document_name,
        "packages": [pkg_entry] + deps,
        "relationships": relationships,
    }

    # Write to SBOM file
    path = os.path.join(spec.prefix, "sbom.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(sbom, f, indent=2)

    tty.msg(f"[SBOM] Wrote SPDX 2.3 SBOM to {path}")
