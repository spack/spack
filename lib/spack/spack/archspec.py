# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Adapter for the archspec library."""

import spack.vendor.archspec.cpu

import spack.spec


def microarchitecture_flags(spec: spack.spec.Spec, language: str) -> str:
    """Return the microarchitecture flags for a given spec and compiler associated with the given
    language."""
    target = spec.target

    if not spec.has_virtual_dependency(language):
        raise ValueError(f"The spec {spec.name} does not depend on {language}")
    elif target is None:
        raise ValueError(f"The spec {spec.name} does not have a target defined")

    compiler = spec.dependencies(virtuals=language)[0]

    return microarchitecture_flags_from_target(target, compiler)


def microarchitecture_flags_from_target(
    target: spack.vendor.archspec.cpu.Microarchitecture, compiler: spack.spec.Spec
) -> str:
    """Return the microarchitecture flags for a given compiler and target."""
    # Try to check if the current compiler comes with a version number or has an unexpected suffix.
    # If so, treat it as a compiler with a custom spec.
    version_number, _ = spack.vendor.archspec.cpu.version_components(
        compiler.version.dotted_numeric_string
    )
    try:
        return target.optimization_flags(compiler.package.archspec_name(), version_number)
    except ValueError:
        return ""
