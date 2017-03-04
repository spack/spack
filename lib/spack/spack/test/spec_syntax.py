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
import pytest
import shlex

import spack.spec as sp
from spack.parse import Token
from spack.spec import *

# Sample output for a complex lexing.
complex_lex = [Token(sp.ID, 'mvapich_foo'),
               Token(sp.DEP),
               Token(sp.ID, '_openmpi'),
               Token(sp.AT),
               Token(sp.ID, '1.2'),
               Token(sp.COLON),
               Token(sp.ID, '1.4'),
               Token(sp.COMMA),
               Token(sp.ID, '1.6'),
               Token(sp.PCT),
               Token(sp.ID, 'intel'),
               Token(sp.AT),
               Token(sp.ID, '12.1'),
               Token(sp.COLON),
               Token(sp.ID, '12.6'),
               Token(sp.ON),
               Token(sp.ID, 'debug'),
               Token(sp.OFF),
               Token(sp.ID, 'qt_4'),
               Token(sp.DEP),
               Token(sp.ID, 'stackwalker'),
               Token(sp.AT),
               Token(sp.ID, '8.1_1e')]

# Another sample lexer output with a kv pair.
kv_lex = [Token(sp.ID, 'mvapich_foo'),
          Token(sp.ID, 'debug'),
          Token(sp.EQ),
          Token(sp.VAL, '4'),
          Token(sp.DEP),
          Token(sp.ID, '_openmpi'),
          Token(sp.AT),
          Token(sp.ID, '1.2'),
          Token(sp.COLON),
          Token(sp.ID, '1.4'),
          Token(sp.COMMA),
          Token(sp.ID, '1.6'),
          Token(sp.PCT),
          Token(sp.ID, 'intel'),
          Token(sp.AT),
          Token(sp.ID, '12.1'),
          Token(sp.COLON),
          Token(sp.ID, '12.6'),
          Token(sp.ON),
          Token(sp.ID, 'debug'),
          Token(sp.OFF),
          Token(sp.ID, 'qt_4'),
          Token(sp.DEP),
          Token(sp.ID, 'stackwalker'),
          Token(sp.AT),
          Token(sp.ID, '8.1_1e')]


class TestSpecSyntax(object):
    # ========================================================================
    # Parse checks
    # ========================================================================

    def check_parse(self, expected, spec=None, remove_arch=True):
        """Assert that the provided spec is able to be parsed.

           If this is called with one argument, it assumes that the
           string is canonical (i.e., no spaces and ~ instead of - for
           variants) and that it will convert back to the string it came
           from.

           If this is called with two arguments, the first argument is
           the expected canonical form and the second is a non-canonical
           input to be parsed.

        """
        if spec is None:
            spec = expected
        output = sp.parse(spec)

        parsed = (" ".join(str(spec) for spec in output))
        assert expected == parsed

    def check_lex(self, tokens, spec):
        """Check that the provided spec parses to the provided token list."""
        spec = shlex.split(spec)
        lex_output = sp.SpecLexer().lex(spec)
        for tok, spec_tok in zip(tokens, lex_output):
            if tok.type == sp.ID or tok.type == sp.VAL:
                assert tok == spec_tok
            else:
                # Only check the type for non-identifiers.
                assert tok.type == spec_tok.type

    def _check_raises(self, exc_type, items):
        for item in items:
            with pytest.raises(exc_type):
                self.check_parse(item)

    # ========================================================================
    # Parse checks
    # ========================================================================
    def test_package_names(self):
        self.check_parse("mvapich")
        self.check_parse("mvapich_foo")
        self.check_parse("_mvapich_foo")

    def test_anonymous_specs(self):
        self.check_parse("%intel")
        self.check_parse("@2.7")
        self.check_parse("^zlib")
        self.check_parse("+foo")
        self.check_parse("arch=test-None-None", "platform=test")

    def test_simple_dependence(self):
        self.check_parse("openmpi^hwloc")
        self.check_parse("openmpi^hwloc^libunwind")

    def test_dependencies_with_versions(self):
        self.check_parse("openmpi^hwloc@1.2e6")
        self.check_parse("openmpi^hwloc@1.2e6:")
        self.check_parse("openmpi^hwloc@:1.4b7-rc3")
        self.check_parse("openmpi^hwloc@1.2e6:1.4b7-rc3")

    def test_multiple_specs(self):
        self.check_parse("mvapich emacs")

    def test_multiple_specs_after_kv(self):
        self.check_parse('mvapich cppflags="-O3 -fPIC" emacs')
        self.check_parse('mvapich cflags="-O3" emacs',
                         'mvapich cflags=-O3 emacs')

    def test_multiple_specs_long_second(self):
        self.check_parse('mvapich emacs@1.1.1%intel cflags="-O3"',
                         'mvapich emacs @1.1.1 %intel cflags=-O3')
        self.check_parse('mvapich cflags="-O3 -fPIC" emacs^ncurses%intel')

    def test_full_specs(self):
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1+debug~qt_4"
            "^stackwalker@8.1_1e")
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1 debug=2 ~qt_4"
            "^stackwalker@8.1_1e")
        self.check_parse(
            'mvapich_foo'
            '^_openmpi@1.2:1.4,1.6%intel@12.1 cppflags="-O3" +debug~qt_4'
            '^stackwalker@8.1_1e')
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1 debug=2 ~qt_4"
            "^stackwalker@8.1_1e arch=test-redhat6-x86_32")

    def test_canonicalize(self):
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4"
            "^stackwalker@8.1_1e",

            "mvapich_foo "
            "^_openmpi@1.6,1.2:1.4%intel@12.1:12.6+debug~qt_4 "
            "^stackwalker@8.1_1e")

        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4"
            "^stackwalker@8.1_1e",

            "mvapich_foo "
            "^stackwalker@8.1_1e "
            "^_openmpi@1.6,1.2:1.4%intel@12.1:12.6~qt_4+debug")

        self.check_parse(
            "x^y@1,2:3,4%intel@1,2,3,4+a~b+c~d+e~f",
            "x ^y~f+e~d+c~b+a@4,2:3,1%intel@4,3,2,1")

        self.check_parse(
            "x arch=test-redhat6-None "
            "^y arch=test-None-x86_64 "
            "^z arch=linux-None-None",

            "x os=fe "
            "^y target=be "
            "^z platform=linux")

        self.check_parse(
            "x arch=test-debian6-x86_64 "
            "^y arch=test-debian6-x86_64",

            "x os=default_os target=default_target "
            "^y os=default_os target=default_target")

        self.check_parse("x^y", "x@: ^y@:")

    def test_parse_errors(self):
        errors = ['x@@1.2', 'x ^y@@1.2', 'x@1.2::', 'x::']
        self._check_raises(SpecParseError, errors)

    def test_spec_by_hash(self, database):
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        # Make sure the database is still the shape we expect
        assert len(specs) > 3

        self.check_parse(str(specs[0]), '/' + hashes[0])
        self.check_parse(str(specs[1]), '/ ' + hashes[1][:5])
        self.check_parse(str(specs[2]), specs[2].name + '/' + hashes[2])
        self.check_parse(str(specs[3]),
                         specs[3].name + '@' + str(specs[3].version) +
                         ' /' + hashes[3][:6])

    def test_dep_spec_by_hash(self, database):
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        # Make sure the database is still the shape we expect
        assert len(specs) > 10
        assert specs[4].name in specs[10]
        assert specs[-1].name in specs[10]

        spec1 = sp.Spec(specs[10].name + '^/' + hashes[4])
        assert specs[4].name in spec1 and spec1[specs[4].name] == specs[4]
        spec2 = sp.Spec(specs[10].name + '%' + str(specs[10].compiler) +
                        ' ^ / ' + hashes[-1])
        assert (specs[-1].name in spec2 and
                spec2[specs[-1].name] == specs[-1] and
                spec2.compiler == specs[10].compiler)
        spec3 = sp.Spec(specs[10].name + '^/' + hashes[4][:4] +
                        '^ / ' + hashes[-1][:5])
        assert (specs[-1].name in spec3 and
                spec3[specs[-1].name] == specs[-1] and
                specs[4].name in spec3 and spec3[specs[4].name] == specs[4])

    def test_multiple_specs_with_hash(self, database):
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        assert len(specs) > 3

        output = sp.parse(specs[0].name + '/' + hashes[0] + '/' + hashes[1])
        assert len(output) == 2
        output = sp.parse('/' + hashes[0] + '/' + hashes[1])
        assert len(output) == 2
        output = sp.parse('/' + hashes[0] + '/' + hashes[1] +
                          ' ' + specs[2].name)
        assert len(output) == 3
        output = sp.parse('/' + hashes[0] +
                          ' ' + specs[1].name + ' ' + specs[2].name)
        assert len(output) == 3
        output = sp.parse('/' + hashes[0] + ' ' +
                          specs[1].name + ' / ' + hashes[1])
        assert len(output) == 2

    def test_ambiguous_hash(self, database):
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        # Make sure the database is as expected
        assert hashes[1][:1] == hashes[2][:1] == 'b'

        ambiguous_hashes = ['/b',
                            specs[1].name + '/b',
                            specs[0].name + '^/b',
                            specs[0].name + '^' + specs[1].name + '/b']
        self._check_raises(AmbiguousHashError, ambiguous_hashes)

    def test_invalid_hash(self, database):
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        # Make sure the database is as expected
        assert (hashes[0] != hashes[3] and
                hashes[1] != hashes[4] and len(specs) > 4)

        inputs = [specs[0].name + '/' + hashes[3],
                  specs[1].name + '^' + specs[4].name + '/' + hashes[0],
                  specs[1].name + '^' + specs[4].name + '/' + hashes[1]]
        self._check_raises(InvalidHashError, inputs)

    def test_nonexistent_hash(self, database):
        # This test uses database to make sure we don't accidentally access
        # real installs, however unlikely
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        # Make sure the database is as expected
        assert 'abc123' not in [h[:6] for h in hashes]

        nonexistant_hashes = ['/abc123',
                              specs[0].name + '/abc123']
        self._check_raises(SystemExit, nonexistant_hashes)

    def test_redundant_spec(self, database):
        specs = database.mock.db.query()
        hashes = [s._hash for s in specs]  # Preserves order of elements

        # Make sure the database is as expected
        assert len(specs) > 3

        redundant_specs = ['/' + hashes[0] + '%' + str(specs[0].compiler),
                           specs[1].name + '/' + hashes[1] +
                           '@' + str(specs[1].version),
                           specs[2].name + '/' + hashes[2] + '^ libelf',
                           '/' + hashes[3] + ' cflags="-O3 -fPIC"']
        self._check_raises(RedundantSpecError, redundant_specs)

    def test_duplicate_variant(self):
        duplicates = [
            'x@1.2+debug+debug',
            'x ^y@1.2+debug debug=true',
            'x ^y@1.2 debug=false debug=true',
            'x ^y@1.2 debug=false ~debug'
        ]
        self._check_raises(DuplicateVariantError, duplicates)

    def test_duplicate_dependency(self):
        self._check_raises(DuplicateDependencyError, ["x ^y ^y"])

    def test_duplicate_compiler(self):
        duplicates = [
            "x%intel%intel",
            "x%intel%gcc",
            "x%gcc%intel",
            "x ^y%intel%intel",
            "x ^y%intel%gcc",
            "x ^y%gcc%intel"
        ]
        self._check_raises(DuplicateCompilerSpecError, duplicates)

    def test_duplicate_architecture(self):
        duplicates = [
            "x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64",
            "x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le",
            "x arch=linux-rhel7-ppc64le arch=linux-rhel7-x86_64",
            "y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64",
            "y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le"
        ]
        self._check_raises(DuplicateArchitectureError, duplicates)

    def test_duplicate_architecture_component(self):
        duplicates = [
            "x os=fe os=fe",
            "x os=fe os=be",
            "x target=fe target=fe",
            "x target=fe target=be",
            "x platform=test platform=test",
            "x os=fe platform=test target=fe os=fe",
            "x target=be platform=test os=be os=fe"
        ]
        self._check_raises(DuplicateArchitectureError, duplicates)

    # ========================================================================
    # Lex checks
    # ========================================================================
    def test_ambiguous(self):
        # This first one is ambiguous because - can be in an identifier AND
        # indicate disabling an option.
        with pytest.raises(AssertionError):
            self.check_lex(
                complex_lex,
                "mvapich_foo"
                "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug-qt_4"
                "^stackwalker@8.1_1e"
            )

    # The following lexes are non-ambiguous (add a space before -qt_4)
    # and should all result in the tokens in complex_lex
    def test_minimal_spaces(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug -qt_4"
            "^stackwalker@8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4"
            "^stackwalker@8.1_1e")

    def test_spaces_between_dependences(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug -qt_4 "
            "^stackwalker @ 8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4 "
            "^stackwalker @ 8.1_1e")

    def test_spaces_between_options(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^_openmpi @1.2:1.4,1.6 %intel @12.1:12.6 +debug -qt_4 "
            "^stackwalker @8.1_1e")

    def test_way_too_many_spaces(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug ~ qt_4 "
            "^ stackwalker @ 8.1_1e")

    def test_kv_with_quotes(self):
        self.check_lex(
            kv_lex,
            "mvapich_foo debug='4' "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            'mvapich_foo debug="4" '
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            "mvapich_foo 'debug = 4' "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")

    def test_kv_without_quotes(self):
        self.check_lex(
            kv_lex,
            "mvapich_foo debug=4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")

    def test_kv_with_spaces(self):
        self.check_lex(
            kv_lex,
            "mvapich_foo debug = 4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            "mvapich_foo debug =4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            "mvapich_foo debug= 4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
