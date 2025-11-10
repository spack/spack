import json
import spack.util.spack_json as sjson
import os
import spack.hooks
import time
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
    document_namespace = f"http://spack.io/sbom/{spec.name}-{str(spec.version)}-{spec.dag_hash()}"
    document_name = f"SBOM of {spec.name}-{spec.version} built with Spack"

    # ---- Package entry for this spec ----
    print("CHECK ONE      !!!!")
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

    # ---- Package entries for dependencies ----
    deps = []
    relationships = [
        {
            "relatedSpdxElement": f"SPDXRef-DOCUMENT-{spec.name}-{str(spec.version)}",
            "relationshipType": "DESCRIBES",
            "spdxElementId": f"SPDXRef-PACKAGE-{spec.name}-{spec.version}",
        }
    ]

    # for dep in spec.dependencies():    
    # for dep in spec.dependencies(deptype='all').values():
    print("CHECK TWO      !!!!")
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
        print(dep_entry)
        deps.append(dep_entry)

        relationships.append(
            {
                "spdxElementId": f"SPDXRef-PACKAGE-{spec.name}-{str(spec.version)}",
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": dep_entry["SPDXID"],
            }
        )

    # Compose SPDX document
    print("CHECK THREE      !!!!")
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": f"SPDXRef-DOCUMENT-{spec.name}-{str(spec.version)}",
        "documentNamespace": document_namespace,
        "creationInfo": {
            "created": created_time,
            "creators": ["Organization: Spack SBOM Generator"],
        },
        "name": document_name,
        "packages": [pkg_entry] + deps,
        "relationships": relationships,
    }
    print("sbom:", sbom)

    # Write to SBOM file
    print("CHECK FOUR      !!!!")
    path = os.path.join(spec.prefix, "sbom.json")
    print("CHECK FIVE      !!!!")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print("CHECK SIX      !!!!")
    with open(path, "w") as f:
        print("CHECK SEVEN      !!!!")
        sjson.dump(sbom, f)
        print("check 8")
    tty.msg(f"[SBOM] Wrote SPDX 2.3 SBOM to {path}")
