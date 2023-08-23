.. Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

===================================
Using an External ROCm Installation
===================================

Spack breaks down ROCm into many separate component packages. The following
is an example packages.yaml that organizes a consistent set of ROCm
components:

.. code-block:: yaml

   packages:
     all:
       compiler: [rocmcc@=5.3.0]
       variants: amdgpu_target=gfx90a
     hip:
       buildable: false
       externals:
       - spec: hip@5.3.0
         prefix: /opt/rocm-5.3.0/hip
     hsa-rocr-dev:
       buildable: false
       externals:
       - spec: hsa-rocr-dev@5.3.0
         prefix: /opt/rocm-5.3.0/
     llvm-amdgpu:
       buildable: false
       externals:
       - spec: llvm-amdgpu@5.3.0
         prefix: /opt/rocm-5.3.0/llvm/
     comgr:
       buildable: false
       externals:
       - spec: comgr@5.3.0
         prefix: /opt/rocm-5.3.0/
     hipsparse:
       buildable: false
       externals:
       - spec: hipsparse@5.3.0
         prefix: /opt/rocm-5.3.0/
     hipblas:
       buildable: false
       externals:
       - spec: hipblas@5.3.0
         prefix: /opt/rocm-5.3.0/
     rocblas:
       buildable: false
       externals:
       - spec: rocblas@5.3.0
         prefix: /opt/rocm-5.3.0/
     rocprim:
       buildable: false
       externals:
       - spec: rocprim@5.3.0
         prefix: /opt/rocm-5.3.0/rocprim/

This is in combination with the following compiler definition:

.. code-block:: yaml

   compilers:
   - compiler:
       spec: rocmcc@=5.3.0
       paths:
         cc: /opt/rocm-5.3.0/bin/amdclang
         cxx: /opt/rocm-5.3.0/bin/amdclang++
         f77: null
         fc: /opt/rocm-5.3.0/bin/amdflang
       flags: {}
       operating_system: rhel8
       target: x86_64
       modules: []
       environment: {}
       extra_rpaths: []
