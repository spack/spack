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
"""
The ``virtual`` module contains utility classes for virtual dependencies.
"""
from itertools import product as iproduct
from six import iteritems
from pprint import pformat

import spack.util.spack_yaml as syaml
from yaml.error import MarkedYAMLError

import spack
import spack.error


class ProviderIndex(object):
    """This is a dict of dicts used for finding providers of particular
       virtual dependencies. The dict of dicts looks like:

       { vpkg name :
           { full vpkg spec : set(packages providing spec) } }

       Callers can use this to first find which packages provide a vpkg,
       then find a matching full spec.  e.g., in this scenario:

       { 'mpi' :
           { mpi@:1.1 : set([mpich]),
             mpi@:2.3 : set([mpich2@1.9:]) } }

       Calling providers_for(spec) will find specs that provide a
       matching implementation of MPI.

    """

    def __init__(self, specs=None, restrict=False):
        """Create a new ProviderIndex.

        Optional arguments:

        specs
            List (or sequence) of specs.  If provided, will call
            `update` on this ProviderIndex with each spec in the list.

        restrict
            "restricts" values to the verbatim input specs; do not
            pre-apply package's constraints.

            TODO: rename this.  It is intended to keep things as broad
            as possible without overly restricting results, so it is
            not the best name.
        """
        if specs is None:
            specs = []

        self.restrict = restrict
        self.providers = {}

        for spec in specs:
            if not isinstance(spec, spack.spec.Spec):
                spec = spack.spec.Spec(spec)

            if spec.virtual:
                continue

            self.update(spec)

    def update(self, spec):
        if not isinstance(spec, spack.spec.Spec):
            spec = spack.spec.Spec(spec)

        if not spec.name:
            # Empty specs do not have a package
            return

        assert(not spec.virtual)

        pkg = spec.package
        for provided_spec, provider_specs in iteritems(pkg.provided):
            for provider_spec in provider_specs:
                # TODO: fix this comment.
                # We want satisfaction other than flags
                provider_spec.compiler_flags = spec.compiler_flags.copy()

                if spec.satisfies(provider_spec, deps=False):
                    provided_name = provided_spec.name

                    provider_map = self.providers.setdefault(provided_name, {})
                    if provided_spec not in provider_map:
                        provider_map[provided_spec] = set()

                    if self.restrict:
                        provider_set = provider_map[provided_spec]

                        # If this package existed in the index before,
                        # need to take the old versions out, as they're
                        # now more constrained.
                        old = set(
                            [s for s in provider_set if s.name == spec.name])
                        provider_set.difference_update(old)

                        # Now add the new version.
                        provider_set.add(spec)

                    else:
                        # Before putting the spec in the map, constrain
                        # it so that it provides what was asked for.
                        constrained = spec.copy()
                        constrained.constrain(provider_spec)
                        provider_map[provided_spec].add(constrained)

    def providers_for(self, *vpkg_specs):
        """Gives specs of all packages that provide virtual packages
           with the supplied specs."""
        providers = set()
        for vspec in vpkg_specs:
            # Allow string names to be passed as input, as well as specs
            if type(vspec) == str:
                vspec = spack.spec.Spec(vspec)

            # Add all the providers that satisfy the vpkg spec.
            if vspec.name in self.providers:
                for p_spec, spec_set in self.providers[vspec.name].items():
                    if p_spec.satisfies(vspec, deps=False):
                        providers.update(spec_set)

        # Return providers in order
        return sorted(providers)

    # TODO: this is pretty darned nasty, and inefficient, but there
    # are not that many vdeps in most specs.
    def _cross_provider_maps(self, lmap, rmap):
        result = {}
        for lspec, rspec in iproduct(lmap, rmap):
            try:
                constrained = lspec.constrained(rspec)
            except spack.spec.UnsatisfiableSpecError:
                continue

            # lp and rp are left and right provider specs.
            for lp_spec, rp_spec in iproduct(lmap[lspec], rmap[rspec]):
                if lp_spec.name == rp_spec.name:
                    try:
                        const = lp_spec.constrained(rp_spec, deps=False)
                        result.setdefault(constrained, set()).add(const)
                    except spack.spec.UnsatisfiableSpecError:
                        continue
        return result

    def __contains__(self, name):
        """Whether a particular vpkg name is in the index."""
        return name in self.providers

    def satisfies(self, other):
        """Check that providers of virtual specs are compatible."""
        common = set(self.providers) & set(other.providers)
        if not common:
            return True

        # This ensures that some provider in other COULD satisfy the
        # vpkg constraints on self.
        result = {}
        for name in common:
            crossed = self._cross_provider_maps(self.providers[name],
                                                other.providers[name])
            if crossed:
                result[name] = crossed

        return all(c in result for c in common)

    def to_yaml(self, stream=None):
        provider_list = self._transform(
            lambda vpkg, pset: [
                vpkg.to_node_dict(), [p.to_node_dict() for p in pset]], list)

        syaml.dump({'provider_index': {'providers': provider_list}},
                   stream=stream)

    @staticmethod
    def from_yaml(stream):
        try:
            yfile = syaml.load(stream)
        except MarkedYAMLError as e:
            raise spack.spec.SpackYAMLError(
                "error parsing YAML ProviderIndex cache:", str(e))

        if not isinstance(yfile, dict):
            raise ProviderIndexError("YAML ProviderIndex was not a dict.")

        if 'provider_index' not in yfile:
            raise ProviderIndexError(
                "YAML ProviderIndex does not start with 'provider_index'")

        index = ProviderIndex()
        providers = yfile['provider_index']['providers']
        index.providers = _transform(
            providers,
            lambda vpkg, plist: (
                spack.spec.Spec.from_node_dict(vpkg),
                set(spack.spec.Spec.from_node_dict(p) for p in plist)))
        return index

    def merge(self, other):
        """Merge `other` ProviderIndex into this one."""
        other = other.copy()   # defensive copy.

        for pkg in other.providers:
            if pkg not in self.providers:
                self.providers[pkg] = other.providers[pkg]
                continue

            spdict, opdict = self.providers[pkg], other.providers[pkg]
            for provided_spec in opdict:
                if provided_spec not in spdict:
                    spdict[provided_spec] = opdict[provided_spec]
                    continue

                spdict[provided_spec] = \
                    spdict[provided_spec].union(opdict[provided_spec])

    def remove_provider(self, pkg_name):
        """Remove a provider from the ProviderIndex."""
        empty_pkg_dict = []
        for pkg, pkg_dict in self.providers.items():
            empty_pset = []
            for provided, pset in pkg_dict.items():
                same_name = set(p for p in pset if p.fullname == pkg_name)
                pset.difference_update(same_name)

                if not pset:
                    empty_pset.append(provided)

            for provided in empty_pset:
                del pkg_dict[provided]

            if not pkg_dict:
                empty_pkg_dict.append(pkg)

        for pkg in empty_pkg_dict:
            del self.providers[pkg]

    def copy(self):
        """Deep copy of this ProviderIndex."""
        clone = ProviderIndex()
        clone.providers = self._transform(
            lambda vpkg, pset: (vpkg, set((p.copy() for p in pset))))
        return clone

    def __eq__(self, other):
        return self.providers == other.providers

    def _transform(self, transform_fun, out_mapping_type=dict):
        return _transform(self.providers, transform_fun, out_mapping_type)

    def __str__(self):
        return pformat(
            _transform(self.providers,
                       lambda k, v: (k, list(v))))


def _transform(providers, transform_fun, out_mapping_type=dict):
    """Syntactic sugar for transforming a providers dict.

    transform_fun takes a (vpkg, pset) mapping and runs it on each
    pair in nested dicts.

    """
    def mapiter(mappings):
        if isinstance(mappings, dict):
            return iteritems(mappings)
        else:
            return iter(mappings)

    return dict(
        (name, out_mapping_type([
            transform_fun(vpkg, pset) for vpkg, pset in mapiter(mappings)]))
        for name, mappings in providers.items())


class ProviderIndexError(spack.error.SpackError):
    """Raised when there is a problem with a ProviderIndex."""
