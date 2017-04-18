##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import itertools

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack
import spack.compilers
import spack.architecture as sarch
import spack.schema as schema
import spack.util.spack_yaml as syaml

from spack.spec import Spec, ArchSpec


class CombinatorialSpecSet:
    """Set of combinatorial Specs constructed from YAML file."""

    def __init__(self, yaml_like, ignore_invalid=True):
        """Construct a combinatorial Spec set.

        Args:
            yaml_like: either raw YAML data as a dict, a file-like object
                to read the YAML from, or a string containing YAML.  * A
                file-like object to read YAML from. In the first case, we
                assume already-parsed YAML data.  In the second two
                cases, we just run yaml.load() on the data.
            ignore_invalid (bool): whether to ignore invalid specs when
                expanding the values of this spec set.
        """
        self.ignore_invalid = ignore_invalid

        if isinstance(yaml_like, dict):
            # if it's raw data, just assign it to self.data
            self.data = yaml_like
        else:
            # otherwise try to load it.
            self.data = syaml.load(yaml_like)

        # validate against the test suite schema
        schema.validate(self.data, schema.test_suite.schema)

        # chop off the initial test-suite label after valiation.
        self.data = self.data['test-suite']

        # initialize these from data.
        self.cdash = self.data.get('cdash', None)
        if isinstance(self.cdash, str):
            self.cdash = [self.cdash]
        self.project = self.data.get('project', None)

        # _spec_lists is a list of lists of specs, to be combined as a
        # cartesian product when we iterate over all specs in the set.
        # it's initialized lazily.
        self._spec_lists = None
        self._include = []
        self._exclude = []

    def all_package_versions(self):
        """Get package/version combinations for all spack packages."""
        for name in spack.repo.all_package_names():
            pkg = spack.repo.get(name)
            for v in pkg.versions:
                yield Spec('{0}@{1}'.format(name, v))

    def _specs(self, data):
        """Read a list of specs from YAML data"""
        return [Spec(s) for s in data]

    def _compiler_specs(self, data):
        """Read compiler specs from YAML data.
        Example YAML:
            gcc:
                versions: [4.4.8, 4.9.3]
            clang:
                versions: [3.6.1, 3.7.2, 3.8]

        Optionally, data can be 'all', in which case all compilers for
        the current platform are returned.
        """
        # get usable compilers for current platform.
        arch = ArchSpec(str(sarch.platform()), 'default_os', 'default_target')
        available_compilers = [
            c.spec for c in spack.compilers.compilers_for_arch(arch)]

        # return compilers for this platform if asked for everything.
        if data == 'all':
            return [Spec("%" + str(cspec.copy()))
                    for cspec in available_compilers]

        # otherwise create specs from the YAML file.
        cspecs = set([
            Spec('%{0}@{1}'.format(compiler, version))
            for compiler in data for version in data[compiler]['versions']])

        # filter out invalid specs if caller said to ignore them.
        if self.ignore_invalid:
            missing = [c for c in cspecs if not any(
                c.compiler.satisfies(comp) for comp in available_compilers)]
            tty.warn("The following compilers were unavailable:")
            colify(sorted(m.compiler for m in missing))
            cspecs -= set(missing)

        return cspecs

    def _package_specs(self, data):
        """Read package/version specs from YAML data.
        Example YAML:
            gmake:
                versions: [4.0, 4.1, 4.2]
            qt:
                versions: [4.8.6, 5.2.1, 5.7.1]

        Optionally, data can be 'all', in which case all packages and
        versions from the package repository are returned.
        """
        if data == 'all':
            return set(self.all_package_versions())

        return set([
            Spec('{0}@{1}'.format(name, version))
            for name in data for version in data[name]['versions']])

    def _get_specs(self, matrix_dict):
        """Parse specs out of an element in the build matrix."""
        readers = {
            'packages': self._package_specs,
            'compilers': self._compiler_specs,
            'specs': self._specs
        }
        
        key = next(iter(matrix_dict), None)
        assert key in readers
        return readers[key](matrix_dict[key])

    def __iter__(self):
        # read in data from YAML file lazily.
        if self._spec_lists is None:
            self._spec_lists = [self._get_specs(spec_list)
                                for spec_list in self.data['matrix']]

            if 'include' in self.data:
                self._include = [Spec(s) for s in self.data['include']]
            if 'exclude' in self.data:
                self._exclude = [Spec(s) for s in self.data['exclude']]

        for spec_list in itertools.product(*self._spec_lists):
            # if there is an empty array in spec_lists, we'll get this.
            if not spec_list:
                yield spec_list
                continue

            # merge all the constraints in spec_list with each other
            spec = spec_list[0].copy()
            for s in spec_list[1:]:
                spec.constrain(s)

            # test each spec for include/exclude
            if (self._include and
                    not any(spec.satisfies(s) for s in self._include)):
                continue

            if any(spec.satisfies(s) for s in self._exclude):
                continue

            # we now know we can include this spec in the set
            yield spec
