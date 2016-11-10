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
import unittest

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


class SpecSyntaxTest(unittest.TestCase):
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
        self.assertEqual(expected, parsed)

    def check_lex(self, tokens, spec):
        """Check that the provided spec parses to the provided token list."""
        lex_output = sp.SpecLexer().lex(spec)
        for tok, spec_tok in zip(tokens, lex_output):
            if tok.type == sp.ID:
                self.assertEqual(tok, spec_tok)
            else:
                # Only check the type for non-identifiers.
                self.assertEqual(tok.type, spec_tok.type)

    # ========================================================================
    # Parse checks
    # ========================================================================
    def test_package_names(self):
        self.check_parse("mvapich")
        self.check_parse("mvapich_foo")
        self.check_parse("_mvapich_foo")

    def test_simple_dependence(self):
        self.check_parse("openmpi^hwloc")
        self.check_parse("openmpi^hwloc^libunwind")

    def test_dependencies_with_versions(self):
        self.check_parse("openmpi^hwloc@1.2e6")
        self.check_parse("openmpi^hwloc@1.2e6:")
        self.check_parse("openmpi^hwloc@:1.4b7-rc3")
        self.check_parse("openmpi^hwloc@1.2e6:1.4b7-rc3")

    def test_full_specs(self):
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1+debug~qt_4"
            "^stackwalker@8.1_1e")
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1 debug=2~qt_4"
            "^stackwalker@8.1_1e")
        self.check_parse(
            'mvapich_foo'
            '^_openmpi@1.2:1.4,1.6%intel@12.1 cppflags="-O3"+debug~qt_4'
            '^stackwalker@8.1_1e')
        self.check_parse(
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1 debug=2~qt_4"
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
            "x arch=test-redhat6-None"
            "^y arch=test-None-x86_64"
            "^z arch=linux-None-None",

            "x os=fe"
            "^y target=be"
            "^z platform=linux")

        self.check_parse(
            "x arch=test-debian6-x86_64"
            "^y arch=test-debian6-x86_64",

            "x os=default_os target=default_target"
            "^y os=default_os target=default_target")

        self.check_parse("x^y", "x@: ^y@:")

    def test_parse_errors(self):
        self.assertRaises(SpecParseError, self.check_parse, "x@@1.2")
        self.assertRaises(SpecParseError, self.check_parse, "x ^y@@1.2")
        self.assertRaises(SpecParseError, self.check_parse, "x@1.2::")
        self.assertRaises(SpecParseError, self.check_parse, "x::")

    def test_duplicate_variant(self):
        self.assertRaises(DuplicateVariantError,
                          self.check_parse, "x@1.2+debug+debug")
        self.assertRaises(DuplicateVariantError,
                          self.check_parse, "x ^y@1.2+debug debug=true")
        self.assertRaises(DuplicateVariantError, self.check_parse,
                          "x ^y@1.2 debug=false debug=true")
        self.assertRaises(DuplicateVariantError,
                          self.check_parse, "x ^y@1.2 debug=false~debug")

    def test_duplicate_depdendence(self):
        self.assertRaises(DuplicateDependencyError,
                          self.check_parse, "x ^y ^y")

    def test_duplicate_compiler(self):
        self.assertRaises(DuplicateCompilerSpecError,
                          self.check_parse, "x%intel%intel")

        self.assertRaises(DuplicateCompilerSpecError,
                          self.check_parse, "x%intel%gcc")
        self.assertRaises(DuplicateCompilerSpecError,
                          self.check_parse, "x%gcc%intel")

        self.assertRaises(DuplicateCompilerSpecError,
                          self.check_parse, "x ^y%intel%intel")
        self.assertRaises(DuplicateCompilerSpecError,
                          self.check_parse, "x ^y%intel%gcc")
        self.assertRaises(DuplicateCompilerSpecError,
                          self.check_parse, "x ^y%gcc%intel")

    def test_duplicate_architecture(self):
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64")

        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le")
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x arch=linux-rhel7-ppc64le arch=linux-rhel7-x86_64")

        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64")
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le")

    def test_duplicate_architecture_component(self):
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x os=fe os=fe")
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x os=fe os=be")

        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x target=fe target=fe")
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x target=fe target=be")

        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x platform=test platform=test")
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x platform=test platform=test")

        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x os=fe platform=test target=fe os=fe")
        self.assertRaises(
            DuplicateArchitectureError, self.check_parse,
            "x target=be platform=test os=be os=fe")

    # ========================================================================
    # Lex checks
    # ========================================================================
    def test_ambiguous(self):
        # This first one is ambiguous because - can be in an identifier AND
        # indicate disabling an option.
        self.assertRaises(
            AssertionError, self.check_lex, complex_lex,
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug-qt_4"
            "^stackwalker@8.1_1e")

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
