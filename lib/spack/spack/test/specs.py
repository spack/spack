import unittest
from spack.spec import *
from spack.parse import *

# Sample output for a complex lexing.
complex_lex = [Token(ID, 'mvapich_foo'),
               Token(DEP),
               Token(ID, '_openmpi'),
               Token(AT),
               Token(ID, '1.2'),
               Token(COLON),
               Token(ID, '1.4'),
               Token(COMMA),
               Token(ID, '1.6'),
               Token(PCT),
               Token(ID, 'intel'),
               Token(AT),
               Token(ID, '12.1'),
               Token(COLON),
               Token(ID, '12.6'),
               Token(ON),
               Token(ID, 'debug'),
               Token(OFF),
               Token(ID, 'qt_4'),
               Token(DEP),
               Token(ID, 'stackwalker'),
               Token(AT),
               Token(ID, '8.1_1e')]


class SpecTest(unittest.TestCase):
    def setUp(self):
        self.parser = SpecParser()
        self.lexer = SpecLexer()

    # ================================================================================
    # Parse checks
    # ================================================================================
    def check_parse(self, expected, spec=None):
        """Assert that the provided spec is able to be parsed.
           If this is called with one argument, it assumes that the string is
           canonical (i.e., no spaces and ~ instead of - for variants) and that it
           will convert back to the string it came from.

           If this is called with two arguments, the first argument is the expected
           canonical form and the second is a non-canonical input to be parsed.
        """
        if spec == None:
            spec = expected
        output = self.parser.parse(spec)
        self.assertEqual(len(output), 1)
        self.assertEqual(str(output[0]), spec)


    def check_lex(self, tokens, spec):
        """Check that the provided spec parses to the provided list of tokens."""
        lex_output = self.lexer.lex(spec)
        for tok, spec_tok in zip(tokens, lex_output):
            if tok.type == ID:
                self.assertEqual(tok, spec_tok)
            else:
                # Only check the type for non-identifiers.
                self.assertEqual(tok.type, spec_tok.type)

    # ================================================================================
    # Parse checks
    # ===============================================================================
    def test_package_names(self):
        self.check_parse("mvapich")
        self.check_parse("mvapich_foo")
        self.check_parse("_mvapich_foo")

    def test_simple_dependence(self):
        self.check_parse("openmpi ^hwloc")
        self.check_parse("openmpi ^hwloc ^libunwind")

    def test_dependencies_with_versions(self):
        self.check_parse("openmpi ^hwloc@1.2e6")
        self.check_parse("openmpi ^hwloc@1.2e6:")
        self.check_parse("openmpi ^hwloc@:1.4b7-rc3")
        self.check_parse("openmpi ^hwloc@1.2e6:1.4b7-rc3")

    def test_full_specs(self):
        self.check_parse("mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1+debug~qt_4 ^stackwalker@8.1_1e")

    def test_canonicalize(self):
        self.check_parse(
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4 ^stackwalker@8.1_1e")

    # ================================================================================
    # Lex checks
    # ================================================================================
    def test_ambiguous(self):
        # This first one is ambiguous because - can be in an identifier AND
        # indicate disabling an option.
        self.assertRaises(
            AssertionError, self.check_lex, complex_lex,
            "mvapich_foo^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug-qt_4^stackwalker@8.1_1e")

    # The following lexes are non-ambiguous (add a space before -qt_4) and should all
    # result in the tokens in complex_lex
    def test_minimal_spaces(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug -qt_4^stackwalker@8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4^stackwalker@8.1_1e")

    def test_spaces_between_dependences(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug -qt_4 ^stackwalker @ 8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4 ^stackwalker @ 8.1_1e")

    def test_spaces_between_options(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo ^_openmpi @1.2:1.4,1.6 %intel @12.1:12.6 +debug -qt_4 ^stackwalker @8.1_1e")

    def test_way_too_many_spaces(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo ^ _openmpi @ 1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 ^ stackwalker @ 8.1_1e")
