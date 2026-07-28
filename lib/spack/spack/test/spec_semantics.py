# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

import pytest

import spack.concretize
import spack.deptypes as dt
import spack.directives
import spack.hash_types as ht
import spack.package_base
import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
import spack.spec_parser
import spack.util.lang
import spack.variant
import spack.version as vn
from spack.enums import PropagationPolicy
from spack.error import SpecError, UnsatisfiableSpecError
from spack.spec import ArchSpec, DependencySpec, Spec, SpecFormatSigilError, SpecFormatStringError
from spack.util.tty.color import colorize
from spack.variant import (
    InvalidVariantValueError,
    MultipleValuesInExclusiveVariantError,
    UnknownVariantError,
)


@pytest.fixture()
def setup_complex_splice(monkeypatch):
    r"""Fixture to set up splicing for two complex specs.

    a_red is a spec in which every node has the variant color=red
    c_blue is a spec in which every node has the variant color=blue

    a_red structure:
                     a -
                    / \ \
                   b   c \
                  /|\ / \ |
                 e | d   g@2
                  \|/
                  g@1

    c_blue structure:
                    c
                   /|\
                  d f \
                 /  |\ \
               g@2  e \ \
                     \| /
                     g@3

    This is not intended for use in tests that use virtuals, so ``_splice_match`` is monkeypatched
    to avoid needing package files for each spec.
    """

    def splice_match(self, other, self_root, other_root):
        return self.name == other.name

    def virtuals_provided(self, root):
        return []

    monkeypatch.setattr(Spec, "_splice_match", splice_match)
    monkeypatch.setattr(Spec, "_virtuals_provided", virtuals_provided)

    g1_red = Spec("pkg-g color=red")
    g1_red.versions = vn.VersionList([vn.Version("1")])
    g2_red = Spec("pkg-g color=red")
    g2_red.versions = vn.VersionList([vn.Version("2")])
    g2_blue = Spec("pkg-g color=blue")
    g2_blue.versions = vn.VersionList([vn.Version("2")])
    g3_blue = Spec("pkg-g color=blue")
    g3_blue.versions = vn.VersionList([vn.Version("3")])

    depflag = dt.LINK | dt.BUILD
    e_red = Spec("pkg-e color=red")
    e_red._add_dependency(g1_red, depflag=depflag, virtuals=())
    e_blue = Spec("pkg-e color=blue")
    e_blue._add_dependency(g3_blue, depflag=depflag, virtuals=())

    d_red = Spec("pkg-d color=red")
    d_red._add_dependency(g1_red, depflag=depflag, virtuals=())
    d_blue = Spec("pkg-d color=blue")
    d_blue._add_dependency(g2_blue, depflag=depflag, virtuals=())

    b_red = Spec("pkg-b color=red")
    b_red._add_dependency(e_red, depflag=depflag, virtuals=())
    b_red._add_dependency(d_red, depflag=depflag, virtuals=())
    b_red._add_dependency(g1_red, depflag=depflag, virtuals=())

    f_blue = Spec("pkg-f color=blue")
    f_blue._add_dependency(e_blue, depflag=depflag, virtuals=())
    f_blue._add_dependency(g3_blue, depflag=depflag, virtuals=())

    c_red = Spec("pkg-c color=red")
    c_red._add_dependency(d_red, depflag=depflag, virtuals=())
    c_red._add_dependency(g2_red, depflag=depflag, virtuals=())
    c_blue = Spec("pkg-c color=blue")
    c_blue._add_dependency(d_blue, depflag=depflag, virtuals=())
    c_blue._add_dependency(f_blue, depflag=depflag, virtuals=())
    c_blue._add_dependency(g3_blue, depflag=depflag, virtuals=())

    a_red = Spec("pkg-a color=red")
    a_red._add_dependency(b_red, depflag=depflag, virtuals=())
    a_red._add_dependency(c_red, depflag=depflag, virtuals=())
    a_red._add_dependency(g2_red, depflag=depflag, virtuals=())

    for spec in [e_red, e_blue, d_red, d_blue, b_red, f_blue, c_red, c_blue, a_red]:
        spec.versions = vn.VersionList([vn.Version("1")])

        a_red._mark_concrete()
        c_blue._mark_concrete()

    return a_red, c_blue


@pytest.mark.usefixtures("config", "mock_packages")
class TestSpecSemantics:
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
            ("foo%gcc@4.5", "%gcc@4.4:4.6", "foo%gcc@4.5"),
            ("foo@2.0%gcc@4.5", "@1:3%gcc@4.4:4.6", "foo@2.0%gcc@4.5"),
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
            ("mpich foo==true", "mpich++foo", "mpich++foo"),
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
            ("mpich", "mpich++foo", "mpich++foo"),
            ("libelf+debug", "libelf+foo", "libelf+debug+foo"),
            ("libelf+debug", "libelf+debug+foo", "libelf+debug+foo"),
            ("libelf debug=2", "libelf foo=1", "libelf debug=2 foo=1"),
            ("libelf debug=2", "libelf debug=2 foo=1", "libelf debug=2 foo=1"),
            ("libelf+debug", "libelf~foo", "libelf+debug~foo"),
            ("libelf+debug", "libelf+debug~foo", "libelf+debug~foo"),
            ("libelf++debug", "libelf+debug+foo", "libelf+debug+foo"),
            ("libelf debug==2", "libelf foo=1", "libelf debug==2 foo=1"),
            ("libelf debug==2", "libelf debug=2 foo=1", "libelf debug=2 foo=1"),
            ("libelf++debug", "libelf++debug~foo", "libelf++debug~foo"),
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
            # Namespace (special case, but like variants
            ("builtin.libelf", "namespace=builtin", "builtin.libelf"),
            ("libelf", "namespace=builtin", "builtin.libelf"),
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
            (
                "libelf patches=ba5e334fe247335f3a116decfb5284100791dc302b5571ff5e664d8f9a6806c2",
                "libelf patches=ba5e3",  # constrain by a patch sha256 prefix
                "libelf patches=ba5e334fe247335f3a116decfb5284100791dc302b5571ff5e664d8f9a6806c2",
            ),
            # deptypes on direct deps
            (
                "mpileaks %[deptypes=build] mpich",
                "mpileaks %[deptypes=link] mpich",
                "mpileaks %[deptypes=build,link] mpich",
            ),
            # conditional edges
            (
                "libelf",
                "%[when='%c' virtuals=c]gcc ^[when='+mpi' virtuals=mpi]mpich",
                "libelf %[when='%c' virtuals=c]gcc ^[when='+mpi' virtuals=mpi]mpich",
            ),
            (
                "libelf %[when='%c' virtuals=c]gcc",
                "%[when='%c' virtuals=c]gcc@10.3.1",
                "libelf%[when='%c' virtuals=c]gcc@10.3.1",
            ),
            (
                "libelf %[when='%c' virtuals=c]gcc",
                "%[when='%c' virtuals=c]gcc@10.3.1 ^[when='+mpi'] mpich",
                "libelf%[when='%c' virtuals=c]gcc@10.3.1 ^[when='+mpi']mpich",
            ),
            (
                "libelf %[when='%c' virtuals=c]gcc",
                "%[when='%cxx' virtuals=cxx]gcc@10.3.1",
                "libelf%[when='%c' virtuals=c]gcc %[when='%cxx' virtuals=cxx]gcc@10.3.1",
            ),
            (
                "libelf %[when='+c' virtuals=c]gcc",
                "%[when='%c' virtuals=c]gcc@10.3.1",
                "libelf %[when='+c' virtuals=c]gcc %[when='%c' virtuals=c]gcc@10.3.1",
            ),
            # Edges under different when conditions are never in effect at the same time, so
            # they are two separate constraints even when they cannot both be met at once.
            (
                "libelf ^[when='+foo'] mpich@3.0",
                "^[when='+bar'] mpich@4.0",
                "libelf ^[when='+foo'] mpich@3.0 ^[when='+bar'] mpich@4.0",
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
        "lhs,rhs,expected_lhs,expected_rhs,propagated_lhs,propagated_rhs",
        [
            (
                'mpich cppflags="-O3"',
                'mpich cppflags="-O2"',
                'mpich cppflags="-O3 -O2"',
                'mpich cppflags="-O2 -O3"',
                [],
                [],
            ),
            (
                'mpich cflags="-O3 -g"',
                'mpich cflags=="-O3"',
                'mpich cflags=="-O3" cflags="-g"',
                'mpich cflags=="-O3" cflags="-g"',
                [("cflags", "-O3")],
                [("cflags", "-O3")],
            ),
            (
                'mpich cflags=="-O3 -g"',
                'mpich cflags=="-O3"',
                'mpich cflags=="-O3 -g"',
                'mpich cflags=="-O3 -g"',
                [("cflags", "-O3"), ("cflags", "-g")],
                [("cflags", "-O3"), ("cflags", "-g")],
            ),
            (
                "mpich cflags=-O2 cflags=-g cflags=-fPIC cflags==-pipe",
                "mpich cflags==-O2 cflags=-g cflags==-fPIC cflags=-pipe",
                "mpich cflags==-O2 cflags=-g cflags==-fPIC cflags==-pipe",
                "mpich cflags==-O2 cflags=-g cflags==-fPIC cflags==-pipe",
                [("cflags", "-O2"), ("cflags", "-fPIC"), ("cflags", "-pipe")],
                [("cflags", "-O2"), ("cflags", "-fPIC"), ("cflags", "-pipe")],
            ),
        ],
    )
    def test_constrain_compiler_flags(
        self, lhs, rhs, expected_lhs, expected_rhs, propagated_lhs, propagated_rhs
    ):
        """Constraining is asymmetric for compiler flags."""
        lhs, rhs, expected_lhs, expected_rhs = (
            Spec(lhs),
            Spec(rhs),
            Spec(expected_lhs),
            Spec(expected_rhs),
        )

        assert lhs.intersects(rhs)
        assert rhs.intersects(lhs)

        c1, c2 = lhs.copy(), rhs.copy()
        c1.constrain(rhs)
        c2.constrain(lhs)

        assert c1 == expected_lhs
        assert c2 == expected_rhs
        for x in [c1, c2]:
            assert x.satisfies(lhs)
            assert x.satisfies(rhs)

        def _propagated_flags(_spec):
            result = set()
            for flagtype in _spec.compiler_flags:
                for flag in _spec.compiler_flags[flagtype]:
                    if flag.propagate:
                        result.add((flagtype, flag))
            return result

        assert set(propagated_lhs) <= _propagated_flags(c1)
        assert set(propagated_rhs) <= _propagated_flags(c2)

    def test_constrain_specs_by_hash(self, database):
        """Test that Specs specified only by their hashes can constrain each other."""
        mpich_dag_hash = "/" + database.query_one("mpich").dag_hash()
        spec = Spec(mpich_dag_hash[:7])
        assert spec.constrain(mpich_dag_hash) is True
        assert spec.abstract_hash == mpich_dag_hash[1:]
        # the full hash is already there, so constraining with it again changes nothing
        assert spec.constrain(mpich_dag_hash) is False

    def test_constrain_extends_the_hash_on_an_edge(self, mock_packages):
        """The changed flag covers the abstract hash of a dependency too."""
        spec = Spec("%gcc")
        assert spec.constrain("%gcc/abc") is True
        assert spec.constrain("%gcc/abc") is False

    def test_failed_constrain_does_not_extend_the_hash(self, mock_packages):
        """The abstract hash merges after the compatibility checks, so a constraint that is
        rejected in another dimension leaves no hash behind."""
        lhs = Spec("pkg-b")
        with pytest.raises(UnsatisfiableSpecError):
            lhs.constrain("pkg-a/abcdef")
        assert lhs.abstract_hash is None
        assert lhs == Spec("pkg-b")

    def test_mismatched_constrain_spec_by_hash(self, database):
        """Test that Specs specified only by their incompatible hashes fail appropriately."""
        lhs = "/" + database.query_one("callpath ^mpich").dag_hash()
        rhs = "/" + database.query_one("callpath ^mpich2").dag_hash()
        with pytest.raises(spack.spec.InvalidHashError):
            Spec(lhs).constrain(Spec(rhs))
        with pytest.raises(spack.spec.InvalidHashError):
            Spec(lhs[:7]).constrain(Spec(rhs))

    @pytest.mark.parametrize(
        "lhs,rhs", [("libelf", Spec()), ("libelf", "@0:1"), ("libelf", "@0:1 %gcc")]
    )
    def test_concrete_specs_which_satisfies_abstract(self, lhs, rhs):
        """Test that constraining an abstract spec by a compatible concrete one makes the
        abstract spec concrete, and equal to the one it was constrained with.
        """
        lhs, rhs = spack.concretize.concretize_one(lhs), Spec(rhs)

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
            ("foo%gcc@4.3", "%gcc@4.4:4.6"),
            ("foo@4.0%gcc", "@1:3%gcc"),
            ("foo@4.0%gcc@4.5", "@1:3%gcc@4.4:4.6"),
            ("builtin.mock.mpich", "builtin.mpich"),
            ("mpileaks^mpi@3:", "^mpich2@1.4"),
            ("mpileaks^mpi@3:", "^mpich2"),
            ("mpileaks^mpi@3:", "^mpich@1.0"),
            ("mpich~foo", "mpich+foo"),
            ("mpich+foo", "mpich~foo"),
            ("mpich foo=True", "mpich foo=False"),
            ("mpich~~foo", "mpich++foo"),
            ("mpich++foo", "mpich~~foo"),
            ("mpich foo==True", "mpich foo==False"),
            ("libelf@0:2.0", "libelf@2.1:3"),
            ("libelf@0:2.5%gcc@4.8:4.9", "libelf@2.1:3%gcc@4.5:4.7"),
            ("libelf+debug", "libelf~debug"),
            ("libelf+debug~foo", "libelf+debug+foo"),
            ("libelf debug=True", "libelf debug=False"),
            ("namespace=builtin.mock", "namespace=builtin"),
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
        "lhs,rhs",
        [
            ("mpich", "mpich +foo"),
            ("mpich", "mpich~foo"),
            ("mpich", "mpich foo=1"),
            ("multivalue-variant foo=bar", "multivalue-variant +foo"),
            ("multivalue-variant foo=bar", "multivalue-variant ~foo"),
            ("multivalue-variant fee=bar", "multivalue-variant fee=baz"),
        ],
    )
    def test_concrete_specs_which_do_not_satisfy_abstract(self, lhs, rhs):
        lhs, rhs = spack.concretize.concretize_one(lhs), Spec(rhs)

        assert lhs.intersects(rhs) is False
        assert rhs.intersects(lhs) is False
        assert not lhs.satisfies(rhs)
        assert not rhs.satisfies(lhs)

        with pytest.raises(UnsatisfiableSpecError):
            assert lhs.constrain(rhs)

        with pytest.raises(UnsatisfiableSpecError):
            assert rhs.constrain(lhs)

    @pytest.mark.parametrize(
        "lhs,rhs", [("mpich", "mpich++foo"), ("mpich", "mpich~~foo"), ("mpich", "mpich foo==1")]
    )
    def test_concrete_specs_which_satisfy_abstract(self, lhs, rhs):
        lhs, rhs = spack.concretize.concretize_one(lhs), Spec(rhs)

        assert lhs.intersects(rhs)
        assert rhs.intersects(lhs)
        assert lhs.satisfies(rhs)

        s1 = lhs.copy()
        s1.constrain(rhs)
        assert s1 == lhs and s1.satisfies(lhs)

        s2 = rhs.copy()
        s2.constrain(lhs)
        assert s2 == lhs and s2.satisfies(lhs)

    @pytest.mark.parametrize(
        "lhs,rhs,expected,constrained",
        [
            # hdf5++mpi satisfies hdf5, and vice versa, because of the non-contradiction semantic
            ("hdf5++mpi", "hdf5", True, "hdf5++mpi"),
            ("hdf5", "hdf5++mpi", True, "hdf5++mpi"),
            # Same holds true for arbitrary propagated variants
            ("hdf5++mpi", "hdf5++shared", True, "hdf5++mpi++shared"),
            # Here hdf5+mpi satisfies hdf5++mpi but not vice versa
            ("hdf5++mpi", "hdf5+mpi", False, "hdf5+mpi"),
            ("hdf5+mpi", "hdf5++mpi", True, "hdf5+mpi"),
            # Non contradiction is violated
            ("hdf5 ^foo~mpi", "hdf5++mpi", False, "hdf5++mpi ^foo~mpi"),
            ("hdf5++mpi", "hdf5 ^foo~mpi", False, "hdf5++mpi ^foo~mpi"),
        ],
    )
    def test_abstract_specs_with_propagation(self, lhs, rhs, expected, constrained):
        """Tests (and documents) behavior of variant propagation on abstract specs.

        Propagated variants do not comply with subset semantic, making it difficult to give
        precise definitions. Here we document the behavior that has been decided for the
        practical cases we face.
        """
        lhs, rhs, constrained = Spec(lhs), Spec(rhs), Spec(constrained)
        assert lhs.satisfies(rhs) is expected

        c = lhs.copy()
        c.constrain(rhs)
        assert c == constrained

        c = rhs.copy()
        c.constrain(lhs)
        assert c == constrained

    def test_basic_satisfies_conditional_dep(self):
        """Tests basic semantic of satisfies with conditional dependencies, on a concrete spec"""
        concrete = spack.concretize.concretize_one("mpileaks ^mpich")

        # This branch exists, so the condition is met, and is satisfied
        assert concrete.satisfies("^[virtuals=mpi] mpich")
        assert concrete.satisfies("^[when='^notapackage' virtuals=mpi] mpich")
        assert concrete.satisfies("^[when='^mpi' virtuals=mpi] mpich")

        # This branch does not exist, but the condition is not met
        assert not concrete.satisfies("^zmpi")
        assert concrete.satisfies("^[when='^notapackage'] zmpi")
        assert not concrete.satisfies("^[when='^mpi'] zmpi")

    def test_concrete_satisfies_does_not_consult_repo(self, monkeypatch):
        """Tests that `satisfies()` on a concrete lhs doesn't need the provider index, when the rhs
        contains a virtual name.
        """
        concrete = spack.concretize.concretize_one("mpileaks ^mpich")

        # Reset the index, will raise if the `_provider_index` is ever removed as an attribute
        monkeypatch.setattr(spack.repo.PATH, "_provider_index", None)

        # Basic match and mismatch cases.
        assert concrete.satisfies("mpileaks")
        assert not concrete.satisfies("zlib")

        # Virtuals on a direct edge
        assert concrete.satisfies("%mpi")
        assert concrete.satisfies("%mpi@3")
        assert not concrete.satisfies("%mpi@5")
        assert concrete.satisfies("%mpi=mpich")
        assert not concrete.satisfies("%lapack")

        # Virtuals on a transitive edge
        assert concrete.satisfies("^mpi")
        assert concrete.satisfies("^mpi=mpich")
        assert not concrete.satisfies("^lapack")

        # Concrete spec asking about one of its concrete deps.
        mpich = concrete["mpich"]
        assert mpich.satisfies("mpich")
        assert mpich.satisfies("mpi")

        # We should not create again the index
        assert spack.repo.PATH._provider_index is None

    def test_concrete_contains_does_not_consult_repo(self, monkeypatch):
        """Tests that `foo in spec` on a concrete spec doesn't need the provider index, when the
        item contains a virtual name.
        """
        concrete = spack.concretize.concretize_one("mpileaks ^mpich")

        # Reset the index, will raise if the `_provider_index` is ever removed as an attribute
        monkeypatch.setattr(spack.repo.PATH, "_provider_index", None)

        assert "mpi" in concrete
        assert "c" in concrete

        # We should not create again the index
        assert spack.repo.PATH._provider_index is None

    def test_abstract_satisfies_with_lhs_provider_rhs_virtual(self):
        """If the left-hand side mentions a provider among dependencies and the right-hand side
        mentions a virtual among its deps, we only have satisfaction if the edge attribute
        specifies this virtual is provided."""
        assert not Spec("mpileaks ^mpich").satisfies("mpileaks ^mpi")
        assert not Spec("mpileaks %mpich").satisfies("mpileaks %mpi")
        assert Spec("mpileaks ^[virtuals=mpi] mpich").satisfies("mpileaks ^mpi")
        assert Spec("mpileaks %[virtuals=mpi] mpich").satisfies("mpileaks ^mpi")
        assert Spec("mpileaks %[virtuals=mpi] mpich").satisfies("mpileaks %mpi")

    def test_concrete_checks_on_virtual_names_dont_need_repo(self, monkeypatch):
        """Tests that ``%mpi`` or similar on a concrete spec doesn't need the repo"""
        concrete = spack.concretize.concretize_one("mpileaks ^mpich")

        # We don't need the repo
        monkeypatch.setattr(spack.repo, "PATH", None)

        assert concrete.satisfies("%mpi")
        assert concrete.satisfies("%c")
        assert concrete.satisfies("%c=gcc")
        assert concrete.satisfies("%mpi=mpich")

        assert not concrete.satisfies("%c,mpi=mpich")

    def test_satisfies_single_valued_variant(self):
        """Tests that the case reported in
        https://github.com/spack/spack/pull/2386#issuecomment-282147639
        is handled correctly.
        """
        a = spack.concretize.concretize_one("pkg-a foobar=bar")

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
        assert "^pkg-b" in a

    def test_unsatisfied_single_valued_variant(self):
        a = spack.concretize.concretize_one("pkg-a foobar=baz")
        assert "^pkg-b" not in a

        mv = spack.concretize.concretize_one("multivalue-variant")
        assert "pkg-a@1.0" not in mv

    def test_indirect_unsatisfied_single_valued_variant(self):
        spec = spack.concretize.concretize_one("singlevalue-variant-dependent")
        assert "pkg-a@1.0" not in spec

    def test_satisfied_namespace(self):
        spec = spack.concretize.concretize_one("zlib")
        assert spec.satisfies("namespace=builtin_mock")
        assert not spec.satisfies("namespace=builtin")

    def test_unset_namespace_does_not_satisfy_a_specified_one(self):
        assert Spec("builtin_mock.pkg-a").satisfies("pkg-a")
        assert not Spec("pkg-a").satisfies("builtin_mock.pkg-a")
        assert Spec("pkg-a").intersects("builtin_mock.pkg-a")
        assert Spec("builtin_mock.pkg-a").intersects("pkg-a")

    @pytest.mark.parametrize(
        "spec_string",
        [
            "tcl namespace==foobar",
            "tcl arch==foobar",
            "tcl os==foobar",
            "tcl patches==foobar",
            "tcl dev_path==foobar",
        ],
    )
    def test_propagate_reserved_variant_names(self, spec_string):
        with pytest.raises(spack.spec_parser.SpecParsingError, match="Propagation"):
            Spec(spec_string)

    def test_multivalued_variant_1(self):
        # Semantics for a multi-valued variant is different
        # Depending on whether the spec is concrete or not

        a = spack.concretize.concretize_one("multivalue-variant foo=bar")
        b = Spec("multivalue-variant foo=bar,baz")
        assert not a.satisfies(b)

    def test_multivalued_variant_2(self):
        a = Spec("multivalue-variant foo=bar")
        b = Spec("multivalue-variant foo=bar,baz")
        # The specs are abstract and they **could** be constrained
        assert b.satisfies(a) and not a.satisfies(b)
        # An abstract spec can instead be constrained
        assert a.constrain(b)

    def test_multivalued_variant_3(self):
        a = spack.concretize.concretize_one("multivalue-variant foo=bar,baz")
        b = Spec("multivalue-variant foo=bar,baz,quux")
        assert not a.satisfies(b)

    def test_multivalued_variant_4(self):
        a = Spec("multivalue-variant foo=bar,baz")
        b = Spec("multivalue-variant foo=bar,baz,quux")
        # The specs are abstract and they **could** be constrained
        assert a.intersects(b)
        # An abstract spec can instead be constrained
        assert a.constrain(b)
        # ...but will fail during concretization if there are
        # values in the variant that are not allowed
        with pytest.raises(InvalidVariantValueError):
            spack.concretize.concretize_one(a)

    def test_multivalued_variant_5(self):
        # This time we'll try to set a single-valued variant
        a = Spec("multivalue-variant fee=bar")
        b = Spec("multivalue-variant fee=baz")
        # The specs are abstract and they **could** be constrained,
        # as before concretization I don't know which type of variant
        # I have (if it is not a BV)
        assert a.intersects(b)
        # A variant cannot be parsed as single-valued until we try to
        # concretize. This means that we can constrain the variant above
        assert a.constrain(b)
        # ...but will fail during concretization if there are
        # multiple values set
        with pytest.raises(MultipleValuesInExclusiveVariantError):
            spack.concretize.concretize_one(a)

    def test_copy_satisfies_transitive(self):
        spec = spack.concretize.concretize_one("dttop")
        copy = spec.copy()
        for s, t in zip(spec.traverse(), copy.traverse()):
            assert s.satisfies(t)
            assert t.satisfies(s)

    def test_intersects_virtual(self):
        assert Spec("mpich").intersects(Spec("mpi"))
        assert Spec("mpich2").intersects(Spec("mpi"))
        assert Spec("zmpi").intersects(Spec("mpi"))

    def test_intersects_virtual_providers(self):
        """Tests that we can always intersect virtual providers from abstract specs.
        Concretization will give meaning to virtuals, and eventually forbid certain
        configurations.
        """
        assert Spec("netlib-lapack ^openblas").intersects("netlib-lapack ^openblas")
        assert Spec("netlib-lapack ^netlib-blas").intersects("netlib-lapack ^openblas")
        assert Spec("netlib-lapack ^openblas").intersects("netlib-lapack ^netlib-blas")
        assert Spec("netlib-lapack ^netlib-blas").intersects("netlib-lapack ^netlib-blas")

    def test_intersectable_concrete_specs_must_have_the_same_hash(self):
        """Ensure that concrete specs are matched *exactly* by hash."""
        s1 = spack.concretize.concretize_one("mpileaks")
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
        """Tests __getitem__ and __contains__ for specs."""
        s = spack.concretize.concretize_one("callpath")

        assert s["callpath"] == s

        # Real dependencies
        for key in ("dyninst", "libdwarf", "libelf"):
            assert isinstance(s[key], Spec)
            assert s[key].name == key
            assert key in s

        # Virtual dependencies
        assert s["mpi"].name == "mpich"
        assert "mpi" in s

    @pytest.mark.usefixtures("config")
    def test_virtual_index(self):
        s = spack.concretize.concretize_one("callpath")
        s_mpich = spack.concretize.concretize_one("callpath ^mpich")
        s_mpich2 = spack.concretize.concretize_one("callpath ^mpich2")
        s_zmpi = spack.concretize.concretize_one("callpath ^zmpi")

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
            ("mpileaks ^callpath %gcc@14", "mpileaks ^callpath %gcc@14.1"),
            ("mpileaks %[deptypes=build] mpich", "mpileaks %[deptypes=link] mpich"),
            ("mpileaks %mpich", "mpileaks %[deptypes=link] mpich"),
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
            ("mpileaks ^callpath %gcc@14.1", "mpileaks ^callpath %gcc@14"),
            ("mpileaks %[deptypes=build] gcc@14.1", "mpileaks %gcc@14"),
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

    def test_spec_formatting(self):
        spec = spack.concretize.concretize_one("multivalue-variant cflags=-O2")

        # Testing named strings ie {string} and whether we get
        # the correct component
        # Mixed case intentional to test both
        # Fields are as follow
        # fmt_str: the format string to test
        # sigil: the portion that is a sigil (may be empty string)
        # prop: the property to get
        # component: subcomponent of spec from which to get property
        package_segments = [
            ("{NAME}", "", "name", lambda spec: spec),
            ("{VERSION}", "", "version", lambda spec: spec),
            ("{compiler}", "", "compiler", lambda spec: spec),
            ("{compiler_flags}", "", "compiler_flags", lambda spec: spec),
            ("{variants}", "", "variants", lambda spec: spec),
            ("{architecture}", "", "architecture", lambda spec: spec),
            ("{@VERSIONS}", "@", "versions", lambda spec: spec),
            ("{%compiler}", "%", "compiler", lambda spec: spec),
            ("{arch=architecture}", "arch=", "architecture", lambda spec: spec),
            ("{namespace=namespace}", "namespace=", "namespace", lambda spec: spec),
            ("{compiler.name}", "", "name", lambda spec: spec.compiler),
            ("{compiler.version}", "", "version", lambda spec: spec.compiler),
            (
                "{compiler.version.up_to_1}",
                "",
                "up_to_1",
                lambda spec: spec.compiler.version.up_to(1),
            ),
            ("{%compiler.name}", "%", "name", lambda spec: spec.compiler),
            ("{@compiler.version}", "@", "version", lambda spec: spec.compiler),
            ("{architecture.platform}", "", "platform", lambda spec: spec.architecture),
            ("{architecture.os}", "", "os", lambda spec: spec.architecture),
            ("{architecture.target}", "", "target", lambda spec: spec.architecture),
            ("{prefix}", "", "prefix", lambda spec: spec),
            ("{external}", "", "external", lambda spec: spec),  # test we print "False"
        ]

        hash_segments = [
            ("{hash:7}", "", lambda s: s.dag_hash(7)),
            ("{/hash}", "/", lambda s: "/" + s.dag_hash()),
        ]

        variants_segments = [
            ("{variants.debug}", spec, "debug"),
            ("{variants.foo}", spec, "foo"),
            ("{^pkg-a.variants.bvv}", spec["pkg-a"], "bvv"),
            ("{^pkg-a.variants.foo}", spec["pkg-a"], "foo"),
        ]

        other_segments = [("{spack_root}", spack.paths.spack_root)]

        def depify(depname, fmt_str, sigil):
            sig = len(sigil)
            opening = fmt_str[: 1 + sig]
            closing = fmt_str[1 + sig :]
            return spec[depname], opening + f"^{depname}." + closing

        def check_prop(check_spec, fmt_str, prop, getter):
            actual = spec.format(fmt_str)
            expected = getter(check_spec)
            assert actual == str(expected).strip()

        for named_str, sigil, prop, get_component in package_segments:
            getter = lambda s: sigil + str(getattr(get_component(s), prop, ""))
            check_prop(spec, named_str, prop, getter)
            mpi, fmt_str = depify("mpi", named_str, sigil)
            check_prop(mpi, fmt_str, prop, getter)

        for named_str, sigil, getter in hash_segments:
            assert spec.format(named_str) == getter(spec)
            callpath, fmt_str = depify("callpath", named_str, sigil)
            assert spec.format(fmt_str) == getter(callpath)

        for named_str, test_spec, variant_name in variants_segments:
            assert test_spec.format(named_str) == str(test_spec.variants[variant_name])
            assert test_spec.format(named_str[:-1] + ".value}") == str(
                test_spec.variants[variant_name].value
            )

        for named_str, expected in other_segments:
            actual = spec.format(named_str)
            assert expected == actual

    @pytest.mark.parametrize(
        "fmt_str",
        [
            "{name}",
            "{version}",
            "{@version}",
            "{namespace}",
            "{ namespace=namespace}",
            "{ namespace =namespace}",
            "{ name space =namespace}",
            "{arch}",
            "{architecture}",
            "{arch=architecture}",
            "{  arch=architecture}",
            "{  arch =architecture}",
        ],
    )
    def test_spec_format_null_attributes(self, fmt_str):
        """Ensure that attributes format to empty strings when their values are null."""
        spec = spack.spec.Spec()
        assert spec.format(fmt_str) == ""

    def test_spec_formatting_spaces_in_key(self):
        spec = spack.concretize.concretize_one("multivalue-variant cflags=-O2")

        # test that spaces are preserved, if they come after some other text, otherwise
        # they are trimmed.
        # TODO: should we be trimming whitespace from formats? Probably not.
        assert spec.format("x{ arch=architecture}") == f"x arch={spec.architecture}"
        assert spec.format("x{ namespace=namespace}") == f"x namespace={spec.namespace}"
        assert spec.format("x{ name space =namespace}") == f"x name space ={spec.namespace}"
        assert spec.format("x{ os =os}") == f"x os ={spec.os}"

    @pytest.mark.parametrize(
        "fmt_str", ["{@name}", "{@version.concrete}", "{%compiler.version}", "{/hashd}"]
    )
    def test_spec_formatting_sigil_mismatches(self, fmt_str):
        spec = spack.concretize.concretize_one("multivalue-variant cflags=-O2")

        with pytest.raises(SpecFormatSigilError):
            spec.format(fmt_str)

    @pytest.mark.parametrize(
        "fmt_str",
        [
            r"{}",
            r"name}",
            r"\{name}",
            r"{name",
            r"{name\}",
            r"{_concrete}",
            r"{dag_hash}",
            r"{foo}",
            r"{spack_install}",
            r"{+variants.debug}",
            r"{variants.this_variant_does_not_exist}",
        ],
    )
    def test_spec_formatting_bad_formats(self, fmt_str):
        spec = spack.concretize.concretize_one("multivalue-variant cflags=-O2")
        with pytest.raises(SpecFormatStringError):
            spec.format(fmt_str)

    def test_wildcard_is_invalid_variant_value(self):
        """The spec string x=* is parsed as a multi-valued variant with values the empty set.
        That excludes * as a literal variant value."""
        with pytest.raises(spack.spec_parser.SpecParsingError, match="cannot use reserved value"):
            Spec("multivalue-variant foo=*,bar")

    def test_errors_in_variant_directive(self):
        variant = spack.directives.variant.__wrapped__

        class Pkg:
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
        assert " it is handled by an attribute of the 'values' argument" in str(exc_info.value)

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
        spec = spack.concretize.concretize_one("libelf target=x86_64")

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
    def test_splice(self, transitive):
        # Tests the new splice function in Spec using a somewhat simple case
        # with a variant with a conditional dependency.
        spec = spack.concretize.concretize_one("splice-t")
        dep = spack.concretize.concretize_one("splice-h+foo")

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

    def test_splice_intransitive_complex(self, setup_complex_splice):
        a_red, c_blue = setup_complex_splice

        spliced = a_red.splice(c_blue, transitive=False)
        assert spliced.satisfies(
            "pkg-a color=red ^pkg-b color=red ^pkg-c color=blue "
            "^pkg-d color=red ^pkg-e color=red ^pkg-f color=blue ^pkg-g@2 color=red"
        )
        assert set(spliced.dependencies(deptype=dt.BUILD)) == set()
        assert spliced.build_spec == a_red

        # We cannot check spliced["b"].build_spec is spliced["b"] because Spec.__getitem__ creates
        # a new wrapper object on each invocation. So we select once and check on that object
        # For the rest of the unchanged specs we will just check the s._build_spec is None.
        b = spliced["pkg-b"]
        assert b == a_red["pkg-b"]
        assert b.build_spec is b
        assert set(b.dependents()) == {spliced}

        assert spliced["pkg-c"].satisfies(
            "pkg-c color=blue ^pkg-d color=red ^pkg-e color=red "
            "^pkg-f color=blue ^pkg-g@2 color=red"
        )
        assert set(spliced["pkg-c"].dependencies(deptype=dt.BUILD)) == set()
        assert spliced["pkg-c"].build_spec == c_blue
        assert set(spliced["pkg-c"].dependents()) == {spliced}

        assert spliced["pkg-d"] == a_red["pkg-d"]
        assert spliced["pkg-d"]._build_spec is None
        # Since D had a parent changed, it has a split edge for link vs build dependent
        # note: spliced["b"] == b_red, referenced differently to preserve logic
        assert set(spliced["pkg-d"].dependents()) == {
            spliced["pkg-b"],
            spliced["pkg-c"],
            a_red["pkg-c"],
        }
        assert set(spliced["pkg-d"].dependents(deptype=dt.BUILD)) == {
            a_red["pkg-b"],
            a_red["pkg-c"],
        }

        assert spliced["pkg-e"] == a_red["pkg-e"]
        assert spliced["pkg-e"]._build_spec is None
        # Because a copy of e is used, it does not have dependnets in the original specs
        assert set(spliced["pkg-e"].dependents()) == {spliced["pkg-b"], spliced["pkg-f"]}
        # Build dependent edge to f because f originally depended on the e this was copied from
        assert set(spliced["pkg-e"].dependents(deptype=dt.BUILD)) == {spliced["pkg-b"]}

        assert spliced["pkg-f"].satisfies("pkg-f color=blue ^pkg-e color=red ^pkg-g@2 color=red")
        assert set(spliced["pkg-f"].dependencies(deptype=dt.BUILD)) == set()
        assert spliced["pkg-f"].build_spec == c_blue["pkg-f"]
        assert set(spliced["pkg-f"].dependents()) == {spliced["pkg-c"]}

        # spliced["pkg-g"] is g2, but spliced["pkg-b"]["pkg-g"] is g1
        assert spliced["pkg-g"] == a_red["pkg-g"]
        assert spliced["pkg-g"]._build_spec is None
        assert set(spliced["pkg-g"].dependents(deptype=dt.LINK)) == {
            spliced,
            spliced["pkg-c"],
            spliced["pkg-f"],
            a_red["pkg-c"],
        }

        assert spliced["pkg-b"]["pkg-g"] == a_red["pkg-b"]["pkg-g"]
        assert spliced["pkg-b"]["pkg-g"]._build_spec is None
        assert set(spliced["pkg-b"]["pkg-g"].dependents()) == {
            spliced["pkg-b"],
            spliced["pkg-d"],
            spliced["pkg-e"],
        }

        for edge in spliced.traverse_edges(cover="edges", deptype=dt.LINK | dt.RUN):
            # traverse_edges creates a synthetic edge with no deptypes to the root
            if edge.depflag:
                depflag = dt.LINK
                if not edge.parent.spliced:
                    depflag |= dt.BUILD
                assert edge.depflag == depflag

    def test_splice_transitive_complex(self, setup_complex_splice):
        a_red, c_blue = setup_complex_splice

        spliced = a_red.splice(c_blue, transitive=True)
        assert spliced.satisfies(
            "pkg-a color=red ^pkg-b color=red ^pkg-c color=blue ^pkg-d color=blue "
            "^pkg-e color=blue ^pkg-f color=blue ^pkg-g@3 color=blue"
        )
        assert set(spliced.dependencies(deptype=dt.BUILD)) == set()
        assert spliced.build_spec == a_red

        assert spliced["pkg-b"].satisfies(
            "pkg-b color=red ^pkg-d color=blue ^pkg-e color=blue ^pkg-g@2 color=blue"
        )
        assert set(spliced["pkg-b"].dependencies(deptype=dt.BUILD)) == set()
        assert spliced["pkg-b"].build_spec == a_red["pkg-b"]
        assert set(spliced["pkg-b"].dependents()) == {spliced}

        # We cannot check spliced["c"].build_spec is spliced["c"] because Spec.__getitem__ creates
        # a new wrapper object on each invocation. So we select once and check on that object
        # For the rest of the unchanged specs we will just check the s._build_spec is None.
        c = spliced["pkg-c"]
        assert c == c_blue
        assert c.build_spec is c
        assert set(c.dependents()) == {spliced}

        assert spliced["pkg-d"] == c_blue["pkg-d"]
        assert spliced["pkg-d"]._build_spec is None
        assert set(spliced["pkg-d"].dependents()) == {spliced["pkg-b"], spliced["pkg-c"]}

        assert spliced["pkg-e"] == c_blue["pkg-e"]
        assert spliced["pkg-e"]._build_spec is None
        assert set(spliced["pkg-e"].dependents()) == {spliced["pkg-b"], spliced["pkg-f"]}

        assert spliced["pkg-f"] == c_blue["pkg-f"]
        assert spliced["pkg-f"]._build_spec is None
        assert set(spliced["pkg-f"].dependents()) == {spliced["pkg-c"]}

        # spliced["g"] is g3, but spliced["d"]["g"] is g1
        assert spliced["pkg-g"] == c_blue["pkg-g"]
        assert spliced["pkg-g"]._build_spec is None
        assert set(spliced["pkg-g"].dependents(deptype=dt.LINK)) == {
            spliced,
            spliced["pkg-b"],
            spliced["pkg-c"],
            spliced["pkg-e"],
            spliced["pkg-f"],
        }
        # Because a copy of g3 is used, it does not have dependents in the original specs
        # It has build dependents on these spliced specs because it is an unchanged dependency
        # for them
        assert set(spliced["pkg-g"].dependents(deptype=dt.BUILD)) == {
            spliced["pkg-c"],
            spliced["pkg-e"],
            spliced["pkg-f"],
        }

        assert spliced["pkg-d"]["pkg-g"] == c_blue["pkg-d"]["pkg-g"]
        assert spliced["pkg-d"]["pkg-g"]._build_spec is None
        assert set(spliced["pkg-d"]["pkg-g"].dependents()) == {spliced["pkg-d"]}

        for edge in spliced.traverse_edges(cover="edges", deptype=dt.LINK | dt.RUN):
            # traverse_edges creates a synthetic edge with no deptypes to the root
            if edge.depflag:
                depflag = dt.LINK
                if not edge.parent.spliced:
                    depflag |= dt.BUILD
                assert edge.depflag == depflag

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_with_cached_hashes(self, transitive):
        spec = spack.concretize.concretize_one("splice-t")
        dep = spack.concretize.concretize_one("splice-h+foo")

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
    def test_splice_input_unchanged(self, transitive):
        spec = spack.concretize.concretize_one("splice-t")
        dep = spack.concretize.concretize_one("splice-h+foo")
        orig_spec_hash = spec.dag_hash()
        orig_dep_hash = dep.dag_hash()
        spec.splice(dep, transitive)
        # Post-splice, dag hash should still be different; no changes should be
        # made to these specs.
        assert spec.dag_hash() == orig_spec_hash
        assert dep.dag_hash() == orig_dep_hash

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_subsequent(self, transitive):
        spec = spack.concretize.concretize_one("splice-t")
        dep = spack.concretize.concretize_one("splice-h+foo")
        out = spec.splice(dep, transitive)

        # Now we attempt a second splice.
        dep = spack.concretize.concretize_one("splice-z+bar")

        # Transitivity shouldn't matter since Splice Z has no dependencies.
        out2 = out.splice(dep, transitive)
        assert out2.concrete
        assert out2["splice-z"].dag_hash() != spec["splice-z"].dag_hash()
        assert out2["splice-z"].dag_hash() != out["splice-z"].dag_hash()
        assert out2["splice-t"].build_spec.dag_hash() == spec["splice-t"].dag_hash()
        assert out2.spliced

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_dict(self, transitive):
        spec = spack.concretize.concretize_one("splice-t")
        dep = spack.concretize.concretize_one("splice-h+foo")
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
    def test_splice_dict_roundtrip(self, transitive):
        spec = spack.concretize.concretize_one("splice-t")
        dep = spack.concretize.concretize_one("splice-h+foo")
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
        with pytest.raises(UnknownVariantError):
            spack.concretize.concretize_one(s)

    @pytest.mark.regression("18527")
    def test_satisfies_dependencies_ordered(self):
        d = Spec("zmpi")
        d._add_dependency(Spec("fake"), depflag=dt.LINK, virtuals=())
        s = Spec("mpileaks")
        s._add_dependency(d, depflag=dt.LINK, virtuals=())
        assert s.satisfies("mpileaks ^zmpi ^fake")

    def test_satisfies_transitive_dependencies_require_link_run_path(self):
        """A ^dep constraint is satisfied by a direct dependency of any type, or one in the
        link/run closure. zmpi's gcc may concretize to a pure build dependency, which is
        neither, so deptype-less edges are not traversed."""
        assert Spec("mpileaks ^zmpi %gcc").satisfies("^zmpi")
        assert not Spec("mpileaks ^zmpi %gcc").satisfies("^gcc")
        assert not Spec("mpileaks ^[deptypes=link] zmpi %gcc").satisfies("^gcc")

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_swap_names(self, transitive):
        spec = spack.concretize.concretize_one("splice-vt")
        dep = spack.concretize.concretize_one("splice-a+foo")
        out = spec.splice(dep, transitive)
        assert dep.name in out
        assert transitive == ("+foo" in out["splice-z"])

    @pytest.mark.parametrize("transitive", [True, False])
    def test_splice_swap_names_mismatch_virtuals(self, transitive):
        vt = spack.concretize.concretize_one("splice-vt")
        vh = spack.concretize.concretize_one("splice-vh+foo")
        with pytest.raises(spack.spec.SpliceError, match="virtual"):
            vt.splice(vh, transitive)

    def test_adaptor_optflags(self):
        """Tests that we can obtain the list of optflags, and debugflags,
        from the compiler adaptor, and that this list is taken from the
        appropriate compiler package.
        """
        # pkg-a depends on c, so only the gcc compiler should be chosen
        spec = spack.concretize.concretize_one(Spec("pkg-a %gcc"))
        assert "-Otestopt" in spec.package.compiler.opt_flags
        # This is not set, make sure we get an empty list
        for x in spec.package.compiler.debug_flags:
            pass

    def test_spec_override(self):
        init_spec = Spec("pkg-a foo=baz foobar=baz cflags=-O3 cxxflags=-O1")
        change_spec = Spec("pkg-a foo=fee cflags=-O2")
        new_spec = spack.concretize.concretize_one(Spec.override(init_spec, change_spec))
        assert "foo=fee" in new_spec
        # This check fails without concretizing: apparently if both specs are
        # abstract, then the spec will always be considered to satisfy
        # 'variant=value' (regardless of whether it in fact does).
        assert "foo=baz" not in new_spec
        assert "foobar=baz" in new_spec
        assert new_spec.compiler_flags["cflags"] == ["-O2"]
        assert new_spec.compiler_flags["cxxflags"] == ["-O1"]

    def test_spec_override_with_nonexisting_variant(self):
        init_spec = Spec("pkg-a foo=baz foobar=baz cflags=-O3 cxxflags=-O1")
        change_spec = Spec("pkg-a baz=fee")
        with pytest.raises(ValueError):
            Spec.override(init_spec, change_spec)

    def test_spec_override_with_variant_not_in_init_spec(self):
        init_spec = Spec("pkg-a foo=baz foobar=baz cflags=-O3 cxxflags=-O1")
        change_spec = Spec("pkg-a +bvv ~lorem_ipsum")
        new_spec = spack.concretize.concretize_one(Spec.override(init_spec, change_spec))
        assert "+bvv" in new_spec
        assert "~lorem_ipsum" in new_spec

    @pytest.mark.parametrize(
        "spec_str,specs_in_dag",
        [
            ("hdf5 ^[virtuals=mpi] mpich", [("mpich", "mpich"), ("mpi", "mpich")]),
            # Try different combinations with packages that provides a
            # disjoint set of virtual dependencies
            (
                "netlib-scalapack ^mpich ^openblas-with-lapack",
                [
                    ("mpi", "mpich"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            (
                "netlib-scalapack ^[virtuals=mpi] mpich ^openblas-with-lapack",
                [
                    ("mpi", "mpich"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            (
                "netlib-scalapack ^mpich ^[virtuals=lapack] openblas-with-lapack",
                [
                    ("mpi", "mpich"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            (
                "netlib-scalapack ^[virtuals=mpi] mpich ^[virtuals=lapack] openblas-with-lapack",
                [
                    ("mpi", "mpich"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            # Test that we can mix dependencies that provide an overlapping
            # sets of virtual dependencies
            (
                "netlib-scalapack ^[virtuals=mpi] intel-parallel-studio "
                "^[virtuals=lapack] openblas-with-lapack",
                [
                    ("mpi", "intel-parallel-studio"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            (
                "netlib-scalapack ^[virtuals=mpi] intel-parallel-studio ^openblas-with-lapack",
                [
                    ("mpi", "intel-parallel-studio"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            (
                "netlib-scalapack ^intel-parallel-studio ^[virtuals=lapack] openblas-with-lapack",
                [
                    ("mpi", "intel-parallel-studio"),
                    ("lapack", "openblas-with-lapack"),
                    ("blas", "openblas-with-lapack"),
                ],
            ),
            # Test that we can bind more than one virtual to the same provider
            (
                "netlib-scalapack ^[virtuals=lapack,blas] openblas-with-lapack",
                [("lapack", "openblas-with-lapack"), ("blas", "openblas-with-lapack")],
            ),
        ],
    )
    def test_virtual_deps_bindings(self, spec_str, specs_in_dag):
        s = spack.concretize.concretize_one(spec_str)
        for label, expected in specs_in_dag:
            assert label in s
            assert s[label].satisfies(expected), label

    @pytest.mark.parametrize(
        "spec_str",
        [
            # openblas-with-lapack needs to provide blas and lapack together
            "netlib-scalapack ^[virtuals=blas] intel-parallel-studio ^openblas-with-lapack",
            # intel-* provides blas and lapack together, openblas can provide blas only
            "netlib-scalapack ^[virtuals=lapack] intel-parallel-studio ^openblas",
        ],
    )
    def test_unsatisfiable_virtual_deps_bindings(self, spec_str):
        with pytest.raises(spack.solver.asp.UnsatisfiableSpecError):
            spack.concretize.concretize_one(spec_str)

    @pytest.mark.parametrize(
        "spec_str,abstract_tests,concrete_tests",
        [
            # Ensure the 'when=+debug' is referred to 'callpath', and not to 'mpileaks',
            # and that we can concretize the spec despite 'callpath' has no debug variant
            (
                "mpileaks+debug ^callpath %[when=+debug virtuals=mpi] zmpi",
                [
                    ("^zmpi", False),
                    ("^mpich", False),
                    ("mpileaks+debug  %[when=+debug virtuals=mpi] zmpi", False),
                ],
                [("^zmpi", False), ("^[virtuals=mpi] mpich", True)],
            ),
            # Ensure we don't skip conditional edges when testing because we associate them
            # with the wrong node (e.g. mpileaks instead of mpich)
            (
                "mpileaks~debug ^mpich+debug %[when=+debug virtuals=c] llvm",
                [("^mpich+debug %[when=+debug virtuals=c] gcc", False)],
                [("^mpich %[virtuals=c] gcc", False), ("^mpich %[virtuals=c] llvm", True)],
            ),
        ],
    )
    def test_conditional_dependencies_satisfies(self, spec_str, abstract_tests, concrete_tests):
        """Tests satisfaction semantics for conditional specs, in different scenarios."""
        s = Spec(spec_str)
        for c, result in abstract_tests:
            assert s.satisfies(c) is result

        concrete = spack.concretize.concretize_one(spec_str)
        for c, result in concrete_tests:
            assert concrete.satisfies(c) is result


@pytest.mark.parametrize(
    "spec_str,format_str,expected",
    [
        ("git-test@git.foo/bar", "{name}-{version}", str(pathlib.Path("git-test-git.foo_bar"))),
        ("git-test@git.foo/bar", "{name}-{version}-{/hash}", None),
        ("git-test@git.foo/bar", "{name}/{version}", str(pathlib.Path("git-test", "git.foo_bar"))),
        # {compiler} is 'none' if a package does not depend on C, C++, or Fortran
        (
            f"git-test@{'a' * 40}=1.0%gcc",
            "{name}/{version}/{compiler}",
            str(pathlib.Path("git-test", f"{'a' * 40}_1.0", "none")),
        ),
        (
            "git-test@git.foo/bar=1.0%gcc",
            "{name}/{version}/{compiler}",
            str(pathlib.Path("git-test", "git.foo_bar_1.0", "none")),
        ),
    ],
)
def test_spec_format_path(spec_str, format_str, expected, mock_git_test_package):
    _check_spec_format_path(spec_str, format_str, expected)


def _check_spec_format_path(spec_str, format_str, expected, path_ctor=None):
    spec = Spec(spec_str)
    if not expected:
        with pytest.raises((spack.spec.SpecFormatPathError, spack.spec.SpecFormatStringError)):
            spec.format_path(format_str, _path_ctor=path_ctor)
    else:
        formatted = spec.format_path(format_str, _path_ctor=path_ctor)
        assert formatted == expected


@pytest.mark.parametrize(
    "spec_str,format_str,expected",
    [
        (
            "git-test@git.foo/bar",
            r"C:\\installroot\{name}\{version}",
            r"C:\installroot\git-test\git.foo_bar",
        ),
        (
            "git-test@git.foo/bar",
            r"\\hostname\sharename\{name}\{version}",
            r"\\hostname\sharename\git-test\git.foo_bar",
        ),
        # leading '/' is preserved on windows but converted to '\'
        # note that it's still not "absolute" -- absolute windows paths start with a drive.
        (
            "git-test@git.foo/bar",
            r"/installroot/{name}/{version}",
            r"\installroot\git-test\git.foo_bar",
        ),
    ],
)
def test_spec_format_path_windows(spec_str, format_str, expected, mock_git_test_package):
    _check_spec_format_path(spec_str, format_str, expected, path_ctor=pathlib.PureWindowsPath)


@pytest.mark.parametrize(
    "spec_str,format_str,expected",
    [
        (
            "git-test@git.foo/bar",
            r"/installroot/{name}/{version}",
            "/installroot/git-test/git.foo_bar",
        ),
        (
            "git-test@git.foo/bar",
            r"//installroot/{name}/{version}",
            "//installroot/git-test/git.foo_bar",
        ),
        # This is likely unintentional on Linux: Firstly, "\" is not a
        # path separator for POSIX, so this is treated as a single path
        # component (containing literal "\" characters); secondly,
        # Spec.format treats "\" as an escape character, so is
        # discarded (unless directly following another "\")
        (
            "git-test@git.foo/bar",
            r"C:\\installroot\package-{name}-{version}",
            r"C__installrootpackage-git-test-git.foo_bar",
        ),
        # "\" is not a POSIX separator, and Spec.format treats "\{" as a literal
        # "{", which means that the resulting format string is invalid
        ("git-test@git.foo/bar", r"package\{name}\{version}", None),
    ],
)
def test_spec_format_path_posix(spec_str, format_str, expected, mock_git_test_package):
    _check_spec_format_path(spec_str, format_str, expected, path_ctor=pathlib.PurePosixPath)


@pytest.mark.regression("3887")
@pytest.mark.parametrize("spec_str", ["py-extension2", "extension1", "perl-extension"])
def test_is_extension_after_round_trip_to_dict(config, mock_packages, spec_str):
    # x is constructed directly from string, y from a
    # round-trip to dict representation
    x = spack.concretize.concretize_one(spec_str)
    y = Spec.from_dict(x.to_dict())

    # Using 'y' since the round-trip make us lose build dependencies
    for d in y.traverse():
        assert x[d.name].package.is_extension == y[d.name].package.is_extension


def test_malformed_spec_dict():
    # FIXME: This test was really testing the specific implementation with an ad-hoc test
    with pytest.raises(SpecError, match="malformed"):
        Spec.from_dict(
            {"spec": {"_meta": {"version": 2}, "nodes": [{"dependencies": {"name": "foo"}}]}}
        )


def test_spec_dict_hashless_dep():
    # FIXME: This test was really testing the specific implementation with an ad-hoc test
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


def test_spec_installed(database):
    """Test whether Database.installed works."""
    # a known installed spec should say that it's installed
    specs = database.query()
    spec = specs[0]
    assert database.installed(spec)
    assert database.installed(spec.copy())

    # an abstract spec should say it's not installed
    spec = Spec("not-a-real-package")
    assert not database.installed(spec)

    # pkg-a is not in the mock DB and is not installed
    spec = spack.concretize.concretize_one("pkg-a")
    assert not database.installed(spec)


@pytest.mark.regression("30678")
def test_call_dag_hash_on_old_dag_hash_spec(mock_packages, config):
    # create a concrete spec
    a = spack.concretize.concretize_one("pkg-a")
    dag_hashes = {spec.name: spec.dag_hash() for spec in a.traverse()}

    # make it look like an old DAG hash spec with no package hash on the spec.
    for spec in a.traverse():
        assert spec.concrete
        spec._package_hash = None

    for spec in a.traverse():
        assert dag_hashes[spec.name] == spec.dag_hash()
        assert "package_hash" not in spec.to_node_dict()


def test_spec_trim(mock_packages, config):
    top = spack.concretize.concretize_one("dt-diamond")
    top.trim("dt-diamond-left")
    remaining = {x.name for x in top.traverse()}
    assert {
        "compiler-wrapper",
        "dt-diamond",
        "dt-diamond-right",
        "dt-diamond-bottom",
        "gcc-runtime",
        "gcc",
    } == remaining

    top.trim("dt-diamond-right")
    remaining = {x.name for x in top.traverse()}
    assert {"compiler-wrapper", "dt-diamond", "gcc-runtime", "gcc"} == remaining


@pytest.mark.regression("30861")
def test_concretize_partial_old_dag_hash_spec(mock_packages, config):
    # create an "old" spec with no package hash
    bottom = spack.concretize.concretize_one("dt-diamond-bottom")
    delattr(bottom, "_package_hash")

    dummy_hash = "zd4m26eis2wwbvtyfiliar27wkcv3ehk"
    bottom._hash = dummy_hash

    # add it to an abstract spec as a dependency
    top = Spec("dt-diamond")
    top.add_dependency_edge(bottom, depflag=0, virtuals=())

    # concretize with the already-concrete dependency
    top = spack.concretize.concretize_one(top)

    for spec in top.traverse():
        assert spec.concrete

    # make sure dag_hash is untouched
    assert spec["dt-diamond-bottom"].dag_hash() == dummy_hash
    assert spec["dt-diamond-bottom"]._hash == dummy_hash

    # make sure package hash is NOT recomputed
    assert not getattr(spec["dt-diamond-bottom"], "_package_hash", None)


def test_package_hash_affects_dunder_and_dag_hash(mock_packages, config):
    a1 = spack.concretize.concretize_one("pkg-a")
    a2 = spack.concretize.concretize_one("pkg-a")

    assert hash(a1) == hash(a2)
    assert a1.dag_hash() == a2.dag_hash()

    a1.clear_caches()
    a2.clear_caches()

    # tweak the dag hash of one of these specs
    new_hash = "00000000000000000000000000000000"
    if new_hash == a1._package_hash:
        new_hash = "11111111111111111111111111111111"
    a1._package_hash = new_hash

    assert hash(a1) != hash(a2)
    assert a1.dag_hash() != a2.dag_hash()


def test_intersects_and_satisfies_on_concretized_spec(config, mock_packages):
    """Test that a spec obtained by concretizing an abstract spec, satisfies the abstract spec
    but not vice-versa.
    """
    a1 = spack.concretize.concretize_one("pkg-a@1.0")
    a2 = Spec("pkg-a@1.0")

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
def test_abstract_provider_in_spec(abstract_spec, spec_str, config, mock_packages):
    s = spack.concretize.concretize_one(spec_str)
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
        (Spec, "gcc", "clang", (False, False, False)),
        (Spec, "gcc", "gcc@5", (True, False, True)),
        (Spec, "gcc@5", "gcc@5.3", (True, False, True)),
        (Spec, "gcc@5", "gcc@5-tag", (True, False, True)),
        # Flags (flags are a map, so for convenience we initialize a full Spec)
        # Note: the semantic is that of sv variants, not mv variants
        (Spec, "cppflags=-foo", "cppflags=-bar", (True, False, False)),
        (Spec, "cppflags='-bar -foo'", "cppflags=-bar", (True, True, False)),
        (Spec, "cppflags=-foo", "cppflags=-foo", (True, True, True)),
        (Spec, "cppflags=-foo", "cflags=-foo", (True, False, False)),
        # Versions
        (Spec, "@0.94h", "@:0.94i", (True, True, False)),
        # Different virtuals intersect if there is at least package providing both
        (Spec, "mpi", "lapack", (True, False, False)),
        (Spec, "mpi", "pkgconfig", (False, False, False)),
        # Intersection among target ranges for different architectures
        (Spec, "target=x86_64:", "target=ppc64le:", (False, False, False)),
        (Spec, "target=x86_64:", "target=:power9", (False, False, False)),
        (Spec, "target=:haswell", "target=:power9", (False, False, False)),
        (Spec, "target=:haswell", "target=ppc64le:", (False, False, False)),
        # Target ranges in one family: ":haswell" is a strict subset of "x86_64:", since x86_64
        # is the family root and broadwell and later are above haswell.
        (Spec, "target=:haswell", "target=x86_64:", (True, True, False)),
        (Spec, "target=:haswell", "target=x86_64_v4:", (False, False, False)),
        # Edge case of uarch that split in a diamond structure, from a common ancestor
        (Spec, "target=:cascadelake", "target=:cannonlake", (False, False, False)),
        # Spec with compilers
        (Spec, "mpileaks %gcc@5", "mpileaks %gcc@6", (False, False, False)),
        # %gcc sits behind an unpinned ^callpath edge, so callpath need not be one node:
        # an mpileaks with two callpath nodes, one per compiler, satisfies both sides.
        (Spec, "mpileaks ^callpath %gcc@5", "mpileaks ^callpath %gcc@6", (True, False, False)),
        (Spec, "mpileaks ^callpath %gcc@5", "mpileaks ^callpath %gcc@5.4", (True, False, True)),
    ],
)
def test_intersects_and_satisfies(mock_packages, factory, lhs_str, rhs_str, results):
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
        (Spec, "foo %gcc@5", "foo %gcc@5-tag", True, "foo %gcc@5-tag"),
        (Spec, "foo %gcc@5", "foo %gcc@5", False, "foo %gcc@5"),
        # Flags
        (Spec, "cppflags=-foo", "cppflags=-foo", False, "cppflags=-foo"),
        (Spec, "cppflags=-foo", "cflags=-foo", True, "cppflags=-foo cflags=-foo"),
        # Target ranges
        (Spec, "target=x86_64:", "target=x86_64:", False, "target=x86_64:"),
        (Spec, "target=x86_64:", "target=:haswell", True, "target=x86_64:haswell"),
        (
            Spec,
            "target=x86_64:haswell",
            "target=x86_64_v2:icelake",
            True,
            "target=x86_64_v2:haswell",
        ),
    ],
)
def test_constrain(factory, lhs_str, rhs_str, result, constrained_str, mock_packages):
    lhs = factory(lhs_str)
    rhs = factory(rhs_str)

    assert lhs.constrain(rhs) is result
    assert lhs == factory(constrained_str)

    # The intersection must be the same, so check that invariant too
    lhs = factory(lhs_str)
    rhs = factory(rhs_str)
    rhs.constrain(lhs)
    assert rhs == factory(constrained_str)


def test_constrain_promotes_edge_propagation(mock_packages):
    """Constraining an edge with a propagated edge to the same package promotes the policy; the
    reverse never demotes it."""
    lhs = Spec("mpileaks %callpath")
    assert lhs.constrain("mpileaks %%callpath")
    assert lhs == Spec("mpileaks %%callpath")

    lhs = Spec("mpileaks %%callpath")
    assert not lhs.constrain("mpileaks %callpath")
    assert lhs == Spec("mpileaks %%callpath")


def test_edge_propagation_is_part_of_spec_identity(mock_packages):
    """%callpath and %%callpath are different states even though they permit the same solutions,
    so they are distinct set elements, in line with to_dict, which serializes the policy."""
    plain, propagated = Spec("mpileaks %callpath"), Spec("mpileaks %%callpath")
    assert plain != propagated
    assert hash(plain) != hash(propagated)
    assert len({plain, propagated}) == 2


def test_constrain_dependencies_copies(mock_packages):
    """Tests that constraining a spec with new deps makes proper copies, and does not accidentally
    share dependency instances, leading to corruption of unrelated Spec instances."""
    x = Spec("root")
    y = Spec("^foo")
    z = Spec("%foo +bar")
    assert x.constrain(y)
    assert x == Spec("root ^foo")
    assert x.constrain(z)
    assert x == Spec("root %foo +bar")
    assert not x.constrain(Spec("root %foo +bar"))  # no new constraints
    # now, double check that we did not mutate `y` after constraining `x` with `z`.
    assert y == Spec("^foo")


def test_abstract_hash_intersects_and_satisfies(config, mock_packages):
    concrete: Spec = spack.concretize.concretize_one("pkg-a")
    hash = concrete.dag_hash()
    hash_5 = hash[:5]
    hash_6 = hash[:6]
    # abstract hash that doesn't have a common prefix with the others.
    hash_other = f"{'a' if hash_5[0] == 'b' else 'b'}{hash_5[1:]}"

    abstract_5 = Spec(f"pkg-a/{hash_5}")
    abstract_6 = Spec(f"pkg-a/{hash_6}")
    abstract_none = Spec(f"pkg-a/{hash_other}")
    abstract = Spec("pkg-a")

    def assert_subset(a: Spec, b: Spec):
        assert a.intersects(b) and b.intersects(a) and a.satisfies(b) and not b.satisfies(a)

    def assert_disjoint(a: Spec, b: Spec):
        assert (
            not a.intersects(b)
            and not b.intersects(a)
            and not a.satisfies(b)
            and not b.satisfies(a)
        )

    # left-hand side is more constrained, so its
    # concretization space is a subset of the right-hand side's
    assert_subset(concrete, abstract_5)
    assert_subset(abstract_6, abstract_5)
    assert_subset(abstract_5, abstract)

    # disjoint concretization space
    assert_disjoint(abstract_none, concrete)
    assert_disjoint(abstract_none, abstract_5)


def test_a_blank_sets_the_abstract_hash_off_from_any_value(mock_packages):
    """str() prints a blank before the abstract hash, so a value that can absorb a slash, a
    namespace, variant, flag or target, does not swallow it and the hash survives reparsing."""
    for spec_str in (
        "namespace=builtin_mock /abcdef",
        "foo=bar /abcdef",
        "pkg-a cflags=-O2 /abcdef",
        "pkg-a target=haswell /abcdef",
    ):
        spec = Spec(spec_str)
        round_tripped = Spec(str(spec))
        assert round_tripped.abstract_hash == spec.abstract_hash, spec_str


def test_edge_equality_does_not_depend_on_virtual_order():
    """Tests that two edges that are constructed with just a different order of the virtuals in
    the input parameters are equal to each other.
    """
    parent, child = Spec("parent"), Spec("child")
    edge1 = DependencySpec(parent, child, depflag=0, virtuals=("mpi", "lapack"))
    edge2 = DependencySpec(parent, child, depflag=0, virtuals=("lapack", "mpi"))
    assert edge1 == edge2
    assert tuple(sorted(edge1.virtuals)) == edge1.virtuals
    assert tuple(sorted(edge2.virtuals)) == edge1.virtuals


def test_update_virtuals():
    parent, child = Spec("parent"), Spec("child")
    edge = DependencySpec(parent, child, depflag=0, virtuals=("mpi", "lapack"))
    assert edge.update_virtuals("blas")
    assert edge.virtuals == ("blas", "lapack", "mpi")
    assert edge.update_virtuals(("c", "fortran", "mpi", "lapack"))
    assert edge.virtuals == ("blas", "c", "fortran", "lapack", "mpi")
    assert not edge.update_virtuals("mpi")
    assert not edge.update_virtuals(("c", "fortran", "mpi", "lapack"))
    assert edge.virtuals == ("blas", "c", "fortran", "lapack", "mpi")


def test_virtual_queries_work_for_strings_and_lists():
    """Ensure that ``dependencies()`` works with both virtuals=str and virtuals=[str, ...]."""
    parent, child = Spec("parent"), Spec("child")
    parent._add_dependency(
        child,
        depflag=dt.BUILD,
        virtuals=("cxx", "fortran"),  # multi-char dep names
    )

    assert not parent.dependencies(virtuals="c")  # not in virtuals but shares a char with cxx

    for lang in ["cxx", "fortran"]:
        assert parent.dependencies(virtuals=lang)  # string arg
        assert parent.edges_to_dependencies(virtuals=lang)  # string arg

        assert parent.dependencies(virtuals=[lang])  # list arg
        assert parent.edges_to_dependencies(virtuals=[lang])  # string arg


def test_old_format_strings_trigger_error(config, mock_packages):
    s = spack.concretize.concretize_one("pkg-a")
    with pytest.raises(SpecFormatStringError):
        s.format("${PACKAGE}-${VERSION}-${HASH}")


@pytest.mark.regression("47362")
@pytest.mark.parametrize(
    "lhs,rhs",
    [
        ("hdf5 +mpi", "hdf5++mpi"),
        ("hdf5 cflags==-g", "hdf5 cflags=-g"),
        ("hdf5 +mpi ++shared", "hdf5+mpi +shared"),
        ("hdf5 +mpi cflags==-g", "hdf5++mpi cflag=-g"),
    ],
)
def test_equality_discriminate_on_propagation(lhs, rhs):
    """Tests that == can discriminate abstract specs based on their 'propagation' status"""
    s, t = Spec(lhs), Spec(rhs)
    assert s != t
    assert len({s, t}) == 2


def test_comparison_multivalued_variants():
    assert Spec("x=a") < Spec("x=a,b") < Spec("x==a,b") < Spec("x==a,b,c")


@pytest.mark.parametrize(
    "specs_in_expected_order",
    [
        ("a", "b", "c", "d", "e"),
        ("a@1.0", "a@2.0", "b", "c@3.0", "c@4.0"),
        ("a^d", "b^c", "c^b", "d^a"),
        ("e^a", "e^b", "e^c", "e^d"),
        ("e^a@1.0", "e^a@2.0", "e^a@3.0", "e^a@4.0"),
        ("e^a@1.0 +a", "e^a@1.0 +b", "e^a@1.0 +c", "e^a@1.0 +c"),
        ("a^b%c", "a^b%d", "a^b%e", "a^b%f"),
        ("a^b%c@1.0", "a^b%c@2.0", "a^b%c@3.0", "a^b%c@4.0"),
        ("a^b%c@1.0 +a", "a^b%c@1.0 +b", "a^b%c@1.0 +c", "a^b%c@1.0 +d"),
        ("a cflags=-O1", "a cflags=-O2", "a cflags=-O3"),
        ("a %cmake@1.0 ^b %cmake@2.0", "a %cmake@2.0 ^b %cmake@1.0"),
        ("a^b^c^d", "a^b^c^e", "a^b^c^f"),
        ("a^b^c^d", "a^b^c^e", "a^b^c^e", "a^b^c^f"),
        ("a%b%c%d", "a%b%c%e", "a%b%c%e", "a%b%c%f"),
        ("d.a", "c.b", "b.c", "a.d"),  # names before namespaces
    ],
)
def test_spec_ordering(specs_in_expected_order):
    specs_in_expected_order = [Spec(s) for s in specs_in_expected_order]
    assert sorted(specs_in_expected_order) == specs_in_expected_order
    assert sorted(reversed(specs_in_expected_order)) == specs_in_expected_order

    for i in range(len(specs_in_expected_order) - 1):
        lhs, rhs = specs_in_expected_order[i : i + 2]
        assert lhs <= rhs
        assert (lhs < rhs and lhs != rhs) or lhs == rhs
        assert rhs >= lhs
        assert (rhs > lhs and rhs != lhs) or rhs == lhs


EMPTY_VER = vn.VersionList(":")
EMPTY_VAR = Spec().variants
EMPTY_FLG = Spec().compiler_flags


@pytest.mark.parametrize(
    "spec,expected_tuplified",
    [
        # simple, no dependencies
        [("a"), ((("a", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),), ())],
        # with some node attributes
        [
            ("a@1.0 +foo cflags='-O3 -g'"),
            (
                (
                    (
                        "a",
                        None,
                        vn.VersionList(["1.0"]),
                        Spec("+foo").variants,
                        Spec("cflags='-O3 -g'").compiler_flags,
                        None,
                        None,
                        None,
                    ),
                ),
                (),
            ),
        ],
        # single edge case
        [
            ("a^b"),
            (
                (
                    ("a", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("b", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                ),
                ((0, 1, 0, (), False, PropagationPolicy.NONE, Spec()),),
            ),
        ],
        # root with multiple deps
        [
            ("a^b^c^d"),
            (
                (
                    ("a", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("b", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("c", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("d", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                ),
                (
                    (0, 1, 0, (), False, PropagationPolicy.NONE, Spec()),
                    (0, 2, 0, (), False, PropagationPolicy.NONE, Spec()),
                    (0, 3, 0, (), False, PropagationPolicy.NONE, Spec()),
                ),
            ),
        ],
        # root with multiple build deps
        [
            ("a%b%c%d"),
            (
                (
                    ("a", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("b", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("c", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("d", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                ),
                (
                    (0, 1, 0, (), True, PropagationPolicy.NONE, Spec()),
                    (0, 2, 0, (), True, PropagationPolicy.NONE, Spec()),
                    (0, 3, 0, (), True, PropagationPolicy.NONE, Spec()),
                ),
            ),
        ],
        # dependencies with dependencies
        [
            ("a  ^b %c %d  ^e %f %g"),
            (
                (
                    ("a", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("b", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("e", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("c", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("d", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("f", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                    ("g", None, EMPTY_VER, EMPTY_VAR, EMPTY_FLG, None, None, None),
                ),
                (
                    (0, 1, 0, (), False, PropagationPolicy.NONE, Spec()),
                    (0, 2, 0, (), False, PropagationPolicy.NONE, Spec()),
                    (1, 3, 0, (), True, PropagationPolicy.NONE, Spec()),
                    (1, 4, 0, (), True, PropagationPolicy.NONE, Spec()),
                    (2, 5, 0, (), True, PropagationPolicy.NONE, Spec()),
                    (2, 6, 0, (), True, PropagationPolicy.NONE, Spec()),
                ),
            ),
        ],
    ],
)
def test_spec_canonical_comparison_form(spec, expected_tuplified):
    """Tests a few expected canonical comparison form of specs"""
    assert spack.util.lang.tuplify(Spec(spec)._cmp_iter) == expected_tuplified


def test_comparison_after_breaking_hash_change():
    # We simulate a breaking change in DAG hash computation in Spack. We have two specs that are
    # entirely equal modulo DAG hash. When deserializing these specs, we don't want them to compare
    # as equal, because DAG hash is used throughout in Spack to distinguish between specs
    # (e.g. database, build caches, install dir).
    s = Spec("example@=1.0")
    s._mark_concrete(True)

    # compute the dag hash and a change to it
    dag_hash = s.dag_hash()
    new_dag_hash = f"{'b' if dag_hash[0] == 'a' else 'a'}{dag_hash[1:]}"

    before_breakage = s.to_dict()
    after_breakage = s.to_dict()
    after_breakage["spec"]["nodes"][0]["hash"] = new_dag_hash
    assert before_breakage != after_breakage

    x = Spec.from_dict(before_breakage)
    y = Spec.from_dict(after_breakage)
    assert x != y
    assert len({x, y}) == 2


def test_satisfies_and_subscript_with_compilers(config, mock_packages):
    """Tests the semantic of "satisfies" and __getitem__ for the following spec:

    [    ]  multivalue-variant@2.3
    [bl  ]      ^callpath@1.0
    [bl  ]          ^dyninst@8.2
    [bl  ]              ^libdwarf@20130729
    [bl  ]              ^libelf@0.8.13
    [b   ]      ^gcc@10.2.1
    [ l  ]      ^gcc-runtime@10.2.1
    [bl  ]      ^mpich@3.0.4
    [bl  ]      ^pkg-a@2.0
    [b   ]          ^gmake@4.4
    [bl  ]          ^pkg-b@1.0
    """
    s = spack.concretize.concretize_one("multivalue-variant")

    # Check a direct build/link dependency
    assert s.satisfies("^pkg-a")
    assert s.dependencies(name="pkg-a")[0] == s["pkg-a"]

    # Transitive build/link dependency
    assert s.satisfies("^libelf")
    assert s["libdwarf"].dependencies(name="libelf")[0] == s["libelf"]

    # Direct build dependencies
    assert s.satisfies("^[virtuals=c] gcc")
    assert s.satisfies("%[virtuals=c] gcc")
    assert s.dependencies(name="gcc")[0] == s["gcc"]
    assert s.dependencies(name="gcc")[0] == s["c"]

    # Transitive build dependencies
    assert not s.satisfies("^gmake")

    # "gmake" is not in the link/run subdag + direct build deps
    with pytest.raises(KeyError):
        _ = s["gmake"]

    # We need to pass through "pkg-a" to get "gmake" with [] notation
    assert s["pkg-a"].dependencies(name="gmake")[0] == s["pkg-a"]["gmake"]


def test_flag_order_survives_formatting(mock_packages):
    """Compiler flags are printed in the order they are stored, grouped into runs that agree on
    whether they propagate. Flag order is significant to the build, so losing it changes the
    hash."""
    spec = Spec("pkg-a cflags==-O2").copy()
    spec.constrain(Spec("pkg-a cflags=-g"))
    assert [str(flag) for flag in spec.compiler_flags["cflags"]] == ["-O2", "-g"]
    assert str(spec) == "pkg-a cflags==-O2 cflags=-g"

    round_tripped = Spec(str(spec))
    assert [str(flag) for flag in round_tripped.compiler_flags["cflags"]] == ["-O2", "-g"]
    assert round_tripped.dag_hash() == spec.dag_hash()


def test_an_anonymous_spec_is_the_top_of_the_order_only(mock_packages):
    """A spec that leaves the name unset denotes every package, so everything is inside it and it
    is inside nothing that names one. Being the bottom too would break transitivity."""
    assert Spec("pkg-a").satisfies("")
    assert Spec("").satisfies("")
    assert not Spec("").satisfies("pkg-b")


def test_the_direct_flag_follows_concreteness(config, mock_packages):
    """A direct dependency is a constraint written with %, so the flag is set when a spec stops
    being concrete and cleared when it becomes concrete again."""
    mpileaks = spack.concretize.concretize_one("mpileaks")
    assert not any(edge.direct for edge in mpileaks.traverse_edges(root=False))

    mpileaks._mark_concrete(False)
    assert all(edge.direct for edge in mpileaks.traverse_edges(root=False))

    mpileaks._mark_concrete(True)
    assert not any(edge.direct for edge in mpileaks.traverse_edges(root=False))


def test_marking_an_abstract_spec_abstract_again_changes_nothing(mock_packages):
    """The direct flag only flips when the concreteness actually changes, so marking an abstract
    spec abstract leaves its transitive edges alone."""
    spec = Spec("mpileaks ^callpath")
    spec._mark_concrete(False)

    assert not spec.edges_to_dependencies(name="callpath")[0].direct
    assert not spec.satisfies("mpileaks %callpath")
    assert spec.satisfies("mpileaks ^callpath")


def test_a_spec_that_stopped_being_concrete_matches_a_direct_constraint(config, mock_packages):
    """A spec that stops being concrete keeps every edge it had, so a direct dependency
    constraint is matched by the package it depends on, and not by one further down."""
    mpileaks = spack.concretize.concretize_one("mpileaks")
    mpileaks._mark_concrete(False)

    assert mpileaks.satisfies("mpileaks %callpath")
    assert mpileaks.satisfies("mpileaks ^libelf")
    assert not mpileaks.satisfies("mpileaks %libelf")


def test_direct_constraint_nested_below_a_concrete_dependency(config, mock_packages):
    """A % constraint below ^ is checked on the node it applies to, so when that node is
    concrete its edges match without the direct flag, even if the root spec is abstract."""
    callpath = spack.concretize.concretize_one("callpath")
    root = Spec("mpileaks")
    root.add_dependency_edge(callpath, depflag=dt.BUILD | dt.LINK, virtuals=())

    assert root.satisfies("mpileaks ^callpath %dyninst")
    assert root.satisfies("mpileaks ^callpath ^libelf")
    assert not root.satisfies("mpileaks ^callpath %libelf")


def test_a_direct_dependency_is_inside_a_transitive_one(mock_packages):
    """'pkg-a ^pkg-b' means pkg-b is somewhere in the DAG and 'pkg-a %pkg-b' means it is a direct
    dependency, so the second is inside the first and not the other way around."""
    anywhere_in_dag = Spec("pkg-a ^pkg-b")
    direct_dependency = Spec("pkg-a %pkg-b")
    assert direct_dependency.satisfies(anywhere_in_dag)
    assert not anywhere_in_dag.satisfies(direct_dependency)


def test_every_edge_of_a_concrete_node_is_a_direct_dependency(mock_packages, config):
    """A concrete spec records its edges without the direct flag, but each of them is a direct
    dependency in fact, so it matches a direct constraint. A package further down does not."""
    mpileaks = spack.concretize.concretize_one("mpileaks")
    assert not mpileaks.edges_to_dependencies(name="callpath")[0].direct

    assert mpileaks.satisfies("mpileaks %callpath")
    assert mpileaks.satisfies("mpileaks ^libelf")
    assert not mpileaks.satisfies("mpileaks %libelf")


@pytest.mark.parametrize(
    "spec_str,spec_fmt,expected",
    [
        # Depends on C
        ("mpileaks", "{name}-{compiler.name}", "mpileaks-gcc"),
        ("mpileaks", "{name}-{compiler.name}-{compiler.version}", "mpileaks-gcc-10.2.1"),
        # No compiler
        ("pkg-c", "{name}-{compiler.name}", "pkg-c-none"),
        ("pkg-c", "{name}-{compiler.name}-{compiler.version}", "pkg-c-none-none"),
    ],
)
def test_spec_format_with_compiler_adaptors(spec_str, spec_fmt, expected, config, mock_packages):
    """Tests the output of spec format, when involving `Spec.compiler` adaptors"""
    s = spack.concretize.concretize_one(spec_str)
    assert s.format(spec_fmt) == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ("mpich %gcc", "mpich %gcc", True),
        ("mpich %gcc", "mpich ^gcc", False),
        ("mpich ^callpath %gcc", "mpich %gcc ^callpath", False),
    ],
)
def test_specs_equality(lhs, rhs, expected):
    """Tests the semantic of == for abstract specs"""
    lhs, rhs = Spec(lhs), Spec(rhs)
    assert (lhs == rhs) is expected


def test_edge_equality_accounts_for_when_condition():
    """Tests that edges can be distinguished by their 'when' condition."""
    parent, child = Spec("parent"), Spec("child")
    edge1 = DependencySpec(parent, child, depflag=0, virtuals=(), when=Spec("%c"))
    edge2 = DependencySpec(parent, child, depflag=0, virtuals=())
    assert edge1 != edge2


def test_long_spec():
    """Test that long_spec preserves dependency types and has correct ordering."""
    assert Spec("foo %m %l ^k %n %j").long_spec == "foo %l %m ^k %j %n"


@pytest.mark.parametrize(
    "constraints,expected",
    [
        # Anonymous specs without dependencies
        (["+baz", "+bar"], "+baz+bar"),
        (["@2.0:", "@:5.1", "+bar"], "@2.0:5.1 +bar"),
        # Anonymous specs with dependencies
        (["^mpich@3.2", "^mpich@:4.0+foo"], "^mpich@3.2 ^mpich@:4.0+foo"),
        # Mix a real package with a virtual one. This test
        # should fail if we start using the repository
        (["^mpich@3.2", "^mpi+foo"], "^mpich@3.2 ^mpi+foo"),
        # Non direct dependencies + direct dependencies
        (["^mpich", "%mpich"], "%mpich"),
        (["^foo", "^bar %foo"], "^foo ^bar%foo"),
        (["^foo", "%bar %foo"], "%bar%foo"),
    ],
)
def test_constrain_symbolically(constraints, expected):
    """Tests the semantics of constraining a spec when we don't resolve virtuals."""
    merged = Spec()
    for c in constraints:
        merged._constrain_symbolically(c)
    assert merged == Spec(expected)

    reverse_order = Spec()
    for c in reversed(constraints):
        reverse_order._constrain_symbolically(c)
    assert reverse_order == Spec(expected)


def test_constrain_does_not_share_flags_or_architecture_with_the_rhs(mock_packages):
    """A successful constrain copies what it takes from the right-hand side instead of aliasing
    it, so narrowing the left-hand side further cannot reach a spec that was only ever read."""
    lhs, rhs = Spec("pkg-a"), Spec("pkg-a cflags=-O2 target=x86_64:")
    lhs.constrain(rhs)
    before = rhs.to_dict()

    # -g extends the flag list, ==-O2 constrains the propagation of -O2, haswell the range
    lhs.constrain(Spec("pkg-a cflags==-O2 cflags=-g target=haswell"))
    assert rhs.to_dict() == before


def test_copy_does_not_share_flag_instances(mock_packages):
    """CompilerFlag is a mutable string in FlagMap; it should not be shared on copy."""
    old = Spec("pkg-a cflags=-O2 cflags==-g")
    new = old.copy()
    assert len(new.compiler_flags["cflags"]) == len(old.compiler_flags["cflags"]) == 2
    for x, y in zip(old.compiler_flags["cflags"], new.compiler_flags["cflags"]):
        assert x is not y
        assert x == y and x.propagate == y.propagate and x.flag_group == y.flag_group


@pytest.mark.parametrize(
    "parent_str,child_str,kwargs,expected_str,expected_repr",
    [
        (
            "mpileaks",
            "callpath",
            {"virtuals": ()},
            "mpileaks ^callpath",
            "DependencySpec('mpileaks', 'callpath', depflag=0, virtuals=())",
        ),
        (
            "mpileaks",
            "callpath",
            {"virtuals": ("mpi", "lapack")},
            "mpileaks ^[virtuals=lapack,mpi] callpath",
            "DependencySpec('mpileaks', 'callpath', depflag=0, virtuals=('lapack', 'mpi'))",
        ),
        (
            "",
            "callpath",
            {"virtuals": ("mpi", "lapack"), "direct": True},
            " %[virtuals=lapack,mpi] callpath",
            "DependencySpec('', 'callpath', depflag=0, virtuals=('lapack', 'mpi'), direct=True)",
        ),
        (
            "",
            "callpath",
            {
                "virtuals": ("mpi", "lapack"),
                "direct": True,
                "propagation": PropagationPolicy.PREFERENCE,
            },
            " %%[virtuals=lapack,mpi] callpath",
            "DependencySpec('', 'callpath', depflag=0, virtuals=('lapack', 'mpi'), direct=True,"
            " propagation=PropagationPolicy.PREFERENCE)",
        ),
        (
            "",
            "callpath",
            {"virtuals": (), "direct": True, "propagation": PropagationPolicy.PREFERENCE},
            " %%callpath",
            "DependencySpec('', 'callpath', depflag=0, virtuals=(), direct=True,"
            " propagation=PropagationPolicy.PREFERENCE)",
        ),
        (
            "mpileaks+foo",
            "callpath+bar",
            {"virtuals": (), "direct": True, "propagation": PropagationPolicy.PREFERENCE},
            "mpileaks+foo %%callpath+bar",
            "DependencySpec('mpileaks+foo', 'callpath+bar', depflag=0, virtuals=(), direct=True,"
            " propagation=PropagationPolicy.PREFERENCE)",
        ),
    ],
)
def test_edge_representation(parent_str, child_str, kwargs, expected_str, expected_repr):
    """Tests the string representations of edges."""
    parent = Spec(parent_str) or Spec()
    child = Spec(child_str) or Spec()
    edge = DependencySpec(parent, child, depflag=0, **kwargs)
    assert str(edge) == expected_str
    assert repr(edge) == expected_repr


def test_parallel_edges_sort_with_differing_propagation(mock_packages):
    """Two edges to one package that differ only in propagation are compared on that field, so
    ``PropagationPolicy`` needs ``<`` and not just ``==``."""
    edges = [
        DependencySpec(Spec("pkg-a"), Spec("pkg-e"), depflag=0, virtuals=(), direct=True),
        DependencySpec(
            Spec("pkg-a"),
            Spec("pkg-e"),
            depflag=0,
            virtuals=(),
            direct=True,
            propagation=PropagationPolicy.PREFERENCE,
        ),
    ]
    assert sorted(edges) == edges


def test_satisfies_tries_every_parallel_edge(mock_packages):
    """Satisfies is exhaustive when there are duplicates on abstract specs."""
    spec = Spec("pkg-a ^[deptypes=link] pkg-b %pkg-c ^[deptypes=build] pkg-b %pkg-e")
    assert spec.satisfies("pkg-a ^pkg-b %pkg-c")
    assert spec.satisfies("pkg-a ^pkg-b %pkg-e")
    assert not spec.satisfies("pkg-a ^pkg-b %pkg-c %pkg-e")


def test_satisfies_checks_all_in_edges_of_shared_node():
    """A node with multiple in-edges must be reachable through any of them; an in-edge that fails
    on edge attributes must not shadow a parallel in-edge that matches."""
    root, a, b, c = Spec("pkg-a"), Spec("pkg-b"), Spec("pkg-c"), Spec("pkg-d")
    root.add_dependency_edge(a, depflag=dt.LINK, virtuals=())
    root.add_dependency_edge(b, depflag=dt.LINK, virtuals=())
    a.add_dependency_edge(c, depflag=dt.TEST | dt.RUN, virtuals=())
    b.add_dependency_edge(c, depflag=dt.BUILD | dt.RUN, virtuals=())
    # each in-edge is the only match for one assertion, so either fails if satisfies stops at
    # the first in-edge of pkg-d regardless of iteration order
    assert root.satisfies("^[deptypes=test] pkg-d")  # only through pkg-b -> pkg-d
    assert root.satisfies("^[deptypes=build] pkg-d")  # only through pkg-c -> pkg-d
    assert root.satisfies("^[deptypes=run] pkg-d")  # through either in-edge
    assert not root.satisfies("^[deptypes=build,test] pkg-d")  # no single in-edge has both


def test_satisfies_tries_every_parallel_edge_of_a_concrete_spec(config, mock_packages):
    """Satisfies is exhaustive when there are duplicates on concrete specs."""
    # dupe-tool-root --build--> dupe-tool@1.0 --build--> cmake
    #                --link-->  dupe-tool-user --link--> dupe-tool@2.0 --build--> gmake
    spec = spack.concretize.concretize_one("dupe-tool-root")
    assert spec.satisfies("^[deptypes=build] dupe-tool@1")
    assert spec.satisfies("^[deptypes=link] dupe-tool@2")
    assert spec.satisfies("^[deptypes=build] dupe-tool@1 ^[deptypes=link] dupe-tool@2 %gmake")
    # each dupe-tool node is the only match for one assertion, so either fails if satisfies bails
    # out on the first dupe-tool it visits regardless of iteration order
    assert spec.satisfies("^dupe-tool %cmake")  # only dupe-tool@1.0
    assert spec.satisfies("^dupe-tool %gmake")  # only dupe-tool@2.0
    assert not spec.satisfies("^dupe-tool %cmake %gmake")  # no single node has both


@pytest.mark.parametrize(
    "spec_str,assertions",
    [
        # Check <key>=* semantics for a "regular" variant
        ("mpileaks foo=abc", [("foo=*", True), ("bar=*", False)]),
        # Check the semantics for architecture related key value pairs
        (
            "mpileaks",
            [
                ("target=*", False),
                ("os=*", False),
                ("platform=*", False),
                ("target=* platform=*", False),
            ],
        ),
        (
            "mpileaks target=x86_64",
            [
                ("target=*", True),
                ("os=*", False),
                ("platform=*", False),
                ("target=* platform=*", False),
            ],
        ),
        ("mpileaks os=debian6", [("target=*", False), ("os=*", True), ("platform=*", False)]),
        ("mpileaks platform=linux", [("target=*", False), ("os=*", False), ("platform=*", True)]),
        ("mpileaks platform=linux", [("target=*", False), ("os=*", False), ("platform=*", True)]),
        (
            "mpileaks platform=linux target=x86_64",
            [
                ("target=*", True),
                ("os=*", False),
                ("platform=*", True),
                ("target=* platform=*", True),
            ],
        ),
    ],
)
def test_attribute_existence_in_satisfies(spec_str, assertions, mock_packages, config):
    """Tests the semantics of <key>=* when used in Spec.satisfies"""
    s = Spec(spec_str)
    for test, expected in assertions:
        assert s.satisfies(test) is expected


@pytest.mark.regression("51768")
@pytest.mark.parametrize("spec_str", ["mpi", "%mpi", "^mpi", "%foo", "%c=gcc", "%[when=%c]c=gcc"])
def test_specs_semantics_on_self(spec_str, mock_packages, config):
    """Tests that an abstract spec satisfies and intersects with itself."""
    s = Spec(spec_str)
    assert s.satisfies(s)
    assert s.intersects(s)


@pytest.mark.parametrize(
    "spec_str,expected_fmt",
    [
        ("mpileaks@2.2", "mpileaks@_R{@=2.2}"),
        ("mpileaks@2.3", "mpileaks@c{@=2.3}"),
        ("mpileaks+debug", "@_R{+debug}"),
    ],
)
def test_highlighting_spec_parts(spec_str, expected_fmt, config, mock_packages):
    """Tests correct highlighting of non-default versions and variants"""
    s = spack.concretize.concretize_one(spec_str)
    expected = colorize(expected_fmt, color=True)

    colorized_str = s.format(
        color=True,
        version_style_fn=spack.package_base.non_preferred_version,
        variant_style_fn=spack.package_base.non_default_variant,
    )
    assert expected in colorized_str


@pytest.mark.parametrize("spec_str", ["mpileaks", "mpileaks ^zmpi"])
def test_mark_concrete_roundtrip_preserves_hashes(spec_str, config, mock_packages):
    """Tests that clearing concreteness and re-finalizing a spec must preserve the DAG hash of the
    root and of every transitive dependency.
    """
    s = spack.concretize.concretize_one(spec_str)

    # Record the DAG hash of every node in the DAG (root and transitive dependencies).
    original = {node.name: node.dag_hash() for node in s.traverse()}
    # Sanity check: we are exercising more than the root node.
    assert len(original) > 1

    # Un-mark concrete: this clears the cached hashes on every node in the DAG.
    s._mark_concrete(False)
    assert all(getattr(node, ht.dag_hash.attr) is None for node in s.traverse())

    # Re-finalize the DAG: the cleared hashes must recompute to the original values.
    s._finalize_concretization()
    roundtrip = {node.name: node.dag_hash() for node in s.traverse()}
    assert roundtrip == original


def test_edge_already_matched_is_not_copied_in(mock_packages):
    """An unconditional edge already covers a conditional edge to the same child, so constraining
    with it adds nothing: the conditional edge is paired with the one matching it, whichever spec
    it comes from."""
    unconditional, conditional = Spec("%pkg-e"), Spec("%[when='+bvv'] pkg-e")
    assert unconditional.intersects(conditional)
    assert conditional.intersects(unconditional)

    forward = unconditional.constrained(conditional)
    backward = conditional.constrained(unconditional)
    assert forward == unconditional
    assert backward == unconditional
    assert forward.to_dict() == backward.to_dict()


def test_edges_differing_in_namespace_stay_parallel(mock_packages):
    """`^pkg-b@1` does not satisfy `^builtin_mock.pkg-b` and vice versa: a concrete spec can have
    a builtin_mock node next to a pkg-b@1 node from another repo, so the merge keeps both edges.
    An edge that does have the namespace absorbs the one it satisfies."""
    lhs, rhs = Spec("pkg-a ^pkg-b@1"), Spec("pkg-a ^builtin_mock.pkg-b")
    forward, backward = lhs.constrained(rhs), rhs.constrained(lhs)
    assert forward.to_dict() == backward.to_dict()
    assert forward == Spec("pkg-a ^pkg-b@1 ^builtin_mock.pkg-b")
    assert len(forward.edges_to_dependencies(name="pkg-b")) == 2

    lhs, rhs = Spec("pkg-a ^pkg-b@1"), Spec("pkg-a ^builtin_mock.pkg-b@1")
    forward, backward = lhs.constrained(rhs), rhs.constrained(lhs)
    assert forward.to_dict() == backward.to_dict()
    assert forward == Spec("pkg-a ^builtin_mock.pkg-b@1")


def test_edge_propagation_is_merged(mock_packages):
    """A propagated edge constrains the whole DAG, so it satisfies its unpropagated counterpart,
    and constrain keeps the propagated policy from whichever spec has it."""
    lhs, rhs = Spec("pkg-a ^pkg-b"), Spec("pkg-a %%pkg-b")
    forward = lhs.copy()
    forward.constrain(rhs)
    backward = rhs.copy()
    backward.constrain(lhs)
    assert forward.to_dict() == backward.to_dict()
    assert forward == Spec("pkg-a %%pkg-b")


def test_edge_propagation_is_merged_at_parse_time(mock_packages):
    """Duplicate % clauses to one name merge into a single direct edge that keeps the propagated
    policy, whichever clause states it."""
    assert Spec("mpileaks %callpath %%callpath") == Spec("mpileaks %%callpath")
    assert Spec("mpileaks %%callpath %callpath") == Spec("mpileaks %%callpath")


def test_satisfies_ignores_edge_propagation(mock_packages):
    """%% expresses a preference the solver may override, so it does not narrow the set of DAGs:
    satisfaction ignores it in both directions. This is one factor that makes the set of Spec
    objects a preorder under satisfies instead of a partial order."""
    assert Spec("mpileaks %%callpath").satisfies("mpileaks %callpath")
    assert Spec("mpileaks %callpath").satisfies("mpileaks %%callpath")


def test_conditional_propagated_edge_is_not_redundant(mock_packages):
    """Satisfaction ignores edge propagation, but the edge redundancy check does not ignore it when
    merging edges."""
    s = Spec("mpileaks %callpath %%[when='+foo'] callpath")
    assert s == Spec("mpileaks %%[when='+foo'] callpath %callpath")
    assert len(s.edges_to_dependencies(name="callpath")) == 2

    t = Spec("mpileaks %%[when='+foo'] callpath")
    assert t.constrain("mpileaks %callpath")
    assert t == s

    # with equal propagation on both edges, the conditional edge is redundant and discarded
    assert Spec("mpileaks %%callpath %%[when='+foo'] callpath") == Spec("mpileaks %%callpath")
    assert Spec("mpileaks %callpath %[when='+foo'] callpath") == Spec("mpileaks %callpath")


def test_direct_and_indirect_provider_of_one_virtual_stay_apart(mock_packages):
    """A direct provider and an indirect one need not be the same node: '%c=llvm ^c=gcc' is
    built with llvm but uses gcc somewhere at runtime."""
    spec = Spec("mpileaks %c=llvm ^c=gcc")
    assert spec.satisfies("%c=llvm")
    assert spec.satisfies("^c=gcc")
    assert len(spec.edges_to_dependencies()) == 2


def test_two_providers_of_one_virtual_merge_as_parallel_edges(mock_packages):
    """Two edges naming different providers of one virtual are two requirements, each matched
    anywhere in the DAG. The parser and constrain keep them side by side."""
    spec = Spec("mpileaks ^mpi=mpich ^mpi=zmpi")
    assert spec == Spec("mpileaks ^mpi=zmpi ^mpi=mpich")

    lhs, rhs = Spec("pkg-a ^mpi=mpich"), Spec("pkg-a ^mpi=zmpi")
    assert lhs.intersects(rhs) and rhs.intersects(lhs)
    forward, backward = lhs.constrained(rhs), rhs.constrained(lhs)
    assert forward == Spec("pkg-a ^mpi=mpich ^mpi=zmpi")
    assert forward.to_dict() == backward.to_dict()


def test_two_providers_under_conditions_that_exclude_each_other_are_fine(mock_packages):
    """Only one provider can be the one at a time, so two of them named under conditions that
    cannot hold together are not in each other's way."""
    lhs = Spec("pkg-a %[when='+foo' virtuals=mpi] mpich")
    rhs = Spec("pkg-a %[when='~foo' virtuals=mpi] zmpi")
    assert lhs.intersects(rhs)
    assert rhs.intersects(lhs)


def test_parallel_build_and_link_edges_merge_cleanly(mock_packages):
    """A build-only and a link-only edge to one package are two nodes that stay apart. The merge
    unions the two edge lists and drops the edges satisfied by another."""
    result = Spec("pkg-a ^[deptypes=build] pkg-b").constrained(
        Spec("pkg-a ^[deptypes=build] pkg-b ^[deptypes=link] pkg-b")
    )
    assert result == Spec("pkg-a ^[deptypes=build] pkg-b ^[deptypes=link] pkg-b")
    assert len(result.edges_to_dependencies(name="pkg-b")) == 2

    # round-trips cleanly: copy, str()/reparse and to_dict/from_dict all agree
    assert result.copy().to_dict() == result.to_dict()
    assert Spec(str(result)).to_dict() == result.to_dict()
    assert Spec.from_dict(result.to_dict()).to_dict() == result.to_dict()

    # the same union from the other side: the pair absorbs the lone build edge
    backward = Spec("pkg-a ^[deptypes=build] pkg-b ^[deptypes=link] pkg-b").constrained(
        Spec("pkg-a ^[deptypes=build] pkg-b")
    )
    assert backward.to_dict() == result.to_dict()


def test_parallel_direct_edges_are_always_the_same_edge(mock_packages):
    """A package has at most one direct dependency on a given name, so two direct edges to one
    name are always merged into one, whatever their deptypes."""
    lhs, rhs = Spec("pkg-a %[deptypes=run] pkg-e"), Spec("pkg-a %[deptypes=link] pkg-e")
    result = lhs.constrained(rhs)
    assert result == Spec("pkg-a %[deptypes=link,run] pkg-e")

    # idempotent: re-applying the same constraint does not change anything further
    assert result.constrain(rhs) is False
    assert result == Spec("pkg-a %[deptypes=link,run] pkg-e")


def test_direct_edges_to_one_name_merge_their_virtuals(mock_packages):
    """A package has at most one direct dependency on a name. Two direct edges to it are one
    dependency, merging their virtuals as they merge their deptypes."""
    spec = Spec("mpileaks %c=gcc %cxx=gcc")
    assert spec == Spec("mpileaks %c,cxx=gcc")

    lhs, rhs = Spec("pkg-a %c=gcc@5"), Spec("pkg-a %cxx=gcc")
    forward, backward = lhs.constrained(rhs), rhs.constrained(lhs)
    assert forward.to_dict() == backward.to_dict()
    assert forward == Spec("pkg-a %c,cxx=gcc@5")


def test_two_versions_of_one_provider_of_a_virtual_intersect(mock_packages):
    """Two edges referring to the same provider for one virtual at versions that do not intersect
    can be matched by a concrete spec with duplicate nodes, cause ^ can refer to two distinct
    unification sets in which virtuals are unified: link/run closure and pure build deps."""
    lhs, rhs = Spec("pkg-a ^mpi=mpich@3"), Spec("pkg-a ^mpi=mpich@4")
    assert lhs.intersects(rhs)
    assert rhs.intersects(lhs)
    result = lhs.constrained(rhs)
    assert result == Spec("pkg-a ^mpi=mpich@3 ^mpi=mpich@4")
    example = Spec("pkg-a %[deptypes=build] mpi=mpich@3 ^[deptypes=link] mpi=mpich@4")
    assert example.satisfies(result)


def test_an_anonymous_dependency_is_a_parallel_edge(mock_packages):
    """An edge with an anonymous target requires some dependency to match it. Constrain appends
    it as a parallel edge, and discards it only when an existing anonymous edge satisfies it."""
    # idempotency: the meet of a spec with itself is itself
    spec = Spec("pkg-a ^*@2")
    assert spec.satisfies(spec)
    assert spec.intersects(spec)
    assert spec.constrain("pkg-a ^*@2") is False

    # commutativity: the meet is the same from either side
    forward, backward = Spec("").constrained(spec), spec.constrained("")
    assert forward.to_dict() == backward.to_dict() == spec.to_dict()

    # Two anonymous constraints can each be matched by a different dependency, so they remain
    # parallel edges under intersection. The test asserts that under the preorder of satisfies
    # both `parallel <= {lhs, rhs}` and `merged <= {lhs, rhs}`, but also that `merged <= parallel`
    # while `parallel <= merged` is not the case. Constrain should pick the greatest lower bound,
    # meaning that `merged` is the incorrect choice.
    lhs, rhs = Spec("pkg-a ^+foo"), Spec("pkg-a ^+bar")
    parallel, merged = Spec("pkg-a ^+foo ^+bar"), Spec("pkg-a ^+foo+bar")
    assert parallel.satisfies(lhs) and parallel.satisfies(rhs)
    assert merged.satisfies(lhs) and merged.satisfies(rhs)
    assert merged.satisfies(parallel) and not parallel.satisfies(merged)
    assert lhs.constrained(rhs) == parallel

    lhs, rhs = Spec("pkg-a %+foo"), Spec("pkg-a %+bar")
    parallel, merged = Spec("pkg-a %+foo %+bar"), Spec("pkg-a %+foo+bar")
    assert parallel.satisfies(lhs) and parallel.satisfies(rhs)
    assert merged.satisfies(lhs) and merged.satisfies(rhs)
    assert merged.satisfies(parallel) and not parallel.satisfies(merged)
    assert lhs.constrained(rhs) == parallel

    # direct deps are written before the first ^ so %+bar binds to the root
    result = Spec("pkg-a ^+foo").constrained("pkg-a %+bar")
    assert result == Spec("pkg-a %+bar ^+foo")
    assert len(result.edges_to_dependencies()) == 2

    lhs, rhs = Spec("pkg-a ^*@1"), Spec("pkg-a ^*@2")
    assert lhs.intersects(rhs) and rhs.intersects(lhs)
    assert lhs.constrained(rhs) == Spec("pkg-a ^*@1 ^*@2")

    # idempotency again, with several anonymous edges
    spec = Spec("pkg-a ^+foo ^+bar")
    before = spec.to_dict()
    assert spec.constrain("pkg-a ^+foo ^+bar") is False
    assert spec.to_dict() == before

    # associativity: parallel edges accumulate the same way in any grouping
    a, b, c = Spec("pkg-a ^+foo"), Spec("pkg-a ^+bar"), Spec("pkg-a ^+baz")
    left, right = a.constrained(b).constrained(c), a.constrained(b.constrained(c))
    assert left.to_dict() == right.to_dict()

    # an anonymous edge satisfied by another anonymous edge is redundant, from either side
    lhs, rhs = Spec("pkg-a ^*+foo"), Spec("pkg-a ^*+foo+bar")
    forward, backward = lhs.constrained(rhs), rhs.constrained(lhs)
    assert forward.to_dict() == backward.to_dict() == rhs.to_dict()

    # a named edge alone satisfies both requirements of a named/anonymous pair
    named, anonymous = Spec("pkg-a ^pkg-b@2"), Spec("pkg-a ^*@2")
    forward, backward = named.constrained(anonymous), anonymous.constrained(named)
    assert forward.to_dict() == backward.to_dict()
    assert forward.satisfies(named) and named.satisfies(forward)


def test_an_edge_bridging_two_parallel_edges(mock_packages):
    """Edges to distinct virtuals of the same provider package stay parallel."""
    spec = Spec("mpileaks ^mpi=mpich ^lapack=mpich ^mpi,lapack=zmpi")
    assert spec == Spec("mpileaks ^mpi,lapack=zmpi ^mpi=mpich ^lapack=mpich")
    assert len(spec.edges_to_dependencies()) == 3

    lhs = Spec("pkg-a ^blas=openblas-with-lapack@1 ^lapack=openblas-with-lapack@2")
    rhs = Spec("pkg-a ^blas,lapack=openblas-with-lapack")
    assert lhs.intersects(rhs)
    assert rhs.intersects(lhs)
    forward, backward = lhs.constrained(rhs), rhs.constrained(lhs)
    assert forward.to_dict() == backward.to_dict()
    assert forward == Spec(
        "pkg-a ^blas=openblas-with-lapack@1 ^lapack=openblas-with-lapack@2"
        " ^blas,lapack=openblas-with-lapack"
    )
    assert len(forward.edges_to_dependencies()) == 3


def test_edges_under_different_conditions_stay_parallel(mock_packages):
    """Two direct edges to the same package name are one node only where both conditions hold, so
    they stay parallel."""
    lhs = Spec("pkg-a %[when='+bvv' virtuals=c] gcc")
    rhs = Spec("pkg-a %[when='~bvv' virtuals=cxx] gcc")
    result = lhs.constrained(rhs)
    assert result == Spec("pkg-a %[when='+bvv' virtuals=c] gcc %[when='~bvv' virtuals=cxx] gcc")

    # this instance would fail if virtuals=c,cxx were merged
    example = Spec("pkg-a ~bvv %cxx=gcc")
    assert example.satisfies(lhs) and example.satisfies(rhs)
    assert example.satisfies(result)


def test_conflicting_deps_under_one_unforced_condition_intersect(mock_packages):
    """Both edges bind only where +foo holds, and pkg-a~foo satisfies both operands, so the
    conflicting conditional deps do not make the pair disjoint."""
    lhs, rhs = Spec("pkg-a %[when='+foo'] pkg-b@1"), Spec("pkg-a %[when='+foo'] pkg-b@2")
    example = Spec("pkg-a ~foo")
    assert example.satisfies(lhs) and example.satisfies(rhs)
    assert lhs.intersects(rhs) and rhs.intersects(lhs)
    result = lhs.constrained(rhs)
    assert result == Spec("pkg-a %[when='+foo'] pkg-b@1 %[when='+foo'] pkg-b@2")
    assert example.satisfies(result)
    assert result.to_dict() == rhs.constrained(lhs).to_dict()


def test_self_constrain_of_parallel_deptype_edges_is_idempotent(mock_packages):
    """Two parallel edges constrained with an equal pair stay themselves. Pairing them by name
    alone would merge build into the link edge and produce an edge neither spec required."""
    s = Spec("pkg-a ^[deptypes=build] pkg-e ^[deptypes=link] pkg-e")
    assert len(s.edges_to_dependencies(name="pkg-e")) == 2
    changed = s.constrain(Spec("pkg-a ^[deptypes=build] pkg-e ^[deptypes=link] pkg-e"))
    assert not changed
    assert s.to_dict() == Spec("pkg-a ^[deptypes=build] pkg-e ^[deptypes=link] pkg-e").to_dict()


def test_copy_keeps_a_redundant_parallel_edge_and_its_subtree(mock_packages):
    """A structural copy reproduces every edge as it is. ``_dup_deps`` builds each edge directly,
    since replaying them through ``add_dependency_edge`` would discard the pkg-b@1: edge before its
    child pkg-e is attached."""
    original = Spec("pkg-a ^[deptypes=link] pkg-b@1")
    dep = Spec("pkg-b@1:")
    dep._add_dependency(Spec("pkg-e"), depflag=dt.LINK, virtuals=())
    original._add_dependency(dep, depflag=dt.LINK, virtuals=())

    copy = original.copy()

    assert copy == original
    assert copy.to_dict() == original.to_dict()
