"""Tests for environment-based subsystem plugin discovery and construction."""

from abc import ABC, abstractmethod
from types import SimpleNamespace

import pytest

from spack.vendor import jsonschema

import spack.config
import spack.extensions
import spack.main
import spack.plugins
import spack.schema.config
import spack.util.lang


class Engine:
    def __init__(self, value=0):
        self.value = value


class CustomEngine(Engine):
    pass


@pytest.mark.parametrize("kind", ["class", "instance", "setup-class", "setup-instance"])
@pytest.mark.parametrize("subsystem", ["ui", "installer", "solver", "parser", "sandbox"])
def test_plugin_contract(monkeypatch, kind, subsystem):
    instance = CustomEngine(7)
    targets = {
        "class": CustomEngine,
        "instance": instance,
        "setup-class": lambda: CustomEngine,
        "setup-instance": lambda: instance,
    }

    def entries(*, group):
        assert group == f"spack.plugins.{subsystem}"
        return [SimpleNamespace(name="custom", load=lambda: targets[kind])]

    monkeypatch.setattr(spack.util.lang, "get_entry_points", entries)
    result = spack.plugins.get_plugin(subsystem, "custom", Engine)
    assert result is (instance if kind.endswith("instance") else CustomEngine)


@pytest.mark.parametrize("selected", [None, "default"])
def test_default_does_not_discover(monkeypatch, selected):
    def entries(**kwargs):
        pytest.fail("default engines must not discover plugins")

    monkeypatch.setattr(spack.util.lang, "get_entry_points", entries)
    assert spack.plugins.get_plugin("solver", selected, Engine) is Engine


@pytest.mark.parametrize(
    "failure", ["missing", "duplicate", "discovery", "import", "setup", "invalid", "abstract"]
)
def test_plugin_failure(monkeypatch, capsys, failure):
    class AbstractEngine(Engine, ABC):
        @abstractmethod
        def run(self):
            pass

    def setup():
        raise RuntimeError("incompatible runtime")

    def load():
        if failure == "import":
            raise ImportError("missing dependency")
        if failure == "setup":
            return setup
        return AbstractEngine if failure == "abstract" else object

    def entries(**kwargs):
        if failure == "discovery":
            raise RuntimeError("broken metadata")
        count = 0 if failure == "missing" else 2 if failure == "duplicate" else 1
        return [SimpleNamespace(name="custom", load=load)] * count

    monkeypatch.setattr(spack.util.lang, "get_entry_points", entries)
    assert spack.plugins.get_plugin("solver", "custom", Engine) is Engine
    assert "using default Engine" in capsys.readouterr().err


@pytest.mark.parametrize("kind", ["class", "instance", "broken"])
def test_plugin_construction(monkeypatch, mutable_config, capsys, kind):
    class BrokenEngine(Engine):
        def __init__(self, **kwargs):
            raise RuntimeError("initialization failed")

    instance = CustomEngine(9)
    target = {"class": CustomEngine, "instance": instance, "broken": BrokenEngine}[kind]
    monkeypatch.setattr(
        spack.util.lang,
        "get_entry_points",
        lambda **kwargs: [SimpleNamespace(name="custom", load=lambda: target)],
    )
    mutable_config.set("config:plugins", {"solver": "custom"})
    engine = spack.plugins.create_plugin("solver", Engine, value=3)
    assert engine.value == (9 if kind == "instance" else 3)
    if kind == "broken":
        assert type(engine) is Engine
        assert "Could not initialize solver plugin" in capsys.readouterr().err


def test_plugins_and_command_extensions_are_independent(monkeypatch, mutable_config, tmp_path):
    paths = [str(tmp_path)]
    mutable_config.set("config:extensions", paths)
    mutable_config.set("config:plugins", {"solver": "custom"})

    def entries(*, group):
        if group == "spack.extensions":
            return [SimpleNamespace(load=lambda: lambda: ["/other"])]
        assert group == "spack.plugins.solver"
        return [SimpleNamespace(name="custom", load=lambda: CustomEngine)]

    monkeypatch.setattr(spack.util.lang, "get_entry_points", entries)
    monkeypatch.setattr(
        spack.extensions,
        "extension_paths_from_entry_points",
        spack.extensions.extension_paths_from_entry_points.__wrapped__,
    )
    assert spack.extensions.get_extension_paths() == paths + ["/other"]
    assert type(spack.plugins.create_plugin("solver", Engine)) is CustomEngine
    assert spack.extensions.get_extension_paths() == paths + ["/other"]
    assert mutable_config.get("config:extensions") == paths
    assert mutable_config.get("config:plugins") == {"solver": "custom"}


def test_nested_config_commands(tmp_path):
    legacy = spack.config.InternalConfigScope("legacy", {"config": {"extensions": ["/commands"]}})
    scope = spack.config.DirectoryConfigScope("plugins-test", str(tmp_path))
    with spack.config.use_configuration(legacy, scope):
        command = spack.main.SpackCommand("config")
        command("add", "config:plugins:ui:custom-ui")
        command("add", "config:plugins:installer:custom-engine")
        assert spack.config.CONFIG.get("config:plugins") == {
            "ui": "custom-ui",
            "installer": "custom-engine",
        }
        assert spack.config.CONFIG.get("config:extensions") == ["/commands"]


@pytest.mark.parametrize(
    "configured,valid",
    [
        ({}, True),
        ({"ui": "custom", "installer": "sandboxed", "solver": "custom-z3"}, True),
        ({"ui": None, "parser": "default", "sandbox": "isolated"}, True),
        ([], False),
        (["/path/to/plugins"], False),
        ({"commands": ["/path/to/spack-commands"]}, False),
        ({"ui": 1}, False),
        ({"ui": ""}, False),
        ({"solver": []}, False),
    ],
)
def test_plugin_configuration_schema(configured, valid):
    configuration = {"config": {"plugins": configured, "extensions": ["/commands"]}}
    if valid:
        jsonschema.validate(configuration, spack.schema.config.schema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(configuration, spack.schema.config.schema)


def test_command_extension_configuration_remains_list_only():
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            {"config": {"extensions": {"ui": "custom"}}}, spack.schema.config.schema
        )


@pytest.mark.parametrize("error", [KeyboardInterrupt, SystemExit])
def test_control_flow_exceptions_propagate(monkeypatch, error):
    def setup():
        raise error()

    monkeypatch.setattr(
        spack.util.lang,
        "get_entry_points",
        lambda **kwargs: [SimpleNamespace(name="custom", load=lambda: setup)],
    )
    with pytest.raises(error):
        spack.plugins.get_plugin("installer", "custom", Engine)


def test_default_constructor_error_propagates(mutable_config):
    class BrokenDefault(Engine):
        def __init__(self):
            raise RuntimeError("broken built-in")

    mutable_config.set("config:plugins", {})
    with pytest.raises(RuntimeError, match="broken built-in"):
        spack.plugins.create_plugin("installer", BrokenDefault)
