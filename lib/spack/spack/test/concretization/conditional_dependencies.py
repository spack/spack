# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.concretize
import spack.spec


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


@pytest.mark.parametrize("holds,mpi", [(True, "zmpi"), (True, "mpich"), (False, "mpich")])
def test_conditional_deps(holds, mpi, config, mock_packages):
    """Test concretizing conditional dependencies.

    Tests two cases of the condition being true (2 different implementations)
    Tests one case for the condition being false

    Testing two cases for condition true ensures that the choice of provider is not coincidental
    """
    sigil = "+" if holds else "~"
    request = f"hdf5{sigil}mpi ^[when='^mpi' virtuals=mpi]{mpi}"
    concrete = spack.concretize.concretize_one(request)

    assert (mpi in concrete) == holds
    assert ("mpi" in concrete) == holds


@pytest.mark.parametrize("c", [True, False])
@pytest.mark.parametrize("cxx", [True, False])
@pytest.mark.parametrize("fortran", [True, False])
def test_conditional_compilers(c, cxx, fortran, mutable_config, mock_packages, config_two_gccs):
    """Test concretizing with conditional compilers

    Tests every combination of +~c, +~cxx, and +~fortran
    """
    # Abstract spec parametrized to depend/not on c/cxx/fortran
    # and with conditional dependencies for each on the less preferred gcc
    abstract = spack.spec.Spec("conditional-languages")
    abstract.constrain(f"c={c}")
    abstract.constrain(f"cxx={cxx}")
    abstract.constrain(f"fortran={fortran}")

    preferred_gcc = spack.concretize.concretize_one(abstract)
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
    assert (concrete == preferred_gcc) == (not any((c, cxx, fortran)))
