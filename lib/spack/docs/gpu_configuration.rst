..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A guide to configuring Spack to use external GPU support, including ROCm and CUDA installations, as well as the OpenGL API.

Using External GPU Support
==========================

Many packages come with a ``+cuda`` or ``+rocm`` variant.
With no added configuration, Spack will download and install the needed components.
It may be preferable to use existing system support: the following sections help with using a system installation of GPU libraries.

Using an External ROCm Installation
-----------------------------------

Spack breaks down ROCm into many separate component packages.
The following is an example ``packages.yaml`` that organizes a consistent set of ROCm components for use by dependent packages:

.. code-block:: yaml

   packages:
     all:
       variants: amdgpu_target=gfx90a
     hip:
       buildable: false
       externals:
       - spec: "hip@10.1 %gcc@13.3.0" # define default GCC libstc++ that should be used
         prefix: /opt/rocm/core-10.1
     amdsmi:
       buildable: false
       externals:
       - spec: amdsmi@10.1
         prefix: /opt/rocm/core-10.1
     comgr:
       buildable: false
       externals:
       - spec: comgr@10.1
         prefix: /opt/rocm/core-10.1
     hipblas:
       buildable: false
       externals:
       - spec: hipblas@10.1
         prefix: /opt/rocm/core-10.1
     hipcub:
       buildable: false
       externals:
       - spec: hipcub@10.1
         prefix: /opt/rocm/core-10.1
     hipfft:
       buildable: false
       externals:
       - spec: hipfft@10.1
         prefix: /opt/rocm/core-10.1
     hiprand:
       buildable: false
       externals:
       - spec: hiprand@10.1
         prefix: /opt/rocm/core-10.1
     hipsparse:
       buildable: false
       externals:
       - spec: hipsparse@10.1
         prefix: /opt/rocm/core-10.1
     miopen-hip:
       buildable: false
       externals:
       - spec: miopen-hip@10.1
         prefix: /opt/rocm/core-10.1
     rccl:
       buildable: false
       externals:
       - spec: rccl@10.1
         prefix: /opt/rocm/core-10.1
     rocblas:
       buildable: false
       externals:
       - spec: rocblas@10.1
         prefix: /opt/rocm/core-10.1
     rocfft:
       buildable: false
       externals:
       - spec: rocfft@10.1
         prefix: /opt/rocm/core-10.1
     rocm-cmake:
       buildable: false
       externals:
       - spec: rocm-cmake@10.1
         prefix: /opt/rocm/core-10.1
     rocm-dbgapi:
       buildable: false
       externals:
       - spec: rocm-dbgapi@10.1
         prefix: /opt/rocm/core-10.1
     rocm-debug-agent:
       buildable: false
       externals:
       - spec: rocm-debug-agent@10.1
         prefix: /opt/rocm/core-10.1
     rocm-device-libs:
       buildable: false
       externals:
       - spec: rocm-device-libs@10.1
         prefix: /opt/rocm/core-10.1
     rocm-gdb:
       buildable: false
       externals:
       - spec: rocm-gdb@10.1
         prefix: /opt/rocm/core-10.1
     rocm-opencl:
       buildable: false
       externals:
       - spec: rocm-opencl@10.1
         prefix: /opt/rocm/core-10.1
     rocm-smi-lib:
       buildable: false
       externals:
       - spec: rocm-smi-lib@10.1
         prefix: /opt/rocm/core-10.1
     rocprofiler-systems:
       buildable: false
       externals:
       - spec: rocprofiler-systems@10.1
         prefix: /opt/rocm/core-10.1
     hipify-clang:
       buildable: false
       externals:
       - spec: hipify-clang@10.1
         prefix: /opt/rocm/core-10.1
     hsa-amd-aqlprofile:
       buildable: false
       externals:
       - spec: hsa-amd-aqlprofile@10.1
         prefix: /opt/rocm/core-10.1
     hsa-rocr-dev:
       buildable: false
       externals:
       - spec: hsa-rocr-dev@10.1
         prefix: /opt/rocm/core-10.1
     roctracer-dev-api:
       buildable: false
       externals:
       - spec: roctracer-dev-api@10.1
         prefix: /opt/rocm/core-10.1
     roctracer-dev:
       buildable: false
       externals:
       - spec: roctracer-dev@10.1
         prefix: /opt/rocm/core-10.1
     rocprim:
       buildable: false
       externals:
       - spec: rocprim@10.1
         prefix: /opt/rocm/core-10.1
     rocrand:
       buildable: false
       externals:
       - spec: rocrand@10.1
         prefix: /opt/rocm/core-10.1
     hipsolver:
       buildable: false
       externals:
       - spec: hipsolver@10.1
         prefix: /opt/rocm/core-10.1
     rocsolver:
       buildable: false
       externals:
       - spec: rocsolver@10.1
         prefix: /opt/rocm/core-10.1
     rocsparse:
       buildable: false
       externals:
       - spec: rocsparse@10.1
         prefix: /opt/rocm/core-10.1
     rocthrust:
       buildable: false
       externals:
       - spec: rocthrust@10.1
         prefix: /opt/rocm/core-10.1
     rocprofiler-dev:
       buildable: false
       externals:
       - spec: rocprofiler-dev@10.1
         prefix: /opt/rocm/core-10.1
     rocprofiler-sdk:
       buildable: false
       externals:
       - spec: rocprofiler-sdk@10.1
         prefix: /opt/rocm/core-10.1
     rocm-core:
       buildable: false
       externals:
       - spec: rocm-core@10.1
         prefix: /opt/rocm/core-10.1


This is in combination with the following compiler definition:

.. code-block:: yaml

   packages:
     llvm-amdgpu:
       buildable: false
       externals:
       - spec: llvm-amdgpu@10.1
         prefix: /opt/rocm/core-10.1/lib/llvm
         extra_attributes:
           compilers:
             c: /opt/rocm/core-10.1/lib/llvm/bin/amdclang
             cxx: /opt/rocm/core-10.1/lib/llvm/bin/amdclang++
             fortran: /opt/rocm/core-10.1/lib/llvm/bin/amdflang

This includes the following considerations:

- Each of the listed externals specifies ``buildable: false`` to force Spack to use only the externals we defined.
- ``spack external find`` can automatically locate some of the ``hip``/``rocm`` packages, but not all of them, and furthermore not in a manner that guarantees a complementary set if multiple ROCm installations are available.
- The ``prefix`` is the same for several components, but note that others require listing one of the subdirectories as a prefix.

Using an External CUDA Installation
-----------------------------------

CUDA is split into fewer components and is simpler to specify:

.. code-block:: yaml

   packages:
     all:
       variants:
       - cuda_arch=70
     cuda:
       buildable: false
       externals:
       - spec: cuda@11.0.2
         prefix: /opt/cuda/cuda-11.0.2/

where ``/opt/cuda/cuda-11.0.2/lib/`` contains ``libcudart.so``.



Using an External OpenGL API
----------------------------
Depending on whether we have a graphics card or not, we may choose to use OSMesa or GLX to implement the OpenGL API.

If a graphics card is unavailable, OSMesa is recommended and can typically be built with Spack.
However, if we prefer to utilize the system GLX tailored to our graphics card, we need to declare it as an external.
Here's how to do it:


.. code-block:: yaml

   packages:
     libglx:
       require: [opengl]
     opengl:
       buildable: false
       externals:
       - prefix: /usr/
         spec: opengl@4.6

Note that the prefix has to be the root of both the libraries and the headers (e.g., ``/usr``), not the path to the ``lib`` directory.
To know which spec for OpenGL is available, use ``cd /usr/include/GL && grep -Ri gl_version``.
