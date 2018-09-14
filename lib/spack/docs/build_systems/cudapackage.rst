.. _cudapackage:

-----------
CudaPackage
-----------

Different from other packages, ``CudaPackage`` does not represent a build
system. Instead its goal is to simplify and unify usage of ``CUDA`` in other
packages.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Provided variants and dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``CudaPackage`` provides ``cuda`` variant (default to ``off``) to enable/disable
``CUDA``, and ``cuda_arch`` variant to optionally specify the architecture.
It also declares dependencies on the ``CUDA`` package ``depends_on('cuda@...')``
based on the architecture as well as specifies conflicts for certain compiler versions.

^^^^^
Usage
^^^^^

In order to use it, just add another base class to your package, for example:

.. code-block:: python

    class MyPackage(CMakePackage, CudaPackage):
        ...
        def cmake_args(self):
            spec = self.spec
            if '+cuda' in spec:
                options.append('-DWITH_CUDA=ON')
                cuda_arch = spec.variants['cuda_arch'].value
                if cuda_arch is not None:
                    options.append('-DCUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0]))
            else:
                options.append('-DWITH_CUDA=OFF')
