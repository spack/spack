##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
The ``virtual`` module contains utility classes for virtual dependencies.
"""
import spack.spec

class ProviderIndex(object):
    """This is a dict of dicts used for finding providers of particular
       virtual dependencies. The dict of dicts looks like:

       { vpkg name :
           { full vpkg spec : package providing spec } }

       Callers can use this to first find which packages provide a vpkg,
       then find a matching full spec.  e.g., in this scenario:

       { 'mpi' :
           { mpi@:1.1 : mpich,
             mpi@:2.3 : mpich2@1.9: } }

       Calling providers_for(spec) will find specs that provide a
       matching implementation of MPI.
    """
    def __init__(self, specs, **kwargs):
        # TODO: come up with another name for this.  This "restricts" values to
        # the verbatim impu specs (i.e., it doesn't pre-apply package's constraints, and
        # keeps things as broad as possible, so it's really the wrong name)
        self.restrict = kwargs.setdefault('restrict', False)

        self.providers = {}

        for spec in specs:
            if not isinstance(spec, spack.spec.Spec):
                spec = spack.spec.Spec(spec)

            if spec.virtual:
                continue

            self.update(spec)


    def update(self, spec):
        if type(spec) != spack.spec.Spec:
            spec = spack.spec.Spec(spec)

        assert(not spec.virtual)

        pkg = spec.package
        for provided_spec, provider_spec in pkg.provided.iteritems():
            if provider_spec.satisfies(spec, deps=False):
                provided_name = provided_spec.name
                if provided_name not in self.providers:
                    self.providers[provided_name] = {}

                if self.restrict:
                    self.providers[provided_name][provided_spec] = spec

                else:
                    # Before putting the spec in the map, constrain it so that
                    # it provides what was asked for.
                    constrained = spec.copy()
                    constrained.constrain(provider_spec)
                    self.providers[provided_name][provided_spec] = constrained


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
                for provider_spec, spec in self.providers[vspec.name].items():
                    if provider_spec.satisfies(vspec, deps=False):
                        providers.add(spec)

        # Return providers in order
        return sorted(providers)


    # TODO: this is pretty darned nasty, and inefficient.
    def _cross_provider_maps(self, lmap, rmap):
        result = {}
        for lspec in lmap:
            for rspec in rmap:
                try:
                    constrained = lspec.copy().constrain(rspec)
                    if lmap[lspec].name != rmap[rspec].name:
                        continue
                    result[constrained] = lmap[lspec].copy().constrain(
                        rmap[rspec], deps=False)
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

        result = {}
        for name in common:
            crossed = self._cross_provider_maps(self.providers[name],
                                                other.providers[name])
            if crossed:
                result[name] = crossed

        return bool(result)
