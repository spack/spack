# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.concretize
import spack.spec


@pytest.mark.parametrize(
    "abstract_spec,expected,not_expected",
    [
        # Set +mpi explicitly
        (
            "hdf5+mpi ^[when='^mpi' virtuals=mpi] zmpi",
            ["%[virtuals=mpi] zmpi", "^mpi", "%mpi"],
            ["%[virtuals=mpi] mpich"],
        ),
        (
            "hdf5+mpi %[when='%mpi' virtuals=mpi] zmpi",
            ["%[virtuals=mpi] zmpi", "^mpi", "%mpi"],
            ["%[virtuals=mpi] mpich"],
        ),
        (
            "hdf5+mpi %[when='+mpi' virtuals=mpi] zmpi",
            ["%[virtuals=mpi] zmpi", "^mpi", "%mpi"],
            ["%[virtuals=mpi] mpich"],
        ),
        (
            "hdf5+mpi ^[when='^mpi' virtuals=mpi] mpich",
            ["%[virtuals=mpi] mpich", "^mpi", "%mpi"],
            ["%[virtuals=mpi] zmpi"],
        ),
        (
            "hdf5+mpi %[when='%mpi' virtuals=mpi] mpich",
            ["%[virtuals=mpi] mpich", "^mpi", "%mpi"],
            ["%[virtuals=mpi] zmpi"],
        ),
        # Use the default, which is to have +mpi
        (
            "hdf5 ^[when='^mpi' virtuals=mpi] zmpi",
            ["%[virtuals=mpi] zmpi", "^mpi", "%mpi"],
            ["%[virtuals=mpi] mpich"],
        ),
        (
            "hdf5 %[when='%mpi' virtuals=mpi] zmpi",
            ["%[virtuals=mpi] zmpi", "^mpi", "%mpi"],
            ["%[virtuals=mpi] mpich"],
        ),
        (
            "hdf5 %[when='+mpi' virtuals=mpi] zmpi",
            ["%[virtuals=mpi] zmpi", "^mpi", "%mpi"],
            ["%[virtuals=mpi] mpich"],
        ),
        # Set ~mpi explicitly
        ("hdf5~mpi ^[when='^mpi' virtuals=mpi] zmpi", [], ["%[virtuals=mpi] zmpi", "^mpi"]),
        ("hdf5~mpi %[when='%mpi' virtuals=mpi] zmpi", [], ["%[virtuals=mpi] zmpi", "^mpi"]),
        ("hdf5~mpi %[when='+mpi' virtuals=mpi] zmpi", [], ["%[virtuals=mpi] zmpi", "^mpi"]),
    ],
)
def test_conditional_mpi_dependency(
    abstract_spec, expected, not_expected, default_mock_concretization
):
    """Test concretizing conditional mpi dependencies."""
    concrete = default_mock_concretization(abstract_spec)

    for x in expected:
        assert concrete.satisfies(x), x

    for x in not_expected:
        assert not concrete.satisfies(x), x

    assert concrete.satisfies(abstract_spec)


@pytest.mark.parametrize("c", [True, False])
@pytest.mark.parametrize("cxx", [True, False])
@pytest.mark.parametrize("fortran", [True, False])
def test_conditional_compilers(c, cxx, fortran, mutable_config, mock_packages, config_two_gccs):
    """Test concretizing with conditional compilers, using every combination of +~c, +~cxx,
    and +~fortran.
    """
    # Abstract spec parametrized to depend/not on c/cxx/fortran
    # and with conditional dependencies for each on the less preferred gcc
    abstract = spack.spec.Spec(f"conditional-languages c={c} cxx={cxx} fortran={fortran}")
    concrete_unconstrained = spack.concretize.concretize_one(abstract)
    abstract.constrain(
        "^[when='%c' virtuals=c]gcc@10.3.1 "
        "^[when='%cxx' virtuals=cxx]gcc@10.3.1 "
        "^[when='%fortran' virtuals=fortran]gcc@10.3.1"
    )
    concrete = spack.concretize.concretize_one(abstract)

    # We should get the dependency we specified for each language we enabled
    assert concrete.satisfies("%[virtuals=c]gcc@10.3.1") == c
    assert concrete.satisfies("%[virtuals=cxx]gcc@10.3.1") == cxx
    assert concrete.satisfies("%[virtuals=fortran]gcc@10.3.1") == fortran

    # The only time the two concrete specs are the same is if we don't use gcc at all
    assert (concrete == concrete_unconstrained) == (not any((c, cxx, fortran)))
