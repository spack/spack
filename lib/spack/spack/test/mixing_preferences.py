# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import archspec.cpu

from llnl.util.filesystem import copy_tree

import spack.compilers.libraries
import spack.config
import spack.error
import spack.operating_systems
import spack.platforms
import spack.repo
import spack.solver.asp
import spack.store
import spack.util.spack_yaml as syaml
from spack.main import SpackCommand
from spack.platforms._platform import Platform
from spack.spec import Spec
from spack.test.conftest import create_test_repo

solve = SpackCommand("solve")


def update_cfg_section(section, conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set(section, conf[section], scope="concretize")


_pkgx1 = (
    "x1",
    """\
from spack.package import *

class X1(Package):
    version("1.2")
    version("1.1")
    depends_on("x2")
    depends_on("x3")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
""",
)


_pkgx2 = (
    "x2",
    """\
from spack.package import *

class X2(Package):
    version("2.1")
    version("2.0")
    depends_on("x4")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
""",
)


_pkgx3 = (
    "x3",
    """\
from spack.package import *

class X3(Package):
    version("3.5")
    version("3.4")
    depends_on("x4")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
""",
)


_pkgx4 = (
    "x4",
    """\
from spack.package import *

class X4(Package):
    version("4.1")
    version("4.0")

    #depends_on("c", type="build")
    #depends_on("cxx", type="build")
    depends_on("fortran", type="build")
""",
)


_compiler_wrapper = (
    "compiler-wrapper",
    """\
from spack.package import *

class CompilerWrapper(Package):
    tags = ["runtime"]

    version("1.0")
    has_code = False

    def install(self, spec, prefix):
        # Not actually installed
        pass
""",
)


_glibc = (
    "glibc",
    """\
from spack.package import *

class Glibc(Package):
    tags = ["runtime"]

    provides("libc")
""",
)


# This includes libc dependency, unlike compiler_runtime.test repo
_gcc_runtime = (
    "gcc-runtime",
    """\
from spack.package import *

class GccRuntime(Package):
    has_code = False

    # Without this line, you get the concretizer version of a segfault
    tags = ["runtime"]

    provides("fortran-rt", "libgfortran")
    provides("libgfortran@3", when="%gcc@:6")
    provides("libgfortran@4", when="%gcc@7")
    provides("libgfortran@5", when="%gcc@8:")

    depends_on("libc", type="link", when="platform=linux")
    depends_on("gcc", type="build")
""",
)


_gcc = (
    "gcc",
    """\
from spack.package import *

class Gcc(CompilerPackage):
    has_code = False

    version("13.2.0")
    version("12.3.0")
    # Without this, I can't do spack spec gcc@11.0.0
    version("11.0.0")

    provides("c")
    provides("cxx")
    provides("fortran")

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        for language in ("c", "cxx", "fortran"):
            pkg("*").depends_on(
                f"gcc-runtime@{spec.version}:",
                when=f"%[virtuals={language}] {spec.name}@{spec.versions}",
                type="link",
                description=f"Inject gcc-runtime when gcc is used as a {language} compiler",
            )

        gfortran_str = "libgfortran@5"
        if spec.satisfies("gcc@:6"):
            gfortran_str = "libgfortran@3"
        elif spec.satisfies("gcc@7"):
            gfortran_str = "libgfortran@4"

        for fortran_virtual in ("fortran-rt", gfortran_str):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%[virtuals=fortran] {spec.name}@{spec.versions}",
                type="link",
                description=f"Add a dependency on '{gfortran_str}' for nodes compiled with "
                f"{spec} and using the 'fortran' language",
            )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(f"@{spec.versions}", when=f"%{spec.name}@{spec.versions}")

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(f"gcc@:{spec.version}", when=f"%{spec.name}@{spec.versions}")
""",
)


_oneapi = (
    "intel-oneapi-compilers",
    """\
from spack.package import *

class IntelOneapiCompilers(CompilerPackage):
    has_code = False

    version("2025.0.3")

    provides("c")
    provides("cxx")
    provides("fortran")

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        for language in ("c", "cxx", "fortran"):
            pkg("*").depends_on(
                f"intel-oneapi-runtime@{spec.version}:",
                when=f"%[virtuals={language}] {spec.name}@{spec.versions}",
                type="link",
                description="Inject intel-oneapi-runtime when oneapi is used as "
                f"a {language} compiler",
            )

        for fortran_virtual in ("fortran-rt", "libifcore@5"):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%[virtuals=fortran] {spec.name}@{spec.versions}",
                type="link",
                description="Add a dependency on 'libifcore' for nodes compiled with "
                f"{spec.name}@{spec.versions} and using the 'fortran' language",
            )
        # The version of intel-oneapi-runtime is the same as the %oneapi used to "compile" it
        pkg("intel-oneapi-runtime").requires(
            f"@{spec.versions}", when=f"%{spec.name}@{spec.versions}"
        )

        # If a node used %intel-oneapi-runtime@X.Y its dependencies must use @:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(
            f"intel-oneapi-compilers@:{spec.version}", when=f"%{spec.name}@{spec.versions}"
        )
""",
)


_intel_runtime = (
    "intel-oneapi-runtime",
    """\
from spack.package import *

class IntelOneapiRuntime(Package):
    has_code = False

    tags = ["runtime"]

    depends_on("gcc-runtime", type="link")

    provides("fortran-rt", "libifcore@5", when="%oneapi@2021:")

    depends_on("libc", type="link", when="platform=linux")
    depends_on("intel-oneapi-compilers", type="build")
""",
)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(
        tmpdir,
        [
            _pkgx1,
            _pkgx2,
            _pkgx3,
            _pkgx4,
            _glibc,
            _gcc,
            _gcc_runtime,
            _oneapi,
            _intel_runtime,
            _compiler_wrapper,
        ],
    )


@pytest.fixture
def enable_runtimes(monkeypatch):
    def yes_we_are_using_it():
        return True

    monkeypatch.setattr(spack.solver.asp, "using_libc_compatibility", yes_we_are_using_it)


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


install = SpackCommand("install")
solve = SpackCommand("solve")
spec_cmd = SpackCommand("spec")


class TestLinux(Platform):
    front_end = "x86_64"
    back_end = "x86_64"
    default = "x86_64"

    front_os = "debian6"
    back_os = "debian6"
    default_os = "debian6"

    def _init_targets(self):
        self.add_target(self.default, archspec.cpu.TARGETS[self.default])
        self.add_target(self.front_end, archspec.cpu.TARGETS[self.front_end])

    def __init__(self):
        super().__init__("linux")
        os = spack.operating_systems.OperatingSystem("debian", 6)
        self.add_operating_system(self.default_os, os)
        self.add_operating_system(self.front_os, os)


@pytest.fixture
def pretend_linux(monkeypatch, tmpdir):
    pretend_glibc = Spec("glibc@=2.28")
    pretend_glibc.external_path = str(tmpdir.join("fake-libc").ensure(dir=True))

    def give_me_a_libc(*args, **kwargs):
        return pretend_glibc

    monkeypatch.setattr(
        spack.compilers.libraries.CompilerPropertyDetector, "default_libc", give_me_a_libc
    )
    fake_linux = TestLinux()
    with spack.platforms.use_platform(fake_linux):
        yield


def set_up_compiler_cfg():
    test_cfg = """\
packages:
  gcc::
    externals:
    - spec: "gcc@11.0.0 os=debian6 target=x86_64"
      prefix: /path1
      extra_attributes:
        compilers:
          c: /path1/bin/gcc
          cxx: /path1/bin/g++
          fortran: /path1/bin/gfortran
  intel-oneapi-compilers::
    externals:
    - spec: "intel-oneapi-compilers@2025.0.3 os=debian6 target=x86_64"
      prefix: /path2
      extra_attributes:
        compilers:
          c: /path2/bin/clang
          cxx: /path2/bin/clang++
          fortran: /path2/bin/flang
"""
    update_cfg_section("packages", test_cfg)


@pytest.fixture(scope="function")
def empty_mock_store(
    tmpdir_factory,
    mock_wsdk_externals,
    mock_repo_path,
    mock_configuration_scopes,
    _store_dir_and_cache,
):
    store_path, store_cache = _store_dir_and_cache
    store_path.chmod(mode=0o555, rec=1)

    if not os.path.exists(str(store_cache.join(".spack-db"))):
        with spack.config.use_configuration(*mock_configuration_scopes):
            with spack.store.use_store(str(store_path)):
                with spack.repo.use_repositories(mock_repo_path):
                    store_path.chmod(mode=0o755, rec=1)
                    store_path.chmod(mode=0o755, rec=1)

        store_cache.chmod(mode=0o755, rec=1)
        copy_tree(str(store_path), str(store_cache))
        store_cache.chmod(mode=0o555, rec=1)

    yield store_path


@pytest.fixture(scope="function")
def empty_database(empty_mock_store):
    """This activates the mock store, packages, AND config."""
    with spack.store.use_store(str(empty_mock_store)) as store:
        yield store.db
        # Force reading the database again between tests
        store.db.last_seen_verifier = ""


def test_diamond_nomixing(
    concretize_scope, test_repo, pretend_linux, enable_runtimes, empty_database
):
    set_up_compiler_cfg()
    # First try gcc itself
    Spec("gcc@11.0.0").concretized()
    # out = solve("--show=asp", "x1 %gcc@11.0.0")
    # with open("/Users/scheibel1/Desktop/spack/spack/x1.asp", "w") as f:
    #    f.write(out)
    # Then try a package w/ no deps
    Spec("x4 %gcc@11.0.0").concretized()
    # Then try a package with deps
    Spec("x1 %gcc@11.0.0").concretized()
    # Spec("x1 ^[virtuals=c] gcc@11.0.0").concretized()


def test_mixing_fortran(
    mutable_mock_env_path,
    temporary_store,
    concretize_scope,
    test_repo,
    pretend_linux,
    enable_runtimes,
):
    """The constraints for the compilers in this test repo should prevent
    mixing them in a DAG where all nodes depend on fortran.
    """
    set_up_compiler_cfg()
    spec_cmd("--reuse", "x4%oneapi")

    # Specifying that the mixing should be forced is awkward. For now
    # this is achieved in part by making x4 Fortan-only
    with pytest.raises(spack.error.UnsatisfiableSpecError):
        spec_cmd("--reuse", "x1 ^[virtuals=fortran] oneapi ^x4%gcc")

    # with pytest.raises(spack.error.UnsatisfiableSpecError):
    #    spec_cmd("--reuse", "x1%gcc ^x4%oneapi")
