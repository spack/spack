# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Note that where possible, this should produce specs using `entries_to_specs`
rather than `spec_from_entry`, since the former does additional work to
establish dependency relationships (and in general the manifest-parsing
logic needs to consume all related specs in a single pass).
"""
import json
import os

import pytest

import spack
import spack.cray_manifest as cray_manifest
from spack.cray_manifest import compiler_from_entry, entries_to_specs

example_x_json_str = """\
{
  "name": "packagex",
  "hash": "hash-of-x",
  "prefix": "/path/to/packagex-install/",
  "version": "1.0",
  "arch": {
    "platform": "linux",
    "platform_os": "centos8",
    "target": {
      "name": "haswell"
    }
  },
  "compiler": {
    "name": "gcc",
    "version": "10.2.0.cray"
  },
  "dependencies": {
    "packagey": {
      "hash": "hash-of-y",
      "type": ["link"]
    }
  },
  "parameters": {
    "precision": ["double", "float"]
  }
}
"""


example_compiler_entry = """\
{
  "name": "gcc",
  "prefix": "/path/to/compiler/",
  "version": "7.5.0",
  "arch": {
    "os": "centos8",
    "target": "x86_64"
  },
  "executables": {
    "cc": "/path/to/compiler/cc",
    "cxx": "/path/to/compiler/cxx",
    "fc": "/path/to/compiler/fc"
  }
}
"""


class JsonSpecEntry(object):
    def __init__(self, name, hash, prefix, version, arch, compiler, dependencies, parameters):
        self.name = name
        self.hash = hash
        self.prefix = prefix
        self.version = version
        self.arch = arch
        self.compiler = compiler
        self.dependencies = dependencies
        self.parameters = parameters

    def to_dict(self):
        return {
            "name": self.name,
            "hash": self.hash,
            "prefix": self.prefix,
            "version": self.version,
            "arch": self.arch,
            "compiler": self.compiler,
            "dependencies": self.dependencies,
            "parameters": self.parameters,
        }

    def as_dependency(self, deptypes):
        return (self.name, {"hash": self.hash, "type": list(deptypes)})


class JsonArchEntry(object):
    def __init__(self, platform, os, target):
        self.platform = platform
        self.os = os
        self.target = target

    def to_dict(self):
        return {"platform": self.platform, "platform_os": self.os, "target": {"name": self.target}}


class JsonCompilerEntry(object):
    def __init__(self, name, version, arch=None, executables=None):
        self.name = name
        self.version = version
        if not arch:
            arch = {"os": "centos8", "target": "x86_64"}
        if not executables:
            executables = {
                "cc": "/path/to/compiler/cc",
                "cxx": "/path/to/compiler/cxx",
                "fc": "/path/to/compiler/fc",
            }
        self.arch = arch
        self.executables = executables

    def compiler_json(self):
        return {
            "name": self.name,
            "version": self.version,
            "arch": self.arch,
            "executables": self.executables,
        }

    def spec_json(self):
        """The compiler spec only lists the name/version, not
        arch/executables.
        """
        return {"name": self.name, "version": self.version}


_common_arch = JsonArchEntry(platform="linux", os="centos8", target="haswell").to_dict()

# Intended to match example_compiler_entry above
_common_compiler = JsonCompilerEntry(
    name="gcc",
    version="10.2.0.cray",
    arch={"os": "centos8", "target": "x86_64"},
    executables={
        "cc": "/path/to/compiler/cc",
        "cxx": "/path/to/compiler/cxx",
        "fc": "/path/to/compiler/fc",
    },
)


def test_compatibility():
    """Make sure that JsonSpecEntry outputs the expected JSON structure
    by comparing it with JSON parsed from an example string. This
    ensures that the testing objects like JsonSpecEntry produce the
    same JSON structure as the expected file format.
    """
    y = JsonSpecEntry(
        name="packagey",
        hash="hash-of-y",
        prefix="/path/to/packagey-install/",
        version="1.0",
        arch=_common_arch,
        compiler=_common_compiler.spec_json(),
        dependencies={},
        parameters={},
    )

    x = JsonSpecEntry(
        name="packagex",
        hash="hash-of-x",
        prefix="/path/to/packagex-install/",
        version="1.0",
        arch=_common_arch,
        compiler=_common_compiler.spec_json(),
        dependencies=dict([y.as_dependency(deptypes=["link"])]),
        parameters={"precision": ["double", "float"]},
    )

    x_from_entry = x.to_dict()
    x_from_str = json.loads(example_x_json_str)
    assert x_from_entry == x_from_str


def test_compiler_from_entry():
    compiler_data = json.loads(example_compiler_entry)
    compiler_from_entry(compiler_data)


def generate_openmpi_entries():
    """Generate two example JSON entries that refer to an OpenMPI
    installation and a hwloc dependency.
    """
    # The hashes need to be padded with 'a' at the end to align with 8-byte
    # boundaries (for base-32 decoding)
    hwloc = JsonSpecEntry(
        name="hwloc",
        hash="hwlocfakehashaaa",
        prefix="/path/to/hwloc-install/",
        version="2.0.3",
        arch=_common_arch,
        compiler=_common_compiler.spec_json(),
        dependencies={},
        parameters={},
    )

    # This includes a variant which is guaranteed not to appear in the
    # OpenMPI package: we need to make sure we can use such package
    # descriptions.
    openmpi = JsonSpecEntry(
        name="openmpi",
        hash="openmpifakehasha",
        prefix="/path/to/openmpi-install/",
        version="4.1.0",
        arch=_common_arch,
        compiler=_common_compiler.spec_json(),
        dependencies=dict([hwloc.as_dependency(deptypes=["link"])]),
        parameters={"internal-hwloc": False, "fabrics": ["psm"], "missing_variant": True},
    )

    return [openmpi, hwloc]


def test_generate_specs_from_manifest():
    """Given JSON entries, check that we can form a set of Specs
    including dependency references.
    """
    entries = list(x.to_dict() for x in generate_openmpi_entries())
    specs = entries_to_specs(entries)
    (openmpi_spec,) = list(x for x in specs.values() if x.name == "openmpi")
    assert openmpi_spec["hwloc"]


def test_translate_cray_platform_to_linux(monkeypatch):
    """Manifests might list specs on newer Cray platforms as being "cray",
    but Spack identifies such platforms as "linux". Make sure we
    automaticaly transform these entries.
    """
    test_linux_platform = spack.platforms.test.Test("linux")

    def the_host_is_linux():
        return test_linux_platform

    monkeypatch.setattr(spack.platforms, "host", the_host_is_linux)

    cray_arch = JsonArchEntry(platform="cray", os="rhel8", target="x86_64").to_dict()
    spec_json = JsonSpecEntry(
        name="cray-mpich",
        hash="craympichfakehashaaa",
        prefix="/path/to/cray-mpich/",
        version="1.0.0",
        arch=cray_arch,
        compiler=_common_compiler.spec_json(),
        dependencies={},
        parameters={},
    ).to_dict()

    (spec,) = entries_to_specs([spec_json]).values()
    assert spec.architecture.platform == "linux"


def test_translate_compiler_name():
    nvidia_compiler = JsonCompilerEntry(
        name="nvidia",
        version="19.1",
        executables={"cc": "/path/to/compiler/nvc", "cxx": "/path/to/compiler/nvc++"},
    )

    compiler = compiler_from_entry(nvidia_compiler.compiler_json())
    assert compiler.name == "nvhpc"

    spec_json = JsonSpecEntry(
        name="hwloc",
        hash="hwlocfakehashaaa",
        prefix="/path/to/hwloc-install/",
        version="2.0.3",
        arch=_common_arch,
        compiler=nvidia_compiler.spec_json(),
        dependencies={},
        parameters={},
    ).to_dict()

    (spec,) = entries_to_specs([spec_json]).values()
    assert spec.compiler.name == "nvhpc"


def test_failed_translate_compiler_name():
    unknown_compiler = JsonCompilerEntry(name="unknown", version="1.0")

    with pytest.raises(spack.compilers.UnknownCompilerError):
        compiler_from_entry(unknown_compiler.compiler_json())

    spec_json = JsonSpecEntry(
        name="packagey",
        hash="hash-of-y",
        prefix="/path/to/packagey-install/",
        version="1.0",
        arch=_common_arch,
        compiler=unknown_compiler.spec_json(),
        dependencies={},
        parameters={},
    ).to_dict()

    with pytest.raises(spack.compilers.UnknownCompilerError):
        entries_to_specs([spec_json])


def create_manifest_content():
    return {
        # Note: the cray_manifest module doesn't use the _meta section right
        # now, but it is anticipated to be useful
        "_meta": {
            "file-type": "cray-pe-json",
            "system-type": "test",
            "schema-version": "1.3",
            "cpe-version": "22.06",
        },
        "specs": list(x.to_dict() for x in generate_openmpi_entries()),
        "compilers": [_common_compiler.compiler_json()],
    }


def test_read_cray_manifest(tmpdir, mutable_config, mock_packages, mutable_database):
    """Check that (a) we can read the cray manifest and add it to the Spack
    Database and (b) we can concretize specs based on that.
    """
    if spack.config.get("config:concretizer") == "clingo":
        pytest.skip(
            "The ASP-based concretizer is currently picky about " " OS matching and will fail."
        )

    with tmpdir.as_cwd():
        test_db_fname = "external-db.json"
        with open(test_db_fname, "w") as db_file:
            json.dump(create_manifest_content(), db_file)
        cray_manifest.read(test_db_fname, True)
        query_specs = spack.store.db.query("openmpi")
        assert any(x.dag_hash() == "openmpifakehasha" for x in query_specs)

        concretized_specs = spack.cmd.parse_specs(
            "depends-on-openmpi %gcc@4.5.0 arch=test-redhat6-x86_64" " ^/openmpifakehasha".split(),
            concretize=True,
        )
        assert concretized_specs[0]["hwloc"].dag_hash() == "hwlocfakehashaaa"


def test_read_cray_manifest_twice_no_compiler_duplicates(
    tmpdir, mutable_config, mock_packages, mutable_database
):
    if spack.config.get("config:concretizer") == "clingo":
        pytest.skip(
            "The ASP-based concretizer is currently picky about " " OS matching and will fail."
        )

    with tmpdir.as_cwd():
        test_db_fname = "external-db.json"
        with open(test_db_fname, "w") as db_file:
            json.dump(create_manifest_content(), db_file)

        # Read the manifest twice
        cray_manifest.read(test_db_fname, True)
        cray_manifest.read(test_db_fname, True)

        compilers = spack.compilers.all_compilers()
        filtered = list(
            c for c in compilers if c.spec == spack.spec.CompilerSpec("gcc@10.2.0.cray")
        )
        assert len(filtered) == 1


def test_read_old_manifest_v1_2(tmpdir, mutable_config, mock_packages, mutable_database):
    """Test reading a file using the older format
    ('version' instead of 'schema-version').
    """
    manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    manifest_file_path = os.path.join(manifest_dir, "test.json")
    with open(manifest_file_path, "w") as manifest_file:
        manifest_file.write(
            """\
{
  "_meta": {
    "file-type": "cray-pe-json",
    "system-type": "EX",
    "version": "1.3"
  },
  "specs": []
}
"""
        )
    cray_manifest.read(manifest_file_path, True)


def test_convert_validation_error(tmpdir, mutable_config, mock_packages, mutable_database):
    manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    # Does not parse as valid JSON
    invalid_json_path = os.path.join(manifest_dir, "invalid-json.json")
    with open(invalid_json_path, "w") as f:
        f.write(
            """\
{
"""
        )
    with pytest.raises(cray_manifest.ManifestValidationError) as e:
        cray_manifest.read(invalid_json_path, True)
    str(e)

    # Valid JSON, but does not conform to schema (schema-version is not a string
    # of length > 0)
    invalid_schema_path = os.path.join(manifest_dir, "invalid-schema.json")
    with open(invalid_schema_path, "w") as f:
        f.write(
            """\
{
  "_meta": {
    "file-type": "cray-pe-json",
    "system-type": "EX",
    "schema-version": ""
  },
  "specs": []
}
"""
        )
    with pytest.raises(cray_manifest.ManifestValidationError) as e:
        cray_manifest.read(invalid_schema_path, True)
    str(e)
