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
and optimizers do require a paid license.  In Spack, they are provided as:

* ``intel-parallel-studio`` – the entire suite of compilers and libraries,
* ``intel`` – a subset containing just the compilers and the Intel-MPI runtime [fn2]_.

------

**TODO:**  Confirm scope of MPI components (runtime vs. devel) in current (and
previous?) *cluster/professional/composer* editions, i.e., presence in downloads,
possibly subject to license coverage(!); see `disussion in PR #4300
<https://github.com/spack/spack/pull/4300#issuecomment-305582898>`_.
[NB: An "mpi" subdirectory is not indicative of the full MPI SDK being present
(``mpicc``, …, and header files).  The directory may contain just the MPI
runtime (``mpirun`` and shared libraries) .]

------

The license is needed at installation time and to compile client packages, but
never to merely run any resulting binaries.

The libraries that are provided in the standalone packages are included in the
all-encompassing ``intel-parallel-studio``. To complicate matters a bit, that
package is sold in 3 "editions", of which only the upper-tier ``cluster``
edition supports compiling MPI applications, and hence only that edition will
provide the ``mpi`` virtual package. The edition forms the *leading part* of
Spack's version numbers for the package:


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

To install the full suite, capable of compiling MPI applications, run:

.. code-block:: sh

  $ spack install intel-parallel-studio@cluster.2018.2        # ca. 12 GB

If you need to save some disk space or installation time, install separately as needed:

.. code-block:: sh

  $ spack install intel         # 0.6 GB
  $ spack install intel-mpi     # 0.5 GB
  $ spack install intel-mkl     # 2.5 GB


^^^^^^^^^^^^^^^^^^^^
Unrelated packages
^^^^^^^^^^^^^^^^^^^^

The following packages do not use the Intel installer and are not in class ``IntelPackage``
discussed here:

* ``intel-gpu-tools`` – Test suite and low-level tools for the Linux `Direct
  Rendering Manager <https://en.wikipedia.org/wiki/Direct_Rendering_Manager>`_.
* ``intel-mkl-dnn`` – Math Kernel Library for Deep Neural Networks (``CMakePackage``)
* ``intel-xed`` – X86 machine instructions encoder/decoder
* ``intel-tbb`` – Standalone version of Intel Threading Building Blocks. – Note that
  development versions and a runtime version of TBB are included in all
  ``intel-parallel-studio/intel`` and ``intel-mkl`` packages, respectively.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configuring Spack to use Intel licenses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you wish to integrate licensed Intel products into Spack as external packages
(`route 1`_ above) we assume that their license configuration is in place and
is working [fn3]_. In this case, skip ahead to section `Integration of Intel
tools installed external to Spack`_.

If you plan to use Spack to install licensed products for you (`route 2`_ above),
the Intel product installer that Spack will run underneath must have access to
a license.  Provide it by one of the means given in the following sections.

For authoritative information on Intel licensing, see:

* https://software.intel.com/en-us/faq/licensing
* https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses

""""""""""""""""""""""""""""""
Pointing to a license server
""""""""""""""""""""""""""""""

Installing and configuring a license server is outside the scope of Spack. We
assume your system administrator has a license server running and has installed
network licenses for Intel packages.  To obtain a license from the server for
installation or temporary use, a process known as "checking out a license", a
client application needs to know the host name and port number of one or more
license servers [fn4]_.

There are three methods to `configure clients to use a network license
<https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license>`_.
Ideally, your license administrator will already have implemented one.
Look for the environment variable ``INTEL_LICENSE_FILE`` or for files
``/opt/intel/licenses/*.lic`` that contain::

  SERVER  hostname  hostid_or_ANY  portnum
  USE_SERVER

The relevant tokens, among possibly others, are the ``USE_SERVER`` line,
intended specifically for clients, and one or more ``SERVER`` lines above it
which give the network address.

""""""""""""""""""""""""""""""""""""
Installing a standalone license file
""""""""""""""""""""""""""""""""""""

If you purchased a user-specific license, "activate" it for your serial number
and download the resulting license file as `instructed by Intel
<https://software.intel.com/en-us/faq/licensing#license-management>`_.
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

* Spack-managed file

  The first time Spack encounters an Intel package that requires a license, it
  will initialize a Spack-global Intel-specific license file for you, as a
  template with instructional comments, and bring up an editor [fn6]_.  Spack
  will do this *even if you have a working license elsewhere* on the system.

  * To proceed with an externally configured license, leave the newly templated
    file as is (containing comments only) and close the editor. You do not need
    to touch the file again.

  * To configure your own license, copy the contents of your downloaded license
    file into the opened file, save it, and close the editor.

  To revisit and manually edit this file, such as prior to a subsequent
  installation attempt, find it at
  ``$SPACK_ROOT/etc/spack/licenses/intel/intel.lic`` .

  Spack will place symbolic links to this file in each directory where licensed
  Intel binaries were installed.  If you kept the template unchanged, Intel tools
  will simply ignore it.

**TODO:** `PR #6534 "Intel v18 License File Format Issue"
<https://github.com/spack/spack/issues/6534>`_.

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

Configure external Intel compilers, like all compilers that Spack is to use,
in ``compilers.yaml`` files located in
``$SPACK_ROOT/etc/spack/`` or your own ``~/.spack/`` directory.
In the Spack documentation, see
:ref:`Configuration Files in Spack <configuration>`
in general and
:ref:`Vendor-Specific Compiler Configuration <getting-started>`,
section Intel Compilers.

.. anchor ../getting_started.rst .. _vendor-specific-compiler-configuration:

Briefly, the ``compilers.yaml`` files combine C and Fortran compilers of a
specific vendor release and define such a set as a Spack
:ref:`spec <sec-specs>`
that in this case has the form ``intel@compilerversion`` [fn7]_.
The entry determines how the spec is to be resolved, via ``paths`` and/or
``modules`` tokens, to each language compiler in the set.

The following example illustrates how to integrate the 2018 Intel compiler
suite, which outside of Spack was activated by users of the example system as
``module load intel/18``. Since Spack must be rather more picky about versions,
we must specify full paths and complete modulefile names in the relevant
``compilers.yaml`` entry:

.. code-block:: yaml

    compilers:
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


^^^^^^^^^^^^^^^^^^^^^^
Integrating libraries
^^^^^^^^^^^^^^^^^^^^^^

Configure external library-type packages (as opposed to compilers)
in the files ``$SPACK_ROOT/etc/spack/packages.yaml`` or
``~/.spack/packages.yaml``, see the Spack documentation under
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

.. code-block:: yaml

   packages:
     intel-mkl:
       modules:
         intel-mkl@2018.1.163  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.1
         intel-mkl@2018.2.199  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.2

Note that the version numbers in the ``intel-mkl`` spec correspond to the ones
used for the Intel products and adopted within Spack. You can inspect them by:

.. code-block:: sh

  spack info intel-mkl

Using the same version numbers is useful for clarity, but not strictly necessary.

**TODO:** Confirm.

Note that the Spack spec in the example does not contain a compiler
specification. This is intentional, as the Intel library packages can be used
unmodified with different compilers.

**TODO:** Confirm how the compiler-less spec is handled.

A slightly more advanced example follows, illustrating how to provide
:ref:`variants <basic-usage>` and using
the ``buildable: False`` directive to prevent Spack from installing other
versions or variants of the named package through its normal internal
mechanism.

.. anchor ../basic_usage.rst .. _variants:

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       modules:
         intel-parallel-studio@cluster.2018.1.163 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.1
         intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.2
       buildable: False

**TODO:** Confirm variant handling.


-------------------------------------
Installing Intel tools *within* Spack
-------------------------------------

This section discusses `route 2`_ from the introduction.

When a system does not yet have Intel tools installed already, or the installed
versions are undesirable, Spack can install Intel tools like any regular Spack
package for you and, after appropriate post-install configuration, use the
compilers and/or libraries to install client packages.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing and integrating compiler components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As stated in the previous section `Integration of Intel tools installed
external to Spack`_, Intel compilers and some early library-type Intel
packages require a license at installation and during runtime. Before
installation, follow the section `Configuring Spack to use Intel licenses`_.

**After installation**, follow the steps under `Integrating Compilers`_ to tell
Spack the minutiae for actually using those compilers with client packages.

* Under ``paths:``, use the full paths to the actual compiler binaries (``icc``,
  ``ifort``, etc.) located within the Spack installation tree, in all their
  unsightly length [fn8]_.

* Use the ``modules:`` or ``cflags:`` tokens to specify a suitable accompanying
  ``gcc`` version to help pacify picky client packages that ask for C++
  standards more recent than supported by your system-provided ``gcc`` and its
  ``libstdc++.so``.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing library packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Standalone Intel library packages are installed like most other Spack packages,
save for the licensing accommodations of the earlier releases, which are the
same as for compilers.

**After installation**, follow `Selecting libraries to satisfy virtual
packages`_.


-------------------------------------------------------
Using Intel tools in Spack to install client packages
-------------------------------------------------------

Finally, this section pertains to `route 3`_ from the introduction.

Once Intel tools are installed within Spack as external or internal package
they can be used as intended for installing client packages.


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
  :ref:`Configuring Package Preferences <configs-tutorial>`
  and
  :ref:`Concretization Preferences <build-settings>`.

  .. anchor ../tutorial_configuration.rst .. _configuring-package-preferences:
  .. anchor ../build_settings.rst  .. _concretization-preferences:

Example: ``etc/spack/packages.yaml`` might contain:

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
:ref:`variants <basic-usage>`
which alter the list of virtual packages they can satisfy.  For Spack-external
packages, the active variants are a combination of the defaults declared in
Spack's package repository and the spec it is declared as in ``packages.yaml``.
Needless to say, those should match the components that are actually present in
the external product installation. Likewise, for Spack-internal packages, the
active variants are determined, persistently at installation time, from the
defaults in the repository and the spec selected to be installed.

.. anchor ../basic_usage.rst .. _variants:

To have Intel packages satisfy virtual package requests for all or selected
client packages, edit the ``packages.yaml`` file.  Customize, either in the
``all:`` or a more specific entry, a ``providers:`` dictionary whose keys are
the virtual packages and whose values are the Spack specs that satisfy the
virtual package, in order of decreasing preference.  To learn more about the
``providers:`` settings, see the Spack tutorial for
:ref:`Configuring Package Preferences <configs-tutorial>`
and the section
:ref:`Concretization Preferences <build-settings>`.

.. anchor ../tutorial_configuration.rst .. _configuring-package-preferences:
.. anchor ../build_settings.rst  .. _concretization-preferences:

Example: The following fairly minimal example for ``packages.yaml`` shows how
to exclusively use the standalone ``intel-mkl`` package for all the linear
algebra virtual packages in Spack, and ``intel-mpi`` as the preferred MPI
implementation, while enabling to choose others on a per-spec basis.

.. code-block:: yaml

  packages:
    all:
      providers:
        mpi: [intel-mpi, openmpi, mpich, ]
        blas: [intel-mkl, ]
        lapack: [intel-mkl, ]
        scalapack: [intel-mkl, ]


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

.. [fn2] The scope of MPI components installed was `discussed in PR #4300
   <https://github.com/spack/spack/pull/4300#issuecomment-305857268>`_.

   The package ``intel`` intentionally does not have a ``+mpi`` variant since
   it is meant to be small. The native installer always adds the MPI *runtime*
   components because it follows defaults defined in the download package.  The
   same applies to ``intel-parallel-studio ~mpi``.

   For ``intel-parallel-studio`` with``+mpi``, Spack requests [in
   ``lib/spack/spack/build_systems/intel.py:pset_components()``] the component
   pattern ``"intel-mpi intel-imb"``, which implies *all* MPI components that
   are present in the download package (``intel-mpi{rt,-rt,-sdk,…}``). The
   native installer expands the component pattern names with an implied glob
   ``*`` to the packages in the product BOM.

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

.. [fn7] The name component ``intel`` of the compiler spec is separate from (in
   a different namespace than) the names of the Spack packages
   ``intel-parallel-studio`` and ``intel``. Both of the latter provide the former.

.. [fn8] With some effort, you can convince Spack to use shorter paths:

   1. Set the ``install_tree`` location in ``config.yaml``
      (:ref:`doc <config-yaml>`).
   2. Set the hash length in ``install-path-scheme``, also in ``config.yaml``
      (:ref:`q.v. <config-yaml>`).
   3. You will want to set the *same* hash length for tcl module files
      if you have Spack produce them for you, under ``naming_scheme`` in
      ``modules.yaml``
      (:ref:`doc <modules-yaml>`).

   .. anchor ../config_yaml.rst .. _install-tree:
   .. anchor ../config_yaml.rst .. _install-hash-length-and-install-path-scheme:
   .. anchor ../module_file_support.rst .. _customize-the-naming-scheme:

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
