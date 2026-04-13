# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Regression tests for concretizer error messages.

Every test asserts two properties:
1. The correct exception type is raised.
2. The message contains every "actionable part" -- a string from the user's
   input (spec token, config key, package name) that helps identify what to
   change.
"""
import pathlib
from io import StringIO
from typing import List

import pytest

import spack.concretize
import spack.config
import spack.error
import spack.main
import spack.solver.asp
import spack.spec

version_error_messages = [
    "Cannot satisfy",
    "        required because quantum-espresso depends on fftw@:1.0",
    "          required because quantum-espresso ^fftw@1.1: requested explicitly",
    "        required because quantum-espresso ^fftw@1.1: requested explicitly",
]

external_error_messages = [
    "Cannot build quantum-espresso, since it is configured `buildable:false` and "
    "no externals satisfy the request"
]

variant_error_messages = [
    "'fftw' requires conflicting variant values '~mpi' and '+mpi'",
    "        required because quantum-espresso depends on fftw+mpi when +invino",
    "          required because quantum-espresso+invino ^fftw~mpi requested explicitly",
    "        required because quantum-espresso+invino ^fftw~mpi requested explicitly",
]

external_config = {
    "packages:quantum-espresso": {
        "buildable": False,
        "externals": [{"spec": "quantum-espresso@1.0~veritas", "prefix": "/path/to/qe"}],
    }
}


@pytest.mark.parametrize(
    "error_messages,config_set,spec",
    [
        (version_error_messages, {}, "quantum-espresso^fftw@1.1:"),
        (external_error_messages, external_config, "quantum-espresso+veritas"),
        (variant_error_messages, {}, "quantum-espresso+invino^fftw~mpi"),
    ],
)
def test_error_messages(error_messages, config_set, spec, mock_packages, mutable_config):
    for path, conf in config_set.items():
        spack.config.set(path, conf)

    with pytest.raises(spack.solver.asp.UnsatisfiableSpecError) as e:
        _ = spack.concretize.concretize_one(spec)

    for em in error_messages:
        assert em in str(e.value), str(e.value)


@pytest.mark.parametrize(
    "spec", ["deprecated-versions@1.1.0", "deprecated-client ^deprecated-versions@1.1.0"]
)
def test_deprecated_version_error(spec, mock_packages, mutable_config):
    with pytest.raises(spack.solver.asp.DeprecatedVersionError, match="deprecated-versions@1.1.0"):
        _ = spack.concretize.concretize_one(spec)

    spack.config.set("config:deprecated", True)
    spack.concretize.concretize_one(spec)


@pytest.mark.parametrize(
    "spec", ["deprecated-versions@99.9", "deprecated-client ^deprecated-versions@99.9"]
)
def test_nonexistent_version_error(spec, mock_packages, mutable_config):
    with pytest.raises(spack.solver.asp.InvalidVersionError, match="deprecated-versions@99.9"):
        _ = spack.concretize.concretize_one(spec)


def test_internal_error_handling_formatting(tmp_path: pathlib.Path):
    log = StringIO()
    input_to_output = [
        (spack.spec.Spec("foo+x"), spack.spec.Spec("foo@=1.0~x")),
        (spack.spec.Spec("bar+y"), spack.spec.Spec("x@=1.0~y")),
        (spack.spec.Spec("baz+z"), None),
    ]
    spack.main._handle_solver_bug(
        spack.solver.asp.OutputDoesNotSatisfyInputError(input_to_output), root=tmp_path, out=log
    )

    output = log.getvalue()
    assert "the following specs were not solved:\n    - baz+z\n" in output
    assert (
        "the following specs were concretized, but do not satisfy the input:\n"
        "    - input: foo+x\n"
        "      output: foo@=1.0~x\n"
        "    - input: bar+y\n"
        "      output: x@=1.0~y"
    ) in output

    files = {f.name: str(f) for f in tmp_path.glob("spack-asp-*/*.json")}
    assert {"input-1.json", "input-2.json", "output-1.json", "output-2.json"} == set(files.keys())

    assert spack.spec.Spec.from_specfile(files["input-1.json"]) == spack.spec.Spec("foo+x")
    assert spack.spec.Spec.from_specfile(files["input-2.json"]) == spack.spec.Spec("bar+y")
    assert spack.spec.Spec.from_specfile(files["output-1.json"]) == spack.spec.Spec("foo@=1.0~x")
    assert spack.spec.Spec.from_specfile(files["output-2.json"]) == spack.spec.Spec("x@=1.0~y")


def assert_actionable_error(exc_info, *required_part: str) -> None:
    """Verify that the error message contains every required part, which is usually a string that
    the user can recognize in their own input.
    """
    msg = str(exc_info.value)
    missing = [h for h in required_part if h not in msg]
    assert not missing, f"Error message is missing parts {missing!r}\n" f"Full message:\n{msg}"


@pytest.mark.parametrize(
    "input_spec,expected_parts",
    [
        # fftw is constrained to ~mpi by the explicit request, but quantum-espresso
        # requires fftw+mpi when +invino. Both values cannot coexist.
        pytest.param(
            "quantum-espresso+invino^fftw~mpi", ["fftw", "mpi"], id="variant_value_conflict"
        ),
        # The user requests a variant that does not exist on the package.
        pytest.param(
            "quantum-espresso+nonexistent",
            ["quantum-espresso", "nonexistent", "No such variant"],
            id="variant_undefined",
        ),
        # quantum-espresso has only version 1.0; @:0.1 cannot be satisfied.
        pytest.param(
            "quantum-espresso@:0.1",
            ["quantum-espresso@:0.1", "No version exists"],
            id="version_constraint_unsatisfied",
        ),
        # hypre propagates ~~shared to its deps, but openblas is explicitly +shared.
        pytest.param(
            "hypre ~~shared ^openblas +shared",
            ["shared", "hypre", "'openblas' requires conflicting variant values"],
            id="propagation_excluded",
        ),
        # dependency-foo-bar (++bar) and direct-dep-foo-bar (~~bar) both propagate
        # variant "bar" with different values to their shared transitive dependency.
        pytest.param(
            "parent-foo-bar ^dependency-foo-bar++bar ^direct-dep-foo-bar~~bar",
            ["cannot both propagate variant 'bar'"],
            id="propagation_conflict_to_dep",
        ),
        # gmake is a build dependency of a transitive dep, not directly reachable
        # via link/run from multivalue-variant.
        pytest.param(
            "multivalue-variant ^gmake",
            ["gmake is not a direct 'build' or"],
            id="literal_not_in_dag",
        ),
        # mvapich2 file_systems uses auto_or_any_combination_of, but "auto" and "lustre"
        # come from disjoint sets and cannot be combined.
        pytest.param(
            "mvapich2 file_systems=auto,lustre",
            ["mvapich2", "file_systems", "the value 'auto' is mutually exclusive"],
            id="variant_disjoint_sets",
        ),
    ],
)
def test_input_spec_driven_errors(
    input_spec: str, expected_parts: List[str], mock_packages, mutable_config
) -> None:
    """Tests errors caused by a token in the CLI input spec. The message must name both the
    affected package and the specific token (variant, version, flag, dep) the user supplied.
    """
    with pytest.raises(spack.error.SpackError) as exc_info:
        spack.concretize.concretize_one(input_spec)
    assert_actionable_error(exc_info, *expected_parts)


@pytest.mark.parametrize(
    "packages_config,input_spec,expected_parts",
    [
        # quantum-espresso is set buildable:false; the available external does not
        # satisfy +veritas, so no valid spec can be found.
        pytest.param(
            {
                "packages:quantum-espresso": {
                    "buildable": False,
                    "externals": [
                        {"spec": "quantum-espresso@1.0~veritas", "prefix": "/path/to/qe"}
                    ],
                }
            },
            "quantum-espresso+veritas",
            ["quantum-espresso", "it is configured `buildable:false`"],
            id="buildable_false",
        ),
        # The user provided a packages.yaml `require:` with a message field. The error must surface
        # the custom message so the user knows the policy and the package name so they can find
        # the config section.
        pytest.param(
            {
                "packages:libelf": {
                    "require": [{"spec": "%clang", "message": "must be compiled with clang"}]
                }
            },
            "libelf%gcc",
            ["libelf", "must be compiled with clang"],
            id="requirement_unsatisfied_custom_message",
        ),
        # Generic message must still name the package so the user knows which entry to look at
        pytest.param(
            {"packages:libelf": {"require": ["%clang"]}},
            "libelf%gcc",
            ["libelf"],
            id="requirement_unsatisfied_generic",
        ),
    ],
)
def test_config_driven_errors(
    packages_config, input_spec: str, expected_parts: List[str], mock_packages, mutable_config
) -> None:
    """Tests errors caused by user configuration, e,g, a setting in packages.yaml. The message must
    identify the package and the config value to fix.
    """
    for path, conf in packages_config.items():
        spack.config.set(path, conf)

    with pytest.raises(spack.error.SpackError) as exc_info:
        spack.concretize.concretize_one(input_spec)
    assert_actionable_error(exc_info, *expected_parts)


@pytest.mark.parametrize(
    "input_spec,expected_handles",
    [
        # conflict-parent@0.9 has conflicts("^conflict~foo", when="@0.9"). When the user requests
        # `^conflict~foo` the conflict fires. The auto-generated message includes the package name
        # and the when-spec version, giving the user two places to look.
        pytest.param(
            "conflict-parent@0.9 ^conflict~foo",
            ["conflict-parent", "'^conflict~foo' conflicts with '@0.9'"],
            id="conflicts_directive",
        ),
        # requires-clang has `requires("%clang", msg="can only be compiled with Clang")`. When
        # compiled with %gcc the requirement is unsatisfied and the custom message is shown
        pytest.param("requires-clang %gcc", ["requires-clang", "Clang"], id="requires_directive"),
    ],
)
def test_package_py_driven_errors(
    input_spec: str, expected_handles: List[str], mock_packages, mutable_config
) -> None:
    """Tests errors involving directives in package.py recipes. The error message must name the
    package whose directive caused the failure.
    """
    with pytest.raises(spack.error.SpackError) as exc_info:
        spack.concretize.concretize_one(input_spec)
    assert_actionable_error(exc_info, *expected_handles)
