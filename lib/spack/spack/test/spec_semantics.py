# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.directives
import spack.error
from spack.error import SpecError, UnsatisfiableSpecError
from spack.spec import (
    ArchSpec,
    CompilerSpec,
    Spec,
    SpecFormatSigilError,
    SpecFormatStringError,
    UnsupportedCompilerError,
)
from spack.variant import (
    InvalidVariantValueError,
    MultipleValuesInExclusiveVariantError,
    UnknownVariantError,
)


@pytest.mark.usefixtures("config", "mock_packages")
class TestSpecSemantics(object):
    """Test satisfies(), intersects(), constrain() and other semantic operations on specs."""

    @pytest.mark.parametrize(
        "lhs,rhs,expected",
        [
            ("libelf@0.8.13", "@0:1", "libelf@0.8.13"),
            ("libdwarf^libelf@0.8.13", "^libelf@0:1", "libdwarf^libelf@0.8.13"),
            ("libelf", Spec(), "libelf"),
            ("libdwarf", Spec(), "libdwarf"),
            ("%intel", Spec(), "%intel"),
            ("^mpi", Spec(), "^mpi"),
            ("+debug", Spec(), "+debug"),
            ("@3:", Spec(), "@3:"),
            # Versions
            ("libelf@0:2.5", "libelf@2.1:3", "libelf@2.1:2.5"),
            ("libelf@0:2.5%gcc@2:4.6", "libelf@2.1:3%gcc@4.5:4.7", "libelf@2.1:2.5%gcc@4.5:4.6"),
            # Namespaces
            ("builtin.mpich", "mpich", "builtin.mpich"),
            ("builtin.mock.mpich", "mpich", "builtin.mock.mpich"),
            ("builtin.mpich", "builtin.mpich", "builtin.mpich"),
            ("mpileaks ^builtin.mock.mpich", "^mpich", "mpileaks ^builtin.mock.mpich"),
            # Virtual dependencies are fully resolved during concretization, so we can constrain
            # abstract specs but that would result in a new node
            ("mpileaks ^builtin.mock.mpich", "^mpi", "mpileaks ^mpi ^builtin.mock.mpich"),
            (
                "mpileaks ^builtin.mock.mpich",
                "^builtin.mock.mpich",
                "mpileaks ^builtin.mock.mpich",
            ),
            # Compilers
            ("foo%gcc", "%gcc", "foo%gcc"),
            ("foo%intel", "%intel", "foo%intel"),
            ("foo%gcc", "%gcc@4.7.2", "foo%gcc@4.7.2"),
            ("foo%intel", "%intel@4.7.2", "foo%intel@4.7.2"),
            ("foo%pgi@4.5", "%pgi@4.4:4.6", "foo%pgi@4.5"),
            ("foo@2.0%pgi@4.5", "@1:3%pgi@4.4:4.6", "foo@2.0%pgi@4.5"),
            ("foo %gcc@4.7.3", "%gcc@4.7", "foo %gcc@4.7.3"),
            ("libelf %gcc@4.4.7", "libelf %gcc@4.4.7", "libelf %gcc@4.4.7"),
            ("libelf", "libelf %gcc@4.4.7", "libelf %gcc@4.4.7"),
            # Architecture
            ("foo platform=test", "platform=test", "foo platform=test"),
            ("foo platform=linux", "platform=linux", "foo platform=linux"),
            (
                "foo platform=test",
                "platform=test target=frontend",
                "foo platform=test target=frontend",
            ),
            (
                "foo platform=test",
                "platform=test os=frontend target=frontend",
                "foo platform=test os=frontend target=frontend",
            ),
            (
                "foo platform=test os=frontend target=frontend",
                "platform=test",
                "foo platform=test os=frontend target=frontend",
            ),
            ("foo arch=test-None-None", "platform=test", "foo platform=test"),
            (
                "foo arch=test-None-frontend",
                "platform=test target=frontend",
                "foo platform=test target=frontend",
            ),
            (
                "foo arch=test-frontend-frontend",
                "platform=test os=frontend target=frontend",
                "foo platform=test os=frontend target=frontend",
            ),
            (
                "foo arch=test-frontend-frontend",
                "platform=test",
                "foo platform=test os=frontend target=frontend",
            ),
            (
                "foo platform=test target=backend os=backend",
                "platform=test target=backend os=backend",
                "foo platform=test target=backend os=backend",
            ),
            (
                "libelf target=default_target os=default_os",
                "libelf target=default_target os=default_os",
                "libelf target=default_target os=default_os",
            ),
            # Dependencies
            ("mpileaks ^mpich", "^mpich", "mpileaks ^mpich"),
            ("mpileaks ^mpich@2.0", "^mpich@1:3", "mpileaks ^mpich@2.0"),
            (
                "mpileaks ^mpich@2.0 ^callpath@1.5",
                "^mpich@1:3 ^callpath@1.4:1.6",
                "mpileaks^mpich@2.0^callpath@1.5",
            ),
            ("mpileaks ^mpi", "^mpi", "mpileaks ^mpi"),
            ("mpileaks ^mpi", "^mpich", "mpileaks ^mpi ^mpich"),
            ("mpileaks^mpi@1.5", "^mpi@1.2:1.6", "mpileaks^mpi@1.5"),
            ("mpileaks^mpi@2:", "^mpich", "mpileaks^mpi@2: ^mpich"),
            ("mpileaks^mpi@2:", "^mpich@3.0.4", "mpileaks^mpi@2: ^mpich@3.0.4"),
            # Variants
            ("mpich+foo", "mpich+foo", "mpich+foo"),
            ("mpich++foo", "mpich++foo", "mpich++foo"),
            ("mpich~foo", "mpich~foo", "mpich~foo"),
            ("mpich~~foo", "mpich~~foo", "mpich~~foo"),
            ("mpich foo=1", "mpich foo=1", "mpich foo=1"),
            ("mpich foo==1", "mpich foo==1", "mpich foo==1"),
            ("mpich+foo", "mpich foo=True", "mpich+foo"),
            ("mpich++foo", "mpich foo=True", "mpich+foo"),
            ("mpich foo=true", "mpich+foo", "mpich+foo"),
            ("mpich foo==true", "mpich++foo", "mpich+foo"),
            ("mpich~foo", "mpich foo=FALSE", "mpich~foo"),
            ("mpich~~foo", "mpich foo=FALSE", "mpich~foo"),
            ("mpich foo=False", "mpich~foo", "mpich~foo"),
            ("mpich foo==False", "mpich~foo", "mpich~foo"),
            ("mpich foo=*", "mpich~foo", "mpich~foo"),
            ("mpich+foo", "mpich foo=*", "mpich+foo"),
            (
                'multivalue-variant foo="bar,baz"',
                "multivalue-variant foo=bar,baz",
                "multivalue-variant foo=bar,baz",
            ),
            (
                'multivalue-variant foo="bar,baz"',
                "multivalue-variant foo=*",
                "multivalue-variant foo=bar,baz",
            ),
            (
                'multivalue-variant foo="bar,baz"',
                "multivalue-variant foo=bar",
                "multivalue-variant foo=bar,baz",
            ),
            (
                'multivalue-variant foo="bar,baz"',
                "multivalue-variant foo=baz",
                "multivalue-variant foo=bar,baz",
            ),
            (
                'multivalue-variant foo="bar,baz,barbaz"',
                "multivalue-variant foo=bar,baz",
                "multivalue-variant foo=bar,baz,barbaz",
            ),
            (
                'multivalue-variant foo="bar,baz"',
                'foo="baz,bar"',  # Order of values doesn't matter
                "multivalue-variant foo=bar,baz",
            ),
            ("mpich+foo", "mpich", "mpich+foo"),
            ("mpich~foo", "mpich", "mpich~foo"),
            ("mpich foo=1", "mpich", "mpich foo=1"),
            ("mpich", "mpich++foo", "mpich+foo"),
            ("libelf+debug", "libelf+foo", "libelf+debug+foo"),
            ("libelf+debug", "libelf+debug+foo", "libelf+debug+foo"),
            ("libelf debug=2", "libelf foo=1", "libelf debug=2 foo=1"),
            ("libelf debug=2", "libelf debug=2 foo=1", "libelf debug=2 foo=1"),
            ("libelf+debug", "libelf~foo", "libelf+debug~foo"),
            ("libelf+debug", "libelf+debug~foo", "libelf+debug~foo"),
            ("libelf++debug", "libelf+debug+foo", "libelf++debug++foo"),
            ("libelf debug==2", "libelf foo=1", "libelf debug==2 foo==1"),
            ("libelf debug==2", "libelf debug=2 foo=1", "libelf debug==2 foo==1"),
            ("libelf++debug", "libelf++debug~foo", "libelf++debug~~foo"),
            ("libelf foo=bar,baz", "libelf foo=*", "libelf foo=bar,baz"),
            ("libelf foo=*", "libelf foo=bar,baz", "libelf foo=bar,baz"),
            (
                'multivalue-variant foo="bar"',
                'multivalue-variant foo="baz"',
                'multivalue-variant foo="bar,baz"',
            ),
            (
                'multivalue-variant foo="bar,barbaz"',
                'multivalue-variant foo="baz"',
                'multivalue-variant foo="bar,baz,barbaz"',
            ),
            # Flags
            ("mpich ", 'mpich cppflags="-O3"', 'mpich cppflags="-O3"'),
            (
                'mpich cppflags="-O3 -Wall"',
                'mpich cppflags="-O3 -Wall"',
                'mpich cppflags="-O3 -Wall"',
            ),
            ('mpich cppflags=="-O3"', 'mpich cppflags=="-O3"', 'mpich cppflags=="-O3"'),
            (
                'libelf cflags="-O3"',
                'libelf cppflags="-Wall"',
                'libelf cflags="-O3" cppflags="-Wall"',
            ),
            (
                'libelf cflags="-O3"',
                'libelf cppflags=="-Wall"',
                'libelf cflags="-O3" cppflags=="-Wall"',
            ),
            (
                'libelf cflags=="-O3"',
                'libelf cppflags=="-Wall"',
                'libelf cflags=="-O3" cppflags=="-Wall"',
            ),
            (
                'libelf cflags="-O3"',
                'libelf cflags="-O3" cppflags="-Wall"',
                'libelf cflags="-O3" cppflags="-Wall"',
            ),
        ],
    )
    def test_abstract_specs_can_constrain_each_other(self, lhs, rhs, expected):
        """Test that lhs and rhs intersect with each other, and that they can be constrained
        with each other. Also check that the constrained result match the expected spec.
        """
        lhs, rhs, expected = Spec(lhs), Spec(rhs), Spec(expected)

        assert lhs.intersects(rhs)
        assert rhs.intersects(lhs)

        c1, c2 = lhs.copy(), rhs.copy()
        c1.constrain(rhs)
        c2.constrain(lhs)
        assert c1 == c2
        assert c1 == expected

    @pytest.mark.parametrize(
        "lhs,rhs", [("libelf", Spec()), ("libelf", "@0:1"), ("libelf", "@0:1 %gcc")]
    )
    def test_concrete_specs_which_satisfies_abstract(self, lhs, rhs, default_mock_concretization):
        """Test that constraining an abstract spec by a compatible concrete one makes the
        abstract spec concrete, and equal to the one it was constrained with.
        """
        lhs, rhs = default_mock_concretization(lhs), Spec(rhs)

        assert lhs.intersects(rhs)
        assert rhs.intersects(lhs)
        assert lhs.satisfies(rhs)
        assert not rhs.satisfies(lhs)

        assert lhs.constrain(rhs) is False
        assert rhs.constrain(lhs) is True

        assert rhs.concrete
        assert lhs.satisfies(rhs)
        assert rhs.satisfies(lhs)
        assert lhs == rhs

    @pytest.mark.parametrize(
        "lhs,rhs",
        [
            ("foo platform=linux", "platform=test os=redhat6 target=x86"),
            ("foo os=redhat6", "platform=test os=debian6 target=x86_64"),
            ("foo target=x86_64", "platform=test os=redhat6 target=x86"),
            ("foo arch=test-frontend-frontend", "platform=test os=frontend target=backend"),
            ("foo%intel", "%gcc"),
            ("foo%intel", "%pgi"),
            ("foo%pgi@4.3", "%pgi@4.4:4.6"),
            ("foo@4.0%pgi", "@1:3%pgi"),
            ("foo@4.0%pgi@4.5", "@1:3%pgi@4.4:4.6"),
            ("builtin.mock.mpich", "builtin.mpich"),
            ("mpileaks ^builtin.mock.mpich", "^builtin.mpich"),
            ("mpileaks^mpich", "^zmpi"),
            ("mpileaks^zmpi", "^mpich"),
            ("mpileaks^mpich@1.2", "^mpich@2.0"),
            ("mpileaks^mpich@4.0^callpath@1.5", "^mpich@1:3^callpath@1.4:1.6"),
            ("mpileaks^mpich@2.0^callpath@1.7", "^mpich@1:3^callpath@1.4:1.6"),
            ("mpileaks^mpich@4.0^callpath@1.7", "^mpich@1:3^callpath@1.4:1.6"),
            ("mpileaks^mpich", "^zmpi"),
            ("mpileaks^mpi@3", "^mpi@1.2:1.6"),
            ("mpileaks^mpi@3:", "^mpich2@1.4"),
            ("mpileaks^mpi@3:", "^mpich2"),
            ("mpileaks^mpi@3:", "^mpich@1.0"),
            ("mpich~foo", "mpich+foo"),
            ("mpich+foo", "mpich~foo"),
            ("mpich foo=True", "mpich foo=False"),
            ("mpich~~foo", "mpich++foo"),
            ("mpich++foo", "mpich~~foo"),
            ("mpich foo==True", "mpich foo==False"),
            ('mpich cppflags="-O3"', 'mpich cppflags="-O2"'),
            ('mpich cppflags="-O3"', 'mpich cppflags=="-O3"'),
            ("libelf@0:2.0", "libelf@2.1:3"),
            ("libelf@0:2.5%gcc@4.8:4.9", "libelf@2.1:3%gcc@4.5:4.7"),
            ("libelf+debug", "libelf~debug"),
            ("libelf+debug~foo", "libelf+debug+foo"),
            ("libelf debug=True", "libelf debug=False"),
            ('libelf cppflags="-O3"', 'libelf cppflags="-O2"'),
            ("libelf platform=test target=be os=be", "libelf target=fe os=fe"),
        ],
    )
    def test_constraining_abstract_specs_with_empty_intersection(self, lhs, rhs):
        """Check that two abstract specs with an empty intersection cannot be constrained
        with each other.
        """
        lhs, rhs = Spec(lhs), Spec(rhs)

        assert not lhs.intersects(rhs)
        assert not rhs.intersects(lhs)

        with pytest.raises(UnsatisfiableSpecError):
            lhs.constrain(rhs)

        with pytest.raises(UnsatisfiableSpecError):
            rhs.constrain(lhs)

    @pytest.mark.parametrize(
        "lhs,rhs,intersection_expected",
        [
            ("mpich", "mpich +foo", True),
            ("mpich", "mpich~foo", True),
            ("mpich", "mpich foo=1", True),
            ("mpich", "mpich++foo", True),
            ("mpich", "mpich~~foo", True),
            ("mpich", "mpich foo==1", True),
            # Flags semantics is currently different from other variant
            ("mpich", 'mpich cflags="-O3"', True),
            ("mpich cflags=-O3", 'mpich cflags="-O3 -Ofast"', False),
            ("mpich cflags=-O2", 'mpich cflags="-O3"', False),
            ("multivalue-variant foo=bar", "multivalue-variant +foo", False),
            ("multivalue-variant foo=bar", "multivalue-variant ~foo", False),
            ("multivalue-variant fee=bar", "multivalue-variant fee=baz", False),
        ],
    )
    def test_concrete_specs_which_do_not_satisfy_abstract(
        self, lhs, rhs, intersection_expected, default_mock_concretization
    ):
        lhs, rhs = default_mock_concretization(lhs), Spec(rhs)

        assert lhs.intersects(rhs) is intersection_expected
        assert rhs.intersects(lhs) is intersection_expected
        assert not lhs.satisfies(rhs)
        assert not rhs.satisfies(lhs)

        with pytest.raises(UnsatisfiableSpecError):
            assert lhs.constrain(rhs)

        with pytest.raises(UnsatisfiableSpecError):
            assert rhs.constrain(lhs)

    def test_satisfies_single_valued_variant(self):
        """Tests that the case reported in
        https://github.com/spack/spack/pull/2386#issuecomment-282147639
        is handled correctly.
        """
        a = Spec("a foobar=bar")
        a.concretize()

        assert a.satisfies("foobar=bar")
        assert a.satisfies("foobar=*")

        # Assert that an autospec generated from a literal
        # gives the right result for a single valued variant
        assert "foobar=bar" in a
        assert "foobar==bar" in a
        assert "foobar=baz" not in a
        assert "foobar=fee" not in a

        # ... and for a multi valued variant
        assert "foo=bar" in a

        # Check that conditional dependencies are treated correctly
        assert "^b" in a

    def test_unsatisfied_single_valued_variant(self):
        a = Spec("a foobar=baz")
        a.concretize()
        assert "^b" not in a

        mv = Spec("multivalue-variant")
        mv.concretize()
        assert "a@1.0" not in mv

    def test_indirect_unsatisfied_single_valued_variant(self):
        spec = Spec("singlevalue-variant-dependent")
        spec.concretize()
        assert "a@1.0" not in spec

    def test_unsatisfiable_multi_value_variant(self, default_mock_concretization):
        # Semantics for a multi-valued variant is different
        # Depending on whether the spec is concrete or not

        a = default_mock_concretization('multivalue-variant foo="bar"')
        spec_str = 'multivalue-variant foo="bar,baz"'
        b = Spec(spec_str)
        assert not a.satisfies(b)
        assert not a.satisfies(spec_str)
        # A concrete spec cannot be constrained further
        with pytest.raises(UnsatisfiableSpecError):
            a.constrain(b)

        a = Spec('multivalue-variant foo="bar"')
        spec_str = 'multivalue-variant foo="bar,baz"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained
        assert a.satisfies(b)
        assert a.satisfies(spec_str)
        # An abstract spec can instead be constrained
        assert a.constrain(b)

        a = default_mock_concretization('multivalue-variant foo="bar,baz"')
        spec_str = 'multivalue-variant foo="bar,baz,quux"'
        b = Spec(spec_str)
        assert not a.satisfies(b)
        assert not a.satisfies(spec_str)
        # A concrete spec cannot be constrained further
        with pytest.raises(UnsatisfiableSpecError):
            a.constrain(b)

        a = Spec('multivalue-variant foo="bar,baz"')
        spec_str = 'multivalue-variant foo="bar,baz,quux"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained
        assert a.intersects(b)
        assert a.intersects(spec_str)
        # An abstract spec can instead be constrained
        assert a.constrain(b)
        # ...but will fail during concretization if there are
        # values in the variant that are not allowed
        with pytest.raises(InvalidVariantValueError):
            a.concretize()

        # This time we'll try to set a single-valued variant
        a = Spec('multivalue-variant fee="bar"')
        spec_str = 'multivalue-variant fee="baz"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained,
        # as before concretization I don't know which type of variant
        # I have (if it is not a BV)
        assert a.intersects(b)
        assert a.intersects(spec_str)
        # A variant cannot be parsed as single-valued until we try to
        # concretize. This means that we can constrain the variant above
        assert a.constrain(b)
        # ...but will fail during concretization if there are
        # multiple values set
        with pytest.raises(MultipleValuesInExclusiveVariantError):
            a.concretize()

    def test_copy_satisfies_transitive(self):
        spec = Spec("dttop")
        spec.concretize()
        copy = spec.copy()
        for s in spec.traverse():
            assert s.satisfies(copy[s.name])
            assert copy[s.name].satisfies(s)

    def test_intersects_virtual(self):
        assert Spec("mpich").intersects(Spec("mpi"))
        assert Spec("mpich2").intersects(Spec("mpi"))
        assert Spec("zmpi").intersects(Spec("mpi"))

    def test_intersects_virtual_dep_with_virtual_constraint(self):
        assert Spec("netlib-lapack ^openblas").intersects("netlib-lapack ^openblas")
        assert not Spec("netlib-lapack ^netlib-blas").intersects("netlib-lapack ^openblas")
        assert not Spec("netlib-lapack ^openblas").intersects("netlib-lapack ^netlib-blas")
        assert Spec("netlib-lapack ^netlib-blas").intersects("netlib-lapack ^netlib-blas")

    def test_intersectable_concrete_specs_must_have_the_same_hash(self):
        """Ensure that concrete specs are matched *exactly* by hash."""
        s1 = Spec("mpileaks").concretized()
        s2 = s1.copy()

        assert s1.satisfies(s2)
        assert s2.satisfies(s1)
        assert s1.intersects(s2)

        # Simulate specs that were installed before and after a change to
        # Spack's hashing algorithm.  This just reverses s2's hash.
        s2._hash = s1.dag_hash()[-1::-1]

        assert not s1.satisfies(s2)
        assert not s2.satisfies(s1)
        assert not s1.intersects(s2)

    # ========================================================================
    # Indexing specs
    # ========================================================================
    def test_self_index(self):
        s = Spec("callpath")
        assert s["callpath"] == s

    def test_dep_index(self):
        s = Spec("callpath")
        s.normalize()

        assert s["callpath"] == s
        assert type(s["dyninst"]) == Spec
        assert type(s["libdwarf"]) == Spec
        assert type(s["libelf"]) == Spec
        assert type(s["mpi"]) == Spec

        assert s["dyninst"].name == "dyninst"
        assert s["libdwarf"].name == "libdwarf"
        assert s["libelf"].name == "libelf"
        assert s["mpi"].name == "mpi"

    def test_spec_contains_deps(self):
        s = Spec("callpath")
        s.normalize()
        assert "dyninst" in s
        assert "libdwarf" in s
        assert "libelf" in s
        assert "mpi" in s

    @pytest.mark.usefixtures("config")
    def test_virtual_index(self):
        s = Spec("callpath")
        s.concretize()

        s_mpich = Spec("callpath ^mpich")
        s_mpich.concretize()

        s_mpich2 = Spec("callpath ^mpich2")
        s_mpich2.concretize()

        s_zmpi = Spec("callpath ^zmpi")
        s_zmpi.concretize()

        assert s["mpi"].name != "mpi"
        assert s_mpich["mpi"].name == "mpich"
        assert s_mpich2["mpi"].name == "mpich2"
        assert s_zmpi["zmpi"].name == "zmpi"

        for spec in [s, s_mpich, s_mpich2, s_zmpi]:
            assert "mpi" in spec

    @pytest.mark.parametrize(
        "lhs,rhs",
        [
            ("libelf", "@1.0"),
            ("libelf", "@1.0:5.0"),
            ("libelf", "%gcc"),
            ("libelf%gcc", "%gcc@4.5"),
            ("libelf", "+debug"),
            ("libelf", "debug=*"),
            ("libelf", "~debug"),
            ("libelf", "debug=2"),
            ("libelf", 'cppflags="-O3"'),
            ("libelf", 'cppflags=="-O3"'),
            ("libelf^foo", "libelf^foo@1.0"),
            ("libelf^foo", "libelf^foo@1.0:5.0"),
            ("libelf^foo", "libelf^foo%gcc"),
            ("libelf^foo%gcc", "libelf^foo%gcc@4.5"),
            ("libelf^foo", "libelf^foo+debug"),
            ("libelf^foo", "libelf^foo~debug"),
            ("libelf", "^foo"),
        ],
    )
    def test_lhs_is_changed_when_constraining(self, lhs, rhs):
        lhs, rhs = Spec(lhs), Spec(rhs)

        assert lhs.intersects(rhs)
        assert rhs.intersects(lhs)
        assert not lhs.satisfies(rhs)

        assert lhs.constrain(rhs) is True
        assert lhs.satisfies(rhs)

    @pytest.mark.parametrize(
        "lhs,rhs",
        [
            ("libelf", "libelf"),
            ("libelf@1.0", "@1.0"),
            ("libelf@1.0:5.0", "@1.0:5.0"),
            ("libelf%gcc", "%gcc"),
            ("libelf%gcc@4.5", "%gcc@4.5"),
            ("libelf+debug", "+debug"),
            ("libelf~debug", "~debug"),
            ("libelf debug=2", "debug=2"),
            ("libelf debug=2", "debug=*"),
            ('libelf cppflags="-O3"', 'cppflags="-O3"'),
            ('libelf cppflags=="-O3"', 'cppflags=="-O3"'),
            ("libelf^foo@1.0", "libelf^foo@1.0"),
            ("libelf^foo@1.0:5.0", "libelf^foo@1.0:5.0"),
            ("libelf^foo%gcc", "libelf^foo%gcc"),
            ("libelf^foo%gcc@4.5", "libelf^foo%gcc@4.5"),
            ("libelf^foo+debug", "libelf^foo+debug"),
            ("libelf^foo~debug", "libelf^foo~debug"),
            ('libelf^foo cppflags="-O3"', 'libelf^foo cppflags="-O3"'),
        ],
    )
    def test_lhs_is_not_changed_when_constraining(self, lhs, rhs):
        lhs, rhs = Spec(lhs), Spec(rhs)
        assert lhs.intersects(rhs)
        assert rhs.intersects(lhs)
        assert lhs.satisfies(rhs)
        assert lhs.constrain(rhs) is False

    def test_exceptional_paths_for_constructor(self):
        with pytest.raises(TypeError):
            Spec((1, 2))

        with pytest.raises(ValueError):
            Spec("libelf foo")

    def test_spec_formatting(self, default_mock_concretization):
        spec = default_mock_concretization("multivalue-variant cflags=-O2")

        # Since the default is the full spec see if the string rep of
        # spec is the same as the output of spec.format()
        # ignoring whitespace (though should we?) and ignoring dependencies
        spec_string = str(spec)
        idx = spec_string.index(" ^")
        assert spec_string[:idx] == spec.format().strip()

        # Testing named strings ie {string} and whether we get
        # the correct component
        # Mixed case intentional to test both
        package_segments = [
            ("{NAME}", "name"),
            ("{VERSION}", "versions"),
            ("{compiler}", "compiler"),
            ("{compiler_flags}", "compiler_flags"),
            ("{variants}", "variants"),
            ("{architecture}", "architecture"),
        ]

        sigil_package_segments = [
            ("{@VERSIONS}", "@" + str(spec.version)),
            ("{%compiler}", "%" + str(spec.compiler)),
            ("{arch=architecture}", "arch=" + str(spec.architecture)),
        ]

        compiler_segments = [("{compiler.name}", "name"), ("{compiler.version}", "versions")]

        sigil_compiler_segments = [
            ("{%compiler.name}", "%" + spec.compiler.name),
            ("{@compiler.version}", "@" + str(spec.compiler.version)),
        ]

        architecture_segments = [
            ("{architecture.platform}", "platform"),
            ("{architecture.os}", "os"),
            ("{architecture.target}", "target"),
        ]

        other_segments = [
            ("{spack_root}", spack.paths.spack_root),
            ("{spack_install}", spack.store.layout.root),
            ("{hash:7}", spec.dag_hash(7)),
            ("{/hash}", "/" + spec.dag_hash()),
        ]

        for named_str, prop in package_segments:
            expected = getattr(spec, prop, "")
            actual = spec.format(named_str)
            assert str(expected).strip() == actual

        for named_str, expected in sigil_package_segments:
            actual = spec.format(named_str)
            assert expected == actual

        compiler = spec.compiler
        for named_str, prop in compiler_segments:
            expected = getattr(compiler, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        for named_str, expected in sigil_compiler_segments:
            actual = spec.format(named_str)
            assert expected == actual

        arch = spec.architecture
        for named_str, prop in architecture_segments:
            expected = getattr(arch, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        for named_str, expected in other_segments:
            actual = spec.format(named_str)
            assert expected == actual

    def test_spec_formatting_escapes(self, default_mock_concretization):
        spec = default_mock_concretization("multivalue-variant cflags=-O2")

        sigil_mismatches = [
            "{@name}",
            "{@version.concrete}",
            "{%compiler.version}",
            "{/hashd}",
            "{arch=architecture.os}",
        ]

        for fmt_str in sigil_mismatches:
            with pytest.raises(SpecFormatSigilError):
                spec.format(fmt_str)

        bad_formats = [
            r"{}",
            r"name}",
            r"\{name}",
            r"{name",
            r"{name\}",
            r"{_concrete}",
            r"{dag_hash}",
            r"{foo}",
            r"{+variants.debug}",
        ]

        for fmt_str in bad_formats:
            with pytest.raises(SpecFormatStringError):
                spec.format(fmt_str)

    def test_spec_deprecated_formatting(self):
        spec = Spec("libelf cflags==-O2")
        spec.concretize()

        # Since the default is the full spec see if the string rep of
        # spec is the same as the output of spec.format()
        # ignoring whitespace (though should we?)
        assert str(spec) == spec.format("$_$@$%@+$+$=").strip()

        # Testing named strings ie {string} and whether we get
        # the correct component
        # Mixed case intentional for testing both
        package_segments = [
            ("${PACKAGE}", "name"),
            ("${VERSION}", "versions"),
            ("${compiler}", "compiler"),
            ("${compilerflags}", "compiler_flags"),
            ("${options}", "variants"),
            ("${architecture}", "architecture"),
        ]

        compiler_segments = [("${compilername}", "name"), ("${compilerver}", "versions")]

        architecture_segments = [
            ("${PLATFORM}", "platform"),
            ("${OS}", "os"),
            ("${TARGET}", "target"),
        ]

        for named_str, prop in package_segments:
            expected = getattr(spec, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        compiler = spec.compiler
        for named_str, prop in compiler_segments:
            expected = getattr(compiler, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        arch = spec.architecture
        for named_str, prop in architecture_segments:
            expected = getattr(arch, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

    @pytest.mark.regression("9908")
    def test_spec_flags_maintain_order(self):
        # Spack was assembling flags in a manner that could result in
        # different orderings for repeated concretizations of the same
        # spec and config
        spec_str = "libelf %gcc@11.1.0 os=redhat6"
        for _ in range(3):
            s = Spec(spec_str).concretized()
            assert all(
                s.compiler_flags[x] == ["-O0", "-g"] for x in ("cflags", "cxxflags", "fflags")
            )

    def test_combination_of_wildcard_or_none(self):
        # Test that using 'none' and another value raises
        with pytest.raises(spack.variant.InvalidVariantValueCombinationError):
            Spec("multivalue-variant foo=none,bar")

        # Test that using wildcard and another value raises
        with pytest.raises(spack.variant.InvalidVariantValueCombinationError):
            Spec("multivalue-variant foo=*,bar")

    def test_errors_in_variant_directive(self):
        variant = spack.directives.variant.__wrapped__

        class Pkg(object):
            name = "PKG"

        # We can't use names that are reserved by Spack
        fn = variant("patches")
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert "The name 'patches' is reserved" in str(exc_info.value)

        # We can't have conflicting definitions for arguments
        fn = variant("foo", values=spack.variant.any_combination_of("fee", "foom"), default="bar")
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert " it is handled by an attribute of the 'values' " "argument" in str(exc_info.value)

        # We can't leave None as a default value
        fn = variant("foo", default=None)
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert "either a default was not explicitly set, or 'None' was used" in str(exc_info.value)

        # We can't use an empty string as a default value
        fn = variant("foo", default="")
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert "the default cannot be an empty string" in str(exc_info.value)

    def test_abstract_spec_prefix_error(self):
        spec = Spec("libelf")

        with pytest.raises(SpecError):
            spec.prefix

    def test_forwarding_of_architecture_attributes(self):
        spec = Spec("libelf target=x86_64").concretized()

        # Check that we can still access each member through
        # the architecture attribute
        assert "test" in spec.architecture
        assert "debian" in spec.architecture
        assert "x86_64" in spec.architecture

        # Check that we forward the platform and os attribute correctly
        assert spec.platform == "test"
        assert spec.os == "debian6"

        # Check that the target is also forwarded correctly and supports
        # all the operators we expect
        assert spec.target == "x86_64"
        assert spec.target.family == "x86_64"
        assert "avx512" not in spec.target
        assert spec.target < "broadwell"

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice(self, transitive, default_mock_concretization):
        # Tests the new splice function in Spec using a somewhat simple case
        # with a variant with a conditional dependency.
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-h+foo")

        # Sanity checking that these are not the same thing.
        assert dep.dag_hash() != spec["splice-h"].dag_hash()

        # Do the splice.
        out = spec.splice(dep, transitive)

        # Returned spec should still be concrete.
        assert out.concrete

        # Traverse the spec and assert that all dependencies are accounted for.
        for node in spec.traverse():
            assert node.name in out

        # If the splice worked, then the dag hash of the spliced dep should
        # now match the dag hash of the build spec of the dependency from the
        # returned spec.
        out_h_build = out["splice-h"].build_spec
        assert out_h_build.dag_hash() == dep.dag_hash()

        # Transitivity should determine whether the transitive dependency was
        # changed.
        expected_z = dep["splice-z"] if transitive else spec["splice-z"]
        assert out["splice-z"].dag_hash() == expected_z.dag_hash()

        # Sanity check build spec of out should be the original spec.
        assert out["splice-t"].build_spec.dag_hash() == spec["splice-t"].dag_hash()

        # Finally, the spec should know it's been spliced:
        assert out.spliced

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_with_cached_hashes(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-h+foo")

        # monkeypatch hashes so we can test that they are cached
        spec._hash = "aaaaaa"
        dep._hash = "bbbbbb"
        spec["splice-h"]._hash = "cccccc"
        spec["splice-z"]._hash = "dddddd"
        dep["splice-z"]._hash = "eeeeee"

        out = spec.splice(dep, transitive=transitive)
        out_z_expected = (dep if transitive else spec)["splice-z"]

        assert out.dag_hash() != spec.dag_hash()
        assert (out["splice-h"].dag_hash() == dep.dag_hash()) == transitive
        assert out["splice-z"].dag_hash() == out_z_expected.dag_hash()

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_input_unchanged(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-h+foo")
        orig_spec_hash = spec.dag_hash()
        orig_dep_hash = dep.dag_hash()
        spec.splice(dep, transitive)
        # Post-splice, dag hash should still be different; no changes should be
        # made to these specs.
        assert spec.dag_hash() == orig_spec_hash
        assert dep.dag_hash() == orig_dep_hash

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_subsequent(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-h+foo")
        out = spec.splice(dep, transitive)

        # Now we attempt a second splice.
        dep = default_mock_concretization("splice-z+bar")

        # Transitivity shouldn't matter since Splice Z has no dependencies.
        out2 = out.splice(dep, transitive)
        assert out2.concrete
        assert out2["splice-z"].dag_hash() != spec["splice-z"].dag_hash()
        assert out2["splice-z"].dag_hash() != out["splice-z"].dag_hash()
        assert out2["splice-t"].build_spec.dag_hash() == spec["splice-t"].dag_hash()
        assert out2.spliced

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_dict(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-h+foo")
        out = spec.splice(dep, transitive)

        # Sanity check all hashes are unique...
        assert spec.dag_hash() != dep.dag_hash()
        assert out.dag_hash() != dep.dag_hash()
        assert out.dag_hash() != spec.dag_hash()
        node_list = out.to_dict()["spec"]["nodes"]
        root_nodes = [n for n in node_list if n["hash"] == out.dag_hash()]
        build_spec_nodes = [n for n in node_list if n["hash"] == spec.dag_hash()]
        assert spec.dag_hash() == out.build_spec.dag_hash()
        assert len(root_nodes) == 1
        assert len(build_spec_nodes) == 1

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_dict_roundtrip(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-h+foo")
        out = spec.splice(dep, transitive)

        # Sanity check all hashes are unique...
        assert spec.dag_hash() != dep.dag_hash()
        assert out.dag_hash() != dep.dag_hash()
        assert out.dag_hash() != spec.dag_hash()
        out_rt_spec = Spec.from_dict(out.to_dict())  # rt is "round trip"
        assert out_rt_spec.dag_hash() == out.dag_hash()
        out_rt_spec_bld_hash = out_rt_spec.build_spec.dag_hash()
        out_rt_spec_h_bld_hash = out_rt_spec["splice-h"].build_spec.dag_hash()
        out_rt_spec_z_bld_hash = out_rt_spec["splice-z"].build_spec.dag_hash()

        # In any case, the build spec for splice-t (root) should point to the
        # original spec, preserving build provenance.
        assert spec.dag_hash() == out_rt_spec_bld_hash
        assert out_rt_spec.dag_hash() != out_rt_spec_bld_hash

        # The build spec for splice-h should always point to the introduced
        # spec, since that is the spec spliced in.
        assert dep["splice-h"].dag_hash() == out_rt_spec_h_bld_hash

        # The build spec for splice-z will depend on whether or not the splice
        # was transitive.
        expected_z_bld_hash = (
            dep["splice-z"].dag_hash() if transitive else spec["splice-z"].dag_hash()
        )
        assert expected_z_bld_hash == out_rt_spec_z_bld_hash

    @pytest.mark.parametrize(
        "spec,constraint,expected_result",
        [
            ("libelf target=haswell", "target=broadwell", False),
            ("libelf target=haswell", "target=haswell", True),
            ("libelf target=haswell", "target=x86_64:", True),
            ("libelf target=haswell", "target=:haswell", True),
            ("libelf target=haswell", "target=icelake,:nocona", False),
            ("libelf target=haswell", "target=haswell,:nocona", True),
            # Check that a single target is not treated as the start
            # or the end of an open range
            ("libelf target=haswell", "target=x86_64", False),
            ("libelf target=x86_64", "target=haswell", False),
        ],
    )
    @pytest.mark.regression("13111")
    def test_target_constraints(self, spec, constraint, expected_result):
        s = Spec(spec)
        assert s.intersects(constraint) is expected_result

    @pytest.mark.regression("13124")
    def test_error_message_unknown_variant(self):
        s = Spec("mpileaks +unknown")
        with pytest.raises(UnknownVariantError, match=r"package has no such"):
            s.concretize()

    @pytest.mark.regression("18527")
    def test_satisfies_dependencies_ordered(self):
        d = Spec("zmpi ^fake")
        s = Spec("mpileaks")
        s._add_dependency(d, deptypes=())
        assert s.satisfies("mpileaks ^zmpi ^fake")

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_swap_names(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-a+foo")
        out = spec.splice(dep, transitive)
        assert dep.name in out
        assert transitive == ("+foo" in out["splice-z"])

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_swap_names_mismatch_virtuals(self, default_mock_concretization, transitive):
        spec = default_mock_concretization("splice-t")
        dep = default_mock_concretization("splice-vh+foo")
        with pytest.raises(spack.spec.SpliceError, match="will not provide the same virtuals."):
            spec.splice(dep, transitive)

    def test_spec_override(self):
        init_spec = Spec("a foo=baz foobar=baz cflags=-O3 cxxflags=-O1")
        change_spec = Spec("a foo=fee cflags=-O2")
        new_spec = Spec.override(init_spec, change_spec)
        new_spec.concretize()
        assert "foo=fee" in new_spec
        # This check fails without concretizing: apparently if both specs are
        # abstract, then the spec will always be considered to satisfy
        # 'variant=value' (regardless of whether it in fact does).
        assert "foo=baz" not in new_spec
        assert "foobar=baz" in new_spec
        assert new_spec.compiler_flags["cflags"] == ["-O2"]
        assert new_spec.compiler_flags["cxxflags"] == ["-O1"]


@pytest.mark.regression("3887")
@pytest.mark.parametrize("spec_str", ["py-extension2", "extension1", "perl-extension"])
def test_is_extension_after_round_trip_to_dict(config, mock_packages, spec_str):
    # x is constructed directly from string, y from a
    # round-trip to dict representation
    x = Spec(spec_str).concretized()
    y = Spec.from_dict(x.to_dict())

    # Using 'y' since the round-trip make us lose build dependencies
    for d in y.traverse():
        assert x[d.name].package.is_extension == y[d.name].package.is_extension


def test_malformed_spec_dict():
    with pytest.raises(SpecError, match="malformed"):
        Spec.from_dict(
            {"spec": {"_meta": {"version": 2}, "nodes": [{"dependencies": {"name": "foo"}}]}}
        )


def test_spec_dict_hashless_dep():
    with pytest.raises(SpecError, match="Couldn't parse"):
        Spec.from_dict(
            {
                "spec": {
                    "_meta": {"version": 2},
                    "nodes": [
                        {"name": "foo", "hash": "thehash", "dependencies": [{"name": "bar"}]}
                    ],
                }
            }
        )


@pytest.mark.parametrize(
    "specs,expected",
    [
        # Anonymous specs without dependencies
        (["+baz", "+bar"], "+baz+bar"),
        (["@2.0:", "@:5.1", "+bar"], "@2.0:5.1 +bar"),
        # Anonymous specs with dependencies
        (["^mpich@3.2", "^mpich@:4.0+foo"], "^mpich@3.2 +foo"),
        # Mix a real package with a virtual one. This test
        # should fail if we start using the repository
        (["^mpich@3.2", "^mpi+foo"], "^mpich@3.2 ^mpi+foo"),
    ],
)
def test_merge_abstract_anonymous_specs(specs, expected):
    specs = [Spec(x) for x in specs]
    result = spack.spec.merge_abstract_anonymous_specs(*specs)
    assert result == Spec(expected)


@pytest.mark.parametrize(
    "anonymous,named,expected",
    [
        ("+plumed", "gromacs", "gromacs+plumed"),
        ("+plumed ^plumed%gcc", "gromacs", "gromacs+plumed ^plumed%gcc"),
        ("+plumed", "builtin.gromacs", "builtin.gromacs+plumed"),
    ],
)
def test_merge_anonymous_spec_with_named_spec(anonymous, named, expected):
    s = Spec(anonymous)
    changed = s.constrain(named)
    assert changed
    assert s == Spec(expected)


def test_spec_installed(default_mock_concretization, database):
    """Test whether Spec.installed works."""
    # a known installed spec should say that it's installed
    specs = database.query()
    spec = specs[0]
    assert spec.installed
    assert spec.copy().installed

    # an abstract spec should say it's not installed
    spec = Spec("not-a-real-package")
    assert not spec.installed

    # 'a' is not in the mock DB and is not installed
    spec = default_mock_concretization("a")
    assert not spec.installed


@pytest.mark.regression("30678")
def test_call_dag_hash_on_old_dag_hash_spec(mock_packages, default_mock_concretization):
    # create a concrete spec
    a = default_mock_concretization("a")
    dag_hashes = {spec.name: spec.dag_hash() for spec in a.traverse()}

    # make it look like an old DAG hash spec with no package hash on the spec.
    for spec in a.traverse():
        assert spec.concrete
        spec._package_hash = None

    for spec in a.traverse():
        assert dag_hashes[spec.name] == spec.dag_hash()

        with pytest.raises(ValueError, match="Cannot call package_hash()"):
            spec.package_hash()


@pytest.mark.regression("30861")
def test_concretize_partial_old_dag_hash_spec(mock_packages, config):
    # create an "old" spec with no package hash
    bottom = Spec("dt-diamond-bottom").concretized()
    delattr(bottom, "_package_hash")

    dummy_hash = "zd4m26eis2wwbvtyfiliar27wkcv3ehk"
    bottom._hash = dummy_hash

    # add it to an abstract spec as a dependency
    top = Spec("dt-diamond")
    top.add_dependency_edge(bottom, deptypes=())

    # concretize with the already-concrete dependency
    top.concretize()

    for spec in top.traverse():
        assert spec.concrete

    # make sure dag_hash is untouched
    assert spec["dt-diamond-bottom"].dag_hash() == dummy_hash
    assert spec["dt-diamond-bottom"]._hash == dummy_hash

    # make sure package hash is NOT recomputed
    assert not getattr(spec["dt-diamond-bottom"], "_package_hash", None)


def test_unsupported_compiler():
    with pytest.raises(UnsupportedCompilerError):
        Spec("gcc%fake-compiler").validate_or_raise()


def test_package_hash_affects_dunder_and_dag_hash(mock_packages, default_mock_concretization):
    a1 = default_mock_concretization("a")
    a2 = default_mock_concretization("a")

    assert hash(a1) == hash(a2)
    assert a1.dag_hash() == a2.dag_hash()
    assert a1.process_hash() == a2.process_hash()

    a1.clear_cached_hashes()
    a2.clear_cached_hashes()

    # tweak the dag hash of one of these specs
    new_hash = "00000000000000000000000000000000"
    if new_hash == a1._package_hash:
        new_hash = "11111111111111111111111111111111"
    a1._package_hash = new_hash

    assert hash(a1) != hash(a2)
    assert a1.dag_hash() != a2.dag_hash()
    assert a1.process_hash() != a2.process_hash()


def test_intersects_and_satisfies_on_concretized_spec(default_mock_concretization):
    """Test that a spec obtained by concretizing an abstract spec, satisfies the abstract spec
    but not vice-versa.
    """
    a1 = default_mock_concretization("a@1.0")
    a2 = Spec("a@1.0")

    assert a1.intersects(a2)
    assert a2.intersects(a1)
    assert a1.satisfies(a2)
    assert not a2.satisfies(a1)


@pytest.mark.parametrize(
    "abstract_spec,spec_str",
    [
        ("v1-provider", "v1-consumer ^conditional-provider+disable-v1"),
        ("conditional-provider", "v1-consumer ^conditional-provider+disable-v1"),
        ("^v1-provider", "v1-consumer ^conditional-provider+disable-v1"),
        ("^conditional-provider", "v1-consumer ^conditional-provider+disable-v1"),
    ],
)
@pytest.mark.regression("35597")
def test_abstract_provider_in_spec(abstract_spec, spec_str, default_mock_concretization):
    s = default_mock_concretization(spec_str)
    assert abstract_spec in s


@pytest.mark.parametrize(
    "lhs,rhs,expected", [("a", "a", True), ("a", "a@1.0", True), ("a@1.0", "a", False)]
)
def test_abstract_contains_semantic(lhs, rhs, expected, mock_packages):
    s, t = Spec(lhs), Spec(rhs)
    result = s in t
    assert result is expected


@pytest.mark.parametrize(
    "factory,lhs_str,rhs_str,results",
    [
        # Architecture
        (ArchSpec, "None-ubuntu20.04-None", "None-None-x86_64", (True, False, False)),
        (ArchSpec, "None-ubuntu20.04-None", "linux-None-x86_64", (True, False, False)),
        (ArchSpec, "None-None-x86_64:", "linux-None-haswell", (True, False, True)),
        (ArchSpec, "None-None-x86_64:haswell", "linux-None-icelake", (False, False, False)),
        (ArchSpec, "linux-None-None", "linux-None-None", (True, True, True)),
        (ArchSpec, "darwin-None-None", "linux-None-None", (False, False, False)),
        (ArchSpec, "None-ubuntu20.04-None", "None-ubuntu20.04-None", (True, True, True)),
        (ArchSpec, "None-ubuntu20.04-None", "None-ubuntu22.04-None", (False, False, False)),
        # Compiler
        (CompilerSpec, "gcc", "clang", (False, False, False)),
        (CompilerSpec, "gcc", "gcc@5", (True, False, True)),
        (CompilerSpec, "gcc@5", "gcc@5.3", (True, False, True)),
        (CompilerSpec, "gcc@5", "gcc@5-tag", (True, False, True)),
        # Flags (flags are a map, so for convenience we initialize a full Spec)
        # Note: the semantic is that of sv variants, not mv variants
        (Spec, "cppflags=-foo", "cppflags=-bar", (False, False, False)),
        (Spec, "cppflags='-bar -foo'", "cppflags=-bar", (False, False, False)),
        (Spec, "cppflags=-foo", "cppflags=-foo", (True, True, True)),
        (Spec, "cppflags=-foo", "cflags=-foo", (True, False, False)),
        # Versions
        (Spec, "@0.94h", "@:0.94i", (True, True, False)),
        # Different virtuals intersect if there is at least package providing both
        (Spec, "mpi", "lapack", (True, False, False)),
        (Spec, "mpi", "pkgconfig", (False, False, False)),
    ],
)
def test_intersects_and_satisfies(factory, lhs_str, rhs_str, results):
    lhs = factory(lhs_str)
    rhs = factory(rhs_str)

    intersects, lhs_satisfies_rhs, rhs_satisfies_lhs = results

    assert lhs.intersects(rhs) is intersects
    assert rhs.intersects(lhs) is lhs.intersects(rhs)

    assert lhs.satisfies(rhs) is lhs_satisfies_rhs
    assert rhs.satisfies(lhs) is rhs_satisfies_lhs


@pytest.mark.parametrize(
    "factory,lhs_str,rhs_str,result,constrained_str",
    [
        # Architecture
        (ArchSpec, "None-ubuntu20.04-None", "None-None-x86_64", True, "None-ubuntu20.04-x86_64"),
        (ArchSpec, "None-None-x86_64", "None-None-x86_64", False, "None-None-x86_64"),
        (
            ArchSpec,
            "None-None-x86_64:icelake",
            "None-None-x86_64:icelake",
            False,
            "None-None-x86_64:icelake",
        ),
        (ArchSpec, "None-ubuntu20.04-None", "linux-None-x86_64", True, "linux-ubuntu20.04-x86_64"),
        (
            ArchSpec,
            "None-ubuntu20.04-nocona:haswell",
            "None-None-x86_64:icelake",
            False,
            "None-ubuntu20.04-nocona:haswell",
        ),
        (
            ArchSpec,
            "None-ubuntu20.04-nocona,haswell",
            "None-None-x86_64:icelake",
            False,
            "None-ubuntu20.04-nocona,haswell",
        ),
        # Compiler
        (CompilerSpec, "gcc@5", "gcc@5-tag", True, "gcc@5-tag"),
        (CompilerSpec, "gcc@5", "gcc@5", False, "gcc@5"),
        # Flags
        (Spec, "cppflags=-foo", "cppflags=-foo", False, "cppflags=-foo"),
        (Spec, "cppflags=-foo", "cflags=-foo", True, "cppflags=-foo cflags=-foo"),
    ],
)
def test_constrain(factory, lhs_str, rhs_str, result, constrained_str):
    lhs = factory(lhs_str)
    rhs = factory(rhs_str)

    assert lhs.constrain(rhs) is result
    assert lhs == factory(constrained_str)

    # The intersection must be the same, so check that invariant too
    lhs = factory(lhs_str)
    rhs = factory(rhs_str)
    rhs.constrain(lhs)
    assert rhs == factory(constrained_str)
