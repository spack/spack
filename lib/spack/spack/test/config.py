# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import getpass
import io
import os
import pathlib
import tempfile
import textwrap
from datetime import date

import pytest

import spack
import spack.config
import spack.directory_layout
import spack.environment as ev
import spack.error
import spack.llnl.util.filesystem as fs
import spack.package_base
import spack.paths
import spack.platforms
import spack.repo
import spack.schema.compilers
import spack.schema.config
import spack.schema.env
import spack.schema.include
import spack.schema.mirrors
import spack.schema.repos
import spack.spec
import spack.store
import spack.util.executable
import spack.util.git
import spack.util.path as spack_path
import spack.util.spack_yaml as syaml
from spack.enums import ConfigScopePriority
from spack.llnl.util.filesystem import join_path, touch
from spack.util.spack_yaml import DictWithLineInfo

# sample config data
config_low = {
    "config": {
        "install_tree": {"root": "install_tree_path"},
        "build_stage": ["path1", "path2", "path3"],
    }
}

config_override_all = {"config:": {"install_tree:": {"root": "override_all"}}}

config_override_key = {"config": {"install_tree:": {"root": "override_key"}}}

config_merge_list = {"config": {"build_stage": ["patha", "pathb"]}}

config_override_list = {"config": {"build_stage:": ["pathd", "pathe"]}}

config_merge_dict = {"config": {"aliases": {"ls": "find", "dev": "develop"}}}

config_override_dict = {"config": {"aliases:": {"be": "build-env", "deps": "dependencies"}}}


@pytest.fixture()
def env_yaml(tmp_path: pathlib.Path):
    """Return a sample env.yaml for test purposes"""
    env_yaml = str(tmp_path / "env.yaml")
    with open(env_yaml, "w", encoding="utf-8") as f:
        f.write(
            """\
spack:
    config:
        verify_ssl: False
        dirty: False
    packages:
        all:
            compiler: [ 'gcc@4.5.3' ]
    repos:
        z: /x/y/z
"""
        )
    return env_yaml


def cross_plat_join(*pths):
    """os.path.join does not prepend paths to other paths
       beginning with a Windows drive label i.e. D:\\
    """
    return os.sep.join([pth for pth in pths])


def check_compiler_config(comps, *compiler_names):
    """Check that named compilers in comps match Spack's config."""
    config = spack.config.get("compilers")
    compiler_list = ["cc", "cxx", "f77", "fc"]
    flag_list = ["cflags", "cxxflags", "fflags", "cppflags", "ldflags", "ldlibs"]
    param_list = ["modules", "paths", "spec", "operating_system"]
    for compiler in config:
        conf = compiler["compiler"]
        if conf["spec"] in compiler_names:
            comp = next(
                (c["compiler"] for c in comps if c["compiler"]["spec"] == conf["spec"]), None
            )
            if not comp:
                raise ValueError("Bad config spec")
            for p in param_list:
                assert conf[p] == comp[p]
            for f in flag_list:
                expected = comp.get("flags", {}).get(f, None)
                actual = conf.get("flags", {}).get(f, None)
                assert expected == actual
            for c in compiler_list:
                expected = comp["paths"][c]
                actual = conf["paths"][c]
                assert expected == actual


#
# Some sample compiler config data and tests.
#
a_comps = {
    "compilers": [
        {
            "compiler": {
                "paths": {"cc": "/gcc473", "cxx": "/g++473", "f77": None, "fc": None},
                "modules": None,
                "spec": "gcc@4.7.3",
                "operating_system": "CNL10",
            }
        },
        {
            "compiler": {
                "paths": {"cc": "/gcc450", "cxx": "/g++450", "f77": "gfortran", "fc": "gfortran"},
                "modules": None,
                "spec": "gcc@4.5.0",
                "operating_system": "CNL10",
            }
        },
        {
            "compiler": {
                "paths": {"cc": "/gcc422", "cxx": "/g++422", "f77": "gfortran", "fc": "gfortran"},
                "flags": {"cppflags": "-O0 -fpic", "fflags": "-f77"},
                "modules": None,
                "spec": "gcc@4.2.2",
                "operating_system": "CNL10",
            }
        },
        {
            "compiler": {
                "paths": {
                    "cc": "<overwritten>",
                    "cxx": "<overwritten>",
                    "f77": "<overwritten>",
                    "fc": "<overwritten>",
                },
                "modules": None,
                "spec": "clang@3.3",
                "operating_system": "CNL10",
            }
        },
    ]
}

b_comps = {
    "compilers": [
        {
            "compiler": {
                "paths": {"cc": "/icc100", "cxx": "/icp100", "f77": None, "fc": None},
                "modules": None,
                "spec": "icc@10.0",
                "operating_system": "CNL10",
            }
        },
        {
            "compiler": {
                "paths": {"cc": "/icc111", "cxx": "/icp111", "f77": "ifort", "fc": "ifort"},
                "modules": None,
                "spec": "icc@11.1",
                "operating_system": "CNL10",
            }
        },
        {
            "compiler": {
                "paths": {"cc": "/icc123", "cxx": "/icp123", "f77": "ifort", "fc": "ifort"},
                "flags": {"cppflags": "-O3", "fflags": "-f77rtl"},
                "modules": None,
                "spec": "icc@12.3",
                "operating_system": "CNL10",
            }
        },
        {
            "compiler": {
                "paths": {
                    "cc": "<overwritten>",
                    "cxx": "<overwritten>",
                    "f77": "<overwritten>",
                    "fc": "<overwritten>",
                },
                "modules": None,
                "spec": "clang@3.3",
                "operating_system": "CNL10",
            }
        },
    ]
}


@pytest.fixture()
def compiler_specs():
    """Returns a couple of compiler specs needed for the tests"""
    a = [ac["compiler"]["spec"] for ac in a_comps["compilers"]]
    b = [bc["compiler"]["spec"] for bc in b_comps["compilers"]]
    CompilerSpecs = collections.namedtuple("CompilerSpecs", ["a", "b"])
    return CompilerSpecs(a=a, b=b)


def test_write_key_in_memory(mock_low_high_config, compiler_specs):
    # Write b_comps "on top of" a_comps.
    spack.config.set("compilers", a_comps["compilers"], scope="low")
    spack.config.set("compilers", b_comps["compilers"], scope="high")

    # Make sure the config looks how we expect.
    check_compiler_config(a_comps["compilers"], *compiler_specs.a)
    check_compiler_config(b_comps["compilers"], *compiler_specs.b)


def test_write_key_to_disk(mock_low_high_config, compiler_specs):
    # Write b_comps "on top of" a_comps.
    spack.config.set("compilers", a_comps["compilers"], scope="low")
    spack.config.set("compilers", b_comps["compilers"], scope="high")

    # Clear caches so we're forced to read from disk.
    spack.config.CONFIG.clear_caches()

    # Same check again, to ensure consistency.
    check_compiler_config(a_comps["compilers"], *compiler_specs.a)
    check_compiler_config(b_comps["compilers"], *compiler_specs.b)


def test_write_to_same_priority_file(mock_low_high_config, compiler_specs):
    # Write b_comps in the same file as a_comps.
    spack.config.set("compilers", a_comps["compilers"], scope="low")
    spack.config.set("compilers", b_comps["compilers"], scope="low")

    # Clear caches so we're forced to read from disk.
    spack.config.CONFIG.clear_caches()

    # Same check again, to ensure consistency.
    check_compiler_config(a_comps["compilers"], *compiler_specs.a)
    check_compiler_config(b_comps["compilers"], *compiler_specs.b)


#
# Sample repo data and tests
#
repos_low = {"repos": {"low": "/some/path"}}
repos_high = {"repos": {"high": "/some/other/path"}}

# Test setting config values via path in filename


def test_add_config_path(mutable_config):
    # Try setting a new install tree root
    path = "config:install_tree:root:/path/to/config.yaml"
    spack.config.add(path)
    set_value = spack.config.get("config")["install_tree"]["root"]
    assert set_value == "/path/to/config.yaml"

    # Now a package:all setting
    path = "packages:all:target:[x86_64]"
    spack.config.add(path)
    targets = spack.config.get("packages")["all"]["target"]
    assert "x86_64" in targets

    # Try quotes to escape brackets
    path = (
        "config:install_tree:projections:cmake:"
        "'{architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}'"
    )
    spack.config.add(path)
    set_value = spack.config.get("config")["install_tree"]["projections"]["cmake"]
    assert set_value == "{architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}"

    path = 'modules:default:tcl:all:environment:set:"{name}_ROOT":"{prefix}"'
    spack.config.add(path)
    set_value = spack.config.get("modules")["default"]["tcl"]["all"]["environment"]["set"]
    assert r"{name}_ROOT" in set_value
    assert set_value[r"{name}_ROOT"] == r"{prefix}"
    assert spack.config.get('modules:default:tcl:all:environment:set:"{name}_ROOT"') == r"{prefix}"

    # NOTE:
    # The config path: "config:install_tree:root:<path>" is unique in that it can accept multiple
    # schemas (such as a dropped "root" component) which is atypical and may lead to passing tests
    # when the behavior is in reality incorrect.
    # the config path below is such that no subkey accepts a string as a valid entry in our schema

    # try quotes to escape colons
    path = "config:build_stage:'C:\\path\\to\\config.yaml'"
    spack.config.add(path)
    set_value = spack.config.get("config")["build_stage"]
    assert "C:\\path\\to\\config.yaml" in set_value


@pytest.mark.regression("17543,23259")
def test_add_config_path_with_enumerated_type(mutable_config):
    spack.config.add("config:flags:keep_werror:all")
    assert spack.config.get("config")["flags"]["keep_werror"] == "all"

    spack.config.add("config:flags:keep_werror:specific")
    assert spack.config.get("config")["flags"]["keep_werror"] == "specific"

    with pytest.raises(spack.error.ConfigError):
        spack.config.add("config:flags:keep_werror:foo")


def test_add_config_filename(mock_low_high_config, tmp_path: pathlib.Path):
    config_yaml = tmp_path / "config-filename.yaml"
    config_yaml.touch()
    with config_yaml.open("w") as f:
        syaml.dump_config(config_low, f)

    spack.config.add_from_file(str(config_yaml), scope="low")
    assert "build_stage" in spack.config.get("config")
    build_stages = spack.config.get("config")["build_stage"]
    for stage in config_low["config"]["build_stage"]:
        assert stage in build_stages


# repos
def test_write_list_in_memory(mock_low_high_config):
    spack.config.set("repos", repos_low["repos"], scope="low")
    spack.config.set("repos", repos_high["repos"], scope="high")

    config = spack.config.get("repos")
    assert config == {**repos_high["repos"], **repos_low["repos"]}


class MockEnv:
    def __init__(self, path):
        self.path = path


def test_substitute_config_variables(mock_low_high_config, monkeypatch):
    prefix = spack.paths.prefix.lstrip("/")
    assert cross_plat_join(
        os.sep + os.path.join("foo", "bar", "baz"), prefix
    ) == spack_path.canonicalize_path("/foo/bar/baz/$spack")

    assert cross_plat_join(
        spack.paths.prefix, os.path.join("foo", "bar", "baz")
    ) == spack_path.canonicalize_path("$spack/foo/bar/baz/")

    assert cross_plat_join(
        os.sep + os.path.join("foo", "bar", "baz"), prefix, os.path.join("foo", "bar", "baz")
    ) == spack_path.canonicalize_path("/foo/bar/baz/$spack/foo/bar/baz/")

    assert cross_plat_join(
        os.sep + os.path.join("foo", "bar", "baz"), prefix
    ) == spack_path.canonicalize_path("/foo/bar/baz/${spack}")

    assert cross_plat_join(
        spack.paths.prefix, os.path.join("foo", "bar", "baz")
    ) == spack_path.canonicalize_path("${spack}/foo/bar/baz/")

    assert cross_plat_join(
        os.sep + os.path.join("foo", "bar", "baz"), prefix, os.path.join("foo", "bar", "baz")
    ) == spack_path.canonicalize_path("/foo/bar/baz/${spack}/foo/bar/baz/")

    assert cross_plat_join(
        os.sep + os.path.join("foo", "bar", "baz"), prefix, os.path.join("foo", "bar", "baz")
    ) != spack_path.canonicalize_path("/foo/bar/baz/${spack/foo/bar/baz/")

    # $env replacement is a no-op when no environment is active
    assert spack_path.canonicalize_path(
        os.sep + os.path.join("foo", "bar", "baz", "$env")
    ) == os.sep + os.path.join("foo", "bar", "baz", "$env")

    # Fake an active environment and $env is replaced properly
    fake_env_path = os.sep + os.path.join("quux", "quuux")
    monkeypatch.setattr(ev, "active_environment", lambda: MockEnv(fake_env_path))
    assert spack_path.canonicalize_path("$env/foo/bar/baz") == os.path.join(
        fake_env_path, os.path.join("foo", "bar", "baz")
    )

    # relative paths without source information are relative to cwd
    assert spack_path.canonicalize_path(os.path.join("foo", "bar", "baz")) == os.path.abspath(
        os.path.join("foo", "bar", "baz")
    )

    # relative paths with source information are relative to the file
    spack.config.set(
        "modules:default", {"roots": {"lmod": os.path.join("foo", "bar", "baz")}}, scope="low"
    )
    spack.config.CONFIG.clear_caches()
    path = spack.config.get("modules:default:roots:lmod")
    assert spack_path.canonicalize_path(path) == os.path.normpath(
        os.path.join(mock_low_high_config.scopes["low"].path, os.path.join("foo", "bar", "baz"))
    )

    # test architecture information is in replacements
    assert spack_path.canonicalize_path(
        os.path.join("foo", "$platform", "bar")
    ) == os.path.abspath(os.path.join("foo", "test", "bar"))

    host_target = spack.platforms.host().default_target()
    host_target_family = str(host_target.family)
    assert spack_path.canonicalize_path(
        os.path.join("foo", "$target_family", "bar")
    ) == os.path.abspath(os.path.join("foo", host_target_family, "bar"))


packages_merge_low = {"packages": {"foo": {"variants": ["+v1"]}, "bar": {"variants": ["+v2"]}}}

packages_merge_high = {
    "packages": {
        "foo": {"version": ["a"]},
        "bar": {"version": ["b"], "variants": ["+v3"]},
        "baz": {"version": ["c"]},
    }
}


@pytest.mark.regression("7924")
def test_merge_with_defaults(mock_low_high_config, write_config_file):
    """This ensures that specified preferences merge with defaults as
    expected. Originally all defaults were initialized with the
    exact same object, which led to aliasing problems. Therefore
    the test configs used here leave 'version' blank for multiple
    packages in 'packages_merge_low'.
    """
    write_config_file("packages", packages_merge_low, "low")
    write_config_file("packages", packages_merge_high, "high")
    cfg = spack.config.get("packages")

    assert cfg["foo"]["version"] == ["a"]
    assert cfg["bar"]["version"] == ["b"]
    assert cfg["baz"]["version"] == ["c"]


def test_substitute_user(mock_low_high_config):
    user = getpass.getuser()
    assert os.sep + os.path.join(
        "foo", "bar"
    ) + os.sep + user + os.sep + "baz" == spack_path.canonicalize_path(
        os.sep + os.path.join("foo", "bar", "$user", "baz")
    )


def test_substitute_user_cache(mock_low_high_config):
    user_cache_path = spack.paths.user_cache_path
    assert user_cache_path + os.sep + "baz" == spack_path.canonicalize_path(
        os.path.join("$user_cache_path", "baz")
    )


def test_substitute_tempdir(mock_low_high_config):
    tempdir = tempfile.gettempdir()
    assert tempdir == spack_path.canonicalize_path("$tempdir")
    assert tempdir + os.sep + os.path.join("foo", "bar", "baz") == spack_path.canonicalize_path(
        os.path.join("$tempdir", "foo", "bar", "baz")
    )


def test_substitute_date(mock_low_high_config):
    test_path = os.path.join("hello", "world", "on", "$date")
    new_path = spack_path.canonicalize_path(test_path)
    assert "$date" in test_path
    assert date.today().strftime("%Y-%m-%d") in new_path


def test_substitute_spack_version():
    version = spack.spack_version_info
    assert spack_path.canonicalize_path(
        "spack$spack_short_version/test"
    ) == spack_path.canonicalize_path(f"spack{version[0]}.{version[1]}/test")


PAD_STRING = spack_path.SPACK_PATH_PADDING_CHARS
MAX_PATH_LEN = spack_path.get_system_path_max()
MAX_PADDED_LEN = MAX_PATH_LEN - spack_path.SPACK_MAX_INSTALL_PATH_LENGTH
reps = [PAD_STRING for _ in range((MAX_PADDED_LEN // len(PAD_STRING) + 1) + 2)]
full_padded_string = os.path.join(os.sep + "path", os.sep.join(reps))[:MAX_PADDED_LEN]


@pytest.mark.parametrize(
    "config_settings,expected",
    [
        ([], [None, None, None]),
        ([["config:install_tree:root", os.sep + "path"]], [os.sep + "path", None, None]),
        (
            [["config:install_tree:projections", {"all": "{name}"}]],
            [None, None, {"all": "{name}"}],
        ),
    ],
)
def test_parse_install_tree(config_settings, expected, mutable_config):
    expected_root = expected[0] or mutable_config.get("config:install_tree:root")
    expected_unpadded_root = expected[1] or expected_root
    expected_proj = expected[2] or spack.directory_layout.default_projections

    # config settings is a list of 2-element lists, [path, value]
    # where path is a config path and value is the value to set at that path
    # these can be "splatted" in as the arguments to config.set
    for config_setting in config_settings:
        mutable_config.set(*config_setting)

    config_dict = mutable_config.get("config")
    root, unpadded_root, projections = spack.store.parse_install_tree(config_dict)
    assert root == expected_root
    assert unpadded_root == expected_unpadded_root
    assert projections == expected_proj


def test_change_or_add(mutable_config, mock_packages):
    spack.config.add("packages:a:version:['1.0']", scope="user")

    spack.config.add("packages:b:version:['1.1']", scope="system")

    class ChangeTest:
        def __init__(self, pkg_name, new_version):
            self.pkg_name = pkg_name
            self.new_version = new_version

        def find_fn(self, section):
            return self.pkg_name in section

        def change_fn(self, section):
            pkg_section = section.get(self.pkg_name, {})
            pkg_section["version"] = self.new_version
            section[self.pkg_name] = pkg_section

    change1 = ChangeTest("b", ["1.2"])
    spack.config.change_or_add("packages", change1.find_fn, change1.change_fn)
    assert "b" not in mutable_config.get("packages", scope="user")
    assert mutable_config.get("packages")["b"]["version"] == ["1.2"]

    change2 = ChangeTest("c", ["1.0"])
    spack.config.change_or_add("packages", change2.find_fn, change2.change_fn)
    assert "c" in mutable_config.get("packages", scope="user")


@pytest.mark.not_on_windows("Padding unsupported on Windows")
@pytest.mark.parametrize(
    "config_settings,expected",
    [
        (
            [
                ["config:install_tree:root", os.sep + "path"],
                ["config:install_tree:padded_length", 11],
            ],
            [os.path.join(os.sep + "path", PAD_STRING[:5]), os.sep + "path", None],
        ),
        (
            [["config:install_tree:root", "/path/$padding:11"]],
            [os.path.join(os.sep + "path", PAD_STRING[:5]), os.sep + "path", None],
        ),
        ([["config:install_tree:padded_length", False]], [None, None, None]),
        (
            [
                ["config:install_tree:padded_length", True],
                ["config:install_tree:root", os.sep + "path"],
            ],
            [full_padded_string, os.sep + "path", None],
        ),
    ],
)
def test_parse_install_tree_padded(config_settings, expected, mutable_config):
    expected_root = expected[0] or mutable_config.get("config:install_tree:root")
    expected_unpadded_root = expected[1] or expected_root
    expected_proj = expected[2] or spack.directory_layout.default_projections

    # config settings is a list of 2-element lists, [path, value]
    # where path is a config path and value is the value to set at that path
    # these can be "splatted" in as the arguments to config.set
    for config_setting in config_settings:
        mutable_config.set(*config_setting)

    config_dict = mutable_config.get("config")
    root, unpadded_root, projections = spack.store.parse_install_tree(config_dict)
    assert root == expected_root
    assert unpadded_root == expected_unpadded_root
    assert projections == expected_proj


def test_read_config(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")
    assert spack.config.get("config") == config_low["config"]


def test_read_config_override_all(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")
    write_config_file("config", config_override_all, "high")
    assert spack.config.get("config") == {"install_tree": {"root": "override_all"}}


def test_read_config_override_key(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")
    write_config_file("config", config_override_key, "high")
    assert spack.config.get("config") == {
        "install_tree": {"root": "override_key"},
        "build_stage": ["path1", "path2", "path3"],
    }


def test_read_config_merge_list(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")
    write_config_file("config", config_merge_list, "high")
    assert spack.config.get("config") == {
        "install_tree": {"root": "install_tree_path"},
        "build_stage": ["patha", "pathb", "path1", "path2", "path3"],
    }


def test_read_config_override_list(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")
    write_config_file("config", config_override_list, "high")
    assert spack.config.get("config") == {
        "install_tree": {"root": "install_tree_path"},
        "build_stage": config_override_list["config"]["build_stage:"],
    }


def test_internal_config_update(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")

    before = mock_low_high_config.get("config")
    assert before["install_tree"]["root"] == "install_tree_path"

    # add an internal configuration scope
    scope = spack.config.InternalConfigScope("command_line")
    assert "InternalConfigScope" in repr(scope)

    mock_low_high_config.push_scope(scope)

    command_config = mock_low_high_config.get("config", scope="command_line")
    command_config["install_tree"] = {"root": "foo/bar"}

    mock_low_high_config.set("config", command_config, scope="command_line")

    after = mock_low_high_config.get("config")
    assert after["install_tree"]["root"] == "foo/bar"


def test_internal_config_filename(mock_low_high_config, write_config_file):
    write_config_file("config", config_low, "low")
    mock_low_high_config.push_scope(spack.config.InternalConfigScope("command_line"))

    with pytest.raises(NotImplementedError):
        mock_low_high_config.get_config_filename("command_line", "config")


def test_mark_internal():
    data = {
        "config": {
            "bool": False,
            "int": 6,
            "numbers": [1, 2, 3],
            "string": "foo",
            "dict": {"more_numbers": [1, 2, 3], "another_string": "foo", "another_int": 7},
        }
    }

    marked = spack.config._mark_internal(data, "x")

    # marked version should be equal to the original
    assert data == marked

    def assert_marked(obj):
        if type(obj) is bool:
            return  # can't subclass bool, so can't mark it

        assert hasattr(obj, "_start_mark") and obj._start_mark.name == "x"
        assert hasattr(obj, "_end_mark") and obj._end_mark.name == "x"

    # everything in the marked version should have marks
    checks = (
        marked.keys(),
        marked.values(),
        marked["config"].keys(),
        marked["config"].values(),
        marked["config"]["numbers"],
        marked["config"]["dict"].keys(),
        marked["config"]["dict"].values(),
        marked["config"]["dict"]["more_numbers"],
    )

    for seq in checks:
        for obj in seq:
            assert_marked(obj)


def test_internal_config_from_data():
    config = spack.config.create_from(
        spack.config.InternalConfigScope(
            "_builtin", {"config": {"verify_ssl": False, "build_jobs": 6}}
        )
    )

    assert config.get("config:verify_ssl", scope="_builtin") is False
    assert config.get("config:build_jobs", scope="_builtin") == 6

    assert config.get("config:verify_ssl") is False
    assert config.get("config:build_jobs") == 6

    # push one on top and see what happens.
    config.push_scope(
        spack.config.InternalConfigScope(
            "higher", {"config": {"checksum": True, "verify_ssl": True}}
        )
    )

    assert config.get("config:verify_ssl", scope="_builtin") is False
    assert config.get("config:build_jobs", scope="_builtin") == 6

    assert config.get("config:verify_ssl", scope="higher") is True
    assert config.get("config:build_jobs", scope="higher") is None

    assert config.get("config:verify_ssl") is True
    assert config.get("config:build_jobs") == 6
    assert config.get("config:checksum") is True

    assert config.get("config:checksum", scope="_builtin") is None
    assert config.get("config:checksum", scope="higher") is True


def test_keys_are_ordered(configuration_dir):
    """Test that keys in Spack YAML files retain their order from the file."""
    expected_order = (
        "./bin",
        "./man",
        "./share/man",
        "./share/aclocal",
        "./lib/pkgconfig",
        "./lib64/pkgconfig",
        "./share/pkgconfig",
        "./",
    )

    config_scope = spack.config.DirectoryConfigScope("modules", configuration_dir / "site")

    data = config_scope.get_section("modules")

    prefix_inspections = data["modules"]["prefix_inspections"]

    for actual, expected in zip(prefix_inspections, expected_order):
        assert actual == expected


def test_config_format_error(mutable_config):
    """This is raised when we try to write a bad configuration."""
    with pytest.raises(spack.config.ConfigFormatError):
        spack.config.set("compilers", {"bad": "data"}, scope="site")


def get_config_error(filename, schema, yaml_string):
    """Parse a YAML string and return the resulting ConfigFormatError.

    Fail if there is no ConfigFormatError
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(yaml_string)

    # parse and return error, or fail.
    try:
        spack.config.read_config_file(filename, schema)
    except spack.config.ConfigFormatError as e:
        return e
    else:
        pytest.fail("ConfigFormatError was not raised!")


def test_config_parse_dict_in_list(tmp_path: pathlib.Path):
    with fs.working_dir(str(tmp_path)):
        e = get_config_error(
            "repos.yaml",
            spack.schema.repos.schema,
            """\
repos:
  a: https://foobar.com/foo
  b: https://foobar.com/bar
  c:
    error:
    - abcdef
  d: https://foobar.com/baz
""",
        )
        assert "repos.yaml:2" in str(e)


def test_config_parse_str_not_bool(tmp_path: pathlib.Path):
    with fs.working_dir(str(tmp_path)):
        e = get_config_error(
            "config.yaml",
            spack.schema.config.schema,
            """\
config:
    verify_ssl: False
    checksum: foobar
    dirty: True
""",
        )
        assert "config.yaml:3" in str(e)


def test_config_parse_list_in_dict(tmp_path: pathlib.Path):
    with fs.working_dir(str(tmp_path)):
        e = get_config_error(
            "mirrors.yaml",
            spack.schema.mirrors.schema,
            """\
mirrors:
    foo: http://foobar.com/baz
    bar: http://barbaz.com/foo
    baz: http://bazfoo.com/bar
    travis: [1, 2, 3]
""",
        )
        assert "mirrors.yaml:5" in str(e)


def test_bad_config_section(mock_low_high_config):
    """Test that getting or setting a bad section gives an error."""
    with pytest.raises(spack.config.ConfigSectionError):
        spack.config.set("foobar", "foobar")

    with pytest.raises(spack.config.ConfigSectionError):
        spack.config.get("foobar")


def test_nested_override():
    """Ensure proper scope naming of nested overrides."""
    base_name = spack.config._OVERRIDES_BASE_NAME

    def _check_scopes(num_expected, debug_values):
        scope_names = [
            s.name for s in spack.config.CONFIG.scopes.values() if s.name.startswith(base_name)
        ]

        for i in range(num_expected):
            name = "{0}{1}".format(base_name, i)
            assert name in scope_names

            data = spack.config.CONFIG.get_config("config", name)
            assert data["debug"] == debug_values[i]

    # Check results from single and nested override
    with spack.config.override("config:debug", True):
        with spack.config.override("config:debug", False):
            _check_scopes(2, [True, False])

        _check_scopes(1, [True])


def test_alternate_override(monkeypatch):
    """Ensure proper scope naming of override when conflict present."""
    base_name = spack.config._OVERRIDES_BASE_NAME

    def _matching_scopes(regexpr):
        return [spack.config.InternalConfigScope("{0}1".format(base_name))]

    # Check that the alternate naming works
    monkeypatch.setattr(spack.config.CONFIG, "matching_scopes", _matching_scopes)

    with spack.config.override("config:debug", False):
        name = "{0}2".format(base_name)

        scope_names = [
            s.name for s in spack.config.CONFIG.scopes.values() if s.name.startswith(base_name)
        ]
        assert name in scope_names

        data = spack.config.CONFIG.get_config("config", name)
        assert data["debug"] is False


def test_immutable_scope(tmp_path: pathlib.Path):
    config_yaml = str(tmp_path / "config.yaml")
    with open(config_yaml, "w", encoding="utf-8") as f:
        f.write(
            """\
config:
    install_tree:
      root: dummy_tree_value
"""
        )
    scope = spack.config.DirectoryConfigScope("test", str(tmp_path), writable=False)

    data = scope.get_section("config")
    assert data is not None
    assert data["config"]["install_tree"] == {"root": "dummy_tree_value"}

    with pytest.raises(spack.error.ConfigError):
        scope._write_section("config")


def test_single_file_scope(config, env_yaml):
    scope = spack.config.SingleFileScope(
        "env", env_yaml, spack.schema.env.schema, yaml_path=["spack"]
    )

    with spack.config.override(scope):
        # from the single-file config
        assert spack.config.get("config:verify_ssl") is False
        assert spack.config.get("config:dirty") is False

        # from the lower config scopes
        assert spack.config.get("config:checksum") is True
        assert spack.config.get("config:checksum") is True
        assert spack.config.get("packages:externalmodule:buildable") is False
        assert spack.config.get("repos") == {
            "z": "/x/y/z",
            "builtin_mock": "$spack/var/spack/test_repos/spack_repo/builtin_mock",
        }


def test_single_file_scope_section_override(tmp_path: pathlib.Path, config):
    """Check that individual config sections can be overridden in an
    environment config. The config here primarily differs in that the
    ``packages`` section is intended to override all other scopes (using the
    "::" syntax).
    """
    env_yaml = str(tmp_path / "env.yaml")
    with open(env_yaml, "w", encoding="utf-8") as f:
        f.write(
            """\
spack:
    config:
        verify_ssl: False
    packages::
        all:
            target: [ x86_64 ]
    repos:
        z: /x/y/z
"""
        )

    scope = spack.config.SingleFileScope(
        "env", env_yaml, spack.schema.env.schema, yaml_path=["spack"]
    )

    with spack.config.override(scope):
        # from the single-file config
        assert spack.config.get("config:verify_ssl") is False
        assert spack.config.get("packages:all:target") == ["x86_64"]

        # from the lower config scopes
        assert spack.config.get("config:checksum") is True
        assert not spack.config.get("packages:externalmodule")
        assert spack.config.get("repos") == {
            "z": "/x/y/z",
            "builtin_mock": "$spack/var/spack/test_repos/spack_repo/builtin_mock",
        }


def test_write_empty_single_file_scope(tmp_path: pathlib.Path):
    env_schema = spack.schema.env.schema
    config_file = tmp_path / "config.yaml"
    config_file.touch()
    scope = spack.config.SingleFileScope("test", str(config_file), env_schema, yaml_path=["spack"])
    scope._write_section("config")
    # confirm we can write empty config
    assert not scope.get_section("config")


def check_schema(name, file_contents):
    """Check a Spack YAML schema against some data"""
    f = io.StringIO(file_contents)
    data = syaml.load_config(f)
    spack.config.validate(data, name)


def test_good_env_yaml():
    check_schema(
        spack.schema.env.schema,
        """\
spack:
    config:
        verify_ssl: False
        dirty: False
    repos:
        - ~/my/repo/location
    mirrors:
        remote: /foo/bar/baz
    compilers:
        - compiler:
            spec: cce@2.1
            operating_system: cnl
            modules: []
            paths:
                cc: /path/to/cc
                cxx: /path/to/cxx
                fc: /path/to/fc
                f77: /path/to/f77
""",
    )


def test_bad_env_yaml():
    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.env.schema,
            """\
spack:
    foobar:
        verify_ssl: False
        dirty: False
""",
        )


def test_bad_config_yaml():
    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.config.schema,
            """\
config:
    verify_ssl: False
    install_tree:
      root:
        extra_level: foo
""",
        )


def test_bad_include_yaml():
    with pytest.raises(spack.config.ConfigFormatError, match="is not of type"):
        check_schema(
            spack.schema.include.schema,
            """\
include: $HOME/include.yaml
""",
        )


def test_bad_mirrors_yaml():
    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.mirrors.schema,
            """\
mirrors:
    local: True
""",
        )


def test_bad_repos_yaml():
    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.repos.schema,
            """\
repos:
    True
""",
        )


def test_bad_compilers_yaml():
    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.compilers.schema,
            """\
compilers:
    key_instead_of_list: 'value'
""",
        )

    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.compilers.schema,
            """\
compilers:
    - shmompiler:
         environment: /bad/value
""",
        )

    with pytest.raises(spack.config.ConfigFormatError):
        check_schema(
            spack.schema.compilers.schema,
            """\
compilers:
    - compiler:
         fenfironfent: /bad/value
""",
        )


def test_internal_config_section_override(mock_low_high_config, write_config_file):
    write_config_file("config", config_merge_list, "low")
    wanted_list = config_override_list["config"]["build_stage:"]
    mock_low_high_config.push_scope(
        spack.config.InternalConfigScope("high", {"config:": {"build_stage": wanted_list}})
    )
    assert mock_low_high_config.get("config:build_stage") == wanted_list


def test_internal_config_dict_override(mock_low_high_config, write_config_file):
    write_config_file("config", config_merge_dict, "low")
    wanted_dict = config_override_dict["config"]["aliases:"]
    mock_low_high_config.push_scope(spack.config.InternalConfigScope("high", config_override_dict))
    assert mock_low_high_config.get("config:aliases") == wanted_dict


def test_internal_config_list_override(mock_low_high_config, write_config_file):
    write_config_file("config", config_merge_list, "low")
    wanted_list = config_override_list["config"]["build_stage:"]
    mock_low_high_config.push_scope(spack.config.InternalConfigScope("high", config_override_list))
    assert mock_low_high_config.get("config:build_stage") == wanted_list


def test_set_section_override(mock_low_high_config, write_config_file):
    write_config_file("config", config_merge_list, "low")
    wanted_list = config_override_list["config"]["build_stage:"]
    with spack.config.override("config::build_stage", wanted_list):
        assert mock_low_high_config.get("config:build_stage") == wanted_list
    assert config_merge_list["config"]["build_stage"] == mock_low_high_config.get(
        "config:build_stage"
    )


def test_set_list_override(mock_low_high_config, write_config_file):
    write_config_file("config", config_merge_list, "low")
    wanted_list = config_override_list["config"]["build_stage:"]
    with spack.config.override("config:build_stage:", wanted_list):
        assert wanted_list == mock_low_high_config.get("config:build_stage")
    assert config_merge_list["config"]["build_stage"] == mock_low_high_config.get(
        "config:build_stage"
    )


def test_set_dict_override(mock_low_high_config, write_config_file):
    write_config_file("config", config_merge_dict, "low")
    wanted_dict = config_override_dict["config"]["aliases:"]
    with spack.config.override("config:aliases:", wanted_dict):
        assert wanted_dict == mock_low_high_config.get("config:aliases")
    assert config_merge_dict["config"]["aliases"] == mock_low_high_config.get("config:aliases")


def test_set_bad_path(config):
    with pytest.raises(ValueError):
        with spack.config.override(":bad:path", ""):
            pass


def test_bad_path_double_override(config):
    with pytest.raises(syaml.SpackYAMLError, match="Meaningless second override"):
        with spack.config.override("bad::double:override::directive", ""):
            pass


def test_license_dir_config(mutable_config, mock_packages):
    """Ensure license directory is customizable"""
    expected_dir = spack.paths.default_license_dir
    assert spack.config.get("config:license_dir") == expected_dir
    assert spack.package_base.PackageBase.global_license_dir == expected_dir
    assert spack.repo.PATH.get_pkg_class("pkg-a").global_license_dir == expected_dir

    rel_path = os.path.join(os.path.sep, "foo", "bar", "baz")
    spack.config.set("config:license_dir", rel_path)
    assert spack.config.get("config:license_dir") == rel_path
    assert spack.package_base.PackageBase.global_license_dir == rel_path
    assert spack.repo.PATH.get_pkg_class("pkg-a").global_license_dir == rel_path


@pytest.mark.regression("22547")
def test_single_file_scope_cache_clearing(env_yaml):
    scope = spack.config.SingleFileScope(
        "env", env_yaml, spack.schema.env.schema, yaml_path=["spack"]
    )
    # Check that we can retrieve data from the single file scope
    before = scope.get_section("config")
    assert before
    # Clear the cache of the Single file scope
    scope.clear()
    # Check that the section can be retireved again and it's
    # the same as before
    after = scope.get_section("config")
    assert after
    assert before == after


@pytest.mark.regression("22611")
def test_internal_config_scope_cache_clearing():
    """
    An InternalConfigScope object is constructed from data that is already
    in memory, therefore it doesn't have any cache to clear. Here we ensure
    that calling the clear method is consistent with that..
    """
    data = {"config": {"build_jobs": 10}}
    internal_scope = spack.config.InternalConfigScope("internal", data)
    # Ensure that the initial object is properly set
    assert internal_scope.sections["config"] == data
    # Call the clear method
    internal_scope.clear()
    # Check that this didn't affect the scope object
    assert internal_scope.sections["config"] == data


def test_system_config_path_is_overridable(working_env):
    p = "/some/path"
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = p
    assert spack.paths._get_system_config_path() == p


def test_system_config_path_is_default_when_env_var_is_empty(working_env):
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = ""
    assert os.sep + os.path.join("etc", "spack") == spack.paths._get_system_config_path()


def test_user_config_path_is_overridable(working_env):
    p = "/some/path"
    os.environ["SPACK_USER_CONFIG_PATH"] = p
    assert p == spack.paths._get_user_config_path()


def test_user_config_path_is_default_when_env_var_is_empty(working_env):
    os.environ["SPACK_USER_CONFIG_PATH"] = ""
    assert os.path.expanduser("~%s.spack" % os.sep) == spack.paths._get_user_config_path()


def test_default_install_tree(monkeypatch, default_config):
    s = spack.spec.Spec("nonexistent@x.y.z arch=foo-bar-baz")
    monkeypatch.setattr(s, "dag_hash", lambda length: "abc123")
    _, _, projections = spack.store.parse_install_tree(spack.config.get("config"))
    assert s.format(projections["all"]) == "foo-baz/nonexistent-x.y.z-abc123"


@pytest.fixture
def mock_include_scope(tmp_path):
    for subdir in ["defaults", "test1", "test2", "test3"]:
        path = tmp_path / subdir
        path.mkdir()

    include = tmp_path / "include.yaml"
    with include.open("w", encoding="utf-8") as f:
        f.write(
            textwrap.dedent(
                """\
                include::
                  - name: "test1"
                    path: "test1"
                    when: '"SPACK_DISABLE_LOCAL_CONFIG" not in env'

                  - name: "test2"
                    path: "test2"

                  - name: "test3"
                    path: "test3"
                    when: '"SPACK_DISABLE_LOCAL_CONFIG" not in env'
                """
            )
        )

    yield tmp_path


@pytest.fixture
def include_config_factory(mock_include_scope):
    def make_config():
        cfg = spack.config.create()
        cfg.push_scope(
            spack.config.DirectoryConfigScope("defaults", str(mock_include_scope / "defaults")),
            priority=ConfigScopePriority.DEFAULTS,
        )
        cfg.push_scope(
            spack.config.DirectoryConfigScope("tmp_path", str(mock_include_scope)),
            priority=ConfigScopePriority.CONFIG_FILES,
        )
        return cfg

    yield make_config


def test_modify_scope_precedence(working_env, include_config_factory, tmp_path):
    """Test how spack selects the scope to modify when commands write config."""

    cfg = include_config_factory()

    # ensure highest precedence writable scope is selected by default
    assert cfg.highest_precedence_scope().name == "tmp_path"

    include_yaml = tmp_path / "include.yaml"
    subdir = tmp_path / "subdir"
    subdir2 = tmp_path / "subdir2"
    subdir.mkdir()
    subdir2.mkdir()

    with include_yaml.open("w", encoding="utf-8") as f:
        f.write(
            textwrap.dedent(
                """\
                include::
                  - name: "subdir"
                    path: "subdir"
                """
            )
        )

    cfg.push_scope(
        spack.config.DirectoryConfigScope("override", str(tmp_path)),
        priority=ConfigScopePriority.CONFIG_FILES,
    )

    # ensure override scope is selected when it is on top
    assert cfg.highest_precedence_scope().name == "override"

    cfg.remove_scope("override")

    with include_yaml.open("w", encoding="utf-8") as f:
        f.write(
            textwrap.dedent(
                """\
                include::
                  - name: "subdir"
                    path: "subdir"
                    prefer_modify: true
                """
            )
        )

    cfg.push_scope(
        spack.config.DirectoryConfigScope("override", str(tmp_path)),
        priority=ConfigScopePriority.CONFIG_FILES,
    )

    # if the top scope prefers another, ensure it is selected
    assert cfg.highest_precedence_scope().name == "subdir"

    cfg.remove_scope("override")

    with include_yaml.open("w", encoding="utf-8") as f:
        f.write(
            textwrap.dedent(
                """\
                include::
                  - name: "subdir"
                    path: "subdir"
                  - name: "subdir2"
                    path: "subdir2"
                    prefer_modify: true
                """
            )
        )

    cfg.push_scope(
        spack.config.DirectoryConfigScope("override", str(tmp_path)),
        priority=ConfigScopePriority.CONFIG_FILES,
    )

    # if there are multiple scopes and one is preferred, make sure it's that one
    assert cfg.highest_precedence_scope().name == "subdir2"


def test_local_config_can_be_disabled(working_env, include_config_factory):
    """Ensure that SPACK_DISABLE_LOCAL_CONFIG disables configurations with `when:`."""
    os.environ["SPACK_DISABLE_LOCAL_CONFIG"] = "true"
    cfg = include_config_factory()
    assert "defaults" in cfg.scopes
    assert "test1" not in cfg.scopes
    assert "test2" in cfg.scopes
    assert "test3" not in cfg.scopes

    os.environ["SPACK_DISABLE_LOCAL_CONFIG"] = ""
    cfg = include_config_factory()
    assert "defaults" in cfg.scopes
    assert "test1" not in cfg.scopes
    assert "test2" in cfg.scopes
    assert "test3" not in cfg.scopes

    del os.environ["SPACK_DISABLE_LOCAL_CONFIG"]
    cfg = include_config_factory()
    assert "defaults" in cfg.scopes
    assert "test1" in cfg.scopes
    assert "test2" in cfg.scopes
    assert "test3" in cfg.scopes


def test_override_included_config(working_env, tmp_path, include_config_factory):
    override_scope = tmp_path / "override"
    override_scope.mkdir()

    include_yaml = override_scope / "include.yaml"
    subdir = override_scope / "subdir"
    subdir.mkdir()

    with include_yaml.open("w", encoding="utf-8") as f:
        f.write(
            textwrap.dedent(
                """\
                include::
                  - name: "subdir"
                    path: "subdir"
                """
            )
        )

    # check the mock config is correct
    cfg = include_config_factory()

    assert "defaults" in cfg.scopes
    assert "test1" in cfg.scopes
    assert "test2" in cfg.scopes
    assert "test3" in cfg.scopes

    active_names = [s.name for s in cfg.active_scopes]
    assert "defaults" in active_names
    assert "test1" in active_names
    assert "test2" in active_names
    assert "test3" in active_names

    # push a scope that overrides everything under it but includes a subdir.
    # its included subdir should be active, but scopes *not* included by the overriding
    # scope should not.
    cfg.push_scope(
        spack.config.DirectoryConfigScope("override", str(override_scope)),
        priority=ConfigScopePriority.CONFIG_FILES,
    )

    assert "defaults" in cfg.scopes
    assert "test1" in cfg.scopes
    assert "test2" in cfg.scopes
    assert "test3" in cfg.scopes
    assert "override" in cfg.scopes
    assert "subdir" in cfg.scopes

    active_names = [s.name for s in cfg.active_scopes]
    assert "defaults" in active_names
    assert "test1" not in active_names
    assert "test2" not in active_names
    assert "test3" not in active_names
    assert "override" in active_names
    assert "subdir" in active_names

    # remove the override and ensure everything is back to normal
    cfg.remove_scope("override")

    assert "defaults" in cfg.scopes
    assert "test1" in cfg.scopes
    assert "test2" in cfg.scopes
    assert "test3" in cfg.scopes

    active_names = [s.name for s in cfg.active_scopes]
    assert "defaults" in active_names
    assert "test1" in active_names
    assert "test2" in active_names
    assert "test3" in active_names


def test_user_cache_path_is_overridable(working_env):
    p = "/some/path"
    os.environ["SPACK_USER_CACHE_PATH"] = p
    assert spack.paths._get_user_cache_path() == p


def test_user_cache_path_is_default_when_env_var_is_empty(working_env):
    os.environ["SPACK_USER_CACHE_PATH"] = ""
    assert os.path.expanduser("~%s.spack" % os.sep) == spack.paths._get_user_cache_path()


def test_config_file_dir_failure(tmp_path: pathlib.Path, mutable_empty_config):
    with pytest.raises(spack.config.ConfigFileError, match="not a file"):
        spack.config.read_config_file(str(tmp_path))


@pytest.mark.not_on_windows("chmod not supported on Windows")
def test_config_file_read_perms_failure(tmp_path: pathlib.Path, mutable_empty_config):
    """Test reading a configuration file without permissions to ensure
    ConfigFileError is raised."""
    filename = join_path(str(tmp_path), "test.yaml")
    touch(filename)
    os.chmod(filename, 0o200)

    with pytest.raises(spack.config.ConfigFileError, match="not readable"):
        spack.config.read_config_file(filename)


def test_config_file_read_invalid_yaml(tmp_path: pathlib.Path, mutable_empty_config):
    """Test reading a configuration file with invalid (unparseable) YAML
    raises a ConfigFileError."""
    filename = join_path(str(tmp_path), "test.yaml")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("spack:\nview")

    with pytest.raises(spack.config.ConfigFileError, match="parsing YAML"):
        spack.config.read_config_file(filename)


@pytest.mark.parametrize(
    "path,it_should_work,expected_parsed",
    [
        ("x:y:z", True, ["x:", "y:", "z"]),
        ("x+::y:z", True, ["x+::", "y:", "z"]),
        ('x:y:"{z}"', True, ["x:", "y:", '"{z}"']),
        ('x:"y"+:z', True, ["x:", '"y"+:', "z"]),
        ('x:"y"trail:z', False, None),
        ("x:y:[1.0]", True, ["x:", "y:", "[1.0]"]),
        ("x:y:['1.0']", True, ["x:", "y:", "['1.0']"]),
        ("x:{y}:z", True, ["x:", "{y}:", "z"]),
        ("x:'{y}':z", True, ["x:", "'{y}':", "z"]),
        ("x:{y}", True, ["x:", "{y}"]),
    ],
)
def test_config_path_dsl(path, it_should_work, expected_parsed):
    if it_should_work:
        assert spack.config.ConfigPath._validate(path) == expected_parsed
    else:
        with pytest.raises(ValueError):
            spack.config.ConfigPath._validate(path)


@pytest.mark.regression("48254")
def test_env_activation_preserves_command_line_scope(mutable_mock_env_path):
    """Check that the "command_line" scope remains the highest priority scope, when we activate,
    or deactivate, environments.
    """
    expected_cl_scope = spack.config.CONFIG.highest()
    assert expected_cl_scope.name == "command_line"

    # Creating an environment pushes a new scope
    ev.create("test")
    with ev.read("test"):
        assert spack.config.CONFIG.highest() == expected_cl_scope

        # No active environment pops the scope
        with ev.no_active_environment():
            assert spack.config.CONFIG.highest() == expected_cl_scope
        assert spack.config.CONFIG.highest() == expected_cl_scope

        # Switch the environment to another one
        ev.create("test-2")
        with ev.read("test-2"):
            assert spack.config.CONFIG.highest() == expected_cl_scope
        assert spack.config.CONFIG.highest() == expected_cl_scope

    assert spack.config.CONFIG.highest() == expected_cl_scope


@pytest.mark.regression("48414")
@pytest.mark.regression("49188")
def test_env_activation_preserves_config_scopes(mutable_mock_env_path):
    """Check that the priority of scopes is respected when merging configuration files."""
    custom_scope = spack.config.InternalConfigScope("custom_scope")
    spack.config.CONFIG.push_scope(custom_scope, priority=ConfigScopePriority.CUSTOM)
    expected_scopes_without_env = ["custom_scope", "command_line"]
    expected_scopes_with_first_env = ["env:test", "custom_scope", "command_line"]
    expected_scopes_with_second_env = ["env:test-2", "custom_scope", "command_line"]

    def highest_priority_scopes(config, *, nscopes):
        return list(config.scopes)[-nscopes:]

    assert highest_priority_scopes(spack.config.CONFIG, nscopes=2) == expected_scopes_without_env
    # Creating an environment pushes a new scope
    ev.create("test")
    with ev.read("test"):
        assert (
            highest_priority_scopes(spack.config.CONFIG, nscopes=3)
            == expected_scopes_with_first_env
        )

        # No active environment pops the scope
        with ev.no_active_environment():
            assert (
                highest_priority_scopes(spack.config.CONFIG, nscopes=2)
                == expected_scopes_without_env
            )
        assert (
            highest_priority_scopes(spack.config.CONFIG, nscopes=3)
            == expected_scopes_with_first_env
        )

        # Switch the environment to another one
        ev.create("test-2")
        with ev.read("test-2"):
            assert (
                highest_priority_scopes(spack.config.CONFIG, nscopes=3)
                == expected_scopes_with_second_env
            )
        assert (
            highest_priority_scopes(spack.config.CONFIG, nscopes=3)
            == expected_scopes_with_first_env
        )

    assert highest_priority_scopes(spack.config.CONFIG, nscopes=2) == expected_scopes_without_env


@pytest.mark.regression("51059")
def test_config_include_similar_name(tmp_path: pathlib.Path):
    config_a = tmp_path / "a" / "config"
    config_b = tmp_path / "b" / "config"

    os.makedirs(config_a)
    with open(config_a / "config.yaml", "w", encoding="utf-8") as fd:
        syaml.dump_config({"config": {"install_tree": {"root": str(tmp_path)}}}, fd)

    os.makedirs(config_b)
    with open(config_b / "config.yaml", "w", encoding="utf-8") as fd:
        syaml.dump_config({"config": {"install_tree": {"padded_length": 64}}}, fd)

    with open(tmp_path / "include.yaml", "w", encoding="utf-8") as fd:
        syaml.dump_config({"include": [str(config_a), str(config_b)]}, fd)

    config = spack.config.create_from(spack.config.DirectoryConfigScope("test", str(tmp_path)))

    # Ensure all of the scopes are found
    assert len(config.matching_scopes("^test$")) == 1
    assert len(config.matching_scopes("^test:a/config$")) == 1
    assert len(config.matching_scopes("^test:b/config$")) == 1


def test_deepcopy_as_builtin(env_yaml):
    cfg = spack.config.create_from(
        spack.config.SingleFileScope("env", env_yaml, spack.schema.env.schema, yaml_path=["spack"])
    )
    config_copy = cfg.deepcopy_as_builtin("config")
    assert config_copy == cfg.get_config("config")
    assert type(config_copy) is DictWithLineInfo
    assert type(config_copy["verify_ssl"]) is bool

    packages_copy = cfg.deepcopy_as_builtin("packages")
    assert type(packages_copy) is DictWithLineInfo
    assert type(packages_copy["all"]) is DictWithLineInfo
    assert type(packages_copy["all"]["compiler"]) is list
    assert type(packages_copy["all"]["compiler"][0]) is str


def test_included_optional_include_scopes():
    with pytest.raises(NotImplementedError):
        spack.config.OptionalInclude({}).scopes(spack.config.ConfigScope("fail"))


def test_included_path_string(
    tmp_path: pathlib.Path, mock_low_high_config, ensure_debug, monkeypatch, capsys
):
    path = tmp_path / "local" / "config.yaml"
    path.parent.mkdir()
    include = spack.config.included_path(path)
    assert isinstance(include, spack.config.IncludePath)
    assert include.path == str(path)
    assert not include.optional
    assert include.evaluate_condition()

    parent_scope = mock_low_high_config.scopes["low"]

    # Trigger failure when required path does not exist
    with pytest.raises(ValueError, match="does not exist"):
        include.scopes(parent_scope)

    # First successful pass builds the scope
    path.touch()
    scopes = include.scopes(parent_scope)
    assert scopes and len(scopes) == 1
    assert isinstance(scopes[0], spack.config.SingleFileScope)

    # Second pass uses the scopes previously built
    assert include._scopes is not None
    scopes = include.scopes(parent_scope)
    captured = capsys.readouterr()[1]
    assert "Using existing scopes" in captured


def test_included_path_string_no_parent_path(
    tmp_path: pathlib.Path, config, ensure_debug, monkeypatch
):
    """Use a relative include path and no parent scope path so destination
    will be rooted in the current working directory (usually SPACK_ROOT)."""
    entry = {"path": "config.yaml", "optional": True}
    include = spack.config.included_path(entry)
    FakeScope = collections.namedtuple("FakeScope", ["path", "name"])
    parent_scope = FakeScope("", "")

    assert not include.scopes(parent_scope)  # type: ignore[arg-type]
    destination = include.destination
    curr_dir = os.getcwd()
    assert curr_dir == os.path.commonprefix([curr_dir, destination])  # type: ignore[list-item]


def test_included_path_conditional_bad_when(
    tmp_path: pathlib.Path, mock_low_high_config, ensure_debug, capsys
):
    path = tmp_path / "local"
    path.mkdir()
    entry = {"path": str(path), "when": 'platform == "nosuchplatform"', "optional": True}
    include = spack.config.included_path(entry)
    assert isinstance(include, spack.config.IncludePath)
    assert include.path == entry["path"]
    assert include.when == entry["when"]
    assert include.optional
    assert not include.evaluate_condition()

    scopes = include.scopes(mock_low_high_config.scopes["low"])
    captured = capsys.readouterr()[1]
    assert "condition is not satisfied" in captured
    assert not scopes


def test_included_path_conditional_success(tmp_path: pathlib.Path, mock_low_high_config):
    path = tmp_path / "local"
    path.mkdir()
    entry = {"path": str(path), "when": 'platform == "test"', "optional": True}
    include = spack.config.included_path(entry)
    assert isinstance(include, spack.config.IncludePath)
    assert include.path == entry["path"]
    assert include.when == entry["when"]
    assert include.optional
    assert include.evaluate_condition()

    scopes = include.scopes(mock_low_high_config.scopes["low"])
    assert scopes and len(scopes) == 1
    assert isinstance(scopes[0], spack.config.DirectoryConfigScope)


def test_included_path_git_missing_args():
    # must have one or more of: branch, tag and commit so fail if missing any
    entry = {"git": "https://example.com/windows/configs.git", "paths": ["config.yaml"]}
    with pytest.raises(spack.error.ConfigError, match="specify one or more"):
        spack.config.included_path(entry)

    # must have one or more paths
    entry["tag"] = "v1.0"
    entry["paths"] = []
    with pytest.raises(spack.error.ConfigError, match="must include one or more"):
        spack.config.included_path(entry)


def test_included_path_git_unsat(
    tmp_path: pathlib.Path, mock_low_high_config, ensure_debug, monkeypatch, capsys
):
    paths = ["config.yaml", "packages.yaml"]
    entry = {
        "git": "https://example.com/windows/configs.git",
        "tag": "v1.0",
        "paths": paths,
        "when": 'platform == "nosuchplatform"',
    }
    include = spack.config.included_path(entry)
    assert isinstance(include, spack.config.GitIncludePaths)
    assert include.repo == entry["git"]
    assert include.tag == entry["tag"]
    assert include.paths == entry["paths"]
    assert include.when == entry["when"]
    assert not include.optional and not include.evaluate_condition()

    scopes = include.scopes(mock_low_high_config.scopes["low"])
    captured = capsys.readouterr()[1]
    assert "condition is not satisfied" in captured
    assert not scopes


@pytest.mark.parametrize(
    "key,value", [("branch", "main"), ("commit", "abcdef123456"), ("tag", "v1.0")]
)
def test_included_path_git(
    tmp_path: pathlib.Path, mock_low_high_config, ensure_debug, monkeypatch, key, value, capsys
):
    monkeypatch.setattr(spack.paths, "user_cache_path", str(tmp_path))

    class MockIncludeGit(spack.util.executable.Executable):
        def __init__(self, required: bool):
            pass

        def __call__(self, *args, **kwargs) -> str:  # type: ignore
            action = args[0]

            if action == "config":
                return "origin"

            return ""

    paths = ["config.yaml", "packages.yaml"]
    entry = {
        "git": "https://example.com/windows/configs.git",
        key: value,
        "paths": paths,
        "when": 'platform == "test"',
    }
    include = spack.config.included_path(entry)
    assert isinstance(include, spack.config.GitIncludePaths)
    assert not include.optional and include.evaluate_condition()

    destination = include._destination()
    assert not os.path.exists(destination)

    # set up minimal git and repository operations
    monkeypatch.setattr(spack.util.git, "git", MockIncludeGit)

    def _init_repo(*args, **kwargs):
        fs.mkdirp(fs.join_path(destination, ".git"))

    def _checkout(*args, **kwargs):
        # Make sure the files exist at the clone destination
        with fs.working_dir(destination):
            for p in paths:
                fs.touch(p)

    monkeypatch.setattr(spack.util.git, "init_git_repo", _init_repo)
    monkeypatch.setattr(spack.util.git, f"pull_checkout_{key}", _checkout)

    # First successful pass builds the scope
    parent_scope = mock_low_high_config.scopes["low"]
    scopes = include.scopes(parent_scope)
    assert scopes and len(scopes) == len(paths)
    for scope in scopes:
        assert isinstance(scope, spack.config.SingleFileScope)
        assert os.path.basename(scope.path) in paths  # type: ignore[union-attr]

    # Second pass uses the scopes previously built.
    # Only need to do this for one of the parameters.
    if key == "branch":
        assert include._scopes is not None
        scopes = include.scopes(parent_scope)
        captured = capsys.readouterr()[1]
        assert "Using existing scopes" in captured

    # A direct clone now returns already cloned destination and debug message.
    # Again only need to run this test once.
    if key == "tag":
        assert include._clone() == include.destination
        captured = capsys.readouterr()[1]
        assert "already cloned" in captured


def test_included_path_git_errs(tmp_path: pathlib.Path, mock_low_high_config, monkeypatch):
    monkeypatch.setattr(spack.paths, "user_cache_path", str(tmp_path))

    paths = ["concretizer.yaml"]
    entry = {
        "git": "https://example.com/linux/configs.git",
        "branch": "develop",
        "paths": paths,
        "when": 'platform == "test"',
    }
    include = spack.config.included_path(entry)
    parent_scope = mock_low_high_config.scopes["low"]

    # fail to initialize the repository
    def _failing_init(*args, **kwargs):
        raise spack.util.executable.ProcessError("mock init repo failure")

    monkeypatch.setattr(spack.util.git, "init_git_repo", _failing_init)

    with pytest.raises(spack.error.ConfigError, match="Unable to initialize"):
        include.scopes(parent_scope)

    # fail in git config (so use default remote) *and* git checkout
    def _init_repo(*args, **kwargs):
        fs.mkdirp(fs.join_path(include.destination, ".git"))

    class MockIncludeGit(spack.util.executable.Executable):
        def __init__(self, required: bool):
            pass

        def __call__(self, *args, **kwargs) -> str:  # type: ignore
            raise spack.util.executable.ProcessError("mock git failure")

    monkeypatch.setattr(spack.util.git, "init_git_repo", _init_repo)
    monkeypatch.setattr(spack.util.git, "git", MockIncludeGit)

    with pytest.raises(spack.error.ConfigError, match="Unable to check out"):
        include.scopes(parent_scope)

    # set up invalid option failure
    include.branch = ""  # type: ignore[union-attr]
    with pytest.raises(spack.error.ConfigError, match="Missing or unsupported options"):
        include.scopes(parent_scope)
