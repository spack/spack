# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib

import pytest

import spack.util.spack_yaml as syaml


@pytest.fixture()
def minimal_configuration():
    return {
        "spack": {
            "specs": ["gromacs", "mpich", "fftw precision=float"],
            "container": {
                "format": "docker",
                "images": {"os": "ubuntu:22.04", "spack": "develop"},
            },
        }
    }


@pytest.fixture()
def config_dumper(tmp_path: pathlib.Path):
    """Function that dumps an environment config in a temporary folder."""

    def dumper(configuration):
        content = syaml.dump(configuration, default_flow_style=False)
        config_file = tmp_path / "spack.yaml"
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(content or "")
        return str(tmp_path)

    return dumper


@pytest.fixture()
def container_config_dir(minimal_configuration, config_dumper):
    return config_dumper(minimal_configuration)
