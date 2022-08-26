# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This test does sanity checks on Spack's builtin package database."""
import os.path

import pytest

# A few functions from this module are used to
# do sanity checks only on packagess modified by a PR
import spack.cmd.style as style
import spack.fetch_strategy
import spack.package_base
import spack.paths
import spack.repo
import spack.spec
import spack.util.crypto as crypto
import spack.util.executable as executable
import spack.variant


def test_get_all_mock_packages(mock_packages):
    """Get the mock packages once each too."""
    for name in mock_packages.all_package_names():
        mock_packages.get_pkg_class(name)


def test_all_virtual_packages_have_default_providers():
    """All virtual packages must have a default provider explicitly set."""
    defaults = spack.config.get("packages", scope="defaults")
    default_providers = defaults["all"]["providers"]
    providers = spack.repo.path.provider_index.providers
    default_providers_filename = spack.config.config.scopes["defaults"].get_section_filename(
        "packages"
    )
    for provider in providers:
        assert provider in default_providers, (
            "all providers must have a default in %s" % default_providers_filename
        )


def test_docstring():
    """Ensure that every package has a docstring."""
    for name in spack.repo.all_package_names():
        pkg_cls = spack.repo.path.get_pkg_class(name)
        assert pkg_cls.__doc__


def test_all_packages_use_sha256_checksums():
    """Make sure that no packages use md5 checksums."""

    errors = []
    for name in spack.repo.all_package_names():
        pkg_cls = spack.repo.path.get_pkg_class(name)
        pkg = pkg_cls(spack.spec.Spec(name))

        # for now, don't enforce on packages that require manual downloads
        # TODO: eventually fix these, too.
        if pkg.manual_download:
            continue

        def invalid_sha256_digest(fetcher):
            if getattr(fetcher, "digest", None):
                h = crypto.hash_algo_for_digest(fetcher.digest)
                if h != "sha256":
                    return h

        for v, args in pkg.versions.items():
            fetcher = spack.fetch_strategy.for_package_version(pkg, v)
            bad_digest = invalid_sha256_digest(fetcher)
            if bad_digest:
                errors.append(
                    "All packages must use sha256 checksums. %s@%s uses %s."
                    % (name, v, bad_digest)
                )

        for _, resources in pkg.resources.items():
            for resource in resources:
                bad_digest = invalid_sha256_digest(resource.fetcher)
                if bad_digest:
                    errors.append(
                        "All packages must use sha256 checksums."
                        "Resource in %s uses %s." % (name, bad_digest)
                    )

    assert [] == errors


def test_api_for_build_and_run_environment():
    """Ensure that every package uses the correct API to set build and
    run environment, and not the old one.
    """
    failing = []
    for pkg_cls in spack.repo.path.all_package_classes():
        add_to_list = hasattr(pkg_cls, "setup_environment") or hasattr(
            pkg_cls, "setup_dependent_environment"
        )
        if add_to_list:
            failing.append(pkg_cls)

    msg = (
        "there are {0} packages using the old API to set build "
        "and run environment [{1}], for further information see "
        "https://github.com/spack/spack/pull/11115"
    )
    assert not failing, msg.format(len(failing), ",".join(x.name for x in failing))


@pytest.mark.skipif(not executable.which("git"), reason="requires git to be installed")
def test_prs_update_old_api():
    """Ensures that every package modified in a PR doesn't contain
    deprecated calls to any method.
    """
    ref = os.getenv("GITHUB_BASE_REF")
    if not ref:
        pytest.skip("No base ref found")

    changed_package_files = [x for x in style.changed_files(base=ref) if style.is_package(x)]
    failing = []
    for file in changed_package_files:
        if "builtin.mock" not in file:  # don't restrict packages for tests
            name = os.path.basename(os.path.dirname(file))
            pkg_cls = spack.repo.path.get_pkg_class(name)
            pkg = pkg_cls(spack.spec.Spec(name))

            failed = hasattr(pkg, "setup_environment") or hasattr(
                pkg, "setup_dependent_environment"
            )
            if failed:
                failing.append(name)

    msg = (
        "there are {0} packages using the old API to set build "
        "and run environment [{1}], for further information see "
        "https://github.com/spack/spack/pull/11115"
    )
    assert not failing, msg.format(len(failing), ",".join(failing))


def test_all_dependencies_exist():
    """Make sure no packages have nonexisting dependencies."""
    missing = {}
    pkgs = [pkg for pkg in spack.repo.path.all_package_names()]
    spack.package_base.possible_dependencies(*pkgs, transitive=True, missing=missing)

    lines = ["%s: [%s]" % (name, ", ".join(deps)) for name, deps in missing.items()]
    assert not missing, "These packages have missing dependencies:\n" + ("\n".join(lines))


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
