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

import spack
from spack.version import *


class PreferredPackages(object):
    def __init__(self):
        self.preferred = spack.config.get_config('packages')
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
        variants = self.preferred.get(pkgname, {}).get('variants', '')
        if not isinstance(variants, basestring):
            variants = " ".join(variants)
        return spack.spec.Spec("%s %s" % (pkgname, variants)).variants

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
