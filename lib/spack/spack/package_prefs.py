##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import spack
import spack.error
from spack.version import *


def get_packages_config():
    """Wrapper around get_packages_config() to validate semantics."""
    config = spack.config.get_config('packages')

    # Get a list of virtuals from packages.yaml.  Note that because we
    # check spack.repo, this collects virtuals that are actually provided
    # by sometihng, not just packages/names that don't exist.
    # So, this won't include, e.g., 'all'.
    virtuals = [(pkg_name, pkg_name._start_mark) for pkg_name in config
                if spack.repo.is_virtual(pkg_name)]

    # die if there are virtuals in `packages.py`
    if virtuals:
        errors = ["%s: %s" % (line_info, name) for name, line_info in virtuals]
        raise VirtualInPackagesYAMLError(
            "packages.yaml entries cannot be virtual packages:",
            '\n'.join(errors))

    return config


class PreferredPackages(object):
    def __init__(self):
        self.preferred = get_packages_config()
        self._spec_for_pkgname_cache = {}

    # Given a package name, sort component (e.g, version, compiler, ...), and
    # a second_key (used by providers), return the list
    def _order_for_package(self, pkgname, component, second_key,
                           test_all=True):
        pkglist = [pkgname]
        if test_all:
            pkglist.append('all')
        for pkg in pkglist:
            order = self.preferred.get(pkg, {}).get(component, {})
            if isinstance(order, dict) and second_key:
                order = order.get(second_key, {})
            if not order:
                continue
            return [str(s).strip() for s in order]
        return []

    # A generic sorting function. Given a package name and sort
    # component, return less-than-0, 0, or greater-than-0 if
    # a is respectively less-than, equal to, or greater than b.
    def _component_compare(self, pkgname, component, a, b,
                           reverse_natural_compare, second_key):
        if a is None:
            return -1
        if b is None:
            return 1
        orderlist = self._order_for_package(pkgname, component, second_key)
        a_in_list = str(a) in orderlist
        b_in_list = str(b) in orderlist
        if a_in_list and not b_in_list:
            return -1
        elif b_in_list and not a_in_list:
            return 1

        cmp_a = None
        cmp_b = None
        reverse = None
        if not a_in_list and not b_in_list:
            cmp_a = a
            cmp_b = b
            reverse = -1 if reverse_natural_compare else 1
        else:
            cmp_a = orderlist.index(str(a))
            cmp_b = orderlist.index(str(b))
            reverse = 1

        if cmp_a < cmp_b:
            return -1 * reverse
        elif cmp_a > cmp_b:
            return 1 * reverse
        else:
            return 0

    # A sorting function for specs.  Similar to component_compare, but
    # a and b are considered to match entries in the sorting list if they
    # satisfy the list component.
    def _spec_compare(self, pkgname, component, a, b,
                      reverse_natural_compare, second_key):
        if not a or (not a.concrete and not second_key):
            return -1
        if not b or (not b.concrete and not second_key):
            return 1
        specs = self._spec_for_pkgname(pkgname, component, second_key)
        a_index = None
        b_index = None
        reverse = -1 if reverse_natural_compare else 1
        for i, cspec in enumerate(specs):
            if a_index is None and (cspec.satisfies(a) or a.satisfies(cspec)):
                a_index = i
                if b_index:
                    break
            if b_index is None and (cspec.satisfies(b) or b.satisfies(cspec)):
                b_index = i
                if a_index:
                    break

        if a_index is not None and b_index is None:
            return -1
        elif a_index is None and b_index is not None:
            return 1
        elif a_index is not None and b_index == a_index:
            return -1 * cmp(a, b)
        elif (a_index is not None and b_index is not None and
              a_index != b_index):
            return cmp(a_index, b_index)
        else:
            return cmp(a, b) * reverse

    # Given a sort order specified by the pkgname/component/second_key, return
    # a list of CompilerSpecs, VersionLists, or Specs for that sorting list.
    def _spec_for_pkgname(self, pkgname, component, second_key):
        key = (pkgname, component, second_key)
        if key not in self._spec_for_pkgname_cache:
            pkglist = self._order_for_package(pkgname, component, second_key)
            if component == 'compiler':
                self._spec_for_pkgname_cache[key] = \
                    [spack.spec.CompilerSpec(s) for s in pkglist]
            elif component == 'version':
                self._spec_for_pkgname_cache[key] = \
                    [VersionList(s) for s in pkglist]
            else:
                self._spec_for_pkgname_cache[key] = \
                    [spack.spec.Spec(s) for s in pkglist]
        return self._spec_for_pkgname_cache[key]

    def provider_compare(self, pkgname, provider_str, a, b):
        """Return less-than-0, 0, or greater than 0 if a is respecively
           less-than, equal-to, or greater-than b. A and b are possible
           implementations of provider_str. One provider is less-than another
           if it is preferred over the other. For example,
           provider_compare('scorep', 'mpi', 'mvapich', 'openmpi') would
           return -1 if mvapich should be preferred over openmpi for scorep."""
        return self._spec_compare(pkgname, 'providers', a, b, False,
                                  provider_str)

    def spec_has_preferred_provider(self, pkgname, provider_str):
        """Return True iff the named package has a list of preferred
           providers"""
        return bool(self._order_for_package(pkgname, 'providers',
                                            provider_str, False))

    def spec_preferred_variants(self, pkgname):
        """Return a VariantMap of preferred variants and their values"""
        for pkg in (pkgname, 'all'):
            variants = self.preferred.get(pkg, {}).get('variants', '')
            if variants:
                break
        if not isinstance(variants, string_types):
            variants = " ".join(variants)
        pkg = spack.repo.get(pkgname)
        spec = spack.spec.Spec("%s %s" % (pkgname, variants))
        # Only return variants that are actually supported by the package
        return dict((name, variant) for name, variant in spec.variants.items()
                    if name in pkg.variants)

    def version_compare(self, pkgname, a, b):
        """Return less-than-0, 0, or greater than 0 if version a of pkgname is
           respectively less-than, equal-to, or greater-than version b of
           pkgname. One version is less-than another if it is preferred over
           the other."""
        return self._spec_compare(pkgname, 'version', a, b, True, None)

    def variant_compare(self, pkgname, a, b):
        """Return less-than-0, 0, or greater than 0 if variant a of pkgname is
           respectively less-than, equal-to, or greater-than variant b of
           pkgname. One variant is less-than another if it is preferred over
           the other."""
        return self._component_compare(pkgname, 'variant', a, b, False, None)

    def architecture_compare(self, pkgname, a, b):
        """Return less-than-0, 0, or greater than 0 if architecture a of pkgname
           is respectively less-than, equal-to, or greater-than architecture b
           of pkgname. One architecture is less-than another if it is preferred
           over the other."""
        return self._component_compare(pkgname, 'architecture', a, b,
                                       False, None)

    def compiler_compare(self, pkgname, a, b):
        """Return less-than-0, 0, or greater than 0 if compiler a of pkgname is
           respecively less-than, equal-to, or greater-than compiler b of
           pkgname. One compiler is less-than another if it is preferred over
           the other."""
        return self._spec_compare(pkgname, 'compiler', a, b, False, None)


def spec_externals(spec):
    """Return a list of external specs (with external directory path filled in),
       one for each known external installation."""
    # break circular import.
    from spack.build_environment import get_path_from_module

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

        external_spec = spack.spec.Spec(external_spec, external=path)
        if external_spec.satisfies(spec):
            external_specs.append(external_spec)

    for external_spec, module in iteritems(pkg_modules):
        if not module:
            continue

        path = get_path_from_module(module)

        external_spec = spack.spec.Spec(
            external_spec, external=path, external_module=module)
        if external_spec.satisfies(spec):
            external_specs.append(external_spec)

    return external_specs


def is_spec_buildable(spec):
    """Return true if the spec pkgspec is configured as buildable"""
    allpkgs = get_packages_config()
    if spec.name not in allpkgs:
        return True
    if 'buildable' not in allpkgs[spec.name]:
        return True
    return allpkgs[spec.name]['buildable']


def cmp_specs(lhs, rhs):
    # Package name sort order is not configurable, always goes alphabetical
    if lhs.name != rhs.name:
        return cmp(lhs.name, rhs.name)

    # Package version is second in compare order
    pkgname = lhs.name
    if lhs.versions != rhs.versions:
        return pkgsort().version_compare(
            pkgname, lhs.versions, rhs.versions)

    # Compiler is third
    if lhs.compiler != rhs.compiler:
        return pkgsort().compiler_compare(
            pkgname, lhs.compiler, rhs.compiler)

    # Variants
    if lhs.variants != rhs.variants:
        return pkgsort().variant_compare(
            pkgname, lhs.variants, rhs.variants)

    # Architecture
    if lhs.architecture != rhs.architecture:
        return pkgsort().architecture_compare(
            pkgname, lhs.architecture, rhs.architecture)

    # Dependency is not configurable
    lhash, rhash = hash(lhs), hash(rhs)
    if lhash != rhash:
        return -1 if lhash < rhash else 1

    # Equal specs
    return 0


_pkgsort = None


def pkgsort():
    global _pkgsort
    if _pkgsort is None:
        _pkgsort = PreferredPackages()
    return _pkgsort


class VirtualInPackagesYAMLError(spack.error.SpackError):
    """Raised when a disallowed virtual is found in packages.yaml"""
