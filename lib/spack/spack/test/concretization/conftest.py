# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest


@pytest.fixture(scope="function")
def config_two_gccs(mutable_config):
    # Configure two gcc compilers that could be concretized to
    extra_attributes_block = {
        "compilers": {"c": "/path/to/gcc", "cxx": "/path/to/g++", "fortran": "/path/to/fortran"}
    }
    mutable_config.set(
        "packages:gcc:externals::",
        [
            {
                "spec": "gcc@12.3.1 languages=c,c++,fortran",
                "prefix": "/path",
                "extra_attributes": extra_attributes_block,
            },
            {
                "spec": "gcc@10.3.1 languages=c,c++,fortran",
                "prefix": "/path",
                "extra_attributes": extra_attributes_block,
            },
        ],
    )
