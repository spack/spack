from spack.package import *
from spack.pkg.builtin.hdf5 import Hdf5 as BuiltinHdf5


class Hdf5(BuiltinHdf5):
    __doc__ = BuiltinHdf5.__doc__

    variant('page_buffer_patch', default=False, when="@1.12.1",
            description='Enable the page buffer in parallel HDF5.')

    # Modifies the check that page buffering is incompatible with parallel
    # HDF5. The issue is that it should also work with the parallel version
    # of the library, but only if one doesn't ask for MPI-IO.
    patch('page-buffer-check-on-file-open_v1.12.1.patch', when="@1.12.1+page_buffer_patch+mpi",
          sha256="379c30fab7abb88e95d6e65c318baaeb3f7443290ad3fab4cfc5bcaa9a3f0a25")
