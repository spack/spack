# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import pytest

import spack.vendor.archspec.cpu

import spack.concretize
import spack.error
import spack.operating_systems
import spack.platforms
from spack.spec import ArchSpec, Spec, _make_gpu_microarch


@pytest.fixture(scope="module")
def current_host_platform():
    """Return the platform of the current host as detected by the
    'platform' stdlib package.
    """
    current_platform = None
    if "Linux" in platform.system():
        current_platform = spack.platforms.Linux()
    elif "Darwin" in platform.system():
        current_platform = spack.platforms.Darwin()
    elif "Windows" in platform.system():
        current_platform = spack.platforms.Windows()
    elif "FreeBSD" in platform.system():
        current_platform = spack.platforms.FreeBSD()
    return current_platform


TEST_PLATFORM = spack.platforms.Test()


@pytest.fixture(
    params=([str(x) for x in TEST_PLATFORM.targets] + ["default_target"]), scope="module"
)
def target_str(request):
    """All the possible strings that can be used for targets"""
    return request.param


@pytest.fixture(
    params=([str(x) for x in TEST_PLATFORM.operating_sys] + ["default_os"]), scope="module"
)
def os_str(request):
    """All the possible strings that can be used for operating systems"""
    return request.param


def test_platform(current_host_platform):
    """Check that current host detection return the correct platform"""
    detected_platform = spack.platforms.real_host()
    assert str(detected_platform) == str(current_host_platform)


def test_user_input_combination(config, target_str, os_str):
    """Test for all the valid user input combinations that both the target and
    the operating system match.
    """
    spec = Spec(f"libelf os={os_str} target={target_str}")
    assert spec.architecture.os == str(TEST_PLATFORM.operating_system(os_str))
    assert spec.architecture.target == TEST_PLATFORM.target(target_str)


def test_default_os_and_target(config, mock_packages):
    """Test that is we don't specify `os=` or `target=` we get the default values
    after concretization.
    """
    spec = spack.concretize.concretize_one("libelf")
    assert spec.architecture.os == str(TEST_PLATFORM.default_operating_system())
    assert spec.architecture.target == TEST_PLATFORM.default_target()


def test_operating_system_conversion_to_dict():
    operating_system = spack.operating_systems.OperatingSystem("os", "1.0")
    assert operating_system.to_dict() == {"name": "os", "version": "1.0"}


@pytest.mark.parametrize(
    "item,architecture_str",
    [
        # We can search the architecture string representation
        ("linux", "linux-ubuntu18.04-haswell"),
        ("ubuntu", "linux-ubuntu18.04-haswell"),
        ("haswell", "linux-ubuntu18.04-haswell"),
        # We can also search flags of the target,
        ("avx512", "linux-ubuntu18.04-icelake"),
    ],
)
def test_arch_spec_container_semantic(item, architecture_str):
    architecture = ArchSpec(architecture_str)
    assert item in architecture


@pytest.mark.regression("15306")
@pytest.mark.parametrize(
    "architecture_tuple,constraint_tuple",
    [
        (("linux", "ubuntu18.04", None), ("linux", None, "x86_64")),
        (("linux", "ubuntu18.04", None), ("linux", None, "x86_64:")),
    ],
)
def test_satisfy_strict_constraint_when_not_concrete(architecture_tuple, constraint_tuple):
    architecture = ArchSpec(architecture_tuple)
    constraint = ArchSpec(constraint_tuple)
    assert not architecture.satisfies(constraint)


def _gpus(names):
    """The archspec nodes for a list of GPU names, as the ArchSpec GPU helpers expect them."""
    return [_make_gpu_microarch(name) for name in names]


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        # a device runs code built for its ancestors: the pair meets at the more generic node
        (["86"], ["80"], ["80"]),
        (["80"], ["86"], ["80"]),
        (["80"], ["80"], ["80"]),
        (["90a"], ["90"], ["90"]),
        (["100a"], ["100f"], ["100f"]),
        (["gfx90a:xnack-"], ["gfx90a"], ["gfx90a"]),
        # lists meet pairwise, each survivor once, in order of first appearance
        (["80", "90"], ["86", "90a"], ["80", "90"]),
        (["80"], ["80", "86"], ["80"]),
        # no path between the two sides
        (["89"], ["90"], []),
        (["gfx90a:xnack-"], ["gfx90a:xnack+"], []),
        (["gfx90a"], ["gfx942"], []),
        (["80"], ["gfx90a"], []),
        # an empty side has nothing to meet
        ([], ["80"], []),
        (["80"], [], []),
    ],
)
def test_gpu_intersection(lhs, rhs, expected):
    result = ArchSpec._gpu_intersection(_gpus(lhs), _gpus(rhs))
    assert [node.name for node in result] == expected
    # the operation is symmetric
    result = ArchSpec._gpu_intersection(_gpus(rhs), _gpus(lhs))
    assert sorted(node.name for node in result) == sorted(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (["86"], ["80"], True),
        (["80", "90"], ["86", "90a"], True),
        (["89"], ["90"], False),
        # an empty side places no constraint
        ([], ["80"], True),
        (["80"], [], True),
        ([], [], True),
    ],
)
def test_gpu_intersects(lhs, rhs, expected):
    assert ArchSpec._gpu_intersects(_gpus(lhs), _gpus(rhs)) is expected
    assert ArchSpec._gpu_intersects(_gpus(rhs), _gpus(lhs)) is expected


@pytest.mark.parametrize(
    "built,requested,expected",
    [
        # the binary runs on the device
        (["80"], ["86"], True),
        (["80"], ["80"], True),
        (["100f"], ["100a"], True),
        # but not the other way around
        (["86"], ["80"], False),
        (["100a"], ["100f"], False),
        # a fat binary serves a device if any of its targets does
        (["80", "90"], ["86", "90a"], True),
        # every requested device must be served
        (["80"], ["86", "90"], False),
        # unrelated nodes
        (["89"], ["90"], False),
        # a request without GPUs is always met, a build without GPUs meets no request
        (["80"], [], True),
        ([], ["80"], False),
        ([], [], True),
    ],
)
def test_gpu_satisfies(built, requested, expected):
    assert ArchSpec._gpu_satisfies(_gpus(built), _gpus(requested)) is expected


@pytest.mark.parametrize(
    "value,expected",
    [(None, None), ([], None), (["90", "80", "90"], ("90", "80"))],
)
def test_gpus_setter(value, expected):
    arch = ArchSpec((None, None, None), gpus=value)
    assert arch.gpus is None if expected is None else tuple(n.name for n in arch.gpus) == expected
    assert ArchSpec(arch).gpus == arch.gpus


@pytest.mark.parametrize("name", ["none", "gfx999", "99"])
def test_gpus_unknown_to_archspec_are_rejected(name):
    with pytest.raises(ValueError, match="not a GPU micro-architecture known to archspec"):
        ArchSpec((None, None, None), gpus=[name])


def test_gpus_are_part_of_identity_but_not_of_the_dict():
    arch = ArchSpec(("linux", "ubuntu22.04", "x86_64"), gpus=["80"])
    assert arch != ArchSpec(("linux", "ubuntu22.04", "x86_64"))
    assert arch != ArchSpec(arch, gpus=["86"])
    assert "gpu" not in arch.to_dict()["arch"]
    assert repr(arch) == "ArchSpec(('linux', 'ubuntu22.04', 'x86_64'), gpus='80')"


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [(None, ["80"], "80"), (["80"], None, "80"), (["86"], ["80"], "80"), (["80"], ["86"], "80")],
)
def test_gpu_constrain(lhs, rhs, expected):
    arch = ArchSpec((None, "debian6", None), gpus=lhs)
    other = ArchSpec((None, None, None), gpus=rhs)
    assert arch._gpu_constrain(other) is (lhs != [expected])
    assert [n.name for n in arch.gpus] == [expected]
    assert arch._gpu_constrain(other) is False


def test_gpu_constrain_is_atomic_when_gpus_are_disjoint():
    arch = ArchSpec((None, None, None), gpus=["89"])
    with pytest.raises(spack.error.UnsatisfiableSpecError):
        arch._gpu_constrain(ArchSpec((None, "debian6", None), gpus=["90"]))
    assert repr(arch) == "ArchSpec((None, None, 'None'), gpus='89')"


def test_bare_gpus_do_not_take_part_in_arch_spec_comparison():
    """Bare GPU values are compared exactly, by the variant that holds them."""
    lhs = ArchSpec(("linux", None, "x86_64"), gpus=["89"])
    rhs = ArchSpec(("linux", None, "x86_64:"), gpus=["90"])
    assert lhs.satisfies(rhs) and lhs.intersects(rhs)
    assert lhs.constrain(rhs) is False
    assert [n.name for n in lhs.gpus] == ["89"]


@pytest.mark.parametrize(
    "lhs_tuple,rhs_tuple,expected_target",
    [
        ((None, "debian6", None), (None, None, "x86_64:"), "x86_64:"),
        ((None, None, "x86_64:"), (None, "debian6", None), "x86_64:"),
        ((None, "debian6", None), (None, None, "haswell"), "haswell"),
    ],
)
def test_constrain_target_when_only_one_side_has_one(lhs_tuple, rhs_tuple, expected_target):
    """The side that has a target wins, ranges included."""
    architecture = ArchSpec(lhs_tuple)
    architecture.constrain(ArchSpec(rhs_tuple))
    assert architecture.target == ArchSpec((None, None, expected_target)).target


def test_constrain_is_atomic_when_targets_are_disjoint():
    """platform and os are applied before the target, so the up-front intersection check is what
    keeps a failed constrain from leaving them behind."""
    architecture = ArchSpec(("linux", None, "haswell"))
    with pytest.raises(spack.error.UnsatisfiableSpecError):
        architecture.constrain(ArchSpec((None, "ubuntu18.04", "ppc64le")))
    assert architecture == ArchSpec(("linux", None, "haswell"))


@pytest.mark.parametrize(
    "architecture_tuple,constraint_tuple",
    [
        (("linux", "ubuntu18.04", "x86_64"), ("*", None, None)),
        (("linux", "ubuntu18.04", "x86_64"), (None, "*", None)),
        (("linux", "ubuntu18.04", "x86_64"), (None, None, "*")),
        (("linux", "ubuntu18.04", "x86_64"), ("*", "*", "*")),
        (("linux", None, None), ("*", None, None)),
    ],
)
def test_star_is_satisfied_and_intersected_and_does_not_constrain(
    architecture_tuple, constraint_tuple
):
    """A star requires the attribute to be set, so a spec that sets it satisfies the star, the
    two overlap in both directions, and merging changes nothing."""
    architecture = ArchSpec(architecture_tuple)
    constraint = ArchSpec(constraint_tuple)

    assert architecture.satisfies(constraint)
    assert architecture.intersects(constraint)
    assert constraint.intersects(architecture)

    merged = architecture.copy()
    assert merged.constrain(constraint) is False
    assert merged == architecture


def test_star_does_not_short_circuit_the_other_attributes():
    """A star on one attribute does not short-circuit satisfies or intersects: the remaining
    attributes are still checked."""
    architecture = ArchSpec(("linux", "ubuntu18.04", "x86_64"))
    assert not architecture.satisfies(ArchSpec(("*", "rhel6", None)))
    assert not architecture.satisfies(ArchSpec(("*", None, "aarch64")))
    assert not architecture.intersects(ArchSpec(("*", "rhel6", None)))


def test_star_target_is_replaced_by_a_named_target_when_constrained():
    """target=* is stored as target=: like @: in version lists"""
    architecture = ArchSpec((None, None, "*"))
    assert str(architecture.target) == ":"
    assert architecture.constrain(ArchSpec((None, None, "x86_64"))) is True
    assert str(architecture.target) == "x86_64"


@pytest.mark.parametrize(
    "root_target_range,dep_target_range,result",
    [
        ("x86_64:nocona", "x86_64:core2", "nocona"),  # pref not in intersection
        ("x86_64:core2", "x86_64:nocona", "nocona"),
        ("x86_64:haswell", "x86_64:mic_knl", "core2"),  # pref in intersection
        ("ivybridge", "nocona:skylake", "ivybridge"),  # one side concrete
        ("haswell:icelake", "broadwell", "broadwell"),
        # multiple ranges in lists with multiple overlaps
        ("x86_64:nocona,haswell:broadwell", "nocona:haswell,skylake:", "nocona"),
        # lists with concrete targets, lists compared to ranges
        ("x86_64,haswell", "core2:broadwell", "haswell"),
    ],
)
@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.skipif(
    str(spack.vendor.archspec.cpu.host().family) != "x86_64",
    reason="tests are for x86_64 uarch ranges",
)
def test_concretize_target_ranges(root_target_range, dep_target_range, result, monkeypatch):
    spec = spack.concretize.concretize_one(
        f"pkg-a foobar=bar target={root_target_range} %gcc@10 ^pkg-b target={dep_target_range}"
    )
    assert spec.target == spec["pkg-b"].target == result


def test_instantiate_non_default_macos(mock_packages):
    darwin = spack.platforms.Darwin()

    for name, macos in darwin.operating_sys.items():
        if name != darwin.default_os:
            non_default_macos_name = name
            non_default_macos = macos
            break
    else:
        assert False, "Failed to find non-default macos version in test"

    with spack.platforms.use_platform(darwin):
        # zlib isn't important but we need a spec with no compiler because our test environment
        # has no macos compilers
        target = str(spack.vendor.archspec.cpu.host().family)
        spec = spack.concretize.concretize_one(
            f"zlib platform=darwin os={non_default_macos_name} target={target}"
        )

    # Primarily testing that these lines doesn't throw
    os = spec.os
    os_object = spack.platforms.by_name(spec.platform).operating_system(os)

    assert os == non_default_macos_name
    assert os_object == non_default_macos
