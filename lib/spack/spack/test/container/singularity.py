# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.container.writers as writers


@pytest.fixture
def singularity_configuration(minimal_configuration):
    minimal_configuration["spack"]["container"]["format"] = "singularity"
    return minimal_configuration


def test_ensure_render_works(default_config, singularity_configuration):
    container_config = singularity_configuration["spack"]["container"]
    assert container_config["format"] == "singularity"
    # Here we just want to ensure that nothing is raised
    writer = writers.create(singularity_configuration)
    writer()


@pytest.mark.parametrize(
    "properties,expected",
    [
        (
            {"runscript": "/opt/view/bin/h5ls"},
            {"runscript": "/opt/view/bin/h5ls", "startscript": "", "test": "", "help": ""},
        )
    ],
)
def test_singularity_specific_properties(properties, expected, singularity_configuration):
    # Set the property in the configuration
    container_config = singularity_configuration["spack"]["container"]
    for name, value in properties.items():
        container_config.setdefault("singularity", {})[name] = value

    # Assert the properties return the expected values
    writer = writers.create(singularity_configuration)
    for name, value in expected.items():
        assert getattr(writer, name) == value
