# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import pickle
import sys
import os

import pytest
import spack.environment as ev
import spack.llnl.util.filesystem as fs

import spack.error
from spack.llnl.util.filesystem import working_dir
from spack.main import SpackCommand

build_env = SpackCommand("build-env")
add = SpackCommand("add")
env = SpackCommand("env")
config = SpackCommand("config")
concretize = SpackCommand("concretize")
install = SpackCommand("install")


@pytest.mark.parametrize("pkg", [("pkg-c",), ("pkg-c", "--")])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_it_just_runs(pkg):
    build_env(*pkg)

    
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_env_mods_with_global_arg_e(monkeypatch, tmp_path):
    with fs.working_dir(str(tmp_path)):
        env("remove", "test", "-y")
        env("create", "test")
        test_env = ev.read("test")
        with test_env:
            config("add", "env_vars:unset:['PE_ENV']")
            add("gmake")
            install()

        with spack.util.environment.set_env(PE_ENV="PE_ENV_TEST"):
            #confirm the env variable is set
            output = os.environ.get("PE_ENV")
            assert "PE_ENV_TEST" in output

            #is it present in build-env -e ...
            output=build_env("gmake", global_args=["-e", str(tmp_path)])
            assert "PE_ENV_TEST" not in output
                
            #does env activate remove it?
            output = env("activate", "--sh", "test")
            assert "PE_ENV_TEST" not in output
            assert "export PE_ENV=''" in output



@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_error_when_multiple_specs_are_given():
    output = build_env("libelf libdwarf", fail_on_error=False)
    assert "only takes one spec" in output


@pytest.mark.parametrize("args", [("--", "/bin/sh", "-c", "echo test"), ("--",), ()])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_build_env_requires_a_spec(args):
    output = build_env(*args, fail_on_error=False)
    assert "requires a spec" in output


_out_file = "env.out"


@pytest.mark.parametrize("shell", ["pwsh", "bat"] if sys.platform == "win32" else ["sh"])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_dump(shell_as, shell, tmp_path: pathlib.Path):
    with working_dir(str(tmp_path)):
        build_env("--dump", _out_file, "pkg-c")
        with open(_out_file, encoding="utf-8") as f:
            if shell == "pwsh":
                assert any(line.startswith("$Env:PATH") for line in f.readlines())
            elif shell == "bat":
                assert any(line.startswith('set "PATH=') for line in f.readlines())
            else:
                assert any(line.startswith("PATH=") for line in f.readlines())


@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_pickle(tmp_path: pathlib.Path):
    with working_dir(str(tmp_path)):
        build_env("--pickle", _out_file, "pkg-c")
        environment = pickle.load(open(_out_file, "rb"))
        assert isinstance(environment, dict)
        assert "PATH" in environment


def test_failure_when_uninstalled_deps(config, mock_packages):
    with pytest.raises(
        spack.error.SpackError, match="Not all dependencies of dttop are installed"
    ):
        build_env("dttop")
