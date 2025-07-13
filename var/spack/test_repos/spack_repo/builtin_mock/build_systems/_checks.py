# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import Builder, BuilderWithDefaults, Spec, execute_install_time_tests

_ = BuilderWithDefaults
_ = execute_install_time_tests


def ensure_build_dependencies_or_raise(spec: Spec, dependencies: List[str], error_msg: str):
    """Ensure that some build dependencies are present in the concrete spec.

    If not, raise a RuntimeError with a helpful error message.

    Args:
        spec: concrete spec to be checked.
        dependencies: list of package names of required build dependencies
        error_msg: brief error message to be prepended to a longer description

    Raises:
          RuntimeError: when the required build dependencies are not found
    """
    assert spec.concrete, "Can ensure build dependencies only on concrete specs"
    build_deps = [d.name for d in spec.dependencies(deptype="build")]
    missing_deps = [x for x in dependencies if x not in build_deps]

    if not missing_deps:
        return

    # Raise an exception on missing deps.
    msg = (
        "{0}: missing dependencies: {1}.\n\nPlease add "
        "the following lines to the package:\n\n".format(
            error_msg, ", ".join(str(d) for d in missing_deps)
        )
    )

    for dep in missing_deps:
        msg += '    depends_on("{0}", type="build", when="@{1} {2}")\n'.format(
            dep, spec.version, "build_system=autotools"
        )

    msg += '\nUpdate the version (when="@{0}") as needed.'.format(spec.version)
    raise RuntimeError(msg)


def execute_build_time_tests(builder: Builder):
    """Execute the build-time tests prescribed by builder.

    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``build_time_test_callbacks`` attribute.
    """
    if not builder.pkg.run_tests or not builder.build_time_test_callbacks:
        return

    builder.pkg.tester.phase_tests(builder, "build", builder.build_time_test_callbacks)
