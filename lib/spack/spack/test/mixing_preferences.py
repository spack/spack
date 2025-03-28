# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import archspec.cpu

import spack.compilers.libraries
import spack.config
import spack.error
import spack.operating_systems
import spack.platforms
import spack.repo
import spack.solver.asp
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
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
    requires("%gcc")

    provides("fortran-rt", "libgfortran")
    provides("libgfortran@3", when="%gcc@:6")
    provides("libgfortran@4", when="%gcc@7")
    provides("libgfortran@5", when="%gcc@8:")

    depends_on("libc", type="link", when="platform=linux")
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

    provides("c")
    provides("cxx")
    provides("fortran")

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        pkg("*").depends_on(
            "gcc-runtime",
            when="%gcc",
            type="link",
            description="If any package uses %gcc, it depends on gcc-runtime",
        )
        pkg("*").depends_on(
            f"gcc-runtime@{str(spec.version)}:",
            when=f"%{str(spec)}",
            type="link",
            description=f"If any package uses %{str(spec)}, "
            f"it depends on gcc-runtime@{str(spec.version)}:",
        )

        gfortran_str = "libgfortran@5"
        if spec.satisfies("gcc@:6"):
            gfortran_str = "libgfortran@3"
        elif spec.satisfies("gcc@7"):
            gfortran_str = "libgfortran@4"

        for fortran_virtual in ("fortran-rt", gfortran_str):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%{str(spec)}",
                languages=["fortran"],
                type="link",
                description=f"Add a dependency on '{gfortran_str}' for nodes compiled with "
                f"{str(spec)} and using the 'fortran' language",
            )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(f"@={str(spec.version)}", when=f"%{str(spec)}")

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(f"%gcc@:{str(spec.version)}", when=f"%{str(spec)}")
""",
)


_oneapi = (
    "intel-oneapi-compilers",
    """\
from spack.package import *

class IntelOneapiCompilers(CompilerPackage):
    has_code = False

    version("2025.0.3")

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        pkg("*").depends_on(
            "intel-oneapi-runtime",
            when="%oneapi",
            type="link",
            description="If any package uses %oneapi, it depends on intel-oneapi-runtime",
        )
        pkg("*").depends_on(
            f"intel-oneapi-runtime@{str(spec.version)}:",
            when=f"%{str(spec)}",
            type="link",
            description=f"If any package uses %{str(spec)}, "
            f"it depends on intel-oneapi-runtime@{str(spec.version)}:",
        )

        for fortran_virtual in ("fortran-rt", "libifcore@5"):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%{str(spec)}",
                languages=["fortran"],
                type="link",
                description=f"Add a dependency on 'libifcore' for nodes compiled with "
                f"{str(spec)} and using the 'fortran' language",
            )
        # The version of intel-oneapi-runtime is the same as the %oneapi used to "compile" it
        pkg("intel-oneapi-runtime").requires(f"@={str(spec.version)}", when=f"%{str(spec)}")
""",
)


_intel_runtime = (
    "intel-oneapi-runtime",
    """\
from spack.package import *

class IntelOneapiRuntime(Package):
    has_code = False

    tags = ["runtime"]
    requires("%oneapi")

    depends_on("gcc-runtime", type="link")

    provides("fortran-rt", "libifcore@5", when="%oneapi@2021:")

    depends_on("libc", type="link", when="platform=linux")
""",
)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(
        tmpdir,
        [_pkgx1, _pkgx2, _pkgx3, _pkgx4, _glibc, _gcc, _gcc_runtime, _oneapi, _intel_runtime],
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

    def __init__(self):
        super().__init__("linux")
        self.add_target(self.default, archspec.cpu.TARGETS[self.default])
        self.add_target(self.front_end, archspec.cpu.TARGETS[self.front_end])

        os = spack.operating_systems.OperatingSystem("debian", 6)
        self.add_operating_system(self.default_os, os)
        self.add_operating_system(self.front_os, os)


@pytest.fixture
def pretend_linux(monkeypatch, tmpdir):
    pretend_glibc = Spec("glibc@=2.28")
    pretend_glibc.external_path = str(tmpdir.join("fake-libc").ensure(dir=True))
    def give_me_a_libc(*args, **kwargs):
        return pretend_glibc

    monkeypatch.setattr(spack.compilers.libraries.CompilerPropertyDetector, "default_libc", give_me_a_libc)
    with spack.platforms.use_platform(TestLinux()):
        yield


def set_up_compiler_cfg():
    test_cfg = """\
packages:
  gcc:
    externals:
    - spec: "gcc@11.0.0 languages='c,c++,fortran' os=debian6 target=x86_64"
      prefix: /path1
      extra_attributes:
        compilers:
          cc: /path1/bin/gcc
          cxx: /path1/bin/g++
          fortran: /path1/bin/gfortran
  intel-oneapi-compilers:
    externals:
    - spec: "intel-oneapi-compilers@2025.0.3 os=debian6 target=x86_64"
      prefix: /path2
      extra_attributes:
        compilers:
          cc: /path2/bin/clang
          cxx: /path2/bin/clang++
          fortran: /path2/bin/flang
"""
    update_cfg_section("packages", test_cfg)


import spack.store
import os
from llnl.util.filesystem import copy_tree


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
            with spack.store.use_store(str(store_path)) as store:
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


def test_diamond_nomixing(concretize_scope, test_repo, pretend_linux, enable_runtimes, empty_database):
    set_up_compiler_cfg()
    Spec("x1").concretized()


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

    with pytest.raises(spack.error.UnsatisfiableSpecError):
        spec_cmd("--reuse", "x1%oneapi ^x4%gcc")

    with pytest.raises(spack.error.UnsatisfiableSpecError):
        spec_cmd("--reuse", "x1%gcc ^x4%oneapi")
