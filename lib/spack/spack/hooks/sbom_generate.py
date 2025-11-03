import json
import os
import spack.hooks
import time
from spack.llnl.util import tty

"""Generate a Software Bill of Materials (SBOM) for each successful Spack installation."""

# SPDX 2.3 Generation
def post_install(spec, explicit=None):
    pkg = spec.package
    
    # extract license info
    license_field = getattr(pkg, "licenses", None)
    if isinstance(license_field, (list, tuple)) and license_field:
        license_id = license_field[0]
    elif isinstance(license_field, str):
        license_id = license_field
    else:
        license_id = "NOASSERTION"

    sbom = {
        "SPDXID": f"SPDXRef-{spec.name}-{spec.version}",
        "name": spec.name,
        "versionInfo": str(spec.version),
        "supplier": getattr(pkg, "homepage", None) or "NOASSERTION",
        "downloadLocation": getattr(pkg, "url", None) or "NOASSERTION",
        "licenseDeclared": license_id,
        "dependencies": [d.name for d in spec.dependencies()],
    }

    path = os.path.join(spec.prefix, "sbom.json")
    print("PATH:", path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(sbom, f, indent=2)
    tty.msg(f"[SBOM] Wrote {path}")
