from spack.package import *
from spack.pkg.builtin.hdf5 import Hdf5 as BuiltinHdf5


class Hdf5(BuiltinHdf5):
    __doc__ = BuiltinHdf5.__doc__

    variant(
        "page_buffer_patch",
        default=False,
        when="@1.12.1,1.14.0",
        description="Enable the page buffer in parallel HDF5.",
    )

    patch(
        "hpe-mpi-type-free_v1.12.1.patch",
        when="@1.12.1+mpi^hpe-mpi",
        sha256="3daa6efc8c04354ea8e7bf0c6529a904c8b94d77c9ae4cfb06ea9efb3e5b6afe",
    )

    patch(
        "hpe-mpi-type-free_v1.14.0.patch",
        when="@1.14.0+mpi^hpe-mpi",
        sha256="474b58caf52eeff5afacc2d4c5ef7b501d2b75f2d81684d303dc60697769e2ec",
    )

    # Modifies the check that page buffering is incompatible with parallel
    # HDF5. The issue is that it should also work with the parallel version
    # of the library, but only if one doesn't ask for MPI-IO.
    patch(
        "page-buffer-check-on-file-open_v1.12.1.patch",
        when="@1.12.1+page_buffer_patch+mpi",
        sha256="379c30fab7abb88e95d6e65c318baaeb3f7443290ad3fab4cfc5bcaa9a3f0a25",
    )

    patch(
        "page-buffer-check-on-file-open_v1.14.0.patch",
        when="@1.14.0+page_buffer_patch+mpi",
        sha256="77fb681371736c156e348b4733e6cb505ed91e3968182a3c08f2eff052b90e34",
    )
