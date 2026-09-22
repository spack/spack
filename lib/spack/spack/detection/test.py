# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Create and run mock e2e tests for package detection."""

import collections
import contextlib
import functools
import os
import pathlib
import sys
import tempfile
from typing import Any, Deque, Dict, Generator, List, NamedTuple, Optional, Tuple

import spack.platforms
import spack.repo
import spack.spec
import spack.util.elf
from spack.util import filesystem, spack_yaml

from .dependencies import detect_with_dependencies
from .elf_closure import DynamicLoader, ElfInfo
from .ownership import ownership_index
from .path import by_path_detailed


class MockExecutables(NamedTuple):
    """Mock executables to be used in detection tests"""

    #: Relative paths for mock executables to be created
    executables: List[str]
    #: Shell script for the mock executable
    script: str
    #: Libraries the executables load, as ``DT_NEEDED`` entries
    needed: List[str] = []
    #: ``DT_RPATH`` of the executables, a colon separated list of directories
    rpath: Optional[str] = None
    #: ``DT_RUNPATH`` of the executables, a colon separated list of directories
    runpath: Optional[str] = None


class MockLibrary(NamedTuple):
    """Mock shared library to be used in detection tests"""

    #: Relative path of the library
    path: str
    soname: Optional[str] = None
    #: ``DT_NEEDED`` entries of the library
    needed: List[str] = []
    #: ``DT_RPATH`` of the library, a colon separated list of directories
    rpath: Optional[str] = None
    #: ``DT_RUNPATH`` of the library, a colon separated list of directories
    runpath: Optional[str] = None


class ExpectedTestResult(NamedTuple):
    """Data structure to model assertions on detection tests"""

    #: Spec to be detected
    spec: str
    #: Attributes expected in the external spec
    extra_attributes: Dict[str, str]
    #: Specs that the dependencies detected for the external satisfy, one per dependency, or
    #: None if dependencies are not tested
    dependencies: Optional[List[str]] = None


class DetectionTest(NamedTuple):
    """Data structure to construct detection tests by PATH inspection.

    Packages may have a YAML file containing the description of one or more detection tests
    to be performed. Each test creates a few mock executable scripts in a temporary folder,
    and checks that detection by PATH gives the expected results.
    """

    pkg_name: str
    layout: List[MockExecutables]
    results: List[ExpectedTestResult]
    libraries: List[MockLibrary] = []


class DetectionOutcome(NamedTuple):
    #: specs that have been detected for the package under test
    specs: List[spack.spec.Spec]
    #: dependencies detected for those specs, as (parent, child) pairs
    dependencies: List[Tuple[spack.spec.Spec, spack.spec.Spec]]


class _MockLoader(DynamicLoader):
    """Dynamic loader that takes the loading information of mock executables, which are shell
    scripts, from the test, and searches libraries only in the directories of mock libraries.
    """

    def __init__(self, *, executables: Dict[str, ElfInfo], default_dirs: List[str]) -> None:
        super().__init__(ld_library_path=[], default_dirs=default_dirs)
        self._executables = executables

    def elf_info(self, path: str) -> Optional[ElfInfo]:
        real_path = os.path.realpath(path)
        if real_path in self._executables:
            return self._executables[real_path]
        return super().elf_info(path)


class Runner:
    """Runs an external detection test"""

    def __init__(self, *, test: DetectionTest, repository: spack.repo.RepoPath) -> None:
        self.test = test
        self.repository = repository
        self.tmpdir = tempfile.TemporaryDirectory()
        self._compat = spack.util.elf.get_elf_compat(sys.executable)
        #: loading information of the mock executables, keyed by real path
        self._executables: Dict[str, ElfInfo] = {}
        #: directories of the mock libraries, in the order of the layout
        self._library_dirs: List[str] = []

    def execute(self) -> List[spack.spec.Spec]:
        """Executes a test and returns the specs that have been detected.

        This function sets-up a test in a temporary directory, according to the prescriptions
        in the test layout, then performs a detection by executables and returns the specs that
        have been detected.
        """
        return self.run().specs

    def run(self) -> DetectionOutcome:
        """Executes a test and returns the specs that have been detected, and their dependencies
        if any result of the test lists them.

        Dependencies are detected with a loader that searches only the directories of the mock
        libraries, so the libraries of the host are never used.
        """
        _, unqualified_name = spack.repo.partition_package_name(self.test.pkg_name)
        with self._mock_layout() as path_hints:
            detect = functools.partial(by_path_detailed, repo=self.repository)
            detected = detect([self.test.pkg_name], path_hints=path_hints)
            if all(x.dependencies is None for x in self.test.results):
                specs = {x.spec for x in detected.get(unqualified_name, [])}
                return DetectionOutcome(specs=list(specs), dependencies=[])

            loader = _MockLoader(executables=self._executables, default_dirs=self._library_dirs)
            result = detect_with_dependencies(
                detected,
                detect=detect,
                configured=[],
                index=ownership_index(self.repository),
                loader=loader,
                repo=self.repository,
            )
            specs = {x.spec for x in result.detected.get(unqualified_name, [])}
            edges = [(x.parent, x.child) for x in result.edges if x.parent in specs]
        return DetectionOutcome(specs=list(specs), dependencies=edges)

    @contextlib.contextmanager
    def _mock_layout(self) -> Generator[List[str], None, None]:
        hints = set()
        try:
            for entry in self.test.layout:
                exes = self._create_executable_scripts(entry)

                for mock_executable in exes:
                    hints.add(str(mock_executable.parent))

            for library in self.test.libraries:
                library_path = self._create_library(library)
                hints.add(str(library_path.parent))
                if str(library_path.parent) not in self._library_dirs:
                    self._library_dirs.append(str(library_path.parent))

            yield list(hints)
        finally:
            self.tmpdir.cleanup()

    def _create_library(self, library: MockLibrary) -> pathlib.Path:
        is_64_bit, is_little_endian, e_machine = self._compat
        abs_path = pathlib.Path(self.tmpdir.name) / library.path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_bytes(
            spack.util.elf.minimal_elf(
                needed=library.needed,
                soname=library.soname,
                rpath=library.rpath,
                runpath=library.runpath,
                e_machine=e_machine,
                is_64_bit=is_64_bit,
                is_little_endian=is_little_endian,
            )
        )
        return abs_path

    def _create_executable_scripts(self, mock_executables: MockExecutables) -> List[pathlib.Path]:
        import spack.vendor.jinja2

        relative_paths = mock_executables.executables
        script = mock_executables.script
        script_template = spack.vendor.jinja2.Template("#!/bin/bash\n{{ script }}\n")
        result = []
        for mock_exe_path in relative_paths:
            rel_path = pathlib.Path(mock_exe_path)
            abs_path = pathlib.Path(self.tmpdir.name) / rel_path
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_text(script_template.render(script=script))
            filesystem.set_executable(abs_path)
            result.append(abs_path)
            self._executables[os.path.realpath(abs_path)] = ElfInfo(
                compat=self._compat,
                has_interpreter=True,
                soname=None,
                needed=list(mock_executables.needed),
                rpath=mock_executables.rpath.split(":") if mock_executables.rpath else [],
                runpath=mock_executables.runpath.split(":") if mock_executables.runpath else [],
            )
        return result

    @property
    def expected_specs(self) -> List[spack.spec.Spec]:
        result = []
        for item in self.test.results:
            spec = spack.spec.Spec.from_detection(
                item.spec, external_path=self.tmpdir.name, extra_attributes=item.extra_attributes
            )
            spack.spec.substitute_abstract_variants(spec, repo=self.repository)
            result.append(spec)
        return result


def detection_tests(pkg_name: str, repository: spack.repo.RepoPath) -> List[Runner]:
    """Returns a list of test runners for a given package.

    Currently, detection tests are specified in a YAML file, called ``detection_test.yaml``,
    alongside the ``package.py`` file.

    This function reads that file to create a bunch of ``Runner`` objects.

    Args:
        pkg_name: name of the package to test
        repository: repository where the package lives
    """
    result = []
    detection_tests_content = read_detection_tests(pkg_name, repository)
    current_platform = str(spack.platforms.host())

    tests_by_path = detection_tests_content.get("paths", [])
    for single_test_data in tests_by_path:
        if current_platform not in single_test_data.get("platforms", [current_platform]):
            continue

        mock_executables: List[MockExecutables] = []
        mock_libraries: List[MockLibrary] = []
        for layout in single_test_data["layout"]:
            if "libraries" in layout:
                mock_libraries.extend(
                    MockLibrary(
                        path=x["path"],
                        soname=x.get("soname"),
                        needed=x.get("needed", []),
                        rpath=x.get("rpath"),
                        runpath=x.get("runpath"),
                    )
                    for x in layout["libraries"]
                )
                continue
            mock_executables.append(
                MockExecutables(
                    executables=layout["executables"],
                    script=layout["script"],
                    needed=layout.get("needed", []),
                    rpath=layout.get("rpath"),
                    runpath=layout.get("runpath"),
                )
            )
        expected_results = []
        for assertion in single_test_data["results"]:
            expected_results.append(
                ExpectedTestResult(
                    spec=assertion["spec"],
                    extra_attributes=assertion.get("extra_attributes", {}),
                    dependencies=assertion.get("dependencies"),
                )
            )

        current_test = DetectionTest(
            pkg_name=pkg_name,
            layout=mock_executables,
            results=expected_results,
            libraries=mock_libraries,
        )
        result.append(Runner(test=current_test, repository=repository))

    return result


def read_detection_tests(pkg_name: str, repository: spack.repo.RepoPath) -> Dict[str, Any]:
    """Returns the normalized content of the detection_tests.yaml associated with the package
    passed in input.

    The content is merged with that of any package that is transitively included using the
    "includes" attribute.

    Args:
        pkg_name: name of the package to test
        repository: repository in which to search for packages
    """
    content_stack, seen = [], set()
    included_packages: Deque[str] = collections.deque()

    root_detection_yaml, result = _detection_tests_yaml(pkg_name, repository)
    included_packages.extend(result.get("includes", []))
    seen |= set(result.get("includes", []))

    while included_packages:
        current_package = included_packages.popleft()
        try:
            current_detection_yaml, content = _detection_tests_yaml(current_package, repository)
        except FileNotFoundError as e:
            msg = (
                f"cannot read the detection tests from the '{current_package}' package, "
                f"included by {root_detection_yaml}"
            )
            raise FileNotFoundError(msg + f"\n\n\t{e}\n")

        content_stack.append((current_package, content))
        included_packages.extend(x for x in content.get("includes", []) if x not in seen)
        seen |= set(content.get("includes", []))

    result.setdefault("paths", [])
    for pkg_name, content in content_stack:
        result["paths"].extend(content.get("paths", []))

    return result


def _detection_tests_yaml(
    pkg_name: str, repository: spack.repo.RepoPath
) -> Tuple[pathlib.Path, Dict[str, Any]]:
    pkg_dir = pathlib.Path(repository.filename_for_package_name(pkg_name)).parent
    detection_tests_yaml = pkg_dir / "detection_test.yaml"
    with open(str(detection_tests_yaml), encoding="utf-8") as f:
        content = spack_yaml.load(f)
    return detection_tests_yaml, content
