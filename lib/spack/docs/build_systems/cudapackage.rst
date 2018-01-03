.. _cudapackage:

-----------
CudaPackage
-----------

Different from other packages, ``CudaPackage`` does not represent a build
system. Instead its goal is to simplify and unify usage of ``CUDA`` in other
packages. It provides ``cuda`` variant to enable/disable ``CUDA``, and
``cuda_arch`` variant to optionally specify the architecture. It also declares
dependencies on the ``CUDA`` package based on the architecture as well as
specifies conflicts for certain compiler versions.

In order to use it, just add another base class to your package, for example:

.. code-block:: python

   class MyPackage(CMakePackage, CudaPackage):
     ...
