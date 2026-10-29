# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.vendor.archspec.gpu as archspec_gpu

import spack.concretize
import spack.error
import spack.gpus
from spack.spec import Spec


@pytest.fixture
def host_gpus(monkeypatch):
    def _set(*names):
        monkeypatch.setattr(spack.gpus, "host", lambda: [archspec_gpu.TARGETS[n] for n in names])

    return _set


def test_exact_gpu_target_concretizes(mock_packages, config):
    spec = spack.concretize.concretize_one(Spec("vtk-m +cuda cuda_arch=70"))
    assert spec.variants["cuda_arch"].value == "70"
    assert ",".join(map(str, spec.architecture.gpus)) == "70"


@pytest.mark.parametrize(
    "host,request_,expected",
    [
        # the host's own target, when it is in the range
        (["75"], ":75", "75"),
        (["70"], ":75", "70"),
        # the top of the range, when the host is above it or has no GPU of that vendor
        (["75"], ":70", "70"),
        ([], ":75", "75"),
        (["gfx900"], ":75", "75"),
    ],
)
def test_compatible_gpu_form_picks_the_best_target(
    mock_packages, config, host_gpus, host, request_, expected
):
    host_gpus(*host)
    spec = spack.concretize.concretize_one(Spec(f"vtk-m +cuda cuda_arch={request_}"))
    assert spec.variants["cuda_arch"].value == expected
    assert spec.satisfies(f"cuda_arch={request_}")


def test_compatible_gpu_form_with_an_incompatible_host_is_an_error(
    mock_packages, config, host_gpus
):
    host_gpus("80")
    with pytest.raises(spack.error.UnsatisfiableSpecError, match="No GPU target of 'vtk-m'"):
        spack.concretize.concretize_one(Spec("vtk-m +cuda cuda_arch=:75"))
