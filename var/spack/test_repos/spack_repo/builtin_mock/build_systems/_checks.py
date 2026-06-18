# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import Builder, BuilderWithDefaults, execute_install_time_tests


def execute_build_time_tests(builder: Builder):
    """Execute the build-time tests prescribed by builder.

    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``build_time_test_callbacks`` attribute.
    """
    if not builder.pkg.run_tests or not builder.build_time_test_callbacks:
        return

    builder.pkg.tester.phase_tests(builder, "build", builder.build_time_test_callbacks)


__all__ = ["execute_build_time_tests", "BuilderWithDefaults", "execute_install_time_tests"]
