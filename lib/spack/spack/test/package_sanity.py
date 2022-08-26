# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This test does sanity checks on Spack's builtin package database."""
# A few functions from this module are used to
# do sanity checks only on packagess modified by a PR
import spack.fetch_strategy
import spack.package_base
import spack.paths
import spack.repo
import spack.spec
import spack.variant


def test_variant_defaults_are_parsable_from_cli():
    """Ensures that variant defaults are parsable from cli."""
    failing = []
    for pkg_cls in spack.repo.path.all_package_classes():
        for variant_name, entry in pkg_cls.variants.items():
            variant, _ = entry
            default_is_parsable = (
                # Permitting a default that is an instance on 'int' permits
                # to have foo=false or foo=0. Other falsish values are
                # not allowed, since they can't be parsed from cli ('foo=')
                isinstance(variant.default, int)
                or variant.default
            )
            if not default_is_parsable:
                failing.append((pkg_cls.name, variant_name))
    assert not failing


def test_variant_defaults_listed_explicitly_in_values():
    failing = []
    for pkg_cls in spack.repo.path.all_package_classes():
        for variant_name, entry in pkg_cls.variants.items():
            variant, _ = entry
            vspec = variant.make_default()
            try:
                variant.validate_or_raise(vspec, pkg_cls=pkg_cls)
            except spack.variant.InvalidVariantValueError:
                failing.append((pkg_cls.name, variant.name))
    assert not failing
