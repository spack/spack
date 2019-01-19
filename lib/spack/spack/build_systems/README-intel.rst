====================================
Development Notes on Intel Packages
====================================

These are notes for concepts and development of
lib/spack/spack/build_systems/intel.py .

For documentation on how to *use* ``IntelPackage``, see
lib/spack/docs/build_systems/intelpackage.rst .

-------------------------------------------------------------------------------
Installation and path handling as implemented in ./intel.py
-------------------------------------------------------------------------------


***************************************************************************
Prefix differences between Spack-external and Spack-internal installations
***************************************************************************


Problem summary
~~~~~~~~~~~~~~~~

For Intel packages that were installed external to Spack, ``self.prefix`` will
be a *component-specific* path (e.g. to an MKL-specific dir hierarchy), whereas
for a package installed by Spack itself, ``self.prefix`` will be a
*vendor-level* path that holds one or more components (or parts thereof), and
must be further qualified down to a particular desired component.

It is possible that a similar conceptual difference is inherent to other
package families that use a common vendor-style installer.


Description
~~~~~~~~~~~~

Spack makes packages available through two routes, let's call them A and B:

A. Packages pre-installed external to Spack and configured *for* Spack
B. Packages built and installed *by* Spack.

For a user who is interested in building end-user applications, it should not
matter through which route any of its dependent packages has been installed.
Most packages natively support a ``prefix`` concept which unifies the two
routes just fine.

Intel packages, however, are more complicated because they consist of a number
of components that are released as a suite of varying extent, like "Intel
Parallel Studio *Foo* Edition", or subsetted into products like "MKL" or "MPI",
each of which also contain libraries from other components like the compiler
runtime and multithreading libraries. For this reason, an Intel package is
"anchored" during installation at a directory level higher than just the
user-facing directory that has the conventional hierarchy of ``bin``, ``lib``,
and others relevant for the end-product.

As a result, internal to Spack, there is a conceptual difference in what
``self.prefix`` represents for the two routes.

For route A, consider MKL installed outside of Spack. It will likely be one
product component among other products, at one particular release among others
that are installed in sibling or cousin directories on the local system.
Therefore, the path given to Spack in ``packages.yaml`` should be a
*product-specific and fully version-specific* directory.  E.g., for an
``intel-mkl`` package, ``self.prefix`` should look like::

  /opt/intel/compilers_and_libraries_2018.1.163/linux/mkl

In this route, the interaction point with the user is encapsulated in an
environment variable which will be (in pseudo-code)::

    MKLROOT := {self.prefix}

For route B, a Spack-based installation of MKL will be placed in the directory
given to the ``./install.sh`` script of Intel's package distribution.  This
directory is taken to be the *vendor*-specific anchor directory, playing the
same role as the default ``/opt/intel``. In this case, ``self.prefix`` will
be::

  $SPACK_ROOT/opt/spack/linux-centos6-x86_64/gcc-4.9.3/intel-mkl-2018.1.163-<HASH>

However, now the environment variable will have to be constructed as *several
directory levels down*::

    MKLROOT := {self.prefix}/compilers_and_libraries_2018.1.163/linux/mkl

A recent post on the Spack mailing list illustrates the confusion when route A
was taken while route B was the only one that was coded in Spack:
https://groups.google.com/d/msg/spack/x28qlmqPAys/Ewx6220uAgAJ


Solution
~~~~~~~~~

Introduce a series of functions which will return the appropriate
directories, regardless of whether the Intel package has been installed
external or internal to Spack:

==========================  ==================================================
Function                    Example return values
--------------------------  --------------------------------------------------
normalize_suite_dir()       Spack-external installation:
                                /opt/intel/compilers_and_libraries_2018.1.163
                            Spack-internal installation:
                                $SPACK_ROOT/...<HASH>/compilers_and_libraries_2018.1.163
--------------------------  --------------------------------------------------
normalize_path('mkl')       <suite_dir>/linux/mkl
component_bin_dir()         <suite_dir>/linux/mkl/bin
component_lib_dir()         <suite_dir>/linux/mkl/lib/intel64
--------------------------  --------------------------------------------------
normalize_path('mpi')       <suite_dir>/linux/mpi
component_bin_dir('mpi')    <suite_dir>/linux/mpi/intel64/bin
component_lib_dir('mpi')    <suite_dir>/linux/mpi/intel64/lib
==========================  ==================================================


*********************************
Analysis of directory layouts
*********************************

Let's look at some sample directory layouts, using ``ls -lF``,
but focusing on names and symlinks only.

Spack-born installation of ``intel-mkl@2018.1.163``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ ls -l <prefix>

  bin/
      - compilervars.*sh (symlinked) ONLY

  compilers_and_libraries -> compilers_and_libraries_2018
      - generically-named entry point, stable across versions (one hopes)

  compilers_and_libraries_2018/
      - vaguely-versioned dirname, holding a stub hierarchy --ignorable

      $ ls -l compilers_and_libraries_2018/linux/
      bin         - actual compilervars.*sh (reg. files) ONLY
      documentation -> ../../documentation_2018/
      lib -> ../../compilers_and_libraries_2018.1.163/linux/compiler/lib/
      mkl -> ../../compilers_and_libraries_2018.1.163/linux/mkl/
      pkg_bin -> ../../compilers_and_libraries_2018.1.163/linux/bin/
      samples -> ../../samples_2018/
      tbb -> ../../compilers_and_libraries_2018.1.163/linux/tbb/

  compilers_and_libraries_2018.1.163/
      - Main "product" + a minimal set of libs from related products

      $ ls -l compilers_and_libraries_2018.1.163/linux/
      bin/        - compilervars.*sh, link_install*sh  ONLY
      mkl/        - Main Product ==> to be assigned to MKLROOT
      compiler/   - lib/intel64_lin/libiomp5*  ONLY
      tbb/        - tbb/lib/intel64_lin/gcc4.[147]/libtbb*.so* ONLY

  parallel_studio_xe_2018 -> parallel_studio_xe_2018.1.038/
  parallel_studio_xe_2018.1.038/
      - Alternate product packaging - ignorable

      $ ls -l parallel_studio_xe_2018.1.038/
      bin/               - actual psxevars.*sh (reg. files)
      compilers_and_libraries_2018 -> <full_path>/comp...aries_2018.1.163
      documentation_2018 -> <full_path_prefix>/documentation_2018
      samples_2018 -> <full_path_prefix>/samples_2018
      ...

  documentation_2018/
  samples_2018/
  lib -> compilers_and_libraries/linux/lib/
  mkl -> compilers_and_libraries/linux/mkl/
  tbb -> compilers_and_libraries/linux/tbb/
                  - auxiliaries and convenience links

Spack-external installation of Intel-MPI 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For MPI, the layout is slightly different than MKL. The prefix will have to
include an architecture directory (typically ``intel64``), which then contains
bin/, lib/, ..., all without further architecture branching.  The environment
variable ``I_MPI_ROOT`` from the API documentation, however, must be the
package's top directory, not including the architecture.

FIXME: For MANPATH, need the parent dir.

::

  $ ls -lF /opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/
  bin64 -> intel64/bin/
  etc64 -> intel64/etc/
  include64 -> intel64/include/
  lib64 -> intel64/lib/

  benchmarks/
  binding/
  intel64/
  man/
  test/

The package contains an MPI-2019 preview; Curiously, its release notes contain
the tag: "File structure clean-up." I could not find further documentation on
this, however, so it is unclear what, if any, changes will make it to release.

https://software.intel.com/en-us/articles/restoring-legacy-path-structure-on-intel-mpi-library-2019

::

  $ ls -lF /opt/intel/compilers_and_libraries_2018.1.163/linux/mpi_2019/
  binding/
  doc/
  imb/
  intel64/
  man/
  test/

Spack-external installation of Intel Parallel Studio 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the main product bundle that I actually downloaded and installed on my
system.  Its nominal installation directory mostly holds merely symlinks
to components installed in sibling dirs::

  $ ls -lF /opt/intel/parallel_studio_xe_2018.1.038/
  advisor_2018		 -> /opt/intel/advisor_2018/
  clck_2018		 -> /opt/intel/clck/2018.1/
  compilers_and_libraries_2018 -> /opt/intel/comp....aries_2018.1.163/
  documentation_2018	 -> /opt/intel/documentation_2018/
  ide_support_2018	 -> /opt/intel/ide_support_2018/
  inspector_2018		 -> /opt/intel/inspector_2018/
  itac_2018		 -> /opt/intel/itac/2018.1.017/
  man		         -> /opt/intel/man/
  samples_2018		 -> /opt/intel/samples_2018/
  vtune_amplifier_2018	 -> /opt/intel/vtune_amplifier_2018/

  psxevars.csh		 -> ./bin/psxevars.csh*
  psxevars.sh		 -> ./bin/psxevars.sh*
  bin/            - *vars.*sh scripts + sshconnectivity.exp ONLY

  licensing/
  uninstall*

The only relevant regular files are ``*vars.*sh``, but those also just churn
through the subordinate vars files of the components.

Installation model
~~~~~~~~~~~~~~~~~~~~

Intel packages come with an ``install.sh`` script that is normally run
interactively (in either text or GUI mode) but can run unattended with a
``--silent <file>`` option, which is of course what Spack uses.

Format of configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file is conventionally called ``silent.cfg`` and has a simple
``token=value`` syntax.  Before using the configuration file, the installer
calls ``<staging_dir>/pset/check.awk`` to validate it. Example paths to the
validator are::

      .../l_mkl_2018.1.163/pset/check.awk .
      .../parallel_studio_xe_2018_update1_cluster_edition/pset/check.awk

The tokens that are accepted in the configuration file vary between packages.
Tokens not supported for a given package **will cause the installer to stop
and fail.** This is particularly relevant for license-related tokens, which are
accepted only for packages that actually require a license.

Reference: [Intel's documentation](https://software.intel.com/en-us/articles/configuration-file-format)

See also:  https://software.intel.com/en-us/articles/silent-installation-guide-for-intel-parallel-studio-xe-composer-edition-for-os-x

The following is from ``.../parallel_studio_xe_2018_update1_cluster_edition/pset/check.awk``:

* Tokens valid for all packages encountered::

    ACCEPT_EULA                                  {accept, decline}
    CONTINUE_WITH_OPTIONAL_ERROR                 {yes, no}
    PSET_INSTALL_DIR                             {/opt/intel, , filepat}
    CONTINUE_WITH_INSTALLDIR_OVERWRITE           {yes, no}
    COMPONENTS                                   {ALL, DEFAULTS, , anythingpat}
    PSET_MODE                                    {install, repair, uninstall}
    NONRPM_DB_DIR                                {, filepat}

    SIGNING_ENABLED                              {yes, no}
    ARCH_SELECTED                                {IA32, INTEL64, ALL}

* Mentioned but unexplained in ``check.awk``::

    NO_VALIDATE   (?!)

* Only for licensed packages::

    ACTIVATION_SERIAL_NUMBER                     {, snpat}
    ACTIVATION_LICENSE_FILE                      {, lspat, filepat}
    ACTIVATION_TYPE                              {exist_lic, license_server,
                                                 license_file, trial_lic,

    PHONEHOME_SEND_USAGE_DATA                    {yes, no}
                                                 serial_number}

* Only for Amplifier (obviously)::

    AMPLIFIER_SAMPLING_DRIVER_INSTALL_TYPE       {build, kit}
    AMPLIFIER_DRIVER_ACCESS_GROUP                {, anythingpat, vtune}
    AMPLIFIER_DRIVER_PERMISSIONS                 {, anythingpat, 666}
    AMPLIFIER_LOAD_DRIVER                        {yes, no}
    AMPLIFIER_C_COMPILER                         {, filepat, auto, none}
    AMPLIFIER_KERNEL_SRC_DIR                     {, filepat, auto, none}
    AMPLIFIER_MAKE_COMMAND                       {, filepat, auto, none}
    AMPLIFIER_INSTALL_BOOT_SCRIPT                {yes, no}
    AMPLIFIER_DRIVER_PER_USER_MODE               {yes, no}

* Only for MKL and Studio::

    CLUSTER_INSTALL_REMOTE                       {yes, no}
    CLUSTER_INSTALL_TEMP                         {, filepat}
    CLUSTER_INSTALL_MACHINES_FILE                {, filepat}

* "backward compatibility" (?)::

    INSTALL_MODE                                 {RPM, NONRPM}
    download_only                                {yes}
    download_dir                                 {, filepat}


Details for licensing tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quoted from
https://software.intel.com/en-us/articles/configuration-file-format,
for reference:

[ed. note: As of 2018-05, the page incorrectly references ``ACTIVATION``, which
was used only until about 2012; this is corrected to ``ACTIVATION_TYPE`` here.]

    ...

    ``ACTIVATION_TYPE=exist_lic``
       This directive tells the install program to look for an existing
       license during the install process.  This is the preferred method for
       silent installs.  Take the time to register your serial number and get
       a license file (see below).  Having a license file on the system
       simplifies the process.  In addition, as an administrator it is good
       practice to know WHERE your licenses are saved on your system.
       License files are plain text files with a .lic extension.  By default
       these are saved in /opt/intel/licenses which is searched by default.
       If you save your license elsewhere, perhaps under an NFS folder, set
       environment variable **INTEL_LICENSE_FILE** to the full path to your
       license file prior to starting the installation or use the
       configuration file directive ``ACTIVATION_LICENSE_FILE`` to specify the
       full pathname to the license file.
    
       Options for ``ACTIVATION_TYPE`` are ``{ exist_lic, license_file, server_lic,
       serial_number, trial_lic }``
    
    ``exist_lic``
       directs the installer to search for a valid license on the server.
       Searches will utilize the environment variable **INTEL_LICENSE_FILE**,
       search the default license directory /opt/intel/licenses, or use the
       ``ACTIVATION_LICENSE_FILE`` directive to find a valid license file.
    
    ``license_file``
       is similar to exist_lic but directs the installer to use
       ``ACTIVATION_LICENSE_FILE`` to find the license file.
    
    ``server_lic``
       is similar to exist_lic and exist_lic but directs the installer that
       this is a client installation and a floating license server will be
       contacted to active the product.  This option will contact your
       floating license server on your network to retrieve the license
       information.  BEFORE using this option make sure your client is
       correctly set up for your network including all networking, routing,
       name service, and firewall configuration.  Insure that your client has
       direct access to your floating license server and that firewalls are
       set up to allow TCP/IP access for the 2 license server ports.
       server_lic will use **INTEL_LICENSE_FILE** containing a port@host format
       OR a client license file.  The formats for these are described here
       https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license
    
    ``serial_number``
       directs the installer to use directive ``ACTIVATION_SERIAL_NUMBER`` for
       activation.  This method will require the installer to contact an
       external Intel activation server over the Internet to confirm your
       serial number.  Due to user and company firewalls, this method is more
       complex and hence error prone of the available activation methods.  We
       highly recommend using a license file or license server for activation
       instead.
    
    ``trial_lic``
       is used only if you do not have an existing license and intend to
       temporarily evaluate the compiler.  This method creates a temporary
       trial license in Trusted Storage on your system.
    
    ...

*******************
vars files
*******************

Intel's product packages contain a number of shell initialization files let's call them vars files.

There are three kinds:

#. Component-specific vars files, such as `mklvars` or `tbbvars`.
#. Toplevel vars files such as "psxevars". They will scan for all
   component-specific vars files associated with the product, and source them
   if found.
#. Symbolic links to either of them. Links may appear under a different name
   for backward compatibility.

At present, IntelPackage class is only concerned with the toplevel vars files,
generally found in the product's toplevel bin/ directory.

For reference, here is an overview of the names and locations of the vars files
in the 2018 product releases, as seen for Spack-native installation. NB: May be
incomplete as some components may have been omitted during installation.

Names of vars files seen::

    $ cd opt/spack/linux-centos6-x86_64
    $ find intel* -name \*vars.sh -printf '%f\n' | sort -u | nl
     1	advixe-vars.sh
     2	amplxe-vars.sh
     3	apsvars.sh
     4	compilervars.sh
     5	daalvars.sh
     6	debuggervars.sh
     7	iccvars.sh
     8	ifortvars.sh
     9	inspxe-vars.sh
    10	ippvars.sh
    11	mklvars.sh
    12	mpivars.sh
    13	pstlvars.sh
    14	psxevars.sh
    15	sep_vars.sh
    16	tbbvars.sh

Names and locations of vars files, sorted by Spack package name::

    $ cd opt/spack/linux-centos6-x86_64
    $ find intel* -name \*vars.sh -printf '%y\t%-15f\t%h\n' \
        | cut -d/ -f1,4- \
        | sed '/iccvars\|ifortvars/d; s,/,\t\t,; s,\.sh,,; s,  */\(intel[/-]\),\1,' \
        | sort -k3,3 -k2,2 \
        | nl \
        | awk '{printf "%6i %-2s %-16s %-24s %s\n", $1, $2, $3, $4, $5}'

    --------------------------------------------------------------------------------------------------------
    item no.
       file or link
          name of vars file
                           Spack package name
                                                    dir relative to Spack install dir
    --------------------------------------------------------------------------------------------------------

     1 f  mpivars          intel                    compilers_and_libraries_2018.1.163/linux/mpi/intel64/bin
     2 f  mpivars          intel                    compilers_and_libraries_2018.1.163/linux/mpirt/bin/ia32_lin
     3 f  tbbvars          intel                    compilers_and_libraries_2018.1.163/linux/tbb/bin
     4 f  pstlvars         intel                    compilers_and_libraries_2018.1.163/linux/pstl/bin
     5 f  compilervars     intel                    compilers_and_libraries_2018.1.163/linux/bin
     6 f  compilervars     intel                    compilers_and_libraries_2018/linux/bin
     7 l  compilervars     intel                    bin
     8 f  daalvars         intel-daal               compilers_and_libraries_2018.2.199/linux/daal/bin
     9 f  psxevars         intel-daal               parallel_studio_xe_2018.2.046/bin
    10 l  psxevars         intel-daal               parallel_studio_xe_2018.2.046
    11 f  compilervars     intel-daal               compilers_and_libraries_2018.2.199/linux/bin
    12 f  compilervars     intel-daal               compilers_and_libraries_2018/linux/bin
    13 l  compilervars     intel-daal               bin
    14 f  ippvars          intel-ipp                compilers_and_libraries_2018.2.199/linux/ipp/bin
    15 f  psxevars         intel-ipp                parallel_studio_xe_2018.2.046/bin
    16 l  psxevars         intel-ipp                parallel_studio_xe_2018.2.046
    17 f  compilervars     intel-ipp                compilers_and_libraries_2018.2.199/linux/bin
    18 f  compilervars     intel-ipp                compilers_and_libraries_2018/linux/bin
    19 l  compilervars     intel-ipp                bin
    20 f  mklvars          intel-mkl                compilers_and_libraries_2018.2.199/linux/mkl/bin
    21 f  psxevars         intel-mkl                parallel_studio_xe_2018.2.046/bin
    22 l  psxevars         intel-mkl                parallel_studio_xe_2018.2.046
    23 f  compilervars     intel-mkl                compilers_and_libraries_2018.2.199/linux/bin
    24 f  compilervars     intel-mkl                compilers_and_libraries_2018/linux/bin
    25 l  compilervars     intel-mkl                bin
    26 f  mpivars          intel-mpi                compilers_and_libraries_2018.2.199/linux/mpi_2019/intel64/bin
    27 f  mpivars          intel-mpi                compilers_and_libraries_2018.2.199/linux/mpi/intel64/bin
    28 f  psxevars         intel-mpi                parallel_studio_xe_2018.2.046/bin
    29 l  psxevars         intel-mpi                parallel_studio_xe_2018.2.046
    30 f  compilervars     intel-mpi                compilers_and_libraries_2018.2.199/linux/bin
    31 f  compilervars     intel-mpi                compilers_and_libraries_2018/linux/bin
    32 l  compilervars     intel-mpi                bin
    33 f  apsvars          intel-parallel-studio    vtune_amplifier_2018.1.0.535340
    34 l  apsvars          intel-parallel-studio    performance_snapshots_2018.1.0.535340
    35 f  ippvars          intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/ipp/bin
    36 f  ippvars          intel-parallel-studio    composer_xe_2015.6.233/ipp/bin
    37 f  mklvars          intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/mkl/bin
    38 f  mklvars          intel-parallel-studio    composer_xe_2015.6.233/mkl/bin
    39 f  mpivars          intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/mpi/intel64/bin
    40 f  mpivars          intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/mpirt/bin/ia32_lin
    41 f  tbbvars          intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/tbb/bin
    42 f  tbbvars          intel-parallel-studio    composer_xe_2015.6.233/tbb/bin
    43 f  daalvars         intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/daal/bin
    44 f  pstlvars         intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/pstl/bin
    45 f  psxevars         intel-parallel-studio    parallel_studio_xe_2018.1.038/bin
    46 l  psxevars         intel-parallel-studio    parallel_studio_xe_2018.1.038
    47 f  sep_vars         intel-parallel-studio    vtune_amplifier_2018.1.0.535340
    48 f  sep_vars         intel-parallel-studio    vtune_amplifier_2018.1.0.535340/target/android_v4.1_x86_64
    49 f  advixe-vars      intel-parallel-studio    advisor_2018.1.1.535164
    50 f  amplxe-vars      intel-parallel-studio    vtune_amplifier_2018.1.0.535340
    51 f  inspxe-vars      intel-parallel-studio    inspector_2018.1.1.535159
    52 f  compilervars     intel-parallel-studio    compilers_and_libraries_2018.1.163/linux/bin
    53 f  compilervars     intel-parallel-studio    compilers_and_libraries_2018/linux/bin
    54 l  compilervars     intel-parallel-studio    bin
    55 f  debuggervars     intel-parallel-studio    debugger_2018/bin


********************
MPI linkage
********************


Library selection
~~~~~~~~~~~~~~~~~~~~~

In the Spack code so far, the library selections for MPI are:

::

        libnames = ['libmpifort', 'libmpi']
        if 'cxx' in self.spec.last_query.extra_parameters:
            libnames = ['libmpicxx'] + libnames
        return find_libraries(libnames,
                              root=self.component_lib_dir('mpi'),
                              shared=True, recursive=False)

The problem is that there are multiple library versions under ``component_lib_dir``::

    $ cd $I_MPI_ROOT 
    $ find . -name libmpi.so | sort
    ./intel64/lib/debug/libmpi.so
    ./intel64/lib/debug_mt/libmpi.so
    ./intel64/lib/libmpi.so
    ./intel64/lib/release/libmpi.so
    ./intel64/lib/release_mt/libmpi.so

"mt" refers to multi-threading, not in the explicit sense but in the sense of being thread-safe::

    $ mpiifort -help | grep mt
       -mt_mpi         link the thread safe version of the Intel(R) MPI Library

Well, why should we not inspect what the canonical script does?  The wrapper
has its own hardcoded "prefix=..." and can thus tell us what it will do, from a
*wiped environment* no less!::

    $ env - intel64/bin/mpiicc -show hello.c | ld-unwrap-args 
    icc 'hello.c' \
        -I/opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/intel64/include \
        -L/opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/intel64/lib/release_mt \
        -L/opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/intel64/lib \
        -Xlinker --enable-new-dtags \
        -Xlinker -rpath=/opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/intel64/lib/release_mt \
        -Xlinker -rpath=/opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/intel64/lib \
        -Xlinker -rpath=/opt/intel/mpi-rt/2017.0.0/intel64/lib/release_mt \
        -Xlinker -rpath=/opt/intel/mpi-rt/2017.0.0/intel64/lib \
        -lmpifort \
        -lmpi \
        -lmpigi \
        -ldl \
        -lrt \
        -lpthread


MPI Wrapper options
~~~~~~~~~~~~~~~~~~~~~

For reference, here's the wrapper's builtin help output::

    $ mpiifort -help
    Simple script to compile and/or link MPI programs.
    Usage: mpiifort [options] <files>
    ----------------------------------------------------------------------------
    The following options are supported:
       -fc=<name> | -f90=<name>
                       specify a FORTRAN compiler name: i.e. -fc=ifort
       -echo           print the scripts during their execution
       -show           show command lines without real calling
       -config=<name>  specify a configuration file: i.e. -config=ifort for mpif90-ifort.conf file
       -v              print version info of mpiifort and its native compiler
       -profile=<name> specify a profile configuration file (an MPI profiling
                       library): i.e. -profile=myprofile for the myprofile.cfg file.
                       As a special case, lib<name>.so or lib<name>.a may be used
                       if the library is found
       -check_mpi      link against the Intel(R) Trace Collector (-profile=vtmc).
       -static_mpi     link the Intel(R) MPI Library statically
       -mt_mpi         link the thread safe version of the Intel(R) MPI Library
       -ilp64          link the ILP64 support of the Intel(R) MPI Library
       -no_ilp64       disable ILP64 support explicitly
       -fast           the same as -static_mpi + pass -fast option to a compiler.
       -t or -trace
                       link against the Intel(R) Trace Collector
       -trace-imbalance
                       link against the Intel(R) Trace Collector imbalance library
                       (-profile=vtim)
       -dynamic_log    link against the Intel(R) Trace Collector dynamically
       -static         use static linkage method
       -nostrip        turn off the debug information stripping during static linking
       -O              enable optimization
       -link_mpi=<name>
                       link against the specified version of the Intel(R) MPI Library
    All other options will be passed to the compiler without changing.
    ----------------------------------------------------------------------------
    The following environment variables are used:
       I_MPI_ROOT      the Intel(R) MPI Library installation directory path
       I_MPI_F90 or MPICH_F90
                       the path/name of the underlying compiler to be used
       I_MPI_FC_PROFILE or I_MPI_F90_PROFILE or MPIF90_PROFILE
                       the name of profile file (without extension)
       I_MPI_COMPILER_CONFIG_DIR
                       the folder which contains configuration files *.conf
       I_MPI_TRACE_PROFILE
                       specify a default profile for the -trace option
       I_MPI_CHECK_PROFILE
                       specify a default profile for the -check_mpi option
       I_MPI_CHECK_COMPILER
                       enable compiler setup checks
       I_MPI_LINK      specify the version of the Intel(R) MPI Library
       I_MPI_DEBUG_INFO_STRIP
                       turn on/off the debug information stripping during static linking
       I_MPI_FCFLAGS
                       special flags needed for compilation
       I_MPI_LDFLAGS 
                       special flags needed for linking
    ----------------------------------------------------------------------------


Side Note: MPI version divergence in 2015 release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package `intel-parallel-studio@cluster.2015.6` contains both a full MPI
development version in `$prefix/impi` and an MPI Runtime under the
`composer_xe*` suite directory. Curiously, these have *different versions*,
with a release date nearly 1 year apart::

    $ $SPACK_ROOT/...uaxaw7/impi/5.0.3.049/intel64/bin/mpiexec --version
    Intel(R) MPI Library for Linux* OS, Version 5.0 Update 3 Build 20150804 (build id: 12452)
    Copyright (C) 2003-2015, Intel Corporation. All rights reserved.

    $ $SPACK_ROOT/...uaxaw7/composer_xe_2015.6.233/mpirt/bin/intel64/mpiexec --version
    Intel(R) MPI Library for Linux* OS, Version 5.0 Update 1 Build 20140709
    Copyright (C) 2003-2014, Intel Corporation. All rights reserved.

I'm not sure what to make of it.


**************
macOS support
**************

- On macOS, the Spack methods here only include support to integrate an
  externally installed MKL.

- URLs in child packages will be Linux-specific; macOS download packages
  are located in differently numbered dirs and are named m_*.dmg.
