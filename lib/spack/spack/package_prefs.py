# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from six import string_types

import spack.repo
import spack.error
from spack.util.path import canonicalize_path
from spack.version import VersionList


_lesser_spec_types = {'compiler': spack.spec.CompilerSpec,
                      'version': VersionList}


def _spec_type(component):
    """Map from component name to spec type for package prefs."""
    return _lesser_spec_types.get(component, spack.spec.Spec)


class PackagePrefs(object):
    """Defines the sort order for a set of specs.

    Spack's package preference implementation uses PackagePrefss to
    define sort order. The PackagePrefs class looks at Spack's
    packages.yaml configuration and, when called on a spec, returns a key
    that can be used to sort that spec in order of the user's
    preferences.

    You can use it like this:

       # key function sorts CompilerSpecs for `mpich` in order of preference
       kf = PackagePrefs('mpich', 'compiler')
       compiler_list.sort(key=kf)

    Or like this:

       # key function to sort VersionLists for OpenMPI in order of preference.
       kf = PackagePrefs('openmpi', 'version')
       version_list.sort(key=kf)

    Optionally, you can sort in order of preferred virtual dependency
    providers.  To do that, provide 'providers' and a third argument
    denoting the virtual package (e.g., ``mpi``):

       kf = PackagePrefs('trilinos', 'providers', 'mpi')
       provider_spec_list.sort(key=kf)

    """
    def __init__(self, pkgname, component, vpkg=None, all=True):
        self.pkgname = pkgname
        self.component = component
        self.vpkg = vpkg
        self.all = all

        self._spec_order = None

    def __call__(self, spec):
        """Return a key object (an index) that can be used to sort spec.

           Sort is done in package order. We don't cache the result of
           this function as Python's sort functions already ensure that the
           key function is called at most once per sorted element.
        """
        if self._spec_order is None:
            self._spec_order = self._specs_for_pkg(
                self.pkgname, self.component, self.vpkg, self.all)
        spec_order = self._spec_order

        # integer is the index of the first spec in order that satisfies
        # spec, or it's a number larger than any position in the order.
        match_index = next(
            (i for i, s in enumerate(spec_order) if spec.satisfies(s)),
            len(spec_order))
        if match_index < len(spec_order) and spec_order[match_index] == spec:
            # If this is called with multiple specs that all satisfy the same
            # minimum index in spec_order, the one which matches that element
            # of spec_order exactly is considered slightly better. Note
            # that because this decreases the value by less than 1, it is not
            # better than a match which occurs at an earlier index.
            match_index -= 0.5
        return match_index

    @classmethod
    def order_for_package(cls, pkgname, component, vpkg=None, all=True):
        """Given a package name, sort component (e.g, version, compiler, ...),
           and an optional vpkg, return the list from the packages config.
        """
        pkglist = [pkgname]
        if all:
            pkglist.append('all')

        for pkg in pkglist:
            pkg_entry = spack.config.get('packages').get(pkg)
            if not pkg_entry:
                continue

            order = pkg_entry.get(component)
            if not order:
                continue

            # vpkg is one more level
            if vpkg is not None:
                order = order.get(vpkg)

            if order:
                ret = [str(s).strip() for s in order]
                if component == 'target':
                    ret = ['target=%s' % tname for tname in ret]
                return ret

        return []

    @classmethod
    def _specs_for_pkg(cls, pkgname, component, vpkg=None, all=True):
        """Given a sort order specified by the pkgname/component/second_key,
           return a list of CompilerSpecs, VersionLists, or Specs for
           that sorting list.
        """
        pkglist = cls.order_for_package(
            pkgname, component, vpkg, all)
        spec_type = _spec_type(component)
        return [spec_type(s) for s in pkglist]

    @classmethod
    def has_preferred_providers(cls, pkgname, vpkg):
        """Whether specific package has a preferred vpkg providers."""
        return bool(cls.order_for_package(pkgname, 'providers', vpkg, False))

    @classmethod
    def has_preferred_targets(cls, pkg_name):
        """Whether specific package has a preferred vpkg providers."""
        return bool(cls.order_for_package(pkg_name, 'target'))

    @classmethod
    def preferred_variants(cls, pkg_name):
        """Return a VariantMap of preferred variants/values for a spec."""
        for pkg in (pkg_name, 'all'):
            variants = spack.config.get('packages').get(pkg, {}).get(
                'variants', '')
            if variants:
                break

        # allow variants to be list or string
        if not isinstance(variants, string_types):
            variants = " ".join(variants)

        # Only return variants that are actually supported by the package
        pkg = spack.repo.get(pkg_name)
        spec = spack.spec.Spec("%s %s" % (pkg_name, variants))
        return dict((name, variant) for name, variant in spec.variants.items()
                    if name in pkg.variants)


def spec_externals(spec):
    """Return a list of external specs (w/external directory path filled in),
       one for each known external installation."""
    # break circular import.
    from spack.util.module_cmd import path_from_modules # NOQA: ignore=F401

    allpkgs = spack.config.get('packages')
    names = set([spec.name])
    names |= set(vspec.name for vspec in spec.package.virtuals_provided)

    external_specs = []
    for name in names:
        pkg_config = allpkgs.get(name, {})
        pkg_externals = pkg_config.get('externals', [])
        for entry in pkg_externals:
            spec_str = entry['spec']
            external_path = entry.get('prefix', None)
            if external_path:
                external_path = canonicalize_path(external_path)
            external_modules = entry.get('modules', None)
            external_spec = spack.spec.Spec.from_detection(
                spack.spec.Spec(
                    spec_str,
                    external_path=external_path,
                    external_modules=external_modules
                ), extra_attributes=entry.get('extra_attributes', {})
            )
            if external_spec.satisfies(spec):
                external_specs.append(external_spec)

    # Defensively copy returned specs
    return [s.copy() for s in external_specs]


def is_spec_buildable(spec):
    """Return true if the spec pkgspec is configured as buildable"""

    allpkgs = spack.config.get('packages')
    all_buildable = allpkgs.get('all', {}).get('buildable', True)

    # Get the list of names for which all_buildable is overridden
    reverse = [name for name, entry in allpkgs.items()
               if entry.get('buildable', all_buildable) != all_buildable]
    # Does this spec override all_buildable
    spec_reversed = (spec.name in reverse or
                     any(spec.package.provides(name) for name in reverse))
    return not all_buildable if spec_reversed else all_buildable


class VirtualInPackagesYAMLError(spack.error.SpackError):
    """Raised when a disallowed virtual is found in packages.yaml"""
