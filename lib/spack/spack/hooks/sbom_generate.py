import os
import spack.hooks
import time
import spack.util.spack_json as sjson
from spack.llnl.util import tty

"""Generate a Software Bill of Materials (SBOM) for each successful Spack installation."""

# SPDX 2.3 Generation
def post_install(spec, explicit=None):
    pkg = spec.package

    # URL location handling 
    download_url = None
    if hasattr(pkg, "versions") and str(spec.version) in pkg.versions:
        # grab url associated with specific version
        version_data = pkg.versions[str(spec.version)]
        download_url = getattr(version_data, "url", None) or "NOASSERTION"
        
    # License handling
    def get_license(pkg):
        if not pkg:
            return "NOASSERTION"

        # Look for license info on both the instance and the class
        lic = (
            getattr(pkg, "licenses", None)
            or getattr(pkg, "license", None)
            or getattr(pkg.__class__, "licenses", None)
            or getattr(pkg.__class__, "license", None)
        )

        if not lic:
            return "NOASSERTION"

        if isinstance(lic, (list, tuple)):
            return " AND ".join(lic)
        return str(lic)

    # Document information
    t = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)
    
    # Create path and dir for sbom
    sbom_path = os.path.join(spec.prefix, "sbom.json")
    os.makedirs(os.path.dirname(sbom_path), exist_ok=True)
     
    unique_str = f"{spec.name}-{spec.version}-{spec.dag_hash()}"
    unique_hash = hashlib.sha256(unique_str.encode("utf-8")).hexdigest()
    document_namespace = f"file://{sbom_path}#spack-{unique_hash}"
    
    # Package entry for each installation.
    # Represents the top-level component in the SBOM (the package being installed).
    pkg_entry = {
        "SPDXID": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        "name": spec.name,
        "versionInfo": str(spec.version),
        "supplier": getattr(pkg, "homepage", None) or "NOASSERTION",
        "downloadLocation": str(download_url or getattr(pkg, "url", None) or "NOASSERTION"),
        "filesAnalyzed": False,
        "licenseDeclared": get_license(pkg),
        "licenseConcluded": "NOASSERTION"
    }

    # Package entry for each dependency of a spec.
    # Each dependency becomes its own entry, linked to the top-level component.
    deps = []
    relationships = [
        {
            "relatedSpdxElement": f"SPDXRef-DOCUMENT-{spec.name}-{str(spec.version)}",
            "relationshipType": "DESCRIBES",
            "spdxElementId": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        }
    ]

    for dep in spec.dependencies(deptype='all'):
        dep_name = dep.name
        dep_spec = dep
        dep_pkg = getattr(dep, "package", None)
        
        license_declared = get_license(dep_pkg) if dep_pkg else "NOASSERTION"

        dep_entry = {
            "SPDXID": f"SPDXRef-PACKAGE-{dep_name}-{str(dep_spec.version)}",
            "name": dep_name,
            "versionInfo": str(dep_spec.version),
            "supplier": getattr(dep_pkg, "homepage", None) or "NOASSERTION",
            "downloadLocation": str(getattr(dep_pkg, "url", None) or "NOASSERTION"),
            "filesAnalyzed": False,
            "licenseDeclared": license_declared,
            "licenseConcluded": "NOASSERTION"
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
            "creators": ["Organization: Spack"],
        },
        "name": document_name,
        "packages": [pkg_entry] + deps,
        "relationships": relationships,
    }
    print("sbom:", sbom)

    # Write to SBOM file
    with open(path, "w") as f:
        sjson.dump(sbom, f)
    tty.msg(f"[SBOM] Wrote SPDX 2.3 SBOM to {path}")
