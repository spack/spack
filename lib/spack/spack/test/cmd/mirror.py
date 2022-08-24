# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import spack.cmd.mirror
import spack.config
import spack.environment as ev
from spack.main import SpackCommand, SpackCommandError

mirror = SpackCommand("mirror")
env = SpackCommand("env")
add = SpackCommand("add")
concretize = SpackCommand("concretize")
install = SpackCommand("install")
buildcache = SpackCommand("buildcache")
uninstall = SpackCommand("uninstall")

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")


@pytest.fixture
def tmp_scope():
    """Creates a temporary configuration scope"""

    base_name = "internal-testing-scope"
    current_overrides = set(
        x.name for x in spack.config.config.matching_scopes(r"^{0}".format(base_name))
    )

    num_overrides = 0
    scope_name = base_name
    while scope_name in current_overrides:
        scope_name = "{0}{1}".format(base_name, num_overrides)
        num_overrides += 1

    with spack.config.override(spack.config.InternalConfigScope(scope_name)):
        yield scope_name


def _validate_url(url):
    return


@pytest.fixture(autouse=True)
def url_check(monkeypatch):
    monkeypatch.setattr(spack.util.url, "require_url_format", _validate_url)


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression("8083")
def test_regression_8083(tmpdir, capfd, mock_packages, mock_fetch, config):
    with capfd.disabled():
        output = mirror("create", "-d", str(tmpdir), "externaltool")
    assert "Skipping" in output
    assert "as it is an external spec" in output


@pytest.mark.regression("12345")
def test_mirror_from_env(tmpdir, mock_packages, mock_fetch, config, mutable_mock_env_path):
    mirror_dir = str(tmpdir)
    env_name = "test"

    env("create", env_name)
    with ev.read(env_name):
        add("trivial-install-test-package")
        add("git-test")
        concretize()
        with spack.config.override("config:checksum", False):
            mirror("create", "-d", mirror_dir, "--all")

    e = ev.read(env_name)
    assert set(os.listdir(mirror_dir)) == set([s.name for s in e.user_specs])
    for spec in e.specs_by_hash.values():
        mirror_res = os.listdir(os.path.join(mirror_dir, spec.name))
        expected = ["%s.tar.gz" % spec.format("{name}-{version}")]
        assert mirror_res == expected


@pytest.fixture
def source_for_pkg_with_hash(mock_packages, tmpdir):
    s = spack.spec.Spec("trivial-pkg-with-valid-hash").concretized()
    local_url_basename = os.path.basename(s.package.url)
    local_path = os.path.join(str(tmpdir), local_url_basename)
    with open(local_path, "w") as f:
        f.write(s.package.hashed_content)
    local_url = "file://" + local_path
    s.package.versions[spack.version.Version("1.0")]["url"] = local_url


def test_mirror_skip_unstable(tmpdir_factory, mock_packages, config, source_for_pkg_with_hash):
    mirror_dir = str(tmpdir_factory.mktemp("mirror-dir"))

    specs = [spack.spec.Spec(x).concretized() for x in ["git-test", "trivial-pkg-with-valid-hash"]]
    spack.mirror.create(mirror_dir, specs, skip_unstable_versions=True)

    assert set(os.listdir(mirror_dir)) - set(["_source-cache"]) == set(
        ["trivial-pkg-with-valid-hash"]
    )


class MockMirrorArgs(object):
    def __init__(
        self,
        specs=None,
        all=False,
        file=None,
        versions_per_spec=None,
        dependencies=False,
        exclude_file=None,
        exclude_specs=None,
        directory=None,
    ):
        self.specs = specs or []
        self.all = all
        self.file = file
        self.versions_per_spec = versions_per_spec
        self.dependencies = dependencies
        self.exclude_file = exclude_file
        self.exclude_specs = exclude_specs
        self.directory = directory


def test_exclude_specs(mock_packages, config):
    args = MockMirrorArgs(
        specs=["mpich"], versions_per_spec="all", exclude_specs="mpich@3.0.1:3.0.2 mpich@1.0"
    )

    mirror_specs = spack.cmd.mirror.concrete_specs_from_user(args)
    expected_include = set(
        spack.spec.Spec(x).concretized() for x in ["mpich@3.0.3", "mpich@3.0.4", "mpich@3.0"]
    )
    expected_exclude = set(spack.spec.Spec(x) for x in ["mpich@3.0.1", "mpich@3.0.2", "mpich@1.0"])
    assert expected_include <= set(mirror_specs)
    assert not any(spec.satisfies(y) for spec in mirror_specs for y in expected_exclude)


def test_exclude_file(mock_packages, tmpdir, config):
    exclude_path = os.path.join(str(tmpdir), "test-exclude.txt")
    with open(exclude_path, "w") as exclude_file:
        exclude_file.write(
            """\
mpich@3.0.1:3.0.2
mpich@1.0
"""
        )

    args = MockMirrorArgs(specs=["mpich"], versions_per_spec="all", exclude_file=exclude_path)

    mirror_specs = spack.cmd.mirror.concrete_specs_from_user(args)
    expected_include = set(
        spack.spec.Spec(x).concretized() for x in ["mpich@3.0.3", "mpich@3.0.4", "mpich@3.0"]
    )
    expected_exclude = set(spack.spec.Spec(x) for x in ["mpich@3.0.1", "mpich@3.0.2", "mpich@1.0"])
    assert expected_include <= set(mirror_specs)
    assert not any(spec.satisfies(y) for spec in mirror_specs for y in expected_exclude)


def test_mirror_crud(tmp_scope, capsys):
    with capsys.disabled():
        mirror("add", "--scope", tmp_scope, "mirror", "http://spack.io")

        output = mirror("remove", "--scope", tmp_scope, "mirror")
        assert "Removed mirror" in output

        mirror("add", "--scope", tmp_scope, "mirror", "http://spack.io")

        # no-op
        output = mirror("set-url", "--scope", tmp_scope, "mirror", "http://spack.io")
        assert "No changes made" in output

        output = mirror("set-url", "--scope", tmp_scope, "--push", "mirror", "s3://spack-public")
        assert "Changed (push) url" in output

        # no-op
        output = mirror("set-url", "--scope", tmp_scope, "--push", "mirror", "s3://spack-public")
        assert "No changes made" in output

        output = mirror("remove", "--scope", tmp_scope, "mirror")
        assert "Removed mirror" in output

        # Test S3 connection info token
        mirror(
            "add",
            "--scope",
            tmp_scope,
            "--s3-access-token",
            "aaaaaazzzzz",
            "mirror",
            "s3://spack-public",
        )

        output = mirror("remove", "--scope", tmp_scope, "mirror")
        assert "Removed mirror" in output

        # Test S3 connection info id/key
        mirror(
            "add",
            "--scope",
            tmp_scope,
            "--s3-access-key-id",
            "foo",
            "--s3-access-key-secret",
            "bar",
            "mirror",
            "s3://spack-public",
        )

        output = mirror("remove", "--scope", tmp_scope, "mirror")
        assert "Removed mirror" in output

        # Test S3 connection info with endpoint URL
        mirror(
            "add",
            "--scope",
            tmp_scope,
            "--s3-access-token",
            "aaaaaazzzzz",
            "--s3-endpoint-url",
            "http://localhost/",
            "mirror",
            "s3://spack-public",
        )

        output = mirror("remove", "--scope", tmp_scope, "mirror")
        assert "Removed mirror" in output

        output = mirror("list", "--scope", tmp_scope)
        assert "No mirrors configured" in output

        # Test GCS Mirror
        mirror("add", "--scope", tmp_scope, "mirror", "gs://spack-test")

        output = mirror("remove", "--scope", tmp_scope, "mirror")
        assert "Removed mirror" in output


def test_mirror_nonexisting(tmp_scope):
    with pytest.raises(SpackCommandError):
        mirror("remove", "--scope", tmp_scope, "not-a-mirror")

    with pytest.raises(SpackCommandError):
        mirror("set-url", "--scope", tmp_scope, "not-a-mirror", "http://spack.io")


def test_mirror_name_collision(tmp_scope):
    mirror("add", "--scope", tmp_scope, "first", "1")

    with pytest.raises(SpackCommandError):
        mirror("add", "--scope", tmp_scope, "first", "1")


def test_mirror_destroy(
    install_mockery_mutable_config,
    mock_packages,
    mock_fetch,
    mock_archive,
    mutable_config,
    monkeypatch,
    tmpdir,
):
    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join("mirror_dir")
    mirror_url = "file://{0}".format(mirror_dir.strpath)
    mirror("add", "atest", mirror_url)

    spec_name = "libdwarf"

    # Put a binary package in a buildcache
    install("--no-cache", spec_name)
    buildcache("create", "-u", "-a", "-f", "-d", mirror_dir.strpath, spec_name)

    contents = os.listdir(mirror_dir.strpath)
    assert "build_cache" in contents

    # Destroy mirror by name
    mirror("destroy", "-m", "atest")

    assert not os.path.exists(mirror_dir.strpath)

    buildcache("create", "-u", "-a", "-f", "-d", mirror_dir.strpath, spec_name)

    contents = os.listdir(mirror_dir.strpath)
    assert "build_cache" in contents

    # Destroy mirror by url
    mirror("destroy", "--mirror-url", mirror_url)

    assert not os.path.exists(mirror_dir.strpath)

    uninstall("-y", spec_name)
    mirror("remove", "atest")


@pytest.mark.usefixtures("mock_packages")
class TestMirrorCreate(object):
    @pytest.mark.regression("31736", "31985")
    def test_all_specs_with_all_versions_dont_concretize(self):
        args = MockMirrorArgs(exclude_file=None, exclude_specs=None)
        specs = spack.cmd.mirror.all_specs_with_all_versions(
            selection_fn=spack.cmd.mirror.not_excluded_fn(args)
        )
        assert all(not s.concrete for s in specs)

    @pytest.mark.parametrize(
        "cli_args,error_str",
        [
            # Passed more than one among -f --all and specs
            ({"specs": "hdf5", "file": None, "all": True}, "cannot specify specs on command line"),
            (
                {"specs": None, "file": "input.txt", "all": True},
                "cannot specify specs with a file if",
            ),
            (
                {"specs": "hdf5", "file": "input.txt", "all": False},
                "cannot specify specs with a file AND",
            ),
            ({"specs": None, "file": None, "all": False}, "no packages were specified"),
            # Passed -n along with --all
            (
                {"specs": None, "file": None, "all": True, "versions_per_spec": 2},
                "cannot specify '--versions_per-spec'",
            ),
        ],
    )
    def test_error_conditions(self, cli_args, error_str):
        args = MockMirrorArgs(**cli_args)
        with pytest.raises(spack.error.SpackError, match=error_str):
            spack.cmd.mirror.mirror_create(args)

    @pytest.mark.parametrize(
        "cli_args,expected_end",
        [
            ({"directory": None}, os.path.join("source")),
            ({"directory": os.path.join("foo", "bar")}, os.path.join("foo", "bar")),
        ],
    )
    def test_mirror_path_is_valid(self, cli_args, expected_end, config):
        args = MockMirrorArgs(**cli_args)
        local_push_url = spack.cmd.mirror.local_mirror_url_from_user(args.directory)
        assert local_push_url.startswith("file:")
        assert os.path.isabs(local_push_url.replace("file://", ""))
        assert local_push_url.endswith(expected_end)

    @pytest.mark.parametrize(
        "cli_args,not_expected",
        [
            (
                {
                    "specs": "boost bowtie callpath",
                    "exclude_specs": "bowtie",
                    "dependencies": False,
                },
                ["bowtie"],
            ),
            (
                {
                    "specs": "boost bowtie callpath",
                    "exclude_specs": "bowtie callpath",
                    "dependencies": False,
                },
                ["bowtie", "callpath"],
            ),
            (
                {
                    "specs": "boost bowtie callpath",
                    "exclude_specs": "bowtie",
                    "dependencies": True,
                },
                ["bowtie"],
            ),
        ],
    )
    def test_exclude_specs_from_user(self, cli_args, not_expected, config):
        specs = spack.cmd.mirror.concrete_specs_from_user(MockMirrorArgs(**cli_args))
        assert not any(s.satisfies(y) for s in specs for y in not_expected)

    @pytest.mark.parametrize(
        "abstract_specs",
        [
            ("bowtie", "callpath"),
        ],
    )
    def test_specs_from_cli_are_the_same_as_from_file(self, abstract_specs, config, tmpdir):
        args = MockMirrorArgs(specs=" ".join(abstract_specs))
        specs_from_cli = spack.cmd.mirror.concrete_specs_from_user(args)

        input_file = tmpdir.join("input.txt")
        input_file.write("\n".join(abstract_specs))
        args = MockMirrorArgs(file=str(input_file))
        specs_from_file = spack.cmd.mirror.concrete_specs_from_user(args)

        assert specs_from_cli == specs_from_file

    @pytest.mark.parametrize(
        "input_specs,nversions",
        [
            ("callpath", 1),
            ("mpich", 4),
            ("callpath mpich", 3),
            ("callpath mpich", "all"),
        ],
    )
    def test_versions_per_spec_produces_concrete_specs(self, input_specs, nversions, config):
        args = MockMirrorArgs(specs=input_specs, versions_per_spec=nversions)
        specs = spack.cmd.mirror.concrete_specs_from_user(args)
        assert all(s.concrete for s in specs)
