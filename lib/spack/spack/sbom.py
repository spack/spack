# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Generate a software bill of materials for a spack package
# Original development work: https://github.com/spack/spack-sbom
# https://www.ntia.gov/files/ntia/publications/howto_guide_for_sbom_generation_v1.pdf

import os
import uuid
from datetime import datetime

import llnl.util.tty as tty

import spack.config
import spack.main
import spack.spec
import spack.util.spack_json as sjson

# Generate the sbom? They can be large, so default is no.
generate_sbom = False

# Use CycloneDX which is a simplified format approved by standards committees
# https://cyclonedx.org/docs/1.3/json
# https://cyclonedx.org/use-cases/
template = {
    "bomFormat": "CycloneDX",
    # The version of the CycloneDX specification a BOM is written to
    "specVersion": "1.3",
    "serialNumber": "",
    # The version WE are generating for the package - this would increment
    "version": 1,
    # Will be populated with metadata
    "metadata": {},
}


def generate_timestamp_now():
    return str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))


def get_component(spec):
    """
    Given a spec, get a component for it.
    """
    # Anything with "lib" is a library, otherwise application
    component_type = "lib" if "lib" in spec.package.name else "application"

    # Must be concrets
    spec.concretize()

    component = {
        # Note that "application" might also be a suitable choice
        # https://cyclonedx.org/docs/1.3/json/#metadata_component_type
        "type": component_type,
        # Specifies the scope of the component. If scope is not specified,
        # 'required' scope should be assumed by the consumer of the BOM
        # Let's explicitly state that :)
        "scope": "required",
        # The name of the component, often shortened
        # Examples: commons-lang3 and jquery
        "name": spec.package.name,
        # Associated mime-type. Spack doesn't have one officially
        # This is what @vsoch using for oras push to an OCI registry
        "mime-type": "application/vnd.spack.package",
        # The grouping name or identifier. This will often be a shortened,
        # single name of the company or project that produced the component,
        # or the source package or domain name. Whitespace and special chars
        # should be avoided. Examples include: apache, org.apache.commons.
        "group": "spack.io",
        # The component version, ideally semver
        "version": str(spec.version),
        # An optional identifier which can be used to reference the component
        # elsewhere in the BOM. Every bom-ref should be unique.
        # We can use the build hash since it's unique to this spec
        "bom-ref": str(spec),
        # Excluded
        # publisher: The person(s) or organization(s) that published it
        # author: The person(s) or organization(s) that authored the component
        # supplier: The organization that supplied the component.
        # licenses: spack doesn't have enough metadata to make a call
        # copyright: An optional copyright notice
        # purl: spack doesn't have these
        # swid: ISO-IEC 19770-2 Software Identification (SWID) Tags
        # pedigree: Component pedigree (document complex supply chain scenarios)
        # components: components referenced within
        # evidence: evidence collected through various forms of analysis.
        # properites: extra name/value keypairs
    }

    # Specifies a description for the component
    # Only add if not empty!
    description = spec.package.format_doc()
    if description:
        component["description"] = description

    # Add hashes, whichever might exist
    # I looked for all unique hash types on 11/28
    # names = set()
    # for package in spack.repo.all_package_names():
    #    spec = spack.spec.Spec(package)
    #    for _, version in spec.package.versions.items():
    #        for alg, _ in version.items():
    #            names.add(alg)

    component["hashes"] = []
    for key, hashvalue in spec.package.versions.get(spec.version, {}).items():

        # Covers both sha256 and sha256sum
        if key.startswith("sha256"):
            component["hashes"].append({"alg": "SHA-256", "content": hashvalue})

    # External references?
    if spec.package.all_urls:
        component["externalReferences"] = []
        for url in spec.package.all_urls:
            component["externalReferences"].append({"type": "website", "url": url})

    # Finally, custom spack metadata (properties)
    component["properties"] = {
        "spack:build_hash": spec.build_hash(),
        "spack:dag_hash": spec.dag_hash(),
        "spack:spec": str(spec),
        "spack:build_spec": str(spec.build_spec),
        "spack:architecture": str(spec.architecture),
        "spack:variants": str(spec.variants),
        "spack:compiler": str(spec.compiler),
    }
    return component


def find_sbom(spec):
    """
    Find the path of an sbom, if it exists, otherwise return None
    """
    if os.path.exists(spec.sbom):
        return spec.sbom


def create_sbom(spec):
    """
    Create an sbom for a spec in the install directory.
    """
    if os.path.exists(spec.sbom):
        tty.die("sbom already exists: %s" % spec.sbom)

    # If more versions are ever supported, we can add them here.
    sbom = generate_cyclonedx(spec)
    with open(spec.sbom, 'w') as f:
        sjson.dump(sbom, stream=f)
    return spec.sbom


def generate_cyclonedx(pkg):
    """
    Generates a CycloneDX sbom based on best practices suggested in the guide.
    """
    bom = template.copy()
    if isinstance(pkg, spack.spec.Spec):
        spec = pkg
    else:
        spec = spack.spec.Spec(pkg)

    # Every BOM generated should have a unique serial number, even if contents
    # being generated have not changed over time. The process/tool responsible
    # for creating the BOM should create random UUID's for every BOM generated.
    bom["serialNumber"] = "urn:uuid:" + str(uuid.uuid4())

    # The date and time (timestamp) when the document was created.
    metadata = {"timestamp": generate_timestamp_now()}

    # The tool(s) used in the creation of the BOM.
    metadata["tools"] = [
        {
            "vendor": "Lawrence Livermore National Lab",
            "name": "Spack",
            "version": spack.main.get_version(),
        }
    ]

    # The person(s) who created the BOM. should be under authors
    # Automatic generation won't have authors

    # The component that the BOM describes.
    metadata["component"] = get_component(spec)

    # Skipped:
    # manufacture: The organization that manufactured the component.
    # supplier: The organization that supplied the component.

    # Assume icenses under the bom describe spack, but not the component
    metadata["licenses"] = [
        {"license": {"name": "MIT"}},
        {"license": {"name": "Apache-2.0"}},
    ]
    bom["metadata"] = metadata

    # We might also assume that properties on this level could be for spack
    # Could put more spack properties here.
    deps = spec.dependencies()
    components = {}

    # Let's include all nested dependencies
    if deps:
        while deps:
            dep = deps.pop(0)
            deps = deps + dep.dependencies()

            if str(dep) not in components:
                components[str(dep)] = get_component(dep)

    if components:
        bom["components"] = components

    # Finally, add direct dependencies
    deps = spec.dependencies()
    if deps:
        bom["dependencies"] = []
        for dep in deps:
            # The bom-ref identifiers of the components that
            # are dependencies of this dependency object.
            dependsOn = [str(x) for x in dep.dependencies()]
            bom["dependencies"].append({"ref": str(dep), "dependsOn": dependsOn})

    # Add an external reference for spack packages, GitHub, etc.
    bom["externalReferences"] = [
        {"type": "website", "url": "https://github.com/spack/spack"},
        {"type": "website", "url": "https://spack.github.io/packages"},
    ]
    return bom
