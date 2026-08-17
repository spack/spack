# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests formatting of spec strings"""

import spack.concretize
from spack.enums import PartStyle
from spack.spec import DIM_COLOR, HIGHLIGHT_COLOR, VARIANT_COLOR, VERSION_COLOR, Spec
from spack.util.tty.color import colorize


def _always_version(style):
    """Returns a version_style_fn that always returns *style*."""
    return lambda node: style


def _always_variant(style):
    """Returns a variant_style_fn that always returns *style* for every key."""
    return lambda node, key: style


def _always_arch(style):
    """Returns an architecture_style_fn that always returns *style*."""
    return lambda node, part: style


def _variant_key(target_key, match_style, other_style=PartStyle.NORMAL):
    """Returns a variant_style_fn that returns *match_style* for *target_key*."""
    return lambda node, key: match_style if key == target_key else other_style


def test_version_style_hidden(config, mock_packages):
    """Tests that HIDDEN suppresses the version entirely."""
    s = spack.concretize.concretize_one("mpileaks@2.3")
    result = s.format("{@version}", version_style_fn=_always_version(PartStyle.HIDDEN))
    assert result == ""

    result = s.format("{name}{@version}", version_style_fn=_always_version(PartStyle.HIDDEN))
    assert result == "mpileaks"


def test_version_style_highlight(config, mock_packages):
    """Tests that HIGHLIGHT applies HIGHLIGHT_COLOR to the version"""
    s = spack.concretize.concretize_one("mpileaks@2.3")
    result = s.format(
        "{name}{@version}", color=True, version_style_fn=_always_version(PartStyle.HIGHLIGHT)
    )
    expected = colorize(f"mpileaks{HIGHLIGHT_COLOR}@@{s.version}@.", color=True)
    assert result == expected


def test_version_style_dim(config, mock_packages):
    """Tests that DIM applies DIM_COLOR to the version."""
    s = spack.concretize.concretize_one("mpileaks@2.3")
    result = s.format(
        "{name}{@version}", color=True, version_style_fn=_always_version(PartStyle.DIM)
    )
    expected = colorize(f"mpileaks{DIM_COLOR}@@{s.version}@.", color=True)
    assert result == expected


def test_version_style_normal_uses_default_color(config, mock_packages):
    """Tests that NORMAL keeps the default VERSION_COLOR."""
    s = spack.concretize.concretize_one("mpileaks@2.3")
    result = s.format(
        "{name}{@version}", color=True, version_style_fn=_always_version(PartStyle.NORMAL)
    )
    expected = colorize(f"mpileaks{VERSION_COLOR}@@{s.version}@.", color=True)
    assert result == expected


def test_single_variant_style_hidden(config, mock_packages):
    """Tests that HIDDEN on a single variant suppresses it."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format("{name}{variants.debug}", variant_style_fn=_always_variant(PartStyle.HIDDEN))
    assert result == "mpileaks"


def test_single_variant_style_highlight(config, mock_packages):
    """Tests that HIGHLIGHT on a single variant applies HIGHLIGHT_COLOR."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format(
        "{name}{variants.debug}", color=True, variant_style_fn=_always_variant(PartStyle.HIGHLIGHT)
    )
    expected = colorize(f"mpileaks{HIGHLIGHT_COLOR}{s.variants['debug']}@.", color=True)
    assert result == expected


def test_single_variant_style_dim(config, mock_packages):
    """Tests that DIM on a single variant applies DIM_COLOR."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format(
        "{name}{variants.debug}", color=True, variant_style_fn=_always_variant(PartStyle.DIM)
    )
    expected = colorize(f"mpileaks{DIM_COLOR}{s.variants['debug']}@.", color=True)
    assert result == expected


def test_single_variant_style_normal_uses_variant_color(config, mock_packages):
    """Tests that NORMAL keeps the default VARIANT_COLOR."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format(
        "{variants.debug}", color=True, variant_style_fn=_always_variant(PartStyle.NORMAL)
    )
    expected = colorize(f"{VARIANT_COLOR}{s.variants['debug']}@.", color=True)
    assert result == expected


def test_all_variants_some_hidden(config, mock_packages):
    """Tests that HIDDEN for a specific key removes it from the output."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format("{variants}", variant_style_fn=_variant_key("debug", PartStyle.HIDDEN))
    assert "+debug" not in result
    assert "~debug" not in result


def test_all_variants_mixed_styles(config, mock_packages):
    """Tests that different keys can have different styles."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format(
        "{variants}",
        color=True,
        variant_style_fn=_variant_key("debug", PartStyle.HIGHLIGHT, PartStyle.DIM),
    )
    highlighted = colorize(f"{HIGHLIGHT_COLOR}+debug@.", color=True)
    assert highlighted in result
    dimmed_shared = colorize(f"{DIM_COLOR}+shared@.", color=True)
    assert dimmed_shared in result


def test_all_variants_all_hidden(config, mock_packages):
    """Tests that all variants HIDDEN leads to the empty string."""
    s = spack.concretize.concretize_one("mpileaks+debug")
    result = s.format("{variants}", variant_style_fn=_always_variant(PartStyle.HIDDEN))
    assert result == ""


def test_architecture_platform_hidden(config, mock_packages):
    """Tests that HIDDEN for 'platform' suppresses the platform part."""
    s = spack.concretize.concretize_one("mpileaks")
    result = s.format(
        "{name}{ platform=architecture.platform}",
        architecture_style_fn=_always_arch(PartStyle.HIDDEN),
    )
    assert result == "mpileaks"


def test_architecture_os_hidden(config, mock_packages):
    """Tests that HIDDEN for 'os' suppresses the os part."""
    s = spack.concretize.concretize_one("mpileaks")
    result = s.format(
        "{name}{ os=architecture.os}", architecture_style_fn=_always_arch(PartStyle.HIDDEN)
    )
    assert result == "mpileaks"


def test_architecture_target_hidden(config, mock_packages):
    """Tests that HIDDEN for 'target' suppresses the target part."""
    s = spack.concretize.concretize_one("mpileaks")
    result = s.format(
        "{name}{ target=architecture.target}", architecture_style_fn=_always_arch(PartStyle.HIDDEN)
    )
    assert result == "mpileaks"


def test_architecture_target_highlight(config, mock_packages):
    """Tests that HIGHLIGHT for 'target' applies HIGHLIGHT_COLOR."""
    s = spack.concretize.concretize_one("mpileaks")
    result = s.format(
        "{ target=architecture.target}",
        color=True,
        architecture_style_fn=_always_arch(PartStyle.HIGHLIGHT),
    )
    expected = colorize(f"{HIGHLIGHT_COLOR} target={s.architecture.target}@.", color=True)
    assert result == expected


def test_architecture_os_dim(config, mock_packages):
    """Tests that DIM for 'os' applies DIM_COLOR."""
    s = spack.concretize.concretize_one("mpileaks")
    result = s.format(
        "{ os=architecture.os}", color=True, architecture_style_fn=_always_arch(PartStyle.DIM)
    )
    expected = colorize(f"{DIM_COLOR} os={s.architecture.os}@.", color=True)
    assert result == expected


def test_architecture_style_fn_receives_correct_part(config, mock_packages):
    """Tests that architecture_style_fn receives the correct sub-part name."""
    s = spack.concretize.concretize_one("mpileaks")
    received_parts = []

    def record_part(node, part):
        received_parts.append(part)
        return PartStyle.NORMAL

    s.format(
        "{ platform=architecture.platform}{ os=architecture.os}{ target=architecture.target}",
        architecture_style_fn=record_part,
    )
    assert received_parts == ["platform", "os", "target"]


def test_abstract_spec_str_roundtrips_namespace(config, mock_packages):
    """Ensure that abstract specs (anonymous or not) round-trip and canonicalize the namespace"""
    named = Spec("foo namespace=bar")
    assert str(named) == "bar.foo"
    assert Spec(str(named)).namespace == "bar"

    anonymous = Spec("namespace=bar")
    assert str(anonymous) == "namespace=bar"
    assert Spec(str(anonymous)).namespace == "bar"

    dep = Spec("pkg-a ^builtin_mock.pkg-b")
    assert str(dep) == "pkg-a ^builtin_mock.pkg-b"

    concrete = spack.concretize.concretize_one("mpileaks")
    assert concrete.namespace == "builtin_mock"
    assert str(concrete).startswith("mpileaks@")
