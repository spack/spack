.. _intelpackage:

.. contents::


--------------------------
Intel packages in Spack
--------------------------

Spack can work with several software development products offered by Intel.
Some of these are available under no-cost terms, others require a paid license.
All share the same basic steps for configuration, installation, and, where
applicable, license management. The relevant Spack Python class is:

.. code-block:: python

  IntelPackage

Spack handles several interaction routes with Intel tools, like it does for any
other package:

.. _`route 1`:

1. Accept system-provided tools in Spack after you declare them as *external packages*.

.. _`route 2`:

2. Install the products for you as *internal packages* in Spack.

.. _`route 3`:

3. *Use* the packages, regardless of installation route, to install what we'll
   call *client packages* for you, this being Spack's primary purpose.

An auxiliary route follows from `route 2`_, as it would for most Spack
packages, namely:

.. _`route 4`:

4. Make Spack-installed Intel tools available outside of Spack for ad-hoc use,
   typically through Spack-managed modulefiles.

This document covers routes 1 through 3.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Packages under no-cost license
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Intel's standalone performance library products, notably MKL and MPI, are
available for use under a `simplified license
<https://software.intel.com/en-us/license/intel-simplified-software-license>`_
since 2017 [fn1]_. They are packaged in Spack as:

* ``intel-mkl`` – Math Kernel Library (linear algebra and FFT),
* ``intel-mpi`` – The Intel-MPI implementation (derived from MPICH),
* ``intel-ipp`` – Primitives for image-, signal-, and data-processing,
* ``intel-daal`` – Machine learning and data analytics.

Some earlier versions of these library products were released under a paid
license, which for these versions must be available, like for compilers
discussed next, at installation time of the products and during compilation of
client packages.

The library packages can be used both with and without Intel compilers.
The latter offer options to simplify linking (sometimes considerably),
but Spack always uses fairly explicit linkage instead.


^^^^^^^^^^^^^^^^^^
Licensed packages
^^^^^^^^^^^^^^^^^^

Intel's core software development products that provide compilers, analyzers,
and optimizers do require a paid license.  In Spack, they are packaged as:

* ``intel-parallel-studio`` – the entire suite of compilers and libraries,
* ``intel`` – a subset containing just the compilers and the Intel-MPI runtime [fn2]_.

------

**TODO:** Confirm scope of MPI components (runtime vs. devel) in current (and
previous?) *cluster/professional/composer* editions, i.e., presence in downloads,
possibly subject to license coverage(!); see `disussion in PR #4300
<https://github.com/spack/spack/pull/4300#issuecomment-305582898>`_.
[NB: An "mpi" subdirectory is not indicative of the full MPI SDK being present
(i.e., ``mpicc``, …, and header files).  The directory may just as well contain
only the MPI runtime (``mpirun`` and shared libraries) .]

------

The license is needed at installation time and to compile client packages, but
never to merely run any resulting binaries.

The libraries that are provided in the standalone packages are also included in the
all-encompassing ``intel-parallel-studio``. To complicate matters a bit, that
package is sold in 3 "editions", of which only the upper-tier ``cluster``
edition supports *compiling* MPI applications, and hence only that edition can
provide the ``mpi`` virtual package.  (As mentioned [fn2]_, all editions
provide support for *running* MPI applications.)

The edition forms the leading part of the version number for Spack's
``intel*`` packages discussed here. This differs from the primarily numeric
version numbers seen with most other Spack packages. For example, we have:


.. code-block:: sh

  $ spack info intel-parallel-studio
  …
  Preferred version:  
      professional.2018.2    http:…

  Safe versions:  
      professional.2018.2    http:…
      …
      composer.2018.2        http:…
      …
      cluster.2018.2         http:…
      …
  …

To install the full studio suite, capable of compiling MPI applications, run:

.. code-block:: sh

  $ spack install intel-parallel-studio@cluster.2018.2        # ca. 12 GB

If you need to save some disk space or installation time, you could install
separately as needed:

.. code-block:: sh

  $ spack install intel         # 0.6 GB
  $ spack install intel-mpi     # 0.5 GB
  $ spack install intel-mkl     # 2.5 GB


^^^^^^^^^^^^^^^^^^^^
Unrelated packages
^^^^^^^^^^^^^^^^^^^^

The following packages do not use the Intel installer and are not in class ``IntelPackage``
that is discussed here:

* ``intel-gpu-tools`` – Test suite and low-level tools for the Linux `Direct
  Rendering Manager <https://en.wikipedia.org/wiki/Direct_Rendering_Manager>`_
* ``intel-mkl-dnn`` – Math Kernel Library for Deep Neural Networks (``CMakePackage``)
* ``intel-xed`` – X86 machine instructions encoder/decoder
* ``intel-tbb`` – Standalone version of Intel Threading Building Blocks. – Note that
  a TBB runtime version is included with ``intel-mkl``, and development
  versions are provided by the packages ``intel-parallel-studio`` (all
  editions) and its ``intel`` subset.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configuring Spack to use Intel licenses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you wish to integrate licensed Intel products into Spack as external packages
(`route 1`_ above) we assume that their license configuration is in place and
is working [fn3]_. In this case, skip to section `Integration of Intel tools
installed external to Spack`_.

If you plan to have Spack install licensed products for you (`route 2`_ above),
the Intel product installer that Spack will run underneath must have access to
a license.  Via the means sketched out in the following sections, check and use
the license provided by default means, or explicitly configure the license for
Spack.  For authoritative information on Intel licensing, see:

* https://software.intel.com/en-us/faq/licensing
* https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses

""""""""""""""""""""""""""""""""""""""
Pointing to an existing license server
""""""""""""""""""""""""""""""""""""""

Installing and configuring a license server is outside the scope of Spack. We
assume that:

* Your system administrator has a license server running.
* The license server offers valid licenses for the Intel packages of interest.
* You can access these licenses under the user id running Spack.

Be aware of the difference between (a) installing and configuring a license
server, and (b) configuring client software to *use* a server's
so-called floating licenses.  We are concerned here with (b) only. The
process of obtaining a license from a server for temporary use is called
"checking out a license".  For that, a client application such as the Intel
package installer or a compiler needs to know the host name and port number of
one or more license servers that it may query [fn4]_.

Follow one of three methods to `point client software to a floating license server
<https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license>`_.
Ideally, your license administrator will already have implemented one that can
be used unchanged in Spack: Look for the environment variable
``INTEL_LICENSE_FILE`` or for files
``/opt/intel/licenses/*.lic`` that contain::

  SERVER  hostname  hostid_or_ANY  portnum
  USE_SERVER

The relevant tokens, among possibly others, are the ``USE_SERVER`` line,
intended specifically for clients, and one or more ``SERVER`` lines above it
which give the network address.

If you cannot find pre-existing ``/opt/intel/licenses/*.lic`` files and the
``INTEL_LICENSE_FILE`` environment variable is not set (even after you loaded
any relevant modulefiles), ask your license administrator for the server
address(es) and place them in a "global" license file within your Spack
directory tree `as shown below <Spack-managed file_>`_).


""""""""""""""""""""""""""""""""""""
Installing a standalone license file
""""""""""""""""""""""""""""""""""""

If you purchased a user-specific license, `follow Intel's instructions to
<https://software.intel.com/en-us/faq/licensing#license-management>`_
"activate" it for your serial number, then download the resulting license file.
If needed, `request to have the file re-sent
<https://software.intel.com/en-us/articles/resend-license-file>`_ to you.

License files are plain text files containing license tokens in FLEXlm format
and whose name ends in ``.lic``.  Intel installers and compilers look for
license files in several locations when they run.  Place your license by one of
the following means, in order of decreasing preference:

* Default directory

  Install your license file in the directory ``/opt/intel/licenses/`` if you
  have write permission to it. This directory is inspected by all Intel tools
  and is therefore preferred, as no further configuration will be needed.
  Create the directory if it does not yet exist.  For the file name, either
  keep the downloaded name or use another suitably plain yet descriptive
  name that ends in ``.lic``. Adjust file permissions for access by licensed
  users.


* Directory given in environment variable

  If you cannot use the default directory, but your system already has set the
  environment variable ``INTEL_LICENSE_FILE`` independent from Spack [fn5]_,
  then, if you have the necessary write permissions, place your license file in
  one of the directories mentioned in this environment variable.  Adjust file
  permissions to match licensed users.


  **Recommendation:**
  If your system has not yet set and used the environment variable
  ``INTEL_LICENSE_FILE``, you could start using it with the ``spack install``
  stage of licensed tools and subsequent client packages. You would, however,
  be in a bind to always set that variable in the same manner, across
  updates and re-installations, and perhaps accommodate additions to it. As
  this may be difficult in the long run, we recommend that you do *not* attempt
  to start using the variable solely for Spack.  Instead, try the next option.

.. _`Spack-managed file`:

* Spack-managed file

  The first time Spack encounters an Intel package that requires a license, it
  will initialize a Spack-global Intel-specific license file for you, as a
  template with instructional comments, and bring up an editor [fn6]_.  Spack
  will do this *even if you have a working license elsewhere* on the system.

  * To proceed with an externally configured license, leave the newly templated
    file as is (containing comments only) and close the editor. You do not need
    to touch the file again.

  * To configure your own standalone license, copy the contents of your
    downloaded license file into the opened file, save it, and close the editor.

  * To use a license server (i.e., a floating network license) that is not
    already configured elsewhere on the system, supply your license server
    address(es) in the form of ``SERVER`` and ``USE_SERVER`` lines at the
    *beginning of the file* [fn7]_, in the format shown in section `Pointing to
    an existing license server`_. Save the file and close the editor.

  To revisit and manually edit this file, such as prior to a subsequent
  installation attempt, find it at
  ``$SPACK_ROOT/etc/spack/licenses/intel/intel.lic`` .

  Spack will place symbolic links to this file in each directory where licensed
  Intel binaries were installed.  If you kept the template unchanged, Intel tools
  will simply ignore it.


.. _integrate-external-intel:

----------------------------------------------------------
Integration of Intel tools installed *external* to Spack
----------------------------------------------------------

This section discusses `route 1`_ from the introduction.

A site that already uses Intel tools, especially licensed ones, will likely
have some versions already installed on the system, especially at a time when
Spack is just being introduced. It will be useful to make such previously
installed tools available for use by Spack as they are. How to do this varies
depending on the type of the tools:

^^^^^^^^^^^^^^^^^^^^^^
Integrating compilers
^^^^^^^^^^^^^^^^^^^^^^

For Spack to use external Intel compilers, you must tell it both *where* to
find them and *when* to use them.  The present section documents the "where"
aspect, involving ``compilers.yaml`` and, sadly, long absolute paths.
The "when" aspect actually relates to `route 3`_ and requires explicitly
stating a compiler component (in the form ``foo %intel``) when installing
client packages or altering Spack's compiler default in ``packages.yaml``.
See section `<Selecting Intel Compilers_>`_ for details.

Configure Spack to find external Intel compilers, like all compilers it is to use,
in ``compilers.yaml`` files located in
``$SPACK_ROOT/etc/spack/`` or your own ``~/.spack/`` directory.
In the Spack documentation, see
:ref:`Configuration Files in Spack <configuration>`
in general and
:ref:`Vendor-Specific Compiler Configuration <vendor-specific-compiler-configuration>`,
section Intel Compilers.

Briefly, the ``compilers.yaml`` files combine C and Fortran compilers of a
specific vendor release and define such a set as a Spack
:ref:`spec <sec-specs>`
that in this case has the form ``intel@compilerversion`` [fn8]_.
The entry determines how the spec is to be resolved, via ``paths`` and/or
``modules`` tokens, to each language compiler in the set.

The following example illustrates how to integrate the 2018 Intel compiler
suite, which outside of Spack was activated by users of the example system as
``module load intel/18``. Since Spack must be rather more picky about versions,
we must specify full paths and complete modulefile names in a relevant
``compilers.yaml`` entry. Edit as follows:

.. code-block:: sh

  spack config --scope=site edit compilers

This command will edit ``$SPACK_ROOT/etc/spack/compilers.yaml`` located inside
Spack's installation.  This scope is likely suitable for an installation that
might be shared between several users.  Choose another scope if desired.

Make sure the file begins with:

.. code-block:: yaml

    compilers:

Append the following, adjusting the paths appropriately:

.. code-block:: yaml

    - compiler:
        spec:       intel@18.0.2
        operating_system:   centos6
        target:     x86_64
        modules:    [intel/18/18.0.2]
        paths:
          cc:       /opt/intel/compilers_and_libraries_2018.2.199/linux/bin/intel64/icc
          cxx:      /opt/intel/compilers_and_libraries_2018.2.199/linux/bin/intel64/icpc
          f77:      /opt/intel/compilers_and_libraries_2018.2.199/linux/bin/intel64/ifort
          fc:       /opt/intel/compilers_and_libraries_2018.2.199/linux/bin/intel64/ifort

The Intel compilers need and use GCC to provide certain functionality, notably
to support C++. In the preceding minimal example, the  system's default ``gcc``
command would be queried for such needs.  To alter the GCC integration:

* add a gcc module to the list at the ``modules:`` tag, separated by comma, e.g. ``[gcc-4.9.3, intel/18/18.0.2]``, or
* add ``cflags:``, ``cxxflags:``, and ``fflags:`` tags under the ``paths:`` tag,

as detailed with examples under
:ref:`Vendor-Specific Compiler Configuration <vendor-specific-compiler-configuration>`
in the Spack documentation. There is also an advanced third option:

* the modulefile that provides the Intel compilers (``intel/18/18.0.2`` in the
  example) could, for the benefit of users outside of Spack, explicitly
  integrate a specific ``gcc`` version via compiler flag environment variables
  or (hopefully not) via a sneaky extra ``PATH`` addition.

.. tip:: Visit section `Selecting Intel Compilers`_ to learn how to tell
   Spack to use the newly configured compilers.

^^^^^^^^^^^^^^^^^^^^^^
Integrating libraries
^^^^^^^^^^^^^^^^^^^^^^

Configure external library-type packages (as opposed to compilers)
in the files ``$SPACK_ROOT/etc/spack/packages.yaml`` or
``~/.spack/packages.yaml``, following the Spack documentation under
:ref:`Build customization <build-settings>`.

Similar to ``compilers.yaml``, the ``packages.yaml`` files define a package
external to Spack in terms of a Spack spec and resolve each such spec via
either the ``paths`` or ``modules`` tokens to a specific pre-installed package
version on the system.  Since Intel tools generally need environment variables
to interoperate, which cannot be conveyed in a mere ``paths`` specification,
the ``modules`` token will be more sensible to use. It resolves the Spack-side
spec to a modulefile generated and managed outside of Spack's purview,
which Spack will load internally and transiently when the corresponding spec is
called upon to compile client packages.

If your system administrator did not provide modules for pre-installed Intel
tools, you could do well to ask for them, because installing multiple copies
of the Intel tools, as is wont to happen once Spack is in the picture, is
bound to stretch disk space and patience thin. If you *are* the system
administrator and are still new to modules, then perhaps it's best to follow
the `next section <Installing Intel tools within Spack_>`_ and install the tools
solely within Spack.

The following example integrates two packages embodied by hypothetical
external modulefiles ``intel-mkl/18/18.0.1`` and ``intel-mkl/18/18.0.2``, as
Spack packages ``intel-mkl@2018.1.163`` and ``intel-mkl@2018.2.199``,
respectively.

.. code-block:: sh

  spack config --scope=site edit packages

Make sure the file begins with:

.. code-block:: yaml

   packages:

Append, indented as shown:

.. code-block:: yaml

   # other content ...

     intel-mkl:
       modules:
         intel-mkl@2018.1.163  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.1
         intel-mkl@2018.2.199  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.2

Note that the version numbers in the ``intel-mkl`` spec correspond to the ones
used for the Intel products and adopted within Spack. You can inspect them by:

.. code-block:: sh

  spack info intel-mkl

Using the same version numbers is useful for clarity, but not strictly necessary.

.. _compiler-neutral-package:

Note that the Spack spec in the example does not contain a compiler
specification. This is intentional, as the Intel library packages can be used
unmodified with different compilers.

**TODO:** Confirm how the compiler-less spec is handled.

A slightly more advanced example illustrates how to provide
:ref:`variants <basic-variants>`
and how to use the ``buildable: False`` directive to prevent Spack from installing
other versions or variants of the named package through its normal internal
mechanism.

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       modules:
         intel-parallel-studio@cluster.2018.1.163 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.1
         intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.2
       buildable: False

**TODO:** Confirm variant handling.

One additional example illustrates the use of ``paths:`` instead of
``modules:``, useful when external modulefiles are not available or not
suitable:

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       paths:
         intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal: /opt/intel/parallel_studio_xe_2018.2.046
       buildable: False

For background and details, see
:ref:`External Packages <sec-external-packages>`.


-------------------------------------
Installing Intel tools *within* Spack
-------------------------------------

This section discusses `route 2`_ from the introduction.

When a system does not yet have Intel tools installed already, or the installed
versions are undesirable, Spack can install Intel tools like any regular Spack
package for you and, after appropriate post-install configuration, use the
compilers and/or libraries to install client packages.

^^^^^^^^^^^^^^^^^^
Install steps
^^^^^^^^^^^^^^^^^^

1. For licensed Intel packages, i.e., compilers and some early
   library-type packages, review the section `Configuring Spack to use Intel licenses`_
   at least once.

.. _intel-compiler-anticipation:

2. If you wish to install the package ``intel-parallel-studio`` to leverage
   both its ``%intel`` compilers and its virtual packages (like ``mkl`` and,
   for the "cluster edition", ``mpi``), apply the following special preparatory
   steps the first time you install each new version of the package.

   .. _`determine-compiler-anticipated`:

   A. From the package version, determine the compiler spec that the package is
      expected to provide.

      Combine the last two digits of the version year, a literal "0", and the
      component immediately following the version year:

      ==========================================  ======================
      Package version                             Compiler spec provided
      ------------------------------------------  ----------------------
       ``intel-parallel-studio@edition.YYyy.u``   ``intel@yy.0.u``
      ==========================================  ======================

      Example:

      The package ``intel-parallel-studio@cluster.2018.2`` provides the
      compiler spec ``intel@18.0.2``.

   .. _`config-compiler-anticipated`:

   B. Declare the compiler spec that you anticipate as a stub entry at the end
      of ``compilers.yaml`` from a suitable scope.

      For example, run:

      .. code-block:: sh

          spack config --scope=site edit compilers

      and append:

      .. code-block:: yaml

         - compiler:
             target:     x86_64
             operating_system:   centos6
             modules:    []
             spec:       intel@18.0.2
             paths:
               cc:       stub
               cxx:      stub
               f77:      stub
               fc:       stub

      Replace ``18.0.2`` with the version that you determined in the preceeding
      step. The contents of the language compiler tags (``cc:`` etc.) do not
      matter at this point.

      **Note:** If you already have a certain ``%intel@x.y.z`` compiler spec in
      place and you wish to re-install the ``intel-parallel-studio`` (or
      ``intel``) package providing the *same* compiler version, you do not need
      to revert its ``compilers.yaml`` declaration to stub form as shown here.
      When done, however, you may still need to adjust the entries under the
      ``paths:`` tag (`see below <Post-install steps for compilers_>`_) if the
      package's installation directory changed, such as in the hash portion.

   .. _`verify-compiler-anticipated`:

   C. Verify that the new compiler version will be used as expected:

      You should see it if you placed the stub last in ``compilers.yaml`` and
      ask for the compiler just by name, e.g.:

      .. code-block:: sh

         spack spec zlib %intel

      Otherwise, or simply to be explicit, state the anticipated compiler
      version as well, e.g.:

      .. code-block:: sh

         spack spec zlib %intel@18.0.2

   You are right to ask: "Why on earth is that necessary?" [fn9]_.
   The answer lies in Spack striving for strict compiler consistency.
   Consider what happens without a pre-declared compiler stub:
   You ask Spack to install a particular version
   ``intel-parallel-studio@edition.V``.  Spack will apply an unrelated compiler
   spec to concretize your request, giving ``intel-parallel-studio@edition.V
   %X``. Naturally, ``%X`` is not going to be the version that this new package
   provides, but typically ``%gcc@...`` in a default Spack installation or possibly
   indeed ``%intel@...``, though at a version preceeding ``V``.

   The problem comes to the fore as soon as you try to use any virtual
   ``mkl`` or ``mpi`` packages that you would expect to now be provided by
   ``intel-parallel-studio@edition.V``.  Spack will indeed see those virtual packages,
   but only as being tied to the compiler concretized *at installation*.
   If you were to install a client package with the new compilers now
   available to you, you would run ``spack install foo +mkl %intel@V``, but
   Spack would complain about ``mkl%intel@V`` being missing, because it only
   knows about ``mkl%X``.

   To escape this trap, put the compiler stub declaration shown here in place,
   then use that pre-declared compiler spec to install the actual package, as
   shown in the next step.  This approach works because only the package's
   builtin binary installer will be used, not any of the compilers.

3. Install the Intel packages using Spack's regular ``install`` command, e.g.:

   .. code-block:: sh

      spack install intel-parallel-studio@cluster.2018.2  %intel

   If you wish or need to force the matching compiler (`see above
   <verify-compiler-anticipated_>`_), give it as additional concretization
   element:

   .. code-block:: sh

      spack install intel-parallel-studio@cluster.2018.2  %intel@18.0.2

   The command for a smaller standalone package is the same:

   .. code-block:: sh

      spack install intel-mpi@2018.2.199  %intel

.. tip::

   As mentioned, Intel packages can be above 10 GB in size, which can tax the
   disk space available for temporary files (usually ``/tmp``) on small, busy,
   or restricted systems (like VMs). The Intel installer will stop and report
   insufficient space as::

       ==> './install.sh' '--silent' 'silent.cfg'
       …
       Missing critical prerequisite
       -- Not enough disk space

   As first remedy, clean Spack's existing staging area:

   .. code-block:: sh

      spack clean --stage

   then retry installing the large package. Spack normally cleans staging
   directories but certain failures may prevent it from doing so.
   
   If the error persists, tell Spack to use an alternative location for
   temporary files:

   1. Run ``df -h`` to identify an alternative location on your system.

   2. Tell Spack to use that location for staging. Do **one** of the following:

      * Run Spack with the environment variable ``TMPDIR`` altered for just a
        single command. For example, to use your ``$HOME`` directory:

        .. code-block:: sh

           TMPDIR="$HOME/spack-stage"  spack install ....

        This example uses Bourne shell syntax. Adapt for other shells as needed.

      * Alternatively, customize
        :ref:`Spack's ``build_stage`` configuration setting <config-overrides_>`.

        .. code-block:: sh

           spack config edit config

        Append:

        .. code-block:: yaml

           config:
             build_stage:
             - /home/$user/spack-stage
        
        Do not duplicate the ``config:`` line if it already is present.
        Adapt the location, which here is the same as in the preceeding example.

   3. Retry installing the large package.

   4. Optionally, clean the staging area:

      .. code-block:: sh

         spack clean --stage

   5. Also optionally, roll back your ``build_stage`` customization:

      .. code-block:: sh

         spack config edit config

     and delete or comment out the ``build_stage`` entry.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Post-install steps for compilers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow the steps under `Integrating Compilers`_ to tell Spack the minutiae for
actually using those compilers with client packages.

* Under ``paths:``, give the full paths to the actual compiler binaries (``icc``,
  ``ifort``, etc.) located within the Spack installation tree, in all their
  unsightly length [fn10]_.

  To determine the full path to the C compiler, adapt and run:

  .. code-block:: sh

     find `spack location -i intel-parallel-studio@cluster.2018.2` \
            -name icc -type f -ls

  If you get hits for both ``intel64`` and ``ia32``, you almost certainly will
  want to use the ``intel64`` variant.  The ``icpc`` and ``ifort`` compilers
  will be located in the same directory as ``icc``.

* Use the ``modules:`` or ``cflags:`` tokens to specify a suitable accompanying
  ``gcc`` version to help pacify picky client packages that ask for C++
  standards more recent than supported by your system-provided ``gcc`` and its
  ``libstdc++.so``.

* To set the Intel compilers for default use, instead of the usual ``%gcc``,
  follow section `<Selecting Intel Compilers_>`_.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Post-install steps for library packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow `Selecting libraries to satisfy virtual packages`_.


^^^^^^^^^^^^^^^^
Debug notes
^^^^^^^^^^^^^^^^

* You can trigger a wall of additional diagnostics by Spack options, e.g.:

  .. code-block:: sh

    $ spack --debug -v install -v intel-mpi

  The the ``--debug`` option can also be useful while installing client
  packages `(see below) <Using Intel tools in Spack to install client
  packages_>`_ to confirm the integration of the Intel tools in Spack, notably
  MKL and MPI.

* The ``.spack/`` subdirectory of an installed ``IntelPackage`` will contain,
  besides Spack's usual archival items, a copy of the ``silent.cfg`` file that
  was passed to the Intel installer:

  .. code-block:: sh

    $ grep COMPONENTS …intel-mpi…<hash>/.spack/silent.cfg
    COMPONENTS=ALL

* If an installation error occurs, Spack will normally clean up and remove a
  partially installed target directory. You can direct Spack to keep it using
  ``--keep-prefix``, e.g.:

  .. code-block:: sh

    $ spack install --keep-prefix  intel-mpi

  You must, however, *remove such partial installations* prior to subsequent
  installation attempts. Otherwise, the Intel installer will behave
  incorrectly.


-------------------------------------------------------
Using Intel tools in Spack to install client packages
-------------------------------------------------------

Finally, this section pertains to `route 3`_ from the introduction.

Once Intel tools are installed within Spack as external or internal package
they can be used as intended for installing client packages.


.. _`select-intel-compilers`:

^^^^^^^^^^^^^^^^^^^^^^^^^^
Selecting Intel compilers
^^^^^^^^^^^^^^^^^^^^^^^^^^

Select Intel compilers to compile client packages by one of the following
means:

* Request the Intel compilers expliclity in the client spec, e.g.:

  .. code-block:: sh

    spack install libxc@3.0.0%intel


* Alternatively, request Intel compilers implicitly by concretization preferences.
  Configure the order of compilers in the appropriate ``packages.yaml`` file,
  under either an ``all:`` or client-package-specific entry, in a
  ``compiler:`` list. Consult the Spack documentation for
  :ref:`Configuring Package Preferences <configs-tutorial-package-prefs>`
  and
  :ref:`Concretization Preferences <concretization-preferences`.

Example: ``etc/spack/packages.yaml`` might simply contain:

.. code-block:: yaml

  packages:
    all:
      compiler: [ intel, gcc, ]

To be more specific, you can state partial or full compiler version numbers,
for example:

.. code-block:: yaml

  packages:
    all:
      compiler: [ intel@18, intel@17, gcc@4.4.7, gcc@4.9.3, gcc@7.3.0, ]



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Selecting libraries to satisfy virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Intel packages, whether integrated into Spack as external packages or
installed within Spack, can be called upon to satisfy the requirement of a
client package for a library that is available from different providers.
The relevant virtual packages for Intel are ``blas``, ``lapack``,
``scalapack``, and ``mpi``.

In both integration routes, Intel packages can have optional
:ref:`variants <basic-variants>`
which alter the list of virtual packages they can satisfy.  For Spack-external
packages, the active variants are a combination of the defaults declared in
Spack's package repository and the spec it is declared as in ``packages.yaml``.
Needless to say, those should match the components that are actually present in
the external product installation. Likewise, for Spack-internal packages, the
active variants are determined, persistently at installation time, from the
defaults in the repository and the spec selected to be installed.

To have Intel packages satisfy virtual package requests for all or selected
client packages, edit the ``packages.yaml`` file.  Customize, either in the
``all:`` or a more specific entry, a ``providers:`` dictionary whose keys are
the virtual packages and whose values are the Spack specs that satisfy the
virtual package, in order of decreasing preference.  To learn more about the
``providers:`` settings, see the Spack tutorial for
:ref:`Configuring Package Preferences <configs-tutorial-package-prefs>`
and the section
:ref:`Concretization Preferences <concretization-preferences>`.

Example: The following fairly minimal example for ``packages.yaml`` shows how
to exclusively use the standalone ``intel-mkl`` package for all the linear
algebra virtual packages in Spack, and ``intel-mpi`` as the preferred MPI
implementation, while enabling to choose others on a per-spec basis.

.. code-block:: yaml

  packages:
    all:
      providers:
        mpi:       [intel-mpi, openmpi, mpich, ]
        blas:      [intel-mkl, ]
        lapack:    [intel-mkl, ]
        scalapack: [intel-mkl, ]

If you have access to the ``intel-parallel-studio@cluster`` edition, you can
use instead:

.. code-block:: yaml

      all:
      providers:
        mpi:       [intel-parallel-studio+mpi, openmpi, mpich, ]
        blas:      [intel-parallel-studio+mkl, ]
        lapack:    [intel-parallel-studio+mkl, ]
        scalapack: [intel-parallel-studio+mkl, ]

If you installed ``intel-parallel-studio`` within Spack ("`route 2`_"), make
sure you followed the `special installation step
<intel-compiler-anticipation_>`_ to ensure that its virtual packages match the
compilers it provides.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using Intel tools as explicit dependency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the proper installation as detailed above, no special steps should be
required when a client package specifically (and thus deliberately) requests an
Intel package as dependency, this being one of the target use cases for Spack.

**TODO:** confirm for DAAL, IPP

----------
Footnotes
----------

.. [fn1] Strictly speaking, versions from ``2017.2`` onward.

.. [fn2] The package ``intel`` intentionally does not have a ``+mpi`` variant since
   it is meant to be small. The native installer always adds the MPI *runtime*
   components because it follows defaults defined in the download package, even
   for ``intel-parallel-studio ~mpi``.

   For ``intel-parallel-studio +mpi``, Spack internally supplies [in code at
   ``lib/spack/spack/build_systems/intel.py:pset_components()``] the component
   pattern ``"intel-mpi intel-imb"`` to the Intel installer, which will expand
   each name with an implied glob-like ``*`` to the package names that are
   *actually present in the product BOM*.  As a side effect, the pattern
   approach accommodates occasional package name changes, e.g., capturing both
   ``intel-mpirt`` and ``intel-mpi-rt`` .

.. [fn3] How could the external installation have succeeded otherwise?

.. [fn4] According to Intel's documentation, there is supposedly a way to install a
   product using a network license even `when a FLEXlm server is not running
   <https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license>`_:
   Specify the license in the form ``port@serverhost`` in the
   ``INTEL_LICENSE_FILE`` environment variable. All other means of specifying a
   network license require that the license server be up.

.. [fn5]  Despite the name, ``INTEL_LICENSE_FILE`` can hold several and diverse entries.
   They  can be either directories (presumed to contain ``*.lic`` files), file
   names, or network locations in the form ``port@host`` (on Linux and Mac),
   with all items separated by ":" (on Linux and Mac).

.. [fn6] Should said editor turn out to be ``vi``, you better be in a position
   to know how to use it.

.. [fn7] Comment lines in FLEXlm files, indicated by ``#`` as the first
   non-white character on the line, are generally allowed anywhere in the file.
   There `have been reports <https://github.com/spack/spack/issues/6534>`_,
   however, that as of 2018, ``SERVER`` and ``USE_SERVER`` lines must precede
   any comment lines.

.. [fn8] The name component ``intel`` of the compiler spec is separate from (in
   a different namespace than) the names of the Spack packages
   ``intel-parallel-studio`` and ``intel``. Both of the latter provide the former.

.. [fn9] Spack's close coupling of installed packages to compilers, which both
   necessitates the detour for installing ``intel-parallel-studio``, and,
   largely limits any of its provided virtual packages to a single compiler, heavily
   favors a `recommendation to install Intel Parallel Studio outside of Spack
   <integrate-external-intel_>`_ and declare it for Spack in ``packages.yaml``
   by a `compiler-less spec <compiler-neutral-package_>`_.

.. [fn10] With some effort, you can convince Spack to use shorter paths:

   1. Set the ``install_tree`` location in ``config.yaml``
      (:ref:`see doc <config-yaml>`).
   2. Set the hash length in ``install-path-scheme``, also in ``config.yaml``
      (:ref:`q.v. <config-yaml>`).
   3. You will want to set the *same* hash length for
      :ref:`tcl module files <modules-naming-scheme>`
      if you have Spack produce them for you, under ``naming_scheme`` in
      ``modules.yaml``.

   .. warning:: Altering the naming scheme means that Spack will lose track of
      all packages it has installed for you so far. In a pinch, you can dive
      into old installation directories by hand until you delete them.
      
      That said, *the time is right* for this kind of customization
      when you are lining up a new set of compilers.

   **Practical hint:** Hashes can be a pain to quickly scan over, especially in
   ragged-right directory listings.  To lessen the eyesore for humans and give
   shell glob patterns a handle to latch on to, prefix hashes with a consistent
   string, such as the letter ``H``.

   Set in ``config.yaml``:

   .. code-block:: yaml

     config:
       install_path_scheme: '${ARCHITECTURE}/${PACKAGE}/${VERSION}-${COMPILERNAME}-${COMPILERVER}/H${HASH:6}'

   and in ``modules.yaml``:

   .. code-block:: yaml

     modules:
       tcl:
         naming_scheme: '${PACKAGE}/${VERSION}/${COMPILERNAME}-${COMPILERVER}/H${HASH:6}'
