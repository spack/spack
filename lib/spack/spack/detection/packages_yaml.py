# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Import external packages from user configuration"""
import collections
import warnings

import spack.concretize
import spack.config
import spack.error

from .common import DetectedPackage, ensure_architecture_and_compiler


def import_externals(scope=None):
    """Return all the specs mentioned as externals in packages.yaml"""
    packages_yaml = spack.config.CONFIG.get("packages", scope=scope)
    result = collections.defaultdict(list)
    for pkg_name, package_configuration in packages_yaml.items():
        for item in package_configuration.get("externals", []):
            # All these steps are needed to ensure "matching" external specs
            # that are either detected or imported from config are hashed in
            # the same way.

            # Here it is essential that we pass a string, otherwise external_path would not be set
            s = spack.spec.Spec(
                str(spack.spec.parse_with_version_concrete(item["spec"])),
                external_path=item.get("prefix"),
                external_modules=item.get("modules"),
            )
            s = spack.spec.Spec.from_detection(
                s, extra_attributes=item.get("extra_attributes", {})
            )
            ensure_architecture_and_compiler(s)
            result[pkg_name].append(DetectedPackage(spec=s, prefix=item.get("prefix")))

    # Try to reconstruct extensions for imported specs
    for name, externals in result.items():
        for candidate in externals:
            s = candidate.spec
            pkg = s.package_class(s)
            if pkg.extendee_spec:
                pkg.update_external_dependencies(result.get(pkg.extendee_spec.name, []))

    return result


def _pkg_config_dict(external_pkg_entries):
    """Generate a package specific config dict according to the packages.yaml schema.

    This does not generate the entire packages.yaml. For example, given some
    external entries for the CMake package, this could return::

        {
            'externals': [{
                'spec': 'cmake@3.17.1',
                'prefix': '/opt/cmake-3.17.1/'
            }, {
                'spec': 'cmake@3.16.5',
                'prefix': '/opt/cmake-3.16.5/'
            }]
       }
    """
    pkg_dict = spack.util.spack_yaml.syaml_dict()
    pkg_dict["externals"] = []
    for e in external_pkg_entries:
        if not _spec_is_valid(e.spec):
            continue

        external_items = [("spec", str(e.spec)), ("prefix", e.prefix)]
        if e.spec.external_modules:
            external_items.append(("modules", e.spec.external_modules))

        if e.spec.extra_attributes:
            external_items.append(
                (
                    "extra_attributes",
                    spack.util.spack_yaml.syaml_dict(e.spec.extra_attributes.items()),
                )
            )

        # external_items.extend(e.spec.extra_attributes.items())
        pkg_dict["externals"].append(spack.util.spack_yaml.syaml_dict(external_items))

    return pkg_dict


def _spec_is_valid(spec):
    try:
        str(spec)
    except spack.error.SpackError:
        # It is assumed here that we can at least extract the package name from
        # the spec, so we can look up the implementation of determine_spec_details
        msg = "Constructed spec for {0} does not have a string representation"
        warnings.warn(msg.format(spec.name))
        return False

    try:
        spack.spec.Spec(str(spec))
    except spack.error.SpackError:
        warnings.warn(
            "Constructed spec has a string representation but the string"
            " representation does not evaluate to a valid spec: {0}".format(str(spec))
        )
        return False

    return True
