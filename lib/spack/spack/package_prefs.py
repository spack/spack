##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from six import string_types
from six import iteritems

from llnl.util.lang import classproperty

import spack.repo
import spack.error
from spack.util.path import canonicalize_path
from spack.version import VersionList


_lesser_spec_types = {'compiler': spack.spec.CompilerSpec,
                      'version': VersionList}


def _spec_type(component):
    """Map from component name to spec type for package prefs."""
    return _lesser_spec_types.get(component, spack.spec.Spec)


def get_packages_config():
    """Wrapper around get_packages_config() to validate semantics."""
    config = spack.config.get('packages')

    # Get a list of virtuals from packages.yaml.  Note that because we
    # check spack.repo, this collects virtuals that are actually provided
    # by sometihng, not just packages/names that don't exist.
    # So, this won't include, e.g., 'all'.
    virtuals = [(pkg_name, pkg_name._start_mark) for pkg_name in config
                if spack.repo.path.is_virtual(pkg_name)]

    # die if there are virtuals in `packages.py`
    if virtuals:
        errors = ["%s: %s" % (line_info, name) for name, line_info in virtuals]
        raise VirtualInPackagesYAMLError(
            "packages.yaml entries cannot be virtual packages:",
            '\n'.join(errors))

    return config


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
    _packages_config_cache = None
    _spec_cache = {}

    def __init__(self, pkgname, component, vpkg=None):
        self.pkgname = pkgname
        self.component = component
        self.vpkg = vpkg

    def __call__(self, spec):
        """Return a key object (an index) that can be used to sort spec.

           Sort is done in package order. We don't cache the result of
           this function as Python's sort functions already ensure that the
           key function is called at most once per sorted element.
        """
        spec_order = self._specs_for_pkg(
            self.pkgname, self.component, self.vpkg)

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

    @classproperty
    @classmethod
    def _packages_config(cls):
        if cls._packages_config_cache is None:
            cls._packages_config_cache = get_packages_config()
        return cls._packages_config_cache

    @classmethod
    def _order_for_package(cls, pkgname, component, vpkg=None, all=True):
        """Given a package name, sort component (e.g, version, compiler, ...),
           and an optional vpkg, return the list from the packages config.
        """
        pkglist = [pkgname]
        if all:
            pkglist.append('all')

        for pkg in pkglist:
            pkg_entry = cls._packages_config.get(pkg)
            if not pkg_entry:
                continue

            order = pkg_entry.get(component)
            if not order:
                continue

            # vpkg is one more level
            if vpkg is not None:
                order = order.get(vpkg)

            if order:
                return [str(s).strip() for s in order]

        return []

    @classmethod
    def _specs_for_pkg(cls, pkgname, component, vpkg=None):
        """Given a sort order specified by the pkgname/component/second_key,
           return a list of CompilerSpecs, VersionLists, or Specs for
           that sorting list.
        """
        key = (pkgname, component, vpkg)

        specs = cls._spec_cache.get(key)
        if specs is None:
            pkglist = cls._order_for_package(pkgname, component, vpkg)
            spec_type = _spec_type(component)
            specs = [spec_type(s) for s in pkglist]
            cls._spec_cache[key] = specs

        return specs

    @classmethod
    def clear_caches(cls):
        cls._packages_config_cache = None
        cls._spec_cache = {}

    @classmethod
    def has_preferred_providers(cls, pkgname, vpkg):
        """Whether specific package has a preferred vpkg providers."""
        return bool(cls._order_for_package(pkgname, 'providers', vpkg, False))

    @classmethod
    def preferred_variants(cls, pkg_name):
        """Return a VariantMap of preferred variants/values for a spec."""
        for pkg in (pkg_name, 'all'):
            variants = cls._packages_config.get(pkg, {}).get('variants', '')
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
    from spack.util.module_cmd import get_path_from_module # NOQA: ignore=F401

    allpkgs = get_packages_config()
    name = spec.name

    external_specs = []
    pkg_paths = allpkgs.get(name, {}).get('paths', None)
    pkg_modules = allpkgs.get(name, {}).get('modules', None)
    if (not pkg_paths) and (not pkg_modules):
        return []

    for external_spec, path in iteritems(pkg_paths):
        if not path:
            # skip entries without paths (avoid creating extra Specs)
            continue

        external_spec = spack.spec.Spec(external_spec,
                                        external_path=canonicalize_path(path))
        if external_spec.satisfies(spec):
            external_specs.append(external_spec)

    for external_spec, module in iteritems(pkg_modules):
        if not module:
            continue

        external_spec = spack.spec.Spec(
            external_spec, external_module=module)
        if external_spec.satisfies(spec):
            external_specs.append(external_spec)

    # defensively copy returned specs
    return [s.copy() for s in external_specs]


def is_spec_buildable(spec):
    """Return true if the spec pkgspec is configured as buildable"""
    allpkgs = get_packages_config()
    if spec.name not in allpkgs:
        return True
    if 'buildable' not in allpkgs[spec.name]:
        return True
    return allpkgs[spec.name]['buildable']


class VirtualInPackagesYAMLError(spack.error.SpackError):
    """Raised when a disallowed virtual is found in packages.yaml"""
