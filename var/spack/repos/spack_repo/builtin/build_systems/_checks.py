# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import Callable, List

import spack.relocate
from spack.package import Builder, InstallError, Spec, run_after


def sanity_check_prefix(builder: Builder):
    """Check that specific directories and files are created after installation.

    The files to be checked are in the ``sanity_check_is_file`` attribute of the
    package object, while the directories are in the ``sanity_check_is_dir``.

    Args:
        builder: builder that installed the package
    """
    pkg = builder.pkg

    def check_paths(path_list: List[str], filetype: str, predicate: Callable[[str], bool]) -> None:
        if isinstance(path_list, str):
            path_list = [path_list]

        for path in path_list:
            if not predicate(os.path.join(pkg.prefix, path)):
                raise InstallError(
                    f"Install failed for {pkg.name}. No such {filetype} in prefix: {path}"
                )

    check_paths(pkg.sanity_check_is_file, "file", os.path.isfile)
    check_paths(pkg.sanity_check_is_dir, "directory", os.path.isdir)

    # Check that the prefix is not empty apart from the .spack/ directory
    with os.scandir(pkg.prefix) as entries:
        f = next(
            (f for f in entries if not (f.name == ".spack" and f.is_dir(follow_symlinks=False))),
            None,
        )

    if f is None:
        raise InstallError(f"Install failed for {pkg.name}.  Nothing was installed!")


def apply_macos_rpath_fixups(builder: Builder):
    """On Darwin, make installed libraries more easily relocatable.

    Some build systems (handrolled, autotools, makefiles) can set their own
    rpaths that are duplicated by spack's compiler wrapper. This fixup
    interrogates, and postprocesses if necessary, all libraries installed
    by the code.

    It should be added as a @run_after to packaging systems (or individual
    packages) that do not install relocatable libraries by default.

    Args:
        builder: builder that installed the package
    """
    spack.relocate.fixup_macos_rpaths(builder.spec)


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


def execute_install_time_tests(builder: Builder):
    """Execute the install-time tests prescribed by builder.

    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``install_time_test_callbacks`` attribute.
    """
    if not builder.pkg.run_tests or not builder.install_time_test_callbacks:
        return

    builder.pkg.tester.phase_tests(builder, "install", builder.install_time_test_callbacks)


class BuilderWithDefaults(Builder):
    """Base class for all specific builders with common callbacks registered."""

    # Check that self.prefix is there after installation
    run_after("install")(sanity_check_prefix)
