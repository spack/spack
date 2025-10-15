# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ManyConditionalDeps(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0")

    variant("cuda", description="enable foo dependencies", default=True)
    variant("rocm", description="enable bar dependencies", default=True)

    for i in range(30):
        depends_on(f"gpu-dep +cuda cuda_arch={i}", when=f"+cuda cuda_arch={i}")

    for i in range(30):
        depends_on(f"gpu-dep +rocm amdgpu_target={i}", when=f"+rocm amdgpu_target={i}")
