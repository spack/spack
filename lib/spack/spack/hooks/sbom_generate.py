import json
import os
import spack.hooks
from llnl.util import tty

"""Generate a Software Bill of Materials (SBOM) for each successful Spack installtion."""

@spack.hooks.register("post_install")
def post_install(spec, **kwargs):
    pkg = spec.package
    sbom = {
        "SPDXID": f"SPDXRef-{spec.name}-{spec.version}",
        "name": spec.name,
        "versionInfo": str(spec.version),
        "supplier": getattr(pkg, "homepage", None) or "NOASSERTION",
        "downloadLocation": getattr(pkg, "url", None) or "NOASSERTION",
        "licenseDeclared": pkg.licenses[0] if getattr(pkg, "licenses", None) else "NOASSERTION",
        "dependencies": [d.name for d in spec.dependencies()],
    }

    path = os.path.join(spec.prefix, "sbom.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(sbom, f, indent=2)
    tty.msg(f"[SBOM] Wrote {path}")

