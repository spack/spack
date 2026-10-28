# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.concretize
import spack.error
from spack.spec import Spec


@pytest.mark.parametrize("variant", ["cuda_arch=:70", "cuda_arch=70,:70"])
def test_compatible_gpu_form_cannot_be_built(mock_packages, config, variant):
    with pytest.raises(spack.error.UnsatisfiableSpecError, match="for queries only"):
        spack.concretize.concretize_one(Spec(f"vtk-m +cuda {variant}"))


def test_exact_gpu_target_concretizes(mock_packages, config):
    spec = spack.concretize.concretize_one(Spec("vtk-m +cuda cuda_arch=70"))
    assert spec.variants["cuda_arch"].value == "70"
    assert ",".join(map(str, spec.architecture.gpus)) == "70"
