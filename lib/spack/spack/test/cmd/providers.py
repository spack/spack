# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

from spack.main import SpackCommand

pytestmark = [pytest.mark.usefixtures("mock_packages")]

providers = SpackCommand("providers")


@pytest.mark.parametrize(
    "pkg",
    [("mpi",), ("mpi@2",), ("mpi", "lapack"), ("",)],  # Lists all the available virtual packages
)
def test_it_just_runs(pkg):
    providers(*pkg)


@pytest.mark.parametrize(
    "vpkg,provider_list",
    [
        (
            ("mpi",),
            [
                "intel-parallel-studio",
                "low-priority-provider",
                "mpich@3:",
                "mpich2",
                "multi-provider-mpi@1.10.0",
                "multi-provider-mpi@2.0.0",
                "zmpi",
            ],
        ),
        (
            ("lapack", "something"),
            [
                "intel-parallel-studio",
                "low-priority-provider",
                "netlib-lapack",
                "openblas-with-lapack",
                "simple-inheritance",
                "splice-a",
                "splice-h",
                "splice-vh",
            ],
        ),  # Call 2 virtual packages at once
    ],
)
def test_provider_lists(vpkg, provider_list):
    output = providers(*vpkg)
    for item in provider_list:
        assert item in output


@pytest.mark.parametrize(
    "pkg,error_cls",
    [
        ("zlib", ValueError),
        ("foo", ValueError),  # Trying to call with a package that does not exist
    ],
)
def test_it_just_fails(pkg, error_cls):
    with pytest.raises(error_cls):
        providers(pkg)
