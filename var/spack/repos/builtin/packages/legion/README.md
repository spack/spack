# Legion Spack Package Notes

The Legion Spack package follows the underlying approach used in Legion's CMake-based build infrastructure.  If you are not familiar with using Spack, we encourage you to start with the **[Spack 101 Tutorial](https://spack-tutorial.readthedocs.io/en/latest/)**.  For more background on Legion please visit the project [website](https://legion.stanford.edu). There you can find information on getting started, tutorials, and supporting documentation.

## Versions

We strongly recommend the majority of users start with the latest **stable** branch of Legion.  This will guarantee the most regularly tested and debugged version of the code.  We also strive to have quarterly tagged release throughout the calendar year starting March (e.g., legion-YY.MM.0 where MM starts at *'03'* and runs through *'12'* for any calendar year).  These versioned downloads are captured via the [Legion GitHub page](https://github.com/StanfordLegion/legion) and captured in the Spack package for individual use via the naming convention above.  The details for each release are captured in the CHANGES.txt file at the top-level of the repository.

## Spack Usage and Details

**NOTE: This version of the Legion *spackage* no longer depends upon an external GASNet spackage.  Instead, as supported and preferred by the GASNet developers, Legion internalizes the GASNet configuration and build process tailored to Legion's needs.  At present this approach should minimize both building and configuration issues that have occurred in the past.**

With a working installation of Spack following variants can be used to download, configure, and build legion.  As of its latest release Legion uses features from C++11 and can be build using either GCC or Clang (and likely any other compilers with full C++11 support).  For example,

    spack install legion %clang@10.0

will build and install Legion using version 10.0 of the clang compiler.  Additional compiler flags (beyond those automatically enabled by the underlying Legion CMake configuration) may be specified by using the `cppflags` option to Spack:

    spack install legion %clang@10.0 cppflags=-Wall

You can find more details about customizing the compiler with Spack [here](https://spack-tutorial.readthedocs.io/en/latest/tutorial_basics.html#customizing-compilers).

There are a number of configuration parameters (variants) for Legion that can be specified on the command line.  To see a complete listing of these variants you can use the following command:

    spack info legion

The default build and install of Legion is suitable for laptop/desktop development needs.  Additional variants will need to be specified to build for distributed memory systems, GPU support, and other features (e.g., debugging, profiling, etc.).  A full list of the currently supported variants is provided below.

These variants may then be used on the Spack command line to customize the build of Legion you would like to install.  For boolean-based variants the `+`, `-`, or `~` *sigils* can be used. In this case, the `+` specifies a `True` value and either `-` or `~` can be used for the `False` setting (two values for `False` are provided to avoid conflicts with shell command line parameters. For example,

    spack install legion@stable~cuda+hdf5%clang10.0

will build/install the stable version of Legion without CUDA and with HDF5 support; using Clang 10.0 as the compiler.  See below for more examples of the various package options. 

## Overview of Legion's Spack Variants


This section provides an overview of the variants that are available for builds and installations of Legion and the underlying Realm runtime libraries.  These variants range from important configuration parameters for many users, to more involved and low-level details more likely to be leveraged when debugging correctness and performance issues.  For these last set of use cases we encourage users to visit the Legion [Debugging](https://legion.stanford.edu/debugging/) and [Profiling](https://legion.stanford.edu/profiling/) pages.

Note that any variants with a default of `on` or `off` are boolean values and may be configured on the Spack command line using the `+`, or `-` (or `~`) sigils.

Finally, to build the highest performing installation of Legion requires an appropriate configuration and installation of GASNet-Ex (while we have support for an MPI transport layer it is still in testing and evaluation for achieving the best possible performance).  See the following section for details on the steps needed to build a high-performance install of Legion using Spack.

### Debugging & Internal Runtime Configurations

* **`build_type`**: This variant exposes the CMake build type setting.  Following directly from CMake these available values for this variant are [`Debug`, `RelWithDebInfo`, and `Release`]. `default=RelWithDebInfo`

* **`bounds_checks`**:  This variant supports `on` or `off` values and enables, or disables bounds checking within the runtime's data accessors.  This is helpful for debugging but  does have the potential to degrade performance (therefore it is disabled in the default build).  `default=off`

* **`privilege_checks`**: This variant enables the runtime checking of data privileges in Legion's data accessors. This can helpful in debugging applications. `default=off`

* **`spy`**: This variant enables applications to produce detailed logging information for debugging with the [Legion Spy](https://legion.stanford.edu/debugging/#legion-spy) tool.  `default=off`

* **`max_dims`**: This variant provides an integral value for the maximum number of dimensions in a logical region that are supported by the build/install.  `default=3`  *Note: Currently supported values range from 1 to 9.*

* **`max_fields`**: This variant provides an integral value for the maximum number of fields that may be stored within a logical region.  `default=512` *Note: Internally this requires a value that is a power-of-two -- if a non power-of-two value is provided the next largest power-of-two will be used.*

* **`output_level`**: This variant enables the (dynamic) debugging level for the runtime.  It can be one of the following values: [`spew`, `debug`, `info`, `print`, `warning`, `error`, `fatal`, or `none`].  `default=warning`

* **`papi`**: This variant enables PAPI performance measurements.  `default=off`

* **`redop_complex`** This variant enables support for the reduction of complex types. `default=off`  Note: will be enabled when `+bindings` is set.

* **`shared_libs`**: Build shared libraries for Legion and Realm. `default=off`

* **`enable_tls`**: This variant supports `on` or `off` and enables thread-local-storage of the Legion runtime context.  `default=off`

### Bindings & Interoperability

* **`bindings`**: This variant supports `on` or `off` and will build the language bindings for Legion.  In addition to the required C++ interface, this currently includes C, Python, and Fortran. `default=off`  Note you can use `+python` or `+fortran` to select a subset of these bindings.

* **`python`**: This variant enables Python support in terms of both bindings and runtime support (where instance(s) of the Python interpreter must be available.) `default=off`

* **`fortran`**: This variant supports `on` or `off` and enables building of Fortran language bindings for Legion. `default=off`

[//]: <> (TOOD: More details here on Kokkos interop?)

* **`kokkos`**: Enable support for interoperability with [Kokkos](https://github.com/kokkos) use in Legion tasks. `default=off`

[//]: <> (TOOD: More details here on OpenMP interop?)

* **`openmp`**: This variant enables OpenMP support within Legion tasks (and within the Realm runtime). Please note that the full OpenMP feature set (e.g. OpenMP 5.0) is not fully supported when enabling this feature.  `default=off`

* **`libdl`**: Enable support for dynamic object loading (via "libdl").  `default=on`

### Processor Architecture Support (e.g., GPUs)

* **`cuda`**: This variant supports `on` or `off` and enables CUDA support within Legion.  `default=off`

* **`cuda_arch`**: This variant specifics the specific CUDA architecture to support within the Legion build/installation.  Currently this variant must be one of [`60`, `70`, `75`, or `80`].  Where `60` is the Pascal architecture, `70` is for Volta, `75` is for Turing, and `80` is for `Volta`. `default=70`

* **`cuda_hijack`**:  This variant supports `on` or `off` and determines if the build enables performance enhancements by "*hijacking* entry points into CUDA's runtime API; thus, it obviously implies `+cuda`.This is a performance enhancement and not necessary but suggested for production use cases on NVIDIA-based systems.  `default=off`

### External Library Support

* **`hdf5`**: This variant supports `on` or `off` and enables building of HDF5 support within the runtime. `default=off`

* **`hwloc`**: Build using "libhwloc" support for numa-aware topology support within Realm (Legion's low-level runtime layer).  `default=off`

* **`zlib`**: This variant enables support for zlib. `default=on`

### Distributed Memory/Network Transport/Interconnect Support

* **`network`**: This variant specifies what network transport layer Legion/Realm should use for moving data across the distributed memories of a system.  The options are currently: [`gasnet`, `mpi`, or `none`].  The most tested and reliable interface for distributed memory systems is `gasnet`.  Via this package GASNet will be automatically configured and built. If you want to use a pre-installed version of GASNet you can use the `gasnet_root` variant; this will disable the automatic/internal installation of GASNet. We strongly encourage the use of the automatic configuration and build mechanism as it is tailored to Legion's use cases. If you would like to read more about please visit their [web page](https://gasnet.lbl.gov).  Note that the `mpi` transport layer is new and still being tuned and debugged.  Finally, if you want to run on a single system (e.g., a desktop or laptop) for development activities you may drop this parameter or specify `network=none`.  `default=none`

* **`conduit`** requires `(network=gasnet)` **only**: This variant selects the GASNet conduit to use and must be provided when `network=gasnet`.  The current choices are: [`aries`, `ibv`, `mpi`, `ucx`, `udp`, or `none`]:  defaults to `none`.
  * **aries**: Aries for Cray XC series (see [documentation](https://gasnet.lbl.gov/dist-ex/aries-conduit/README)).
  * **ibv**: OpenIB/OpenFabrics Verbs for InfiniBand (see [documentation](https://gasnet.lbl.gov/dist-ex/ibv-conduit/README)).
  * **mpi**: Portable conduit, works on any network with MPI 1.1 or newer (see [documentation](https://gasnet.lbl.gov/dist-ex/mpi-conduit/README)).
  * **ucx**: *(NOTE: EXPERIMENTAL)*  Unified Communication X framework (see [documentation](https://gasnet.lbl.gov/dist-ex/ucx-conduit/README)).
  * **udp**: Portable conduit, works on any network with a TCP/IP stack (see [documentation](https://gasnet.lbl.gov/dist-ex/udp-conduit/README)).

* **`gasnet_root`**: This variant points the package at a pre-installed version of GASNet for use when building Legion.  This skips the default behavior of embedding the GASNet build within that of Legion. It requires that `conduit` be set to match that used by the installed version of GASNet (*note that incorrectly setting `conduit` could result in failures that are not caught by the Spack package as failures will only occur during the build of Legion*). `default=/usr/local`

## Examples

This section highlights a few common configurations/installations for various common installations of Legion. 

### Laptop/Desktop Development

The default configuration will build a version of Legion without network support that is often helpful in laptop or desktop installs for development using Legion. The first example is the most straightforward and enables a CPU-only configuration of Legion:

`$ spack install legion@stable`

Given that many uses cases for laptop/desktop development involve debugging Legion you might want to consider enabling [Legion Spy](https://legion.stanford.edu/debugging/#legion-spy), bounds and privilege checks, and optionally enable debugging level output diagnostics:

`$ spack install legion@stable +spy +bounds_checks +privilege_checks [output=debug]`

Note that by specifying `+spy` the package will also install the Legion profiler.  Both will be available in the corresponding `bin` directory created by Spack's install mechanisms.

#### Adding GPU Support

To enable support for NVIDIA GPUs with Legion you can add the `+cuda` variant to the examples provided above.  In addition, you can also use the `cuda_arch` flag to enable specific GPU architectures.  For example, the follow command line installs the stable version of Legion with CUDA support for NVIDIA's Volta architecture:

`$ spack install legion@stable +cuda cuda_arch=70`

If you wanted to program tasks using Kokkos support for GPUs you can simply add the `+kokkos` option to the previous command line: 

`$ spack install legion@stable +cuda cuda_arch=70 +kokkos`

this will enable Kokkos interoperability in Legion and also build and configure a version of Kokkos with cuda and Volta GPU support.

#### Networking/Distributed Memory Support 

In order to add modify the above configuration to support a distributed memory architecture you need to add a `network` target.  For example, to build a version of Legion that uses GASNet for the data transport layer you would specify:

`$ spack install legion@stable +cuda cuda_arch=70 +kokkos network=gasnet`

Without the addition of a specific GASNet *conduit* this command will use the UDP conduit. To change this to support a Infniband-based cluster you would add:

`$ spack install legion@stable +cuda cuda_arch=70 +kokkos network=gasnet conduit=ibv`

For a pre-existing installation of GASNet you can point the package at the root directory of the installation (also often know as the installation *prefix*). For example, to point the package at a version installed under `/opt/local` (*i.e., the include files are stored under `/opt/local/include` and libraries are in `/opt/local/lib`*) you would add `gasnet_root=/opt/local` to the command line.
